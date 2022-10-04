from folioqpy.stats import roll_beta
from folioqpy.portfolio_data import Portfolio
from folioqpy.periods import AnnualizationFactor

import plotly.graph_objects as go


def plot_rolling_beta(
    portfolio: Portfolio,
    title="Rolling Beta",
    **kwargs,
) -> go.Figure:
    fig = go.Figure()
    pf_name = portfolio.name
    bm_name = portfolio.benchmark_name
    for n in [6, 12]:

        beta = roll_beta(
            portfolio.returns[pf_name],
            portfolio.returns[bm_name],
            # risk_free=0.0,
            window=AnnualizationFactor.MONTHLY.value * n,
        ).reindex(portfolio.returns.index)

        fig.add_trace(
            go.Scatter(
                # legendgroup=name,
                name=f"{n}-mo window",
                meta=f"{n}-mo window",
                x=beta.index,
                y=beta.values,
                mode="lines",
                # visible="legendonly" if i > 0 else True,
            ),
        )

    fig.add_hline(
        y=1.0,
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
            title="Beta",
            tickformat=".1f",
        ),
    )

    return fig
