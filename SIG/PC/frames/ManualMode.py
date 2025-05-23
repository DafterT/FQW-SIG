import struct
import tkinter
from tkinter import ttk

from frames.BaseFrame import BaseFrame
from utils.PressureGraph import PressureGraph
from utils.constants_for_regs import *


class ManualMode(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.set_background('imgs/manual_mode.png')
        self.test_counter = 0

        # Основные элементы интерфейса
         # Кнопка возврата
        self.btn_settings = ttk.Button(self, text="Выбор режима",
                              command=lambda: self.controller.show_frame("MainMenu"),
                              style="Second.TButton")
        self.btn_settings.place(x=10, y=10, width=120, height=50)

        # Метки и поля ввода
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

        # Кнопки управления
        self.start_automat_n3 = ttk.Button(self, text="Запуск автомат Н3",
                                           style="NonActive.TButton",
                                           command=lambda :self.start_mode_func(self.start_automat_n3, START_AUTOMAT_N3_MANUAL_REG))
        self.start_automat_n3.place(x=630, y=260, width=120, height=50)

        self.start_mode = ttk.Button(self, text="Запуск режима",
                                     command=lambda: self.start_mode_func(self.start_mode, START_MODE_MANUAL_REG),
                                     style="NonActive.TButton")
        self.start_mode.place(x=630, y=330, width=120, height=50)
        
        self.start_valve = ttk.Button(self, text="Сброс давления",
                                     command=lambda: self.start_mode_func(self.start_valve, START_MODE_CYCLE_REG),
                                     style="NonActive.TButton")
        self.start_valve.place(x=630, y=400, width=120, height=50)

        self.ent_frequency_percent = ttk.Entry(self, style="Main.TEntry",
                                               font=('Times New Roman', 22),
                                               justify="center",
                                               state="readonly")
        self.ent_frequency_percent.insert(0, "0")
        self.ent_frequency_percent.place(x=654, y=94, width=72, height=42)

        self.ent_frequency_percent.bind("<Button-1>",
                                        lambda e: self.on_entry_click(e, FREQ_MANUAL, min_val=FREQ_MANUAL_MIN_MAX[0],
                                                                      max_val=FREQ_MANUAL_MIN_MAX[1],
                                                                      entry=self.ent_frequency_percent,
                                                                      ask_float=False))

        # Инициализация графика
        self.pressure_graph = PressureGraph(self)

    def update_widgets(self):
        mn1_value = self.get_float_from_registers(PRESSURE_MN1)
        self.controller.mn1_mpa_var.set(round(mn1_value, 1))

        # Обновление MN2
        mn2_value = self.get_float_from_registers(PRESSURE_MN2)
        self.controller.mn2_mpa_var.set(round(mn2_value, 1))

        # Обновление скорости
        speed_value = self.get_float_from_registers(SPEED)
        self.controller.speed_mpa_var.set(round(speed_value, 1))

        self.refresh_entry(self.ent_frequency_percent, FREQ_MANUAL, is_float=False)
        self.update_back_button_state(self.btn_settings)






