import empyrical as ep
from typing import Any
import plotly.graph_objects as go
from folioqpy.portfolio_data import Portfolio


def plot_monthly_returns_dist(
    portfolio: Portfolio,
    **kwargs: dict[str, Any],
) -> go.Figure:
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

    fig.update_layout(
        title=dict(
            text="Distribution of Monthly Returns",
            x=0.5,
            y=0.85,
            xanchor="center",
            yanchor="top",
        ),
        bargap=0.05,
        yaxis=dict(title="Number of Months"),
        xaxis=dict(
            title="Returns",
            tickformat=",.1%",
            ticks="outside",
        ),
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


def plot_annual_returns(portfolio: Portfolio, **kwargs: dict[str, Any]) -> go.Figure:
    fig = go.Figure()

    for i, name in enumerate(portfolio.returns.columns):
        ann_ret_df = ep.aggregate_returns(portfolio.returns[name], "yearly")

        fig.add_trace(
            go.Bar(
                name=name,
                meta=name,
                x=ann_ret_df.values,
                y=ann_ret_df.index,
                text=ann_ret_df.values,
                orientation="h",
                texttemplate="%{text:,.2%}",
                hovertemplate="(%{y}, %{x:,.2%}<extra>%{meta}</extra>)",
                visible="legendonly" if i > 0 else True,
            )
        )

    fig.add_vline(
        x=0,
        line_width=2,
        line_color="black",
    )

    fig.update_layout(
        xaxis=dict(
            title="Returns",
            tickformat=",.1%",
            ticks="outside",
        ),
        yaxis=dict(title="Year"),
        title=dict(
            text="Annual Returns",
            x=0.5,
            y=0.85,
            xanchor="center",
            yanchor="top",
        ),
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
