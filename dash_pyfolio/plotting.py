# import pandas as pd
from dash_pyfolio.portfolio_data import Portfolio
from plotly.graph_objects import Figure
import plotly.graph_objects as go


def plot_returns(portfolio: Portfolio) -> Figure:
    returns = portfolio.returns
    live_start_date = portfolio.live_start_date

    if live_start_date is not None:
        sim_returns = returns.loc[returns.index < live_start_date]
        live_returns = returns.loc[returns.index >= live_start_date]

        fig = go.Figure(
            data=go.Scatter(
                x=sim_returns.index,
                y=sim_returns.values,
                mode="lines",
                line_color="#006400",
            ),
        )
        fig.add_trace(
            go.Scatter(
                x=live_returns.index,
                y=live_returns.values,
                mode="lines",
                line=dict(color="#ff0000"),
            ),
        )
    else:
        fig = go.Figure(
            data=go.Scatter(
                x=returns.index,
                y=returns.values,
                mode="lines",
                line_color="#006400",
            ),
        )

    fig.update_layout(
        title={
            "text": "Returns",
            "y": 0.85,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        }
    )
    fig.update_xaxes(
        # dtick="M3",
        tickformat="%Y-%m-%d",
    )
    fig.update_yaxes(tickformat=",.2%")

    return fig
