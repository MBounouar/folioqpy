# import pandas as pd
from dash_pyfolio.portfolio_data import Portfolio
import plotly.graph_objects as go
import numpy as np
import empyrical as ep
import calendar


def _center_title(fig: go.Figure, title: str = "", **kwargs) -> None:
    title = dict(
        text=title,
        x=0.5,
        y=0.85,
        xanchor="center",
        yanchor="top",
    )

    fig.update_layout(title=title, showlegend=False, **kwargs)


def plot_returns(portfolio: Portfolio) -> go.Figure:
    fig = go.Figure()

    if portfolio.live_start_date is not None:
        back_ret = portfolio.returns.loc[
            portfolio.returns.index < portfolio.live_start_date
        ]
        live_ret = portfolio.returns.loc[
            portfolio.returns.index >= portfolio.live_start_date
        ]
        fig.add_trace(
            go.Scatter(
                meta=portfolio.portfolio_name,
                x=back_ret[portfolio.portfolio_name].index,
                y=back_ret[portfolio.portfolio_name].values,
                mode="lines",
                line_color="#006400",
            ),
        )

        fig.add_trace(
            go.Scatter(
                meta=portfolio.portfolio_name,
                x=live_ret[portfolio.portfolio_name].index,
                y=live_ret[portfolio.portfolio_name].values,
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
    fig.update_traces(
        hovertemplate="(%{x:'%Y-%m-%d'}, %{y:,.2%}<extra>%{meta}</extra>)"
    )

    return fig


def plot_rolling_returns(portfolio: Portfolio) -> go.Figure:
    fig = go.Figure()

    if portfolio.live_start_date is not None:
        cum_back_ret = portfolio.cum_returns.loc[
            portfolio.cum_returns.index < portfolio.live_start_date
        ]
        cum_live_ret = portfolio.cum_returns.loc[
            portfolio.cum_returns.index >= portfolio.live_start_date
        ]

        fig.add_trace(
            go.Scatter(
                meta=portfolio.portfolio_name,
                x=cum_back_ret[portfolio.portfolio_name].index,
                y=cum_back_ret[portfolio.portfolio_name].values,
                mode="lines",
                line_color="#006400",
            ),
        )
        fig.add_trace(
            go.Scatter(
                meta=portfolio.portfolio_name,
                x=cum_live_ret[portfolio.portfolio_name].index,
                y=cum_live_ret[portfolio.portfolio_name].values,
                mode="lines",
                line=dict(color="#ff0000"),
            ),
        )
        if portfolio.benchmark_name is not None:
            fig.add_trace(
                go.Scatter(
                    meta=portfolio.benchmark_name,
                    x=portfolio.cum_returns[portfolio.benchmark_name].index,
                    y=portfolio.cum_returns[portfolio.benchmark_name].values,
                    mode="lines",
                    line=dict(color="grey"),
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
    fig.update_traces(hovertemplate="(%{x:'%Y-%m-%d'}, %{y:.2f}<extra>%{meta}</extra>)")

    return fig


def plot_drawdown_underwater(portfolio: Portfolio) -> go.Figure:
    df_cum_rets = portfolio.cum_returns[portfolio.portfolio_name]
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


def plot_monthly_returns_heatmap(portfolio: Portfolio) -> go.Figure:
    monthly_ret_table = ep.aggregate_returns(
        portfolio.returns[portfolio.portfolio_name], "monthly"
    )
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
) -> go.Figure:
    APPROX_BDAYS_PER_YEAR = 252
    fig = go.Figure()

    rolling_vol_ts = portfolio.returns.rolling(rolling_vol_window).std() * np.sqrt(
        APPROX_BDAYS_PER_YEAR
    )

    fig.add_trace(
        go.Scatter(
            meta=portfolio.portfolio_name,
            x=rolling_vol_ts[portfolio.portfolio_name].index,
            y=rolling_vol_ts[portfolio.portfolio_name].values,
            mode="lines",
            line_color="orangered",
        ),
    )

    if portfolio.benchmark_name is not None:
        fig.add_trace(
            go.Scatter(
                meta=portfolio.benchmark_name,
                x=rolling_vol_ts[portfolio.benchmark_name].index,
                y=rolling_vol_ts[portfolio.benchmark_name].values,
                mode="lines",
                line_color="grey",
            ),
        )

    fig.add_shape(
        type="line",
        yref="y",
        xref="paper",
        x0=0,
        y0=rolling_vol_ts[portfolio.portfolio_name].mean(),
        x1=1,
        y1=rolling_vol_ts[portfolio.portfolio_name].mean(),
        line=dict(
            color="steelblue",
            # width=4,
            dash="4px",
        ),
    )
    _center_title(fig, title="Rolling Volatility (6-month) %")
    fig.update_traces(hovertemplate="(%{x:'%Y-%m-%d'}, %{y:.2f}<extra>%{meta}</extra>)")
    fig.update_xaxes(tickformat="%Y-%m")
    fig.update_yaxes(tickformat=",.1%")
    return fig


def plot_monthly_returns_dist(portfolio: Portfolio) -> go.Figure:
    monthly_ret_table = ep.aggregate_returns(
        portfolio.returns[portfolio.portfolio_name],
        "monthly",
    )

    fig = go.Figure(
        go.Histogram(
            x=monthly_ret_table,
            opacity=0.8,
            nbinsx=20,
        ),
    )
    _center_title(fig, title="Distribution of Monthly Returns", bargap=0.1)
    fig.update_yaxes(dict(title="Number of Months"))
    fig.update_xaxes(
        dict(title="Returns"),
        tickformat=",.1%",
    )

    fig.add_vline(
        x=monthly_ret_table.mean(),
        line_width=1.5,
        line_dash="4px",
        line_color="red",
    )
    fig.add_vline(
        x=0.0,
        line_width=1.5,
        line_color="black",
    )

    return fig
