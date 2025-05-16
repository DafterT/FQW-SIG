import struct
import threading
import serial
import serial.tools.list_ports
import time
from crcmod import mkCrcFun


class ModbusSlave:
    """
    Класс реализующий Modbus Slave (сервер)
    с возможностью установки колбэков при получении корректных запросов.
    """

    # Modbus исключения
    ILLEGAL_FUNCTION = 0x01
    ILLEGAL_DATA_ADDRESS = 0x02
    ILLEGAL_DATA_VALUE = 0x03

    # Функции Modbus
    READ_HOLDING_REGISTERS = 0x03
    WRITE_SINGLE_REGISTER = 0x06
    WRITE_MULTIPLE_REGISTERS = 0x10

    def __init__(
        self, baudrate=9600, timeout=1, slave_id=1, bytesize=8, parity="E", stopbits=1
    ):
        """
        Инициализация Modbus Slave

        :param baudrate: скорость для RTU
        :param timeout: таймаут ожидания данных
        :param slave_id: идентификатор устройства (1-247)
        """
        self.thread = None
        self.port = None
        self.baudrate = baudrate
        self.timeout = timeout
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.serial = serial.Serial()

        self.slave_id = slave_id
        self.running = False
        self.callbacks = {}
        self.data_store = {
            "holding_registers": [0] * 256,
        }

        # Инициализация CRC функции для RTU
        self.crc16 = mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)

        self.command_list = [self.WRITE_SINGLE_REGISTER, self.WRITE_MULTIPLE_REGISTERS, self.READ_HOLDING_REGISTERS]

    def start(self):
        """Запуск сервера Modbus Slave с автоопределением порта"""
        self.running = True

        if hasattr(self, "serial") and self.serial.is_open:
            self.serial.close()

        # Попытка автоматического определения порта
        if self._auto_detect_port():
            self.thread = threading.Thread(target=self._rtu_loop)
            self.thread.daemon = True
            self.thread.start()
        else:
            print("Не удалось найти подходящий COM-порт")
            self.running = False
            return

    def _auto_detect_port(self, timeout=2.0):
        """Автоматическое определение COM-порта"""
        # Получаем список доступных портов
        available_ports = serial.tools.list_ports.comports()
        test_ports = [p.device for p in available_ports]

        if not test_ports:
            print("Нет доступных COM-портов")
            return False

        print(f"Доступные порты: {test_ports}")

        for port in test_ports:
            try:
                print(f"Проверка порта {port}...")
                ser = serial.Serial(
                    port=port,
                    baudrate=self.baudrate,
                    bytesize=self.bytesize,
                    parity=self.parity,
                    stopbits=self.stopbits,
                    timeout=self.timeout,
                )

                # Проверяем, есть ли входящие данные
                start_time = time.time()
                data_received = False

                while time.time() - start_time < timeout:
                    if ser.in_waiting > 0:
                        data = ser.read(ser.in_waiting)
                        print(f"Получены данные на порту {port}: {data.hex()}")
                        data_received = True
                        break
                    time.sleep(0.1)

                if data_received:
                    print(f"Выбран порт {port} (обнаружена активность)")
                    self.port = port
                    self.serial = ser
                    return True
                else:
                    print(f"Порт {port} доступен, но активность не обнаружена")
                    ser.close()

            except serial.SerialException as e:
                print(f"Ошибка при работе с портом {port}: {str(e)}")
                continue

        # Если ни один порт не подошел, пробуем использовать указанный в конфигурации
        try:
            print(f"Попытка использовать указанный порт {self.port}")
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=self.bytesize,
                parity=self.parity,
                stopbits=self.stopbits,
                timeout=self.timeout,
            )
            return True
        except serial.SerialException as e:
            print(f"Не удалось открыть указанный порт {self.port}: {str(e)}")

            return False

    def stop(self):
        """Остановка сервера Modbus Slave"""
        if self.running:
            self.running = False
            self.thread.join()

        if self.serial.is_open:
            self.serial.close()

    def set_callback(self, function_code, callback):
        """
        Установка колбэка для определенной функции Modbus

        :param function_code: код функции Modbus
        :param callback: функция обратного вызова (принимает данные запроса)
        """
        self.callbacks[function_code] = callback

    def _rtu_loop(self):
        """Основной цикл обработки запросов в режиме RTU"""
        buffer = bytearray()

        while self.running:
            # Чтение данных из последовательного порта
            data = self.serial.read(1)
            if not data:
                continue

            buffer.extend(data)

            if len(buffer) == 1:
                if buffer[0] != self.slave_id:  # 0 - широковещательный адрес
                    buffer.clear()
                continue

            if len(buffer) == 2:
                if buffer[1] not in self.command_list:
                    buffer.clear()
                continue

            # Проверка на полный пакет
            expected_length = self._get_expected_rtu_length(buffer)
            if len(buffer) < expected_length:
                continue

            # Проверка CRC
            crc_received = buffer[-2:]  # Последние 2 байта - CRC
            crc_calculated = self._calculate_crc(buffer[:-2])
            if crc_received != crc_calculated:
                buffer.clear()
                continue

            # Обработка корректного пакета
            request = buffer.copy()
            print("REQUEST ", buffer.hex())
            buffer.clear()

            # Формирование ответа
            response = self._process_request(request)
            if response:
                print("RESPONSE ", response.hex())
                self.serial.write(response)

            # Вызов колбэка если он установлен
            function_code = request[1]
            if function_code in self.callbacks:
                self.callbacks[function_code](request)

    def _get_expected_rtu_length(self, data):
        """Определение ожидаемой длины пакета RTU на основе кода функции"""
        if len(data) < 2:
            return 4  # минимальная длина (адрес + функция + CRC)

        # Базовые длины для разных функций
        lengths = {
            self.READ_HOLDING_REGISTERS: 8,
            self.WRITE_SINGLE_REGISTER: 8,
            self.WRITE_MULTIPLE_REGISTERS: 9 + data[6] if len(data) > 7 else 9,
        }

        function_code = data[1]
        return lengths.get(function_code, 256)  # 256 - максимальная длина по умолчанию

    def _calculate_crc(self, data):
        """Вычисление CRC16 для RTU пакета"""
        crc = self.crc16(data)
        return struct.pack("<H", crc)

    def _process_request(self, request):
        """Обработка Modbus запроса и формирование ответа"""

        slave_id = request[0]

        pdu = request[1:-2]  # Исключаем адрес и CRC

        function_code = pdu[0] if len(pdu) > 1 else None

        try:
            match function_code:
                case self.READ_HOLDING_REGISTERS:
                    return self._read_holding_registers(slave_id, pdu)
                case self.WRITE_SINGLE_REGISTER:
                    return self._write_single_register(slave_id, pdu)
                case self.WRITE_MULTIPLE_REGISTERS:
                    return self._write_multiple_registers(slave_id, pdu)
                case _:
                    return self._exception_response(
                        slave_id, function_code, self.ILLEGAL_FUNCTION
                    )

        except IndexError:
            return self._exception_response(
                slave_id, function_code, self.ILLEGAL_DATA_ADDRESS
            )
        except Exception:
            return self._exception_response(
                slave_id, function_code, self.ILLEGAL_DATA_VALUE
            )

    def _write_multiple_registers(self, slave_id, pdu):
        address = struct.unpack(">H", pdu[1:3])[0]
        quantity = struct.unpack(">H", pdu[3:5])[0]

        reg_data = []

        for i in range(quantity):
            data = struct.unpack(">H", pdu[6 + i * 2 : 8 + i * 2])[0]
            self.data_store["holding_registers"][address + i] = data
            reg_data.append(data)

        response = (
            bytearray([slave_id, self.WRITE_MULTIPLE_REGISTERS]) + pdu[1:3] + pdu[3:5]
        )
        response += self._calculate_crc(response)

        return response

    def _write_single_register(self, slave_id, pdu):
        address = struct.unpack(">H", pdu[1:3])[0]
        data = struct.unpack(">H", pdu[3:5])[0]

        self.data_store["holding_registers"][address] = data

        response = (
            bytearray([slave_id, self.WRITE_SINGLE_REGISTER])
            + address.to_bytes(2, "big")
            + data.to_bytes(2, "big")
        )
        response += self._calculate_crc(response)

        return response


    def _read_holding_registers(self, slave_id, pdu):
        """Обработка функции чтения holding регистров (0x03)"""
        address = struct.unpack(">H", pdu[1:3])[0]
        quantity = struct.unpack(">H", pdu[3:5])[0]

        if quantity < 1 or quantity > 125:
            return self._exception_response(
                slave_id, self.READ_HOLDING_REGISTERS, self.ILLEGAL_DATA_VALUE
            )

        end_address = address + quantity - 1
        if end_address >= len(self.data_store["holding_registers"]):
            return self._exception_response(
                slave_id, self.READ_HOLDING_REGISTERS, self.ILLEGAL_DATA_ADDRESS
            )

        # Формирование данных ответа
        byte_count = quantity * 2
        registers_data = bytearray(byte_count)

        for i in range(quantity):
            registers_data[i * 2 : (i * 2) + 2] = struct.pack(
                ">H", self.data_store["holding_registers"][address + i]
            )

        # Формирование ответа

        response = (
            bytearray([slave_id, self.READ_HOLDING_REGISTERS, byte_count])
            + registers_data
        )
        response += self._calculate_crc(response)

        return response

    def _exception_response(self, slave_id, function_code, exception_code):
        """Формирование ответа с исключением"""

        response = bytearray([slave_id, function_code | 0x80, exception_code])
        response += self._calculate_crc(response)

        return response
