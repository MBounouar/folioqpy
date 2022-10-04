import numpy as np
import plotly.graph_objects as go
from folioqpy.portfolio_data import Portfolio
from typing import Any
from ..periods import APPROX_BDAYS_PER_MONTH, APPROX_BDAYS_PER_YEAR


def plot_rolling_volatility(
    portfolio: Portfolio,
    rolling_vol_window: int = APPROX_BDAYS_PER_MONTH * 6,
    **kwargs: dict[str, Any],
) -> go.Figure:
    fig = go.Figure()

    rolling_vol_ts = portfolio.returns.rolling(rolling_vol_window).std() * np.sqrt(
        APPROX_BDAYS_PER_YEAR
    )

    for name in rolling_vol_ts.columns:
        fig.add_trace(
            go.Scatter(
                name=name,
                meta=name,
                x=rolling_vol_ts[name].index,
                y=rolling_vol_ts[name].values,
                mode="lines",
                # line_color="orangered",
            ),
        )

        if name == portfolio.name:
            fig.add_hline(
                y=rolling_vol_ts[name].mean(),
                line_width=1.5,
                line_dash="4px",
                # line_color="red",
            )

    fig.update_layout(
        title=dict(
            text="Rolling Volatility (6-month) %",
            x=0.5,
            y=0.85,
            xanchor="center",
            yanchor="top",
        ),
        showlegend=True,
        legend=dict(
            yanchor="top",
            x=0,
            y=1,
            xanchor="left",
            bgcolor="rgba(0,0,0,0)",
            bordercolor="#DDDDDD",
            borderwidth=1,
        ),
        xaxis=dict(
            tickformat="%Y-%m",
            ticks="outside",
        ),
        yaxis=dict(
            title="Volatility %",
            tickformat=",.1%",
        ),
    )

    fig.update_traces(hovertemplate="(%{x:'%Y-%m-%d'}, %{y:.2f}<extra>%{meta}</extra>)")

    return fig
