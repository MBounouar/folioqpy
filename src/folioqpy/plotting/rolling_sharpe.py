from folioqpy.stats import roll_sharpe_ratio
from folioqpy.portfolio_data import Portfolio
from typing import Any
from folioqpy.periods import AnnualizationFactor

import plotly.graph_objects as go


def plot_rolling_sharpe(
    portfolio: Portfolio,
    title="Rolling Sharpe Ratio (6-month) %",
    rolling_window=6 * AnnualizationFactor.MONTHLY.value,
    **kwargs: dict[str, Any],
) -> go.Figure:
    fig = go.Figure()

    for i, name in enumerate(portfolio.returns.columns):
        r_sharpe_ratio_ts = roll_sharpe_ratio(
            portfolio.returns[name],
            window=rolling_window,
        ).reindex(portfolio.returns.index)
        avg_sharpe_ratio = r_sharpe_ratio_ts.mean()

        fig.add_trace(
            go.Scatter(
                # legendgroup=name,
                name=name,
                meta=name,
                x=r_sharpe_ratio_ts.index,
                y=r_sharpe_ratio_ts.values,
                mode="lines",
                visible="legendonly" if i > 0 else True,
            ),
        )

        fig.add_trace(
            go.Scatter(
                # legendgroup=name,
                name=f"Average - [{name}]",
                meta=f"Average - [{name}]",
                x=[r_sharpe_ratio_ts.index[0], r_sharpe_ratio_ts.index[-1]],
                y=[avg_sharpe_ratio, avg_sharpe_ratio],
                hoverinfo="skip",
                mode="lines",
                line=dict(dash="4px"),
                visible="legendonly" if i > 0 else True,
                # line_color="orangered",
            ),
        )

    fig.add_hline(
        y=0,
        line_width=1.5,
        line_dash="4px",
        # line_color="red",
    )

    fig.update_layout(
        title=dict(
            text=title,
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
            title="Sharpe Ratio",
            tickformat=".1f",
        ),
    )

    return fig
