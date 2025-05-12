from frames.BaseFrame import BaseFrame
from tkinter import ttk

from utils.constants_for_regs import *


class CycleSettings(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.set_background('imgs/cycle_settings.png')
        # Здесь можно добавить настройки для циклического режима
        # label = ttk.Label(self, text="Настройки циклического режима", font=('Helvetica', 14))
        # label.pack(pady=20)

        self.ent_pressure_end = ttk.Entry(self, style="Main.TEntry", font=('Times New Roman', 24), justify="center",
                                        state="readonly")
        self.ent_pressure_end.insert(0, "0.0")

        self.ent_pressure_end.bind("<Button-1>",
                                   lambda e: self.on_entry_click(e, PRESSURE_END_CYCLE, min_val=PRESSURE_END_MIN_MAX[0],
                                                                 max_val=PRESSURE_END_MIN_MAX[1],
                                                                 entry=self.ent_pressure_end,
                                                                 ask_float=True))

        self.ent_pressure_end.place(x=454, y=94, width=112)

        self.ent_pressure_speed = ttk.Entry(self, style="Main.TEntry", font=('Times New Roman', 24), justify="center",
                                        state="readonly")
        self.ent_pressure_speed.insert(0, "0.0")

        self.ent_pressure_speed.bind("<Button-1>",
                            lambda e: self.on_entry_click(e, PRESSURE_SPEED_CYCLE, min_val=PRESSURE_SPEED_MIN_MAX[0],
                                                          max_val=PRESSURE_SPEED_MIN_MAX[1],
                                                          entry=self.ent_pressure_speed,
                                                          ask_float=True))

        self.ent_pressure_speed.place(x=454, y=174, width=112)

        self.ent_time_pause = ttk.Entry(self, style="Main.TEntry", font=('Times New Roman', 24), justify="center",
                                        state="readonly")
        self.ent_time_pause.insert(0, "0")

        self.ent_time_pause.bind("<Button-1>",
                            lambda e: self.on_entry_click(e, TIME_PAUSE_CYCLE , min_val=TIME_WAIT_MIN_MAX[0],
                                                          max_val=TIME_WAIT_MIN_MAX[1],
                                                          entry=self.ent_time_pause,
                                                          ask_float=False))

        self.ent_time_pause.place(x=454, y=254, width=112)


        self.cycle_need = ttk.Entry(self, style="Main.TEntry", font=('Times New Roman', 24), justify="center",
                                        state="readonly")
        self.cycle_need.insert(0, "0")

        self.cycle_need.bind("<Button-1>",
                            lambda e: self.on_entry_click(e, CYCLES_NEED_CYCLE , min_val=TIME_WAIT_MIN_MAX[0],
                                                          max_val=TIME_WAIT_MIN_MAX[1],
                                                          entry=self.cycle_need,
                                                          ask_float=False))

        self.cycle_need.place(x=454, y=330, width=112)


        self.reset_cycle_set = ttk.Button(self, text="Сбросить", command=self.reset_cycle_set_func,
                                          style="NonActive.TButton")
        self.reset_cycle_set.place(x=450, y=406, width=120, height=50)

        # Кнопки
        btn_back = ttk.Button(self, text="Выбор режима",
                              command=lambda: controller.show_frame("MainMenu"), style="Second.TButton")
        btn_start = ttk.Button(self, text="Запуск режима",
                               command=lambda: controller.show_frame("CycleMode"), style="Second.TButton")

        btn_back.place(x=10, y=10, width=120, height=50)
        btn_start.place(x=601, y=12, width=120, height=50)

    def reset_cycle_set_func(self):
        print("Сброс числа циклов")
        self.controller.slave.data_store["holding_registers"][DROP_NUMBER_OF_CYCLES] = 1
        # self.after(200, self.reset_reset_cycle_set_func)

    def reset_reset_cycle_set_func(self):
        self.controller.slave.data_store["holding_registers"][DROP_NUMBER_OF_CYCLES] = 0


    def get_ent_pressure_end(self):
        return self.ent_pressure_end.get()

    def get_ent_pressure_speed(self):
        return self.ent_pressure_speed.get()

    def get_ent_time_pause(self):
        return self.ent_time_pause.get()

    def update_widgets(self):
        print("Cycle Sets")
        self.refresh_entry(self.ent_pressure_end, PRESSURE_END_CYCLE, is_float=True)
        self.refresh_entry(self.ent_pressure_speed, PRESSURE_SPEED_CYCLE, is_float=True)
        self.refresh_entry(self.ent_time_pause, TIME_PAUSE_CYCLE, is_float=False)
        self.refresh_entry(self.cycle_need, CYCLES_NEED_CYCLE, is_float=False)
