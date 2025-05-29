"""
Приложение SIG Plotter GUI.

Предоставляет интерфейс на основе Tkinter для выбора CSV-файла SIG,
ввода названия испытания и построения графика давления с помощью функции plot_built.plot_sig_data.
"""
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, font, ttk
from PIL import Image, ImageTk

import plot_built
from settings import *

class PlaceholderEntry(ttk.Entry):
    """Виджет ttk.Entry с функциональностью плейсхолдера."""

    def __init__(self, master, placeholder: str, prefix: str, **kwargs) -> None:
        super().__init__(master, **kwargs)
        # Текст плейсхолдера и префикс для нового ввода
        self.placeholder = placeholder
        self.prefix = prefix
        self.default_fg = kwargs.get('foreground', 'grey')
        # Устанавливаем плейсхолдер
        self.insert(0, self.placeholder)
        self.configure(foreground=self.default_fg)
        # Привязываем обработчики фокуса
        self.bind('<FocusIn>', self._on_focus_in)
        self.bind('<FocusOut>', self._on_focus_out)

    def _on_focus_in(self, event: tk.Event) -> None:
        """При получении фокуса очищаем плейсхолдер и вставляем префикс."""
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.insert(0, self.prefix)
            self.configure(foreground='black')

    def _on_focus_out(self, event: tk.Event) -> None:
        """При потере фокуса восстанавливаем плейсхолдер, если поле пустое или содержит только префикс."""
        text = self.get().strip()
        if not text or text == self.prefix.strip():
            self.delete(0, tk.END)
            self.insert(0, self.placeholder)
            self.configure(foreground=self.default_fg)

class SIGPlotterApp(tk.Tk):
    """Главное окно приложения SIG Plotter."""

    def __init__(self) -> None:
        super().__init__()
        # Выбранный путь к файлу
        self.selected_file: str = ''
        self._configure_window()
        self._init_fonts()
        self._init_styles()
        self._build_ui()

    def _configure_window(self) -> None:
        """Настройка параметров главного окна."""
        self.title(APP_TITLE)
        self.geometry(WINDOW_SIZE)
        self.resizable(False, False)
        # Устанавливаем иконку, если файл существует
        if ICON_PATH.exists():
            try:
                self.iconbitmap(str(ICON_PATH))
            except tk.TclError:
                pass

    def _init_fonts(self) -> None:
        """Инициализация пользовательских шрифтов."""
        self.font_regular = font.Font(family='Arial', size=14)
        self.font_header = font.Font(family='Century Gothic', size=24, weight='bold')
        self.font_subheader = font.Font(family='Arial', size=18, weight='bold')

    def _init_styles(self) -> None:
        """Инициализация стилей ttk-виджетов."""
        style = ttk.Style(self)
        style.configure(
            BUTTON_STYLE,
            padding=(10, 6),
            font=('Arial', 14),
            relief='flat'
        )

    def _build_ui(self) -> None:
        """Сборка и размещение всех компонентов интерфейса."""
        self._create_logo_section()
        self._create_subtitle()
        self._create_name_entry()
        self._create_file_selector()
        self._create_plot_button()

    def _create_logo_section(self) -> None:
        """Создание секции с логотипом и названием компании."""
        container = tk.Frame(self)
        container.pack(pady=(20, 10))

        # Отображаем логотип, если файл существует
        if ICON_PATH.exists():
            logo = Image.open(ICON_PATH)
            logo.thumbnail((80, 80), Image.Resampling.LANCZOS)
            self._logo_image = ImageTk.PhotoImage(logo)
            ttk.Label(container, image=self._logo_image).grid(row=0, column=0)

        # Отображаем название компании
        ttk.Label(
            container,
            text='АО «НПО «Прибор»',
            font=self.font_header
        ).grid(row=0, column=1, padx=(10, 0))

    def _create_subtitle(self) -> None:
        """Создание подзаголовка 'Генератор графиков'."""
        ttk.Label(
            self,
            text='Генератор графиков',
            font=self.font_subheader
        ).pack(pady=(0, 15))

    def _create_name_entry(self) -> None:
        """Создание поля ввода названия испытания с плейсхолдером."""
        frame = tk.Frame(self)
        frame.pack(padx=80, anchor='w', pady=(0, 15))

        ttk.Label(
            frame,
            text='Введите название испытания:',
            font=self.font_regular
        ).grid(row=0, column=0, sticky='w')

        self.entry_name = PlaceholderEntry(
            frame,
            placeholder=PLACEHOLDER_TEXT,
            prefix=DEFAULT_TEST_PREFIX,
            width=25,
            font=self.font_regular
        )
        self.entry_name.grid(row=0, column=1, padx=(10, 0))

    def _create_file_selector(self) -> None:
        """Создание секции выбора CSV-файла SIG."""
        frame = tk.Frame(self)
        frame.pack(padx=80, anchor='w', pady=(0, 15))

        ttk.Label(
            frame,
            text='Укажите путь до данных SIG:',
            font=self.font_regular
        ).grid(row=0, column=0, sticky='w')

        # Кнопка выбора файла
        self.btn_browse = ttk.Button(
            frame,
            text='Выбрать файл',
            style=BUTTON_STYLE,
            command=self._on_browse
        )
        self.btn_browse.grid(row=0, column=1, padx=(20, 0), sticky='w')

        # Метка пути к выбранному файлу
        self.label_path = ttk.Label(
            frame,
            text='Выбранный файл: Файл не выбран',
            font=self.font_regular
        )
        self.label_path.grid(row=1, column=0, columnspan=2, pady=(15, 0), sticky='w')

    def _create_plot_button(self) -> None:
        """Создание кнопки "Создать график" ниже остальных элементов."""
        self.btn_plot = ttk.Button(
            self,
            text='Создать график',
            style=BUTTON_STYLE,
            command=self._on_plot,
            state='disabled'
        )
        self.btn_plot.pack(pady=(15, 20))

    def _on_browse(self) -> None:
        """Обработка выбора файла и обновление интерфейса."""
        path = filedialog.askopenfilename(
            parent=self,
            title='Выберите файл SIG',
            filetypes=[('CSV files', '*.csv')]
        )
        if path:
            self.selected_file = path
            self.label_path.config(text=f"Выбранный файл: {Path(path).name}")
            self.btn_plot.state(['!disabled'])
        else:
            self.selected_file = ''
            self.label_path.config(text='Выбранный файл: Файл не выбран')
            self.btn_plot.state(['disabled'])

    def _on_plot(self) -> None:
        """Вызов функции построения графика из модуля plot_built."""
        name = self.entry_name.get().strip()
        # Если введено значение плейсхолдера, используем префикс
        if name == PLACEHOLDER_TEXT:
            name = DEFAULT_TEST_PREFIX.strip()
        plot_built.plot_sig_data(sig_path=self.selected_file, test_name=name)


def main() -> None:
    """Точка входа в приложение."""
    app = SIGPlotterApp()
    app.mainloop()


if __name__ == '__main__':
    main()
