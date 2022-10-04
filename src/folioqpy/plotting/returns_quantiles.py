import plotly.graph_objects as go

from ..periods import DAILY, MONTHLY, QUARTERLY, WEEKLY
from ..portfolio_data import Portfolio
from ..stats import aggregate_returns


def plot_return_quantiles(
    portfolio: Portfolio,
    title: str = "Returns Quantiles",
) -> go.Figure:
    """Box plot of daily, weekly, and monthly return distributions.

    Parameters
    ----------
    portfolio : Portfolio
        Portfolio instance
    title : str, optional
        title, by default "Returns Quantiles"

    Returns
    -------
    go.Figure

    """

    pf_name = portfolio.name
    plot_periods = [DAILY, WEEKLY, MONTHLY, QUARTERLY]
    palette = {
        "daily": "#4c72B0",
        "weekly": "#55A868",
        "monthly": "#CCB974",
        "quarterly": "#BCBD22",
    }

    # palette = {
    #     str(x): px.colors.qualitative.Plotly[i] for i, x in enumerate(plot_periods)
    # }

    fig = go.Figure()

    if portfolio.live_start_date is not None:
        is_returns = portfolio.returns[pf_name].loc[
            portfolio.returns.index < portfolio.live_start_date
        ]
        oos_returns = portfolio.returns[pf_name].loc[
            portfolio.returns.index > portfolio.live_start_date
        ]
    else:
        is_returns = portfolio.returns[pf_name]

    for prd in plot_periods:
        name = str(prd).title()
        if prd is DAILY:
            is_y = is_returns.values
        else:
            is_y = aggregate_returns(is_returns, convert_to=prd).values

        fig.add_trace(
            go.Box(
                name=name,
                y=is_y,
                marker_color=palette[name.lower()],
            ),
        )
        if portfolio.live_start_date is not None:
            if prd is DAILY:
                oos_y = oos_returns.values
            else:
                oos_y = aggregate_returns(oos_returns, convert_to=prd).values
            fig.add_trace(
                go.Box(
                    name=name,
                    y=oos_y,
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

    # else:
    #     is_returns = portfolio.returns

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
