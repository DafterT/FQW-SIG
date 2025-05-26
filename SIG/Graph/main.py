import pandas as pd
import dearpygui.dearpygui as dpg
import config
import plot_built

pd.options.plotting.backend = "plotly"


def start_button():
    plot_built.build_plot(
        acm=config.files["file_dialog_acm"][1],
        metrol=config.files["file_dialog_metrol"][1],
        sig=config.files["file_dialog_sig"][1],
        name=dpg.get_value("input_text_item_name"),
        time_acm=dpg.get_value("input_time_offset_acm"),
        time_metrol=dpg.get_value("input_time_offset_metrol"),
        time_sig=dpg.get_value("input_time_offset_sig"),
    )


def callback(sender, app_data):
    selected_file = list(app_data["selections"])[0]
    selected_path = app_data["selections"][selected_file]

    dpg.set_value(config.file_to_text[sender], f"{selected_path}")

    config.files[sender][0] = True
    config.files[sender][1] = selected_path


def cancel_callback(sender):
    dpg.set_value(config.file_to_text[sender], "Путь не указан")
    config.files[sender][0] = False
    config.files[sender][1] = ""


def colour_change(value):
    if value < 0.3:
        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram, (80, 200, 0), category=dpg.mvThemeCat_Core)
        dpg.bind_theme(global_theme)

    if 0.4 < value < 0.6:
        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram, (216, 230, 0), category=dpg.mvThemeCat_Core)
        dpg.bind_theme(global_theme)

    if 0.6 < value < 0.8:
        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram, (240, 160, 0), category=dpg.mvThemeCat_Core)
        dpg.bind_theme(global_theme)

    if 0.8 < value < 1:
        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram, (205, 70, 0), category=dpg.mvThemeCat_Core)
        dpg.bind_theme(global_theme)


def generate_screen_dpg():
    # Отступ слева
    start_offset = 80
    
    with dpg.font_registry():
        with dpg.font("assets/arial.ttf", 18) as font1:
            # Добавление области шрифтов
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
            dpg.add_font_range_hint(dpg.mvFontRangeHint)

    # Выбор файла для АЦМ
    with dpg.file_dialog(
        directory_selector=False,
        show=False,
        callback=callback,
        tag="file_dialog_acm",
        cancel_callback=cancel_callback,
        width=700,
        height=400,
    ):
        dpg.add_file_extension(".*")

    # Выбор файла для Метрол
    with dpg.file_dialog(
        directory_selector=False,
        show=False,
        callback=callback,
        tag="file_dialog_metrol",
        cancel_callback=cancel_callback,
        width=700,
        height=400,
    ):
        dpg.add_file_extension(".*")

    # Выбор файла для СИГ
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

    # Основное окно
    with dpg.window(tag="Primary Window", width=800, height=600, label="СИГ"):
        dpg.add_spacer(width=10, height=150)

        with dpg.group(horizontal=True):
            dpg.add_spacer(width=start_offset)
            dpg.add_text("Введите название испытуемого изделия: Испытание")
            dpg.add_input_text(width=200, tag="input_text_item_name")

        with dpg.group(horizontal=True):
            dpg.add_spacer(width=start_offset)
            dpg.add_text("Укажите путь до данных АЦМ")
            dpg.add_spacer(width=20)
            dpg.add_button(label="Выбрать путь", callback=lambda: dpg.show_item("file_dialog_acm"))
            dpg.add_text("Путь не указан", tag="path_text_acm")

        with dpg.group(horizontal=True):
            dpg.add_spacer(width=start_offset)
            dpg.add_text("Укажите путь до данных Метрол")
            dpg.add_spacer(width=0)
            dpg.add_button(label="Выбрать путь", callback=lambda: dpg.show_item("file_dialog_metrol"))
            dpg.add_text("Путь не указан", tag="path_text_metrol")

        with dpg.group(horizontal=True):
            dpg.add_spacer(width=start_offset)
            dpg.add_text("Укажите путь до данных СИГ")
            dpg.add_spacer(width=23)
            dpg.add_button(label="Выбрать путь", callback=lambda: dpg.show_item("file_dialog_sig"))
            dpg.add_text("Путь не указан", tag="path_text_sig")

        dpg.add_spacer(width=1, height=10)

        with dpg.group(horizontal=True):
            dpg.add_spacer(width=start_offset)
            dpg.add_text("Смещение времени АЦМ, с")
            dpg.add_spacer(width=34)
            dpg.add_input_text(width=100, tag="input_time_offset_acm")

        with dpg.group(horizontal=True):
            dpg.add_spacer(width=start_offset)
            dpg.add_text("Смещение времени Метрол, с")
            dpg.add_spacer(width=14)
            dpg.add_input_text(width=100, tag="input_time_offset_metrol")

        with dpg.group(horizontal=True):
            dpg.add_spacer(width=start_offset)
            dpg.add_text("Смещение времени СИГ, с")
            dpg.add_spacer(width=37)
            dpg.add_input_text(width=100, tag="input_time_offset_sig")

        dpg.add_spacer(width=1, height=10)

        with dpg.group(horizontal=True):
            dpg.add_spacer(width=300)
            dpg.add_button(label="Создать график", callback=start_button)


        # Натягиваем окно на системное
        dpg.set_primary_window("Primary Window", True)
        # Применяем шрифт
        dpg.bind_font(font1)


def main():
    # Создание контекста, идет всегда первым
    dpg.create_context()

    # Создание вьюпорта (окно системы)
    dpg.create_viewport(title="SIG", width=800, height=600)

    generate_screen_dpg()

    dpg.setup_dearpygui()
    # Показ вьюпорта
    dpg.show_viewport()

    dpg.start_dearpygui()
    # Очистка контекста
    dpg.destroy_context()


if __name__ == "__main__":
    main()
