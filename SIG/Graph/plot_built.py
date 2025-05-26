import pandas as pd

import plotly.graph_objects as go

pd.options.plotting.backend = "plotly"


def acm_dataframe(acm, time_offset="0"):
    if not acm.endswith(".xlsx"):
        return

    acm_df = pd.DataFrame(pd.read_excel(acm, header=11, usecols=[1, 2, 4]))
    # Удаление двух строк между шапкой и началом данных
    acm_df = acm_df.set_axis([acm_df.columns[0], acm_df.columns[1], f'Давление, кгс/см2'], axis=1)
    acm_df = acm_df.drop(index=[0, 1])
    acm_df = acm_df.loc[acm_df[acm_df.columns[2]] > -1]

    # перевод в МПа
    acm_df["Давление, кгс/см2"] = acm_df["Давление, кгс/см2"].multiply(0.0980665)
    # Удаление ошибочных значений
    acm_df = acm_df.loc[acm_df[acm_df.columns[2]] > -1]
    # Сброс индексов
    acm_df = acm_df.reset_index(drop=True)
    # Объединение даты и время
    acm_df["Время"] = acm_df["Дата"] + " " + acm_df["Время"]
    acm_df = acm_df.drop("Дата", axis=1)

    acm_df["Время"] = pd.to_datetime(acm_df["Время"])
    try:
        offset = int(time_offset)
    except Exception:
        offset = 0

    acm_df["Время"] = acm_df["Время"] + pd.Timedelta(seconds=int(offset))

    return acm_df


def metrol_dataframe(metrol, time_offset="0"):
    if not metrol.endswith(".csv"):
        return
    metrol_df = pd.DataFrame(pd.read_csv(metrol, delimiter=";", decimal="."))

    # перевод в МПа
    metrol_df["var"] = metrol_df["var"].multiply(0.0980665)

    # Объединение даты и время
    metrol_df["time"] = metrol_df["date"] + " " + metrol_df["time"]
    metrol_df = metrol_df.drop("date", axis=1)

    metrol_df["time"] = pd.to_datetime(metrol_df["time"])
    try:
        offset = int(time_offset)
    except Exception:
        offset = 0
    metrol_df["time"] = metrol_df["time"] + pd.Timedelta(seconds=int(offset))

    return metrol_df


def sig_dataframe(sig, time_offset="0"):
    if not sig.endswith(".csv"):
        return
    sig_df = pd.DataFrame(pd.read_csv(sig, delimiter=";", decimal="."))

    # Объединение даты и время
    sig_df["Time"] = sig_df["Date"] + " " + sig_df["Time"]
    sig_df = sig_df.drop("Date", axis=1)

    sig_df["Time"] = pd.to_datetime(sig_df["Time"])
    try:
        offset = int(time_offset)
    except Exception:
        offset = 0

    sig_df["Time"] = sig_df["Time"] + pd.Timedelta(seconds=int(offset))
    return sig_df


def build_plot(
        acm="", metrol="", sig="", name="", time_acm="0", time_metrol="0", time_sig="0"
):
    fig = go.Figure()
    if len(acm) > 1:
        acm_df = acm_dataframe(acm, time_offset=time_acm)

        fig.add_trace(
            go.Scatter(
                x=acm_df["Время"],
                y=acm_df["Давление, кгс/см2"],
                mode="lines",
                name="Давление внутри образца (показания АЦМ-6-20 60/100)",
                line=dict(color="black", width=2, dash="dashdot"),
            )
        )

    if len(metrol) > 1:
        metrol_df = metrol_dataframe(metrol, time_offset=time_metrol)
        fig.add_trace(go.Line())
        fig.add_trace(
            go.Scatter(
                x=metrol_df["time"],
                y=metrol_df["var"],
                mode="lines",
                name="Давление в гидробаке (показания Metrol 100)",
                line=dict(color="black", width=2, dash="solid"),
                showlegend=True,
            )
        )

    if len(sig) > 1:
        sig_df = sig_dataframe(sig, time_offset=time_sig)

        fig.add_trace(
            go.Scatter(
                x=sig_df["Time"][::60],
                y=sig_df["Pressure 2"][::60],
                mode="markers",
                name="Давление в гидробаке (показания ПД100)",
                line=dict(color="white", width=2, dash="dash"),
            )
        )
        fig.update_traces(marker=dict(size=6,
                                      line=dict(width=2,
                                                color='black')),
                          selector=dict(mode='markers'))

    fig.update_layout(
        title=dict(text=f"Испытание {name.replace('#', '№')}", xanchor="center", x=0.5, y=0.9),
        xaxis_title="<b>Длительность испытания</b>",
        yaxis_title="<b>Давление, МПа</b>", plot_bgcolor="rgba(0, 0, 0, 0)", title_font={"size": 24},
        font_color="black", title_font_color="black"
    )
    fig.update_xaxes(showline=True, linewidth=1, linecolor="black")
    fig.update_yaxes(showline=True, linewidth=1, linecolor="black")
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="black")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="black")
    fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='black')

    fig.update_xaxes(tickformat="%H:%M:%S \n%d-%m-%Y", dtick=60 * 1000 * 5)
    fig.update_yaxes(dtick=2)

    fig.update_layout(
        legend=dict(orientation="h", yanchor="top", y=-0.25, xanchor="center", x=0.5),
        font=dict(
            size=12
        )
    )

    # fig.update_xaxes(ticklabelmode="period", dtick="D1")
    fig["data"][0]["showlegend"] = True
    fig.update_layout(showlegend=True)
    print(fig)
    fig.show()
