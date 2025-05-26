"""Конфигурация путей к файлам и виджетам GUI."""

from __future__ import annotations

# Файл SIG: [выбран ли файл, путь]
files: dict[str, list[bool | str]] = {
    "file_dialog_sig": [False, ""],
}

# Маппинг «тег диалога -> тег текст‑виджета с путём»
file_to_text: dict[str, str] = {
    "file_dialog_sig": "path_text_sig",
}
