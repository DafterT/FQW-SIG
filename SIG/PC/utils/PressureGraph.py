import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from tkinter import ttk

class PressureGraph:
    def __init__(self, parent, x=10, y=230, width=500, height=210):
        self.parent = parent
        self.time_data = []
        self.pressure_data = []
        self.current_x_offset = 0
        self.max_visible_points = 8

        # Создание фигуры matplotlib
        self.fig, self.ax = plt.subplots(figsize=(width / 80, height / 80))
        self.line, = self.ax.plot([], [], 'b-')
        self.ax.set_xlabel("Время", fontsize=8)
        self.ax.set_ylabel("Давление (МПа)", fontsize=8)
        self.ax.grid(True)

        # Размещение графика
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().place(x=x, y=y, width=width, height=height)

        # Кнопки управления
        self._create_controls(x, y + height + 10, width)

    def _create_controls(self, x, y, width):
        control_frame = ttk.Frame(self.parent)
        control_frame.place(x=x, y=y, width=width)

        self.btn_left = ttk.Button(control_frame, text="← Влево", command=self.scroll_left)
        self.btn_left.pack(side=tk.LEFT, padx=5)

        self.btn_right = ttk.Button(control_frame, text="→ Вправо", command=self.scroll_right)
        self.btn_right.pack(side=tk.LEFT, padx=5)

        self.btn_reset = ttk.Button(control_frame, text="Сброс", command=self.reset_view)
        self.btn_reset.pack(side=tk.LEFT, padx=5)

    def update_data(self, new_pressure):
        """Обновление данных графика (вызывается извне)"""
        current_time = datetime.now()
        self.time_data.append(current_time)
        self.pressure_data.append(new_pressure)

        if self.current_x_offset == 0:
            self._update_graph()

    def _update_graph(self):
        """Внутренний метод обновления графика"""
        if not self.time_data:
            return

        start_idx = max(0, len(self.time_data) - self.max_visible_points - self.current_x_offset)
        end_idx = len(self.time_data) - self.current_x_offset

        visible_times = self.time_data[start_idx:end_idx]
        visible_pressures = self.pressure_data[start_idx:end_idx]
        time_str = [t.strftime("%H:%M:%S") for t in visible_times]

        self.line.set_data(range(len(time_str)), visible_pressures)
        self.ax.set_xlim(0, len(time_str) - 1)
        self.ax.set_ylim(0, 50)

        self.ax.set_xticks(range(len(time_str)))
        self.ax.set_xticklabels(time_str, rotation=0)
        self.ax.tick_params(axis='both', labelsize=8)

        self.canvas.draw()

    def scroll_left(self):
        if len(self.time_data) > self.max_visible_points:
            self.current_x_offset = min(
                self.current_x_offset + 1,
                len(self.time_data) - self.max_visible_points
            )
            self._update_graph()

    def scroll_right(self):
        self.current_x_offset = max(0, self.current_x_offset - 1)
        self._update_graph()

    def reset_view(self):
        self.current_x_offset = 0
        self._update_graph()

    def cleanup(self):
        """Очистка ресурсов"""
        if hasattr(self, 'fig'):
            plt.close(self.fig)
        if hasattr(self, 'widget') and self.widget.winfo_exists():
            self.widget.destroy()