from frames.BaseFrame import BaseFrame
from tkinter import ttk
from utils.constants_for_regs import *


class MainMenu(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.set_background("imgs/main_menu.png")

        # Кнопки главного меню
        btn_stat = ttk.Button(self, text="Статический режим",
                              command=lambda: controller.show_frame("StatSettings"), style="Main.TButton")
        btn_cycle = ttk.Button(self, text="Циклический режим",
                               command=lambda: controller.show_frame("CycleSettings"), style="Main.TButton")
        btn_manual = ttk.Button(self, text="Ручной режим",
                                command=lambda: controller.show_frame("ManualMode"), style="Main.TButton")

        btn_stat.place(x=200, y=130, width=395, height=68)
        btn_cycle.place(x=200, y=240, width=395, height=68)
        btn_manual.place(x=200, y=350, width=395, height=68)

    def update_widgets(self):
        print("main menu")

    def test(self):
        self.controller.slave.data_store["holding_registers"][CURRENT_FRAME_REG] = 4

        self.controller.write_multiple_registers_callback(0)
