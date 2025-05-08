from frames.BaseFrame import BaseFrame
from tkinter import ttk

from utils.PressureGraph import PressureGraph
from utils.constants_for_regs import *


class StatMode(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.set_background('imgs/stat_mode.png')

        # Кнопка возврата к настройкам
        btn_settings = ttk.Button(self, text="Настройки\n  режима",
                                  command=lambda: controller.show_frame("StatSettings"), style="Second.TButton")
        btn_settings.place(x=10, y=10, width=120, height=50)

        # btn_test = ttk.Button(self, text="TECT", command=self.test, style="Second.TButton")
        # btn_test.place(x=50, y=50, width = 120, height=50)

        self.mn1_mpa = ttk.Label(self, style="Main.TLabel", text="0.0", textvariable=self.controller.mn1_mpa_var)
        self.mn1_mpa.place(x=128, y=96, width=76)

        self.mn1_kgs = ttk.Label(self, style="Main.TLabel", text="0.0", textvariable=self.controller.mn1_kgs_var)
        self.mn1_kgs.place(x=319, y=97, width=84)

        self.mn2_mpa = ttk.Label(self, style="Main.TLabel", text="0.0", textvariable=self.controller.mn2_mpa_var)
        self.mn2_mpa.place(x=128, y=176, width=76)

        self.mn2_kgs = ttk.Label(self, style="Main.TLabel", text="0.0", textvariable=self.controller.mn2_kgs_var)
        self.mn2_kgs.place(x=319, y=177, width=84)

        self.current_speed = ttk.Label(self, style="Main.TLabel", text="0.0", textvariable=self.controller.speed_mpa_var)
        self.current_speed.place(x=655, y=177, width=66)

        self.start_automat_n3 = ttk.Button(self, text="Запуск автомат Н3", style="NonActive.TButton",
                                           command=lambda :self.start_mode_func(self.start_automat_n3, START_AUTOMAT_N3_STAT_REG))
        self.start_automat_n3.place(x=630, y=260, width=120, height=50)

        self.start_mode = ttk.Button(self, text="Запуск режима", command=lambda: self.start_mode_func(self.start_mode, START_MODE_STAT_REG),
                                     style="NonActive.TButton")
        self.start_mode.place(x=630, y=360, width=120, height=50)

        # Инициализация графика
        self.pressure_graph = PressureGraph(self)

    def test(self):
        print(self.controller.frames["StatSettings"].get_ent_pressure_end())

    def set_mn1_mpa(self, text):
        self.mn1_mpa.configure(text=text)

    def set_mn1_kgs(self, text):
        self.mn1_kgs.configure(text=text)

    def set_mn2_mpa(self, text):
        self.mn2_mpa.configure(text=text)

    def set_mn2_kgs(self, text):
        self.mn2_kgs.configure(text=text)

    def set_current_speed(self, text):
        self.current_speed.configure(text=text)

    def update_widgets(self):
        print("Stat Mode")
        mn1_value = self.get_float_from_registers(PRESSURE_MN1)
        self.controller.mn1_mpa_var.set(round(mn1_value, 1))

        # Обновление MN2
        mn2_value = self.get_float_from_registers(PRESSURE_MN2)
        self.controller.mn2_mpa_var.set(round(mn2_value, 1))

        # Обновление скорости
        speed_value = self.get_float_from_registers(SPEED)
        self.controller.speed_mpa_var.set(round(speed_value, 1))

