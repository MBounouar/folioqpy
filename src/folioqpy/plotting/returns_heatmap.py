import calendar

import plotly.graph_objects as go
from ..portfolio_data import Portfolio
from ..periods import AnnualizationFactor
from ..stats.qstats import aggregate_returns


def plot_monthly_returns_heatmap(portfolio: Portfolio, **kwargs) -> go.Figure:
    monthly_ret_table = aggregate_returns(
        portfolio.returns[portfolio.portfolio_name], AnnualizationFactor.MONTHLY
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
            hoverongaps=False,
            hovertemplate="%{x:'%B'}-%{y:'%Y'}, %{z:,.2%}<extra></extra>",
        ),
    )

    fig.update_layout(
        xaxis=dict(title="Month"),
        yaxis=dict(title="Year"),
        title=dict(
            text="Monthly Returns %",
            x=0.5,
            y=0.85,
            xanchor="center",
            yanchor="top",
        ),
    )
    return fig
