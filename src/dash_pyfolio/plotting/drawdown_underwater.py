# import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dash_pyfolio.portfolio_data import Portfolio


def plot_drawdown_underwater(portfolio: Portfolio) -> go.Figure:
    fig = go.Figure()
    df_cum_rets = portfolio.cum_returns
    running_max = np.maximum.accumulate(df_cum_rets)
    underwater = -((running_max - df_cum_rets) / running_max)

    for i, name in enumerate(df_cum_rets.columns):
        fig.add_trace(
            go.Scatter(
                meta=name,
                name=name,
                x=underwater[name].index,
                y=underwater[name].values,
                mode="lines",
                # line_color="#FA8072",
                fill="tozeroy",
                visible="legendonly" if i > 0 else True,
            ),
        )

    fig.update_xaxes(
        tickformat="%Y-%m",
        ticks="outside",
    )
    fig.update_yaxes(tickformat=",.1%")
    fig.update_traces(
        hovertemplate="(%{x:'%Y-%m-%d'}, %{y:,.2%}<extra>%{meta}</extra>)"
    )
    fig.update_layout(
        title=dict(
            text="Underwater Plot",
            x=0.5,
            y=0.85,
            xanchor="center",
            yanchor="top",
        ),
        showlegend=True,
        legend=dict(
            yanchor="bottom",
            y=0,
            xanchor="left",
            x=0,
            bgcolor="rgba(0,0,0,0)",
            bordercolor="#DDDDDD",
            borderwidth=1,
        ),
    )
    return fig
