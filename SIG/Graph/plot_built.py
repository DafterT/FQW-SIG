"""
Модуль: refactored_sig_plot.py

Построение интерактивного графика давления по данным SIG

Этот модуль читает CSV-файл SIG и отображает интерактивный график давления
с использованием Plotly.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

import pandas as pd
import plotly.graph_objects as go

from settings import *

# Настройки pandas
pd.options.plotting.backend = "plotly"


def _read_sig_csv(sig_path: Union[str, Path]) -> Optional[pd.DataFrame]:
    """
    Читает CSV SIG и возвращает DataFrame с объединённым столбцом Time.

    Параметры
    ----------
    sig_path : str | Path
        Путь к SIG CSV-файлу.

    Возвращает
    ----------
    pd.DataFrame | None
        DataFrame с колонками Time, Pressure 1, Pressure 2 или None,
        если расширение файла неверное.
    """
    path = Path(sig_path)
    if path.suffix.lower() != CSV_SUFFIX:
        return None

    df = pd.read_csv(path, delimiter=";", decimal=".")
    # Объединяем Date и Time и преобразуем в datetime
    df["Time"] = pd.to_datetime(
        df["Date"] + " " + df["Time"], errors="coerce"
    )
    df.drop(columns=["Date"], inplace=True)
    return df


def _create_pressure_plot(df: pd.DataFrame, test_name: str) -> go.Figure:
    """
    Создаёт интерактивный график давления из DataFrame.

    Параметры
    ----------
    df : pd.DataFrame
        Данные SIG с колонкой Time и двумя давлением.
    test_name : str
        Название испытания (для заголовка).

    Возвращает
    ----------
    go.Figure
        Объект Figure для отображения.
    """
    fig = go.Figure()
    sensors = [
        ("Pressure 2", "Давление в гидробаке (ПД100) Д2"),
        ("Pressure 1", "Давление в гидробаке (ПД100) Д1"),
    ]
    for column, label in sensors:
        fig.add_trace(
            go.Scatter(
                x=df["Time"].iloc[::MARKER_INTERVAL],
                y=df[column].iloc[::MARKER_INTERVAL],
                mode="lines+markers",
                name=label,
                line=dict(width=1),
                marker=dict(size=4),
            )
        )

    # Общие настройки оформления
    fig.update_layout(
        showlegend=True,
        title=dict(text=f"{test_name}", x=0.5, xanchor="center", y=0.95),
        xaxis_title="<b>Длительность испытания</b>",
        yaxis_title="<b>Давление, МПа</b>",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        title_font_size=24,
        font_color="black",
        legend=dict(orientation="h", y=-0.25, x=0.5, yanchor="top", xanchor="center"),
        font=dict(size=12),
    )
    fig.update_xaxes(
        showline=True,
        linewidth=1,
        linecolor="black",
        tickformat="%H:%M:%S \n%d-%m-%Y",
        dtick=DEFAULT_X_DTICK_MS,
        showgrid=True,
        gridwidth=1,
        gridcolor="black",
    )
    fig.update_yaxes(
        showline=True,
        linewidth=1,
        linecolor="black",
        dtick=2,
        showgrid=True,
        gridwidth=1,
        gridcolor="black",
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor="black",
    )
    return fig


def plot_sig_data(sig_path: Union[str, Path], test_name: str = "") -> None:
    """
    Загружает данные SIG из CSV и отображает график.

    Параметры
    ----------
    sig_path : str | Path
        Путь к SIG CSV-файлу.
    test_name : str
        Название испытания.

    Raises
    ------
    ValueError
        Если файл не CSV или его невозможно прочитать.
    """
    df = _read_sig_csv(sig_path)
    if df is None:
        raise ValueError(f"Файл '{sig_path}' должен иметь расширение {CSV_SUFFIX}")

    safe_name = test_name.replace("#", "№")
    fig = _create_pressure_plot(df, safe_name)
    fig.show()
