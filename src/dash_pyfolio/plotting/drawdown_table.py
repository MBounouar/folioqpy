from ..portfolio_data import Portfolio
from ..stats_summary import top_drawdown_table
import plotly.graph_objects as go


def show_top_drawdown(portfolio: Portfolio) -> go.Figure:
    df = top_drawdown_table(portfolio, top=5)
    format = [None, ".2%", None, None, None, None]

    fig = go.Figure(
        data=go.Table(
            header=dict(
                values=[f"<b>{x}</b>" for x in df.columns],
                align="left",
                font=dict(color="black"),
                line=dict(color="#e6e6e6"),
                fill=dict(color="#e6e6e6"),
            ),
            cells=dict(
                values=[df[k].tolist() for k in df.columns],
                align="left",
                format=format,
                fill=dict(color="white"),
            ),
        ),
    )
    return fig
