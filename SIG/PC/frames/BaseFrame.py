import struct
import tkinter as tk
import os
from PIL import Image, ImageTk
from tkinter import simpledialog
from utils.constants_for_regs import *
import sys
import bidict


class BaseFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.start_mode = None
        self.start_automat_n3 = None
        self.controller = controller
        self.bind("<<ShowFrame>>", self.on_show_frame)
        self.bind("<<HideFrame>>", self.on_hide_frame)

        self.after_id = None

        # Переменные для фона
        self.bg_image = None
        self.bg_image_raw = None
        self.bg_label = tk.Label(self)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_label.bind("<Button-1>", self._print_click_coordinates)
        self.bind("<Button-1>", self._print_click_coordinates)

        # Основной контейнер для содержимого
        # self.content = tk.Frame(self)
        # self.content.place(relx=0.5, rely=0.5, anchor="center")

        # Привязка к изменению размера окна
        self.bind("<Configure>", self._resize_background)

        self.resources_dir = os.path.join(os.path.dirname(__file__), '..', 'imgs')

        # Добавляем привязку горячей клавиши для дебага (Ctrl+Alt+Shift+D)
        self.bind_all("<Control-Alt-Shift-D>", self.show_debug_window)
        self.debug_window = None  # Ссылка на дебаг-окно



    def load_image(self, filename, size=None):
        """Универсальная загрузка изображений с обработкой ошибок"""
        try:
            path = os.path.join(self.resources_dir, filename)
            img = Image.open(path)
            if size:
                img = img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Ошибка загрузки {filename}: {e}")
            return None

    def on_show_frame(self, event=None):
        # Метод, вызываемый при показе фрейма
        if self.__class__.__name__ == "MainMenu":
            self.controller.slave.data_store["holding_registers"][CURRENT_FRAME_REG] = 3
        if self.__class__.__name__ == "ManualMode":
            self.controller.slave.data_store["holding_registers"][CURRENT_FRAME_REG] = 4
        if self.__class__.__name__ == "CycleMode":
            self.controller.slave.data_store["holding_registers"][CURRENT_FRAME_REG] = 5
        if self.__class__.__name__ == "StatMode":
            self.controller.slave.data_store["holding_registers"][CURRENT_FRAME_REG] = 6
        if self.__class__.__name__ == "StatSettings":
            self.controller.slave.data_store["holding_registers"][CURRENT_FRAME_REG] = 7
        if self.__class__.__name__ == "CycleSettings":
            self.controller.slave.data_store["holding_registers"][CURRENT_FRAME_REG] = 8

        self.stop_after()  # Отменяем текущие задачи фрейма
        # Запускаем новую задачу и сохраняем её ID
        self.after_id = self.after(200, self.after_update)

    def on_hide_frame(self, event=None):
        """Вызывается при скрытии фрейма"""
        self.stop_after()

    def stop_after(self):
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None

    def after_update(self):
        self.update_widgets()
        # Перезапускаем задачу и обновляем after_id
        self.after_id = self.after(1000, self.after_update)

    def update_widgets(self):
        print("base")

    def set_background(self, image_path):
        """Установка фонового изображения с автоматическим масштабированием"""
        try:
            self.bg_image_raw = Image.open(image_path)
            self._resize_background()
        except Exception as e:
            print(f"Ошибка загрузки фона: {e}")

    def _resize_background(self, event=None):
        """Масштабирование фонового изображения под текущий размер окна"""
        if self.bg_image_raw:
            # Получаем текущие размеры окна
            width = self.winfo_width()
            height = self.winfo_height()

            if width > 0 and height > 0:
                # Масштабируем изображение с сохранением пропорций
                image = self.bg_image_raw.copy()
                image.thumbnail((width, height), Image.Resampling.LANCZOS)

                # Создаем изображение для Tkinter
                self.bg_image = ImageTk.PhotoImage(image)
                self.bg_label.config(image=self.bg_image)
                self.bg_label.lower()  # Отправляем фон на задний план

    def _print_click_coordinates(self, event):
        """Вывод координат клика в консоль"""
        print(f"Клик на координатах: x={event.x}, y={event.y}")
        print(f"Экранные координаты: x_root={event.x_root}, y_root={event.y_root}")

    def ask_value_in_range(self, title, prompt, initial_value, min_value, max_value, ask_float=False):
        """Диалог ввода числа в заданном диапазоне."""
        while True:
            if ask_float:
                value = simpledialog.askfloat(title, prompt, initialvalue=initial_value)
            else:
                value = simpledialog.askinteger(title, prompt, initialvalue=initial_value)
            if value is None:  # Если нажата "Отмена"
                return None
            if min_value <= value <= max_value or value == 0:
                return value
            tk.messagebox.showerror("Ошибка", f"Допустимый диапазон: {min_value}-{max_value}")

    def on_entry_click(self, event, regs,  min_val=13, max_val=100, entry=None, ask_float=False):
        """Обработчик клика по Entry с настраиваемым диапазоном."""

        current_value = entry.get()
        try:
            current_value = current_value
        except ValueError:
            current_value = min_val  # Значение по умолчанию

        new_value = self.ask_value_in_range(
            title="Ввод частоты",
            prompt=f"Введите значение ({min_val}-{max_val}):",
            initial_value=current_value,
            min_value=min_val,
            max_value=max_val,
            ask_float=ask_float
        )

        if new_value is not None:

            if ask_float:
                f_bytes = struct.pack('<f', new_value)  # Упаковка float в байты
                f_uint = struct.unpack('<I', f_bytes)[0]  # Преобразование в unsigned int
                f_hex = f"{f_uint:08x}"  # Форматирование в 8-значный hex (с ведущими нулями)

                # Теперь можно безопасно разбивать:
                self.controller.slave.data_store["holding_registers"][regs] = int(f_hex[4:8], 16)  # Младшие 2 байта
                self.controller.slave.data_store["holding_registers"][regs + 1] = int(f_hex[0:4], 16)  # Старшие 2 байта

            else:
                self.controller.slave.data_store["holding_registers"][regs] = new_value

    def show_debug_window(self, event=None):
        """Отображение/скрытие дебаг-окна"""
        if self.debug_window is None or not self.debug_window.winfo_exists():
            self.create_debug_window()
        else:
            self.debug_window.destroy()
            self.debug_window = None

    def create_debug_window(self):
        """Создание дебаг-окна с полезной информацией"""
        self.debug_window = tk.Toplevel(self)
        self.debug_window.title("Debug Information")
        self.debug_window.geometry("600x800")

        # Делаем окно поверх других
        self.debug_window.attributes('-topmost', True)

        # Создаем текстовое поле с прокруткой
        text_frame = tk.Frame(self.debug_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        debug_text = tk.Text(
            text_frame,
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD,
            font=('Consolas', 10)
        )
        debug_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=debug_text.yview)

        # Добавляем информацию в дебаг-окно
        debug_info = self.get_debug_info()
        debug_text.insert(tk.END, debug_info)
        debug_text.config(state=tk.DISABLED)  # Делаем текст только для чтения

        # Кнопка обновления
        btn_frame = tk.Frame(self.debug_window)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Button(
            btn_frame,
            text="Refresh",
            command=lambda: self.update_debug_info(debug_text)
        ).pack(side=tk.LEFT)

        tk.Button(
            btn_frame,
            text="Close",
            command=self.debug_window.destroy
        ).pack(side=tk.RIGHT)

    def get_debug_info(self):
        """Собирает отладочную информацию"""
        info = [
            "=== DEBUG INFORMATION ===",
            f"Current frame: {self.__class__.__name__}",
            f"Window size: {self.winfo_width()}x{self.winfo_height()}",
            f"Controller: {self.controller.__class__.__name__}",
            "\n=== Widgets Info ===",
            f"Children widgets count: {len(self.winfo_children())}",
            "\n=== System Info ===",
            f"Tkinter version: {tk.Tcl().eval('info patchlevel')}",
            f"Python version: {sys.version.split()[0]}",
            "\n=== Custom Debug ===",
            "Add your custom debug data here..."
        ]

        # Добавляем информацию о контроллере, если есть нужные атрибуты
        if hasattr(self.controller, 'slave') and hasattr(self.controller.slave, 'data_store'):
            info.append("\n=== Modbus Registers ===")
            info.append(
                f"CURRENT_FRAME_REG: {self.controller.slave.data_store['holding_registers'][CURRENT_FRAME_REG]}\n"
                f"START_AUTOMAT_N3_MANUAL_REG: {self.controller.slave.data_store['holding_registers'][START_AUTOMAT_N3_MANUAL_REG]}\n"
                f"START_MODE_MANUAL_REG: {self.controller.slave.data_store['holding_registers'][START_MODE_MANUAL_REG]}\n"
                f"START_AUTOMAT_N3_STAT_REG: {self.controller.slave.data_store['holding_registers'][START_AUTOMAT_N3_STAT_REG]}\n"
                f"START_MODE_STAT_REG: {self.controller.slave.data_store['holding_registers'][START_MODE_STAT_REG]}\n"
                f"START_AUTOMAT_N3_CYCLE_REG: {self.controller.slave.data_store['holding_registers'][START_AUTOMAT_N3_CYCLE_REG]}\n"
                f"START_MODE_CYCLE_REG: {self.controller.slave.data_store['holding_registers'][START_MODE_CYCLE_REG]}\n"
                f"PRESSURE_MN1: {self.controller.slave.data_store['holding_registers'][PRESSURE_MN1], self.controller.slave.data_store['holding_registers'][PRESSURE_MN1 + 1]}\n"
                f"PRESSURE_MN2: {self.controller.slave.data_store['holding_registers'][PRESSURE_MN2], self.controller.slave.data_store['holding_registers'][PRESSURE_MN2 + 1]}\n"
                f"SPEED: {self.controller.slave.data_store['holding_registers'][SPEED], self.controller.slave.data_store['holding_registers'][SPEED + 1]}\n"
                f"FREQ_MANUAL: {self.controller.slave.data_store['holding_registers'][FREQ_MANUAL]}\n"
                f"PRESSURE_END_STAT: {self.controller.slave.data_store['holding_registers'][PRESSURE_END_STAT], self.controller.slave.data_store['holding_registers'][PRESSURE_END_STAT + 1]}\n"
                f"PRESSURE_MID_STAT: {self.controller.slave.data_store['holding_registers'][PRESSURE_MID_STAT], self.controller.slave.data_store['holding_registers'][PRESSURE_MID_STAT + 1]}\n"
                f"PRESSURE_SPEED_STAT: {self.controller.slave.data_store['holding_registers'][PRESSURE_SPEED_STAT], self.controller.slave.data_store['holding_registers'][PRESSURE_SPEED_STAT + 1]}\n"
                f"TIME_WAIT_1_STAT: {self.controller.slave.data_store['holding_registers'][TIME_WAIT_1_STAT]}\n"
                f"TIME_WAIT_2_STAT: {self.controller.slave.data_store['holding_registers'][TIME_WAIT_2_STAT]}\n"
                f"PRESSURE_END_CYCLE: {self.controller.slave.data_store['holding_registers'][PRESSURE_END_CYCLE], self.controller.slave.data_store['holding_registers'][PRESSURE_END_CYCLE + 1]}\n"
                f"PRESSURE_SPEED_CYCLE: {self.controller.slave.data_store['holding_registers'][PRESSURE_SPEED_CYCLE], self.controller.slave.data_store['holding_registers'][PRESSURE_SPEED_CYCLE + 1]}\n"
                f"TIME_PAUSE_CYCLE: {self.controller.slave.data_store['holding_registers'][TIME_PAUSE_CYCLE]}\n"
                f"NUMBER_OF_CYCLES: {self.controller.slave.data_store['holding_registers'][NUMBER_OF_CYCLES]}\n"
                f"DROP_NUMBER_OF_CYCLES: {self.controller.slave.data_store['holding_registers'][DROP_NUMBER_OF_CYCLES]}\n"
                f"WARNING_SCREENS: {self.controller.slave.data_store['holding_registers'][WARNING_SCREENS]}\n"
                f"WARNING_BUTTON_BLOCK: {self.controller.slave.data_store['holding_registers'][WARNING_BUTTON_BLOCK]}\n"
                f"WORK: {self.controller.slave.data_store['holding_registers'][WORK]}\n"
            )

        return "\n".join(info)

    def update_debug_info(self, text_widget):
        """Обновляет информацию в дебаг-окне"""
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, self.get_debug_info())
        text_widget.config(state=tk.DISABLED)

    def get_float_from_registers(self, start_reg):
        """Получение float значения из двух 16-битных регистров"""
        try:
            register0 = self.controller.slave.data_store["holding_registers"][start_reg]
            register1 = self.controller.slave.data_store["holding_registers"][start_reg + 1]
            uint32 = (register1 << 16) | register0
            return struct.unpack('<f', struct.pack('<I', uint32))[0]
        except (KeyError, IndexError, struct.error) as e:
            print(f"Error reading registers {start_reg}-{start_reg+1}: {e}")
            return 0.0  # Значение по умолчанию при ошибке

    def start_mode_func(self, button, reg):
        print("Старт режима")
        if button.cget("style") == "NonActive.TButton":

            if reg in [START_AUTOMAT_N3_CYCLE_REG, START_AUTOMAT_N3_MANUAL_REG, START_AUTOMAT_N3_STAT_REG]:
                self.controller.slave.data_store["holding_registers"][START_AUTOMAT_N3_CYCLE_REG] = 1
                self.controller.slave.data_store["holding_registers"][START_AUTOMAT_N3_MANUAL_REG] = 1
                self.controller.slave.data_store["holding_registers"][START_AUTOMAT_N3_STAT_REG] = 1
            else:
                self.controller.slave.data_store["holding_registers"][reg] = 1
            button.configure(style="Active.TButton")
        else:
            if reg in [START_AUTOMAT_N3_CYCLE_REG, START_AUTOMAT_N3_MANUAL_REG, START_AUTOMAT_N3_STAT_REG]:

                self.controller.slave.data_store["holding_registers"][START_AUTOMAT_N3_CYCLE_REG] = 0
                self.controller.slave.data_store["holding_registers"][START_AUTOMAT_N3_MANUAL_REG] = 0
                self.controller.slave.data_store["holding_registers"][START_AUTOMAT_N3_STAT_REG] = 0
            else:
                self.controller.slave.data_store["holding_registers"][reg] = 0
            button.configure(style="NonActive.TButton")

    def update_button_state_by_register(self,  start_n3_reg, start_mode_reg):
        if self.controller.slave.data_store["holding_registers"][start_n3_reg] == 1:
            self.start_automat_n3.configure(style="Active.TButton")
        if self.controller.slave.data_store["holding_registers"][start_n3_reg] == 0:
            self.start_automat_n3.configure(style="NonActive.TButton")

        if self.controller.slave.data_store["holding_registers"][start_mode_reg] == 1:
            self.start_mode.configure(style="Active.TButton")
        if self.controller.slave.data_store["holding_registers"][start_mode_reg] == 0:
            self.start_mode.configure(style="NonActive.TButton")

    def refresh_entry(self, entry, reg, is_float):
        if is_float:
            new_value = self.get_float_from_registers(reg)
        else:
            new_value = self.controller.slave.data_store["holding_registers"][reg]
        entry.config(state="normal")
        entry.delete(0, tk.END)
        entry.insert(0, str(new_value))
        entry.config(state="readonly")

