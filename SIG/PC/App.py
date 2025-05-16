import tkinter as tk
from tkinter import ttk

from frames.MainMenu import MainMenu
from frames.StatSettings import StatSettings
from frames.CycleSettings import CycleSettings
from frames.ManualMode import ManualMode
from frames.StatMode import StatMode
from frames.CycleMode import CycleMode

from utils.ModbusSlave import ModbusSlave
from utils.constants_for_regs import *
import bidict
from utils.math_functions import get_kgs



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Управление режимами")
        self.geometry("800x480")

        self.screen_numbers = bidict.bidict({
            "MainMenu": 3,
            "ManualMode": 4,
            "CycleMode": 5,
            "StatMode": 6,
            "StatSettings": 7,
            "CycleSettings": 8,
        })

        # Контейнер для всех фреймов
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.after_id = None
        self.plots_upd_id = None

        self.style = ttk.Style()
        self.style.theme_use('alt')

        self.current_frame = None  # Текущий активный фрейм

        # Установка шрифта по умолчанию для всех кнопок
        self.style.configure("Main.TButton",
                             font=('Times New Roman', 32),
                             padding=6, anchor="center", background="white")

        self.style.configure("Second.TButton",
                             font=('Times New Roman', 14),
                             padding=0, anchor="nsew", wraplength=120, background="white")

        self.style.configure("Main.TEntry",
                             padding=1, foreground="black")

        self.style.configure("Main.TLabel",
                             font=('Times New Roman', 22),
                             padding=0, background="white", anchor="center", borderwidth=3, bordercolor="black",
                             relief="solid")

        self.style.map("NonActive.TButton",
                       background=[("!active", "#808080"), ("active", "#b3b3b3")],
                       foreground=[("!active", "white"), ("active", "white")])

        self.style.configure("NonActive.TButton",
                             font=('Times New Roman', 14),
                             wraplength=120)

        self.style.map("Active.TButton",
                       background=[("!active", "#32cd32"), ("active", "#5ad65a")],
                       foreground=[("!active", "black"), ("active", "black")])

        self.style.configure("Active.TButton",
                             font=('Times New Roman', 14),
                             wraplength=120)

        self.speed_mpa_var = tk.DoubleVar(value=3.2)

        self.mn1_mpa_var = tk.DoubleVar()
        self.mn1_kgs_var = tk.DoubleVar()
        self.mn1_mpa_var.trace_add("write", self.update_kgs1)
        self.mn1_mpa_var.set(0.2)
        self.mn2_mpa_var = tk.DoubleVar()
        self.mn2_kgs_var = tk.DoubleVar()
        self.mn2_mpa_var.trace_add("write", self.update_kgs2)
        self.mn2_mpa_var.set(0.3)
        self.number_of_cycles_var = tk.IntVar()
        self.number_of_cycles_var.set(0)


        self.frames = {}

        self.slave = ModbusSlave(baudrate=38400, slave_id=2)

        self.slave.set_callback(self.slave.WRITE_MULTIPLE_REGISTERS, self.write_registers_callback)
        self.slave.set_callback(self.slave.WRITE_SINGLE_REGISTER, self.write_registers_callback)

        # Создаем все экраны
        for F in (MainMenu, StatSettings, CycleSettings, ManualMode, StatMode, CycleMode):
            frame = F(self.container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")
        
        try:
            self.slave.start()
        except Exception as e:
            print(e)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self._center_window()
        self.plots_upd_id = self.after(1000, self.plots_upd)


    def plots_upd(self):
        pressure = self.frames["ManualMode"].get_float_from_registers(PRESSURE_MN1)

        self.frames["ManualMode"].pressure_graph.update_data(pressure)
        self.frames["StatMode"].pressure_graph.update_data(pressure)
        self.frames["CycleMode"].pressure_graph.update_data(pressure)
        # UPD
        self.plots_upd_id = self.after(1000, self.plots_upd)


    def on_close(self):
        for frame in self.frames.values():
            frame.event_generate("<<HideFrame>>")

        try:
            self.slave.stop()
        except Exception as e:
            print(e)

        self.frames["ManualMode"].pressure_graph.cleanup() if hasattr(self.frames["ManualMode"],
                                                                      'pressure_graph') else None
        self.frames["StatMode"].pressure_graph.cleanup() if hasattr(self.frames["StatMode"],
                                                                    'pressure_graph') else None
        self.frames["CycleMode"].pressure_graph.cleanup() if hasattr(self.frames["CycleMode"],
                                                                     'pressure_graph') else None
        self.destroy()

    def write_registers_callback(self, request):
        # Обновление экрана
        if self.slave.data_store["holding_registers"][CURRENT_FRAME_REG] != self.screen_numbers[self.current_frame.__class__.__name__]:
            self.show_frame(self.screen_numbers.inverse[self.slave.data_store["holding_registers"][CURRENT_FRAME_REG]])
            
        # Обновление состояния кнопок
        self.frames["ManualMode"].update_button_state_by_register(START_AUTOMAT_N3_MANUAL_REG, START_MODE_MANUAL_REG)
        self.frames["StatMode"].update_button_state_by_register(START_AUTOMAT_N3_STAT_REG, START_MODE_STAT_REG)
        self.frames["CycleMode"].update_button_state_by_register(START_AUTOMAT_N3_CYCLE_REG, START_MODE_CYCLE_REG)

    def show_frame(self, cont):
        """Показ фрейма с обработкой переключения"""
        # Уведомляем предыдущий фрейм о скрытии
        if self.current_frame:
            self.current_frame.event_generate("<<HideFrame>>")

        # Получаем новый фрейм
        frame = self.frames[cont]

        # Уведомляем новый фрейм о показе
        frame.event_generate("<<ShowFrame>>")
        frame.tkraise()

        # Обновляем текущий фрейм
        self.current_frame = frame

    def _center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    
    def update_kgs1(self, *args):
        mpa_value = self.mn1_mpa_var.get()
        rounded_kgs = round(get_kgs(mpa_value), 1)
        self.mn1_kgs_var.set(rounded_kgs)

    def update_kgs2(self, *args):
        mpa_value = self.mn2_mpa_var.get()
        rounded_kgs = round(get_kgs(mpa_value), 1)
        self.mn2_kgs_var.set(rounded_kgs)
