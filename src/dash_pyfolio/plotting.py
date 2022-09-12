# import pandas as pd
from dash_pyfolio.portfolio_data import Portfolio
from plotly.graph_objects import Figure
import plotly.graph_objects as go
import numpy as np
import empyrical as ep
import calendar


def _center_title(fig: Figure, title: str = "") -> None:
    title = dict(
        text=title,
        x=0.5,
        y=0.85,
        xanchor="center",
        yanchor="top",
    )

    fig.update_layout(title=title, showlegend=False)


def plot_returns(portfolio: Portfolio) -> Figure:

    fig = go.Figure(
        data=go.Scatter(
            x=portfolio.back_returns.index,
            y=portfolio.back_returns.values,
            mode="lines",
            line_color="#006400",
        ),
    )
    if portfolio.live_start_date is not None:
        fig.add_trace(
            go.Scatter(
                x=portfolio.live_returns.index,
                y=portfolio.live_returns.values,
                mode="lines",
                line=dict(color="#ff0000"),
            ),
        )

    _center_title(fig, title="Returns")

    fig.update_xaxes(
        # dtick="M6",
        tickformat="%Y-%m",
        # tickformat="%Y-%m-%d",
    )
    fig.update_yaxes(tickformat=",.1%")
    fig.update_traces(hovertemplate="(%{x:'%Y-%m-%d'}, %{y:,.2%}<extra></extra>)")

    return fig


def plot_rolling_returns(portfolio: Portfolio) -> Figure:
    fig = go.Figure(
        data=go.Scatter(
            x=portfolio.cum_back_returns.index,
            y=portfolio.cum_back_returns.values,
            mode="lines",
            line_color="#006400",
        ),
    )
    if portfolio.live_start_date is not None:
        fig.add_trace(
            go.Scatter(
                x=portfolio.cum_live_returns.index,
                y=portfolio.cum_live_returns.values,
                mode="lines",
                line=dict(color="#ff0000"),
            ),
        )

    fig.add_shape(
        type="line",
        yref="y",
        xref="paper",
        x0=0,
        y0=1,
        x1=1,
        y1=1,
        line=dict(
            # color="LightSeaGreen",
            # width=4,
            dash="4px",
        ),
    )
    _center_title(fig, title="Cumulative Returns")

    fig.update_xaxes(
        # dtick="M3",
        tickformat="%Y-%m",
    )
    fig.update_yaxes(tickformat=".2f")
    # fig.update_traces(hovertemplate="%{x}  %{y:.2f}<extra></extra>")
    fig.update_traces(hovertemplate="(%{x:'%Y-%m-%d'}, %{y:.2f}<extra></extra>)")

    return fig


def plot_drawdown_underwater(portfolio: Portfolio) -> Figure:
    df_cum_rets = portfolio.cum_returns
    running_max = np.maximum.accumulate(df_cum_rets)
    underwater = -((running_max - df_cum_rets) / running_max)

    fig = go.Figure(
        data=go.Scatter(
            x=underwater.index,
            y=underwater.values,
            mode="lines",
            line_color="#FA8072",
            fill="tozeroy",
        ),
    )
    _center_title(fig, title="Underwater Plot")

    fig.update_xaxes(tickformat="%Y-%m")
    fig.update_yaxes(tickformat=",.1%")
    fig.update_traces(hovertemplate="(%{x:'%Y-%m-%d'}, %{y:,.2%}<extra></extra>)")
    return fig


def plot_monthly_returns_heatmap(portfolio: Portfolio) -> Figure:
    monthly_ret_table = ep.aggregate_returns(portfolio.returns, "monthly")
    monthly_ret_table = monthly_ret_table.unstack().round(3)

    monthly_ret_table.rename(
        columns={i: m for i, m in enumerate(calendar.month_abbr)},
        inplace=True,
    )

    fig = go.Figure(
        data=go.Heatmap(
            z=monthly_ret_table.values,
            x=monthly_ret_table.columns,
            y=monthly_ret_table.index,
            colorscale="RdYlGn",
            text=monthly_ret_table.applymap(lambda x: f"{x:,.2%}"),
            texttemplate="%{text}",
            showscale=False,
            # textfont={"size": 20},
            hoverongaps=False,
            hovertemplate="%{x:'%B'}-%{y:'%Y'}, %{z:,.2%}<extra></extra>",
        ),
    )
    fig.update_yaxes(dict(title="Year"))
    fig.update_xaxes(dict(title="Month"))
    _center_title(fig, title="Monthly Returns %")
    return fig


def plot_rolling_volatility(
    portfolio: Portfolio,
    rolling_vol_window: int = 21 * 6,
) -> Figure:
    APPROX_BDAYS_PER_YEAR = 252
    rolling_vol_ts = portfolio.returns.rolling(rolling_vol_window).std() * np.sqrt(
        APPROX_BDAYS_PER_YEAR
    )

    fig = go.Figure(
        data=go.Scatter(
            x=rolling_vol_ts.index,
            y=rolling_vol_ts.values,
            mode="lines",
            line_color="orangered",
        ),
    )
    fig.add_shape(
        type="line",
        yref="y",
        xref="paper",
        x0=0,
        y0=rolling_vol_ts.mean(),
        x1=1,
        y1=rolling_vol_ts.mean(),
        line=dict(
            color="steelblue",
            # width=4,
            dash="4px",
        ),
    )
    return fig
