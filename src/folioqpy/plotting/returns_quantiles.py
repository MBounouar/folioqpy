import plotly.graph_objects as go
from ..portfolio_data import Portfolio
from ..stats import aggregate_returns
from ..periods import WEEKLY, MONTHLY


def plot_return_quantiles(
    portfolio: Portfolio, title: str = "Returns Quantiles"
) -> go.Figure:
    """Box plot of daily, weekly, and monthly return
    distributions.

    Args:
        portfolio (Portfolio): _description_

    Returns:
        Figure: plotly graph object Figure instance
    """
    pf_name = portfolio.portfolio_name
    palette = {"daily": "#4c72B0", "weekly": "#55A868", "monthly": "#CCB974"}

    fig = go.Figure()

    if portfolio.live_start_date is not None:
        is_returns = portfolio.returns[pf_name].loc[
            portfolio.returns.index < portfolio.live_start_date
        ]
        oos_returns = portfolio.returns[pf_name].loc[
            portfolio.returns.index > portfolio.live_start_date
        ]

        is_weekly = aggregate_returns(is_returns, WEEKLY)
        oos_weekly = aggregate_returns(oos_returns, WEEKLY)

        is_monthly = aggregate_returns(is_returns, MONTHLY)
        oos_monthly = aggregate_returns(oos_returns, MONTHLY)

        fig.add_trace(
            go.Box(
                name="Daily",
                y=is_returns.values,
                marker_color=palette["daily"],
            )
        )
        fig.add_trace(
            go.Box(
                name="Daily",
                y=oos_returns.values,
                boxpoints="all",
                hoverinfo="skip",
                pointpos=0,
                # jitter=0.5,
                marker_size=2,
                marker=dict(color="rgb(255, 0, 0)"),
                line=dict(color="rgba(0,0,0,0)"),
                fillcolor="rgba(0,0,0,0)",
            )
        )
        fig.add_trace(
            go.Box(
                name="Weekly",
                y=is_weekly.values,
                marker_color=palette["weekly"],
            )
        )
        fig.add_trace(
            go.Box(
                name="Weekly",
                y=oos_weekly.values,
                boxpoints="all",
                hoverinfo="skip",
                pointpos=0,
                # jitter=0.5,
                marker_size=2,
                marker=dict(color="rgb(255, 0, 0)"),
                line=dict(color="rgba(0,0,0,0)"),
                fillcolor="rgba(0,0,0,0)",
            )
        )
        fig.add_trace(
            go.Box(
                y=is_monthly.values,
                name="Monthly",
                marker_color=palette["monthly"],
            )
        )
        fig.add_trace(
            go.Box(
                name="Monthly",
                y=oos_monthly.values,
                boxpoints="all",
                hoverinfo="skip",
                pointpos=0,
                # jitter=0.5,
                marker_size=2,
                marker=dict(color="rgb(255, 0, 0)"),
                line=dict(color="rgba(0,0,0,0)"),
                fillcolor="rgba(0,0,0,0)",
            )
        )

    else:
        is_returns = portfolio.returns

    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            y=0.85,
            xanchor="center",
            yanchor="top",
        ),
        yaxis=dict(
            tickformat=",.1%",
            title="Returns %",
            zeroline=True,
            autorange=True,
        ),
        showlegend=False,
        # boxmode="group",
    )
    return fig
