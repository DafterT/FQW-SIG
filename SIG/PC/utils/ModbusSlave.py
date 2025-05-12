import struct
import threading

import serial
import socket
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
    READ_COILS = 0x01
    READ_DISCRETE_INPUTS = 0x02
    READ_HOLDING_REGISTERS = 0x03
    READ_INPUT_REGISTERS = 0x04
    WRITE_SINGLE_COIL = 0x05
    WRITE_SINGLE_REGISTER = 0x06
    WRITE_MULTIPLE_COILS = 0x0F
    WRITE_MULTIPLE_REGISTERS = 0x10

    def __init__(self, port='/dev/ttyS0', baudrate=9600, timeout=1, slave_id=1, bytesize=8, parity='E', stopbits=1):
        """
        Инициализация Modbus Slave

        :param port: последовательный порт для RTU
        :param baudrate: скорость для RTU
        :param timeout: таймаут ожидания данных
        :param slave_id: идентификатор устройства (1-247)
        """
        self.thread = None
        self.port = port
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
            'coils': [False] * 65536,
            'discrete_inputs': [False] * 65536,
            'holding_registers': [0] * 65536,
            'input_registers': [0] * 65536
        }

        # Инициализация CRC функции для RTU
        self.crc16 = mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)

        self.command_list = [self.WRITE_SINGLE_REGISTER, self.WRITE_MULTIPLE_REGISTERS]

    def start(self):
        """Запуск сервера Modbus Slave с автоопределением порта"""
        self.running = True

        if hasattr(self, 'serial') and self.serial.is_open:
            self.serial.close()

        # Попытка автоматического определения порта
        if self._auto_detect_port():
            self.thread = threading.Thread(target=self._rtu_loop)
            self.thread.daemon = True
            self.thread.start()
            threading.Timer(5.0, self.read_delay).start()
        else:
            print("Не удалось найти подходящий COM-порт")
            self.running = False
            return

    def _auto_detect_port(self, timeout=2.0):
        """Автоматическое определение COM-порта"""
        import serial.tools.list_ports

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
                    timeout=self.timeout
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
                timeout=self.timeout
            )
            return True
        except serial.SerialException as e:
            print(f"Не удалось открыть указанный порт {self.port}: {str(e)}")

            return False

    def read_delay(self):
        self.command_list.append(self.READ_HOLDING_REGISTERS)



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
            #print(data)
            if not data:
                continue

            buffer.extend(data)

            # Проверка на минимальную длину пакета (адрес + функция + CRC)
            #if len(buffer) < 4:
            #    continue
            # Проверка, что пакет адресован нам
            if len(buffer) == 1:
                if buffer[0] != self.slave_id:  # 0 - широковещательный адрес
                    buffer.clear()
                continue
            #TODO (ДОБАВИТЬ ВСе ХУЕТЫ)

            #print("PRE_REG ", buffer.hex())
            if len(buffer) == 2:
                if buffer[1] not in self.command_list:
                    buffer.clear()
                continue


            #print("PRE_PAC ", buffer.hex())
            # Проверка на полный пакет
            expected_length = self._get_expected_rtu_length(buffer)
            if len(buffer) < expected_length:
                continue

            # Проверка CRC
            #print("PRE_CRC ", buffer.hex())
            crc_received = buffer[-2:]  # Последние 2 байта - CRC
            crc_calculated = self._calculate_crc(buffer[:-2])
            if crc_received != crc_calculated:
                buffer.clear()
                continue

            # Обработка корректного пакета
            request = buffer.copy()
            print("REQUEST ", buffer.hex())
            buffer.clear()
            # Вызов колбэка если он установлен
            function_code = request[1]


            # Формирование ответа (если не широковещательный запрос)
            if request[0] != 0:
                response = self._process_request(request)
                if response:

                    print("RESPONSE ", response.hex())
                    self.serial.write(response)
            if function_code in self.callbacks:
                self.callbacks[function_code](request)



    def _get_expected_rtu_length(self, data):
        """Определение ожидаемой длины пакета RTU на основе кода функции"""
        if len(data) < 2:
            return 4  # минимальная длина (адрес + функция + CRC)

        function_code = data[1]

        # Базовые длины для разных функций
        lengths = {

            #TODO(Проверить длины)
            self.READ_COILS: 8,
            self.READ_DISCRETE_INPUTS: 8,
            self.READ_HOLDING_REGISTERS: 8,
            self.READ_INPUT_REGISTERS: 8,
            self.WRITE_SINGLE_COIL: 8,
            self.WRITE_SINGLE_REGISTER: 8,
            self.WRITE_MULTIPLE_COILS: 9 + data[6] if len(data) > 7 else 9,
            self.WRITE_MULTIPLE_REGISTERS: 9 + data[6] if len(data) > 7 else 9
        }

        return lengths.get(function_code, 256)  # 256 - максимальная длина по умолчанию

    def _calculate_crc(self, data):
        """Вычисление CRC16 для RTU пакета"""
        crc = self.crc16(data)
        return struct.pack('<H', crc)

    def _process_request(self, request):
        """Обработка Modbus запроса и формирование ответа"""

        slave_id = request[0]

        pdu = request[1:-2]  # Исключаем адрес и CRC


        function_code = pdu[0] if len(pdu) > 1 else None

        try:
            if function_code == self.READ_COILS:
                return self._read_coils(slave_id, pdu)
            elif function_code == self.READ_DISCRETE_INPUTS:
                return self._read_discrete_inputs(slave_id, pdu)
            elif function_code == self.READ_HOLDING_REGISTERS:
                return self._read_holding_registers(slave_id, pdu)
            elif function_code == self.READ_INPUT_REGISTERS:
                return self._read_input_registers(slave_id, pdu)
            elif function_code == self.WRITE_SINGLE_COIL:
                return self._write_single_coil(slave_id, pdu)
            elif function_code == self.WRITE_SINGLE_REGISTER:
                return self._write_single_register(slave_id, pdu)
            elif function_code == self.WRITE_MULTIPLE_COILS:
                return self._write_multiple_coils(slave_id, pdu)
            elif function_code == self.WRITE_MULTIPLE_REGISTERS:
                return self._write_multiple_registers(slave_id, pdu)
            else:
                return self._exception_response(slave_id, function_code, self.ILLEGAL_FUNCTION)
        except IndexError:
            return self._exception_response(slave_id, function_code, self.ILLEGAL_DATA_ADDRESS)
        except Exception:
            return self._exception_response(slave_id, function_code, self.ILLEGAL_DATA_VALUE)

    def _write_multiple_registers(self, slave_id, pdu):
        address = struct.unpack('>H', pdu[1:3])[0]
        quantity = struct.unpack('>H', pdu[3:5])[0]

        byte_count = quantity * 2

        reg_data = []

        for i in range(quantity):
            data = struct.unpack('>H', pdu[6 + i * 2:8 + i * 2])[0]
            self.data_store["holding_registers"][address + i] = data
            reg_data.append(data)

        response = bytearray([slave_id, self.WRITE_MULTIPLE_REGISTERS]) + pdu[1:3] + pdu[3:5]
        response += self._calculate_crc(response)

        return response

    def _write_single_register(self, slave_id, pdu):
        address = struct.unpack('>H', pdu[1:3])[0]
        data = struct.unpack('>H', pdu[3:5])[0]

        self.data_store["holding_registers"][address] = data

        response = bytearray([slave_id, self.WRITE_SINGLE_REGISTER]) + address.to_bytes(2, 'big') + data.to_bytes(2, 'big')
        response += self._calculate_crc(response)

        return response



    def _write_single_coil(self, slave_id, pdu):

        # TODO(ХЗ РАБОТАЕТ ЛИ ВОО БЩ+Е, ДАНЯ ПИ)
        address = struct.unpack('>H', pdu[1:3])[0]
        quantity = struct.unpack('>H', pdu[3:5])[0]

        byte_count = (quantity + 7) // 8

        coils_data = []


        for i in range(quantity):
            data = struct.unpack('>H', pdu[5+i*2:7+i*2])[0]
            self.data_store["coils"][address + i] = data
            coils_data.append(data)

        response = bytearray([slave_id, self.READ_COILS, byte_count, coils_data])
        response += self._calculate_crc(response)

        return response


    def _read_coils(self, slave_id, pdu):
        """Обработка функции чтения coils (0x01)"""
        address = struct.unpack('>H', pdu[1:3])[0]
        quantity = struct.unpack('>H', pdu[3:5])[0]

        if quantity < 1 or quantity > 2000:
            return self._exception_response(slave_id, self.READ_COILS, self.ILLEGAL_DATA_VALUE)

        end_address = address + quantity - 1
        if end_address >= len(self.data_store['coils']):
            return self._exception_response(slave_id, self.READ_COILS, self.ILLEGAL_DATA_ADDRESS)

        # Формирование данных ответа
        byte_count = (quantity + 7) // 8
        coils_data = bytearray(byte_count)

        for i in range(quantity):
            if self.data_store['coils'][address + i]:
                coils_data[i // 8] |= 1 << (i % 8)

        # Формирование ответа

        response = bytearray([slave_id, self.READ_COILS, byte_count]) + coils_data
        response += self._calculate_crc(response)

        return response

    def _read_discrete_inputs(self, slave_id, pdu):
        """Обработка функции чтения дискретных входов (0x02)"""
        # Аналогично _read_coils, но для discrete_inputs
        pass

    def _read_holding_registers(self, slave_id, pdu):
        """Обработка функции чтения holding регистров (0x03)"""
        address = struct.unpack('>H', pdu[1:3])[0]
        #address = 0
        quantity = struct.unpack('>H', pdu[3:5])[0]

        if quantity == 1:
            pass
        if quantity < 1 or quantity > 125:
            return self._exception_response(slave_id, self.READ_HOLDING_REGISTERS, self.ILLEGAL_DATA_VALUE)

        end_address = address + quantity - 1
        if end_address >= len(self.data_store['holding_registers']):
            return self._exception_response(slave_id, self.READ_HOLDING_REGISTERS, self.ILLEGAL_DATA_ADDRESS)

        # Формирование данных ответа
        byte_count = quantity * 2
        registers_data = bytearray(byte_count)

        for i in range(quantity):
            registers_data[i * 2:(i * 2) + 2] = struct.pack('>H', self.data_store['holding_registers'][address + i])

        # Формирование ответа

        response = bytearray([slave_id, self.READ_HOLDING_REGISTERS, byte_count]) + registers_data
        response += self._calculate_crc(response)


        return response

    def _exception_response(self, slave_id, function_code, exception_code):
        """Формирование ответа с исключением"""

        response = bytearray([slave_id, function_code | 0x80, exception_code])
        response += self._calculate_crc(response)


        return response



    # Другие методы обработки функций Modbus (_write_single_coil, _write_single_register и т.д.)
    # ...


# # Пример использования
# if __name__ == '__main__':
#     def my_callback(request):
#         print(f"Получен корректный Modbus запрос: {request.hex()}")
#
#
#     # Создание и запуск Modbus Slave в режиме RTU
#     slave = ModbusSlave(port='/dev/ttyUSB0', baudrate=19200, slave_id=1)
#
#     # Установка колбэка для функции чтения holding регистров (0x03)
#     slave.set_callback(slave.READ_HOLDING_REGISTERS, my_callback)
#
#     slave.start()
#
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         slave.stop()