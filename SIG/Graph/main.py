"""Графический интерфейс для выбора CSV‑файла SIG и построения графика"""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import dearpygui.dearpygui as dpg

import config
import plot_built

# Plotly — бэкенд для ``pandas.DataFrame.plot``
pd.options.plotting.backend = "plotly"

# ------------------------------------------------------------------
#                           CONSTANTS / PATHS
# ------------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent
ASSETS_DIR = ROOT_DIR / "assets"
LOGO_PATH = ASSETS_DIR / "logo.png"
ICON_PATH = ASSETS_DIR / "icon.ico"

# ------------------------------------------------------------------
#                        TEXTURE REGISTRATION
# ------------------------------------------------------------------

def _register_textures() -> None:
    """Регистрирует текстуры"""

    if LOGO_PATH.exists():
        with dpg.texture_registry(show=False):
            width, height, _, data = dpg.load_image(str(LOGO_PATH))
            dpg.add_static_texture(width, height, data, tag="logo_tex")

# ------------------------------------------------------------------
#                               CALLBACKS
# ------------------------------------------------------------------


def start_button() -> None:
    """Читает параметры из GUI и строит график."""
    plot_built.build_plot(
        sig=config.files["file_dialog_sig"][1],
        name=dpg.get_value("input_text_item_name"),
    )


def callback(sender: str, app_data: dict) -> None:
    """Обработчик выбора файла в диалоге."""
    selected_path = next(iter(app_data["selections"].values()))
    dpg.set_value(config.file_to_text[sender], selected_path)
    config.files[sender] = [True, selected_path]


def cancel_callback(sender: str) -> None:
    """Сбрасывает путь, если пользователь нажал «Cancel»."""

    dpg.set_value(config.file_to_text[sender], "Путь не указан")
    config.files[sender] = [False, ""]


def generate_screen_dpg() -> None:
    """Создаёт все элементы интерфейса"""

    start_offset = 80  # Левый отступ для выравнивания подписей

    # ================== Регистрируем шрифты ==================
    with dpg.font_registry():
        with dpg.font(str(ASSETS_DIR / "arial.ttf"), 18) as font_main:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

    # ================= Диалог выбора файла ==================
    with dpg.file_dialog(
        directory_selector=False,
        show=False,
        callback=callback,
        tag="file_dialog_sig",
        cancel_callback=cancel_callback,
        width=700,
        height=400,
    ):
        dpg.add_file_extension(".*")

    # ===================== Главное окно =====================
    with dpg.window(
        tag="Primary Window",
        width=800,
        height=600,
        label="SIG",
        no_resize=True,
    ):
        # ----------- Логотип слева сверху -----------
        if LOGO_PATH.exists():
            with dpg.group(horizontal=True):
                dpg.add_image("logo_tex",
                              pos=((800 - 399) // 2, 20))
                dpg.add_spacer(width=20)

        dpg.add_spacer(width=10, height=60)

        # ----------- Название изделия ---------------
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=start_offset)
            dpg.add_text("Введите название испытуемого изделия: Испытание")
            dpg.add_input_text(width=200, tag="input_text_item_name")

        # ------------- Выбор файла SIG --------------
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=start_offset)
            dpg.add_text("Укажите путь до данных SIG")
            dpg.add_spacer(width=25)
            dpg.add_button(
                label="Выбрать путь",
                callback=lambda: dpg.show_item("file_dialog_sig"),
            )
            dpg.add_text("Путь не указан", tag="path_text_sig")

        dpg.add_spacer(width=1, height=50)

        # ------------- Кнопка построения -------------
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=300)
            dpg.add_button(label="Создать график", callback=start_button)

        # --------- Делает окно главным и шрифт ---------
        dpg.set_primary_window("Primary Window", True)
        dpg.bind_font(font_main)


def main() -> None:
    dpg.create_context()
    _register_textures()

    dpg.create_viewport(
        title="SIG Plotter",
        width=800,
        height=600,
        resizable=False,          
        small_icon=str(ICON_PATH),   # значок в левом-верхнем углу
        large_icon=str(ICON_PATH)    # значок в панели задач / Alt-Tab
    )
    generate_screen_dpg()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()

    dpg.destroy_context()


if __name__ == "__main__":
    main()
