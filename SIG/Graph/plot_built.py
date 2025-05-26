"""Построение интерактивного графика давления по данным SIG.

* Вход — CSV‑файл с колонками ``Date``, ``Time``, ``Pressure 2``.
* Выход — интерактивный график **Plotly** (линия + маленькие маркеры).

Смещение временной шкалы убрано: время берётся «как есть».
"""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

pd.options.plotting.backend = "plotly"

# ------------------------------------------------------------------
#                        DATA PRE‑PROCESSING
# ------------------------------------------------------------------


def sig_dataframe(sig_path: str) -> pd.DataFrame | None:
    """Читает CSV SIG и возвращает подготовленный ``DataFrame``.

    Parameters
    ----------
    sig_path
        Полный путь к файлу SIG (должен заканчиваться на ``.csv``).

    Returns
    -------
    pd.DataFrame | None
        Подготовленные данные или ``None``, если файл не *.csv*.
    """

    if not sig_path.endswith(".csv"):
        return None

    sig_df = pd.read_csv(sig_path, delimiter=";", decimal=".")

    # Объединяем столбцы даты и времени в единый тайм‑стемп
    sig_df["Time"] = sig_df["Date"] + " " + sig_df["Time"]
    sig_df.drop(columns=["Date"], inplace=True)
    sig_df["Time"] = pd.to_datetime(sig_df["Time"], errors="coerce")

    return sig_df


# ------------------------------------------------------------------
#                              PLOTTING
# ------------------------------------------------------------------


def build_plot(sig: str = "", name: str = "") -> None:
    """Строит интерактивный график давления.

    Parameters
    ----------
    sig
        Путь к CSV‑файлу SIG.
    name
        Название испытания (отображается в заголовке).
    """

    fig = go.Figure()

    if sig:
        sig_df = sig_dataframe(sig)
        if sig_df is None:
            raise ValueError("Файл SIG должен быть в формате .csv")

        # Отрисовываем линию + маленькие маркеры (шаг = 1 минута)
        fig.add_trace(
            go.Scatter(
                x=sig_df["Time"][::60],
                y=sig_df["Pressure 2"][::60],
                mode="lines+markers",
                name="Давление в гидробаке (ПД100)",
                line=dict(width=1),
                marker=dict(size=4),
            )
        )

    # ============ Оформление =========
    fig.update_layout(
        showlegend=True,  
        title=dict(
            text=f"Испытание {name.replace('#', '№')}",
            xanchor="center",
            x=0.5,
            y=0.9,
        ),
        xaxis_title="<b>Длительность испытания</b>",
        yaxis_title="<b>Давление, МПа</b>",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        title_font_size=24,
        font_color="black",
        legend=dict(orientation="h", yanchor="top", y=-0.25, xanchor="center", x=0.5),
        font=dict(size=12),
    )

    fig.update_xaxes(
        showline=True,
        linewidth=1,
        linecolor="black",
        tickformat="%H:%M:%S \n%d-%m-%Y",
        dtick=60 * 1000 * 5,  # 5 минут
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

    fig.show()
