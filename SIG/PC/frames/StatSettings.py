from frames.BaseFrame import BaseFrame
from tkinter import ttk

from utils.constants_for_regs import *

class StatSettings(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        # Здесь можно добавить настройки для статического режима
        # label = ttk.Label(self.content, text="Настройки статического режима", font=('Helvetica', 14))
        # label.pack(pady=20)
        self.set_background("imgs/stat_settings.png")
        # Кнопки
        btn_back = ttk.Button(self, text="Выбор\nрежима",
                              command=lambda: controller.show_frame("MainMenu"), style="Second.TButton")
        btn_start = ttk.Button(self, text="Запуск\nрежима",
                               command=lambda: controller.show_frame("StatMode"), style="Second.TButton")

        btn_back.place(x=12, y=11, width=120, height=50)
        btn_start.place(x=601, y=11, width=120, height=50)

        self.ent_pressure_end = ttk.Entry(self, style="Main.TEntry", font=('Times New Roman', 24), justify="center",
                                        state="readonly")
        self.ent_pressure_end.insert(0, "0.0")

        self.ent_pressure_end.bind("<Button-1>",
                                        lambda e: self.on_entry_click(e, PRESSURE_END_STAT, min_val=PRESSURE_END_MIN_MAX[0],
                                                                      max_val=PRESSURE_END_MIN_MAX[1],
                                                                      entry=self.ent_pressure_end,
                                                                      ask_float=True))

        self.ent_pressure_end.place(x=454, y=94, width=112)

        self.ent_pressure_mid = ttk.Entry(self, style="Main.TEntry", font=('Times New Roman', 24), justify="center",
                                        state="readonly")
        self.ent_pressure_mid.insert(0, "0.0")

        self.ent_pressure_mid.bind("<Button-1>",
                                   lambda e: self.on_entry_click(e, PRESSURE_MID_STAT, min_val=PRESSURE_END_MIN_MAX[0],
                                                                 max_val=PRESSURE_END_MIN_MAX[1],
                                                                 entry=self.ent_pressure_mid,
                                                                 ask_float=True))

        self.ent_pressure_mid.place(x=454, y=174, width=112)

        self.ent_speed = ttk.Entry(self, style="Main.TEntry", font=('Times New Roman', 24), justify="center",
                                        state="readonly")
        self.ent_speed.insert(0, "0.0")

        self.ent_speed.bind("<Button-1>",
                                   lambda e: self.on_entry_click(e, PRESSURE_SPEED_STAT, min_val=PRESSURE_SPEED_MIN_MAX[0],
                                                                 max_val=PRESSURE_SPEED_MIN_MAX[1],
                                                                 entry=self.ent_speed,
                                                                 ask_float=True))

        self.ent_speed.place(x=454, y=254, width=112)

        self.time_wait_1 = ttk.Entry(self, style="Main.TEntry", font=('Times New Roman', 24), justify="center",
                                        state="readonly")
        self.time_wait_1.insert(0, "0")

        self.time_wait_1.bind("<Button-1>",
                            lambda e: self.on_entry_click(e, TIME_WAIT_1_STAT , min_val=TIME_WAIT_MIN_MAX[0],
                                                          max_val=TIME_WAIT_MIN_MAX[1],
                                                          entry=self.time_wait_1,
                                                          ask_float=False))

        self.time_wait_1.place(x=454, y=334, width=112)

        self.time_wait_2 = ttk.Entry(self, style="Main.TEntry", font=('Times New Roman', 24), justify="center",
                                        state="readonly")
        self.time_wait_2.insert(0, "0")

        self.time_wait_2.bind("<Button-1>",
                            lambda e: self.on_entry_click(e, TIME_WAIT_2_STAT, min_val=TIME_WAIT_MIN_MAX[0],
                                                          max_val=TIME_WAIT_MIN_MAX[1],
                                                          entry=self.time_wait_2,
                                                          ask_float=False))

        self.time_wait_2.place(x=454, y=414, width=112)

    def get_ent_pressure_end(self):
        return self.ent_pressure_end.get()

    def get_ent_pressure_mid(self):
        return self.ent_pressure_mid.get()

    def get_ent_speed(self):
        return self.ent_speed.get()

    def get_time_wait_1(self):
        return self.time_wait_1.get()

    def get_time_wait_2(self):
        return self.time_wait_2.get()

    def update_widgets(self):
        print("Stat Sets")
        self.refresh_entry(self.ent_pressure_end, PRESSURE_END_STAT, is_float=True)
        self.refresh_entry(self.ent_pressure_mid, PRESSURE_MID_STAT, is_float=True)
        self.refresh_entry(self.ent_speed, PRESSURE_SPEED_STAT, is_float=True)
        self.refresh_entry(self.time_wait_1, TIME_WAIT_1_STAT, is_float=False)
        self.refresh_entry(self.time_wait_2, TIME_WAIT_2_STAT, is_float=False)

