from ..portfolio_data import Portfolio
from ..stats_summary import perf_stats, STAT_FUNC_NAMES
import plotly.graph_objects as go


def show_perf_stats(portfolio: Portfolio) -> go.Figure:
    df = perf_stats(portfolio)
    stats_fmt  = [fmt for _, fmt in STAT_FUNC_NAMES.values()]
    format = [[None]*len(df.index)]
    
    for _ in df.columns[1:]:
        format.append(stats_fmt)

    fig = go.Figure(
        layout=dict(height=600, width=600),
        data=go.Table(
            # domain=dict(x=[0, 0.5], y=[0, 1.0]),
            columnwidth=[80, 20],
            # columnorder=list(range(len(df.columns))),
            header=dict(
                # height=50,
                values=[f"<b>{x}</b>" for x in df.columns],
                align="left",
                font=dict(color="black"),
                # font=dict(color=["rgb(45, 45, 45)"] * (len(df.columns)), size=14),
                line=dict(color="#e6e6e6"),
                fill=dict(color="#e6e6e6"),
            ),
            cells=dict(
                values=[df[k].tolist() for k in df.columns],
                # line=dict(color="#506784"),
                align="left",
                # font=dict(color=["rgb(40, 40, 40)"] * len(df.columns), size=12),
                format=format,
                # prefix=[None] + ["$", "\u20BF"],
                # suffix=[None] * 4,
                # height=27,
                fill=dict(color='white'),
                # fill=dict(color=["rgb(235, 193, 238)", "rgba(228, 222, 249, 0.65)"]),
            ),
        )
    )
    return fig
    