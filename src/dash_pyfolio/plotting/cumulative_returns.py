import plotly.graph_objects as go
from dash_pyfolio.portfolio_data import Portfolio


def plot_cumulative_returns(portfolio: Portfolio) -> go.Figure:
    fig = go.Figure()

    for i, name in enumerate(portfolio.cum_returns.columns):
        if portfolio.live_start_date is not None and name == portfolio.portfolio_name:
            cum_back_ret = portfolio.cum_returns.loc[
                portfolio.cum_returns.index < portfolio.live_start_date
            ][name]

            cum_live_ret = portfolio.cum_returns.loc[
                portfolio.cum_returns.index >= portfolio.live_start_date
            ][name]

            fig.add_trace(
                go.Scatter(
                    name=f"{name}-Backtest",
                    meta=f"{name}-Backtest",
                    x=cum_back_ret.index,
                    y=cum_back_ret.values,
                    mode="lines",
                    line_color="#006400",
                ),
            )
            fig.add_trace(
                go.Scatter(
                    name=f"{name}-Live",
                    meta=f"{name}-Live",
                    x=cum_live_ret.index,
                    y=cum_live_ret.values,
                    mode="lines",
                    line=dict(color="#ff0000"),
                ),
            )
            continue

        fig.add_trace(
            go.Scatter(
                name=name,
                meta=name,
                x=portfolio.cum_returns[name].index,
                y=portfolio.cum_returns[name].values,
                mode="lines",
                # line=dict(color="grey"),
            ),
        )

    fig.add_hline(
        y=1,
        line_width=1.5,
        line_dash="4px",
        # line_color="red",
    )

    fig.update_layout(
        title=dict(
            text="Cumulative Returns",
            x=0.5,
            y=0.85,
            xanchor="center",
            yanchor="top",
        ),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=1,
            xanchor="left",
            x=0,
            bgcolor="rgba(0,0,0,0)",
            bordercolor="#DDDDDD",
            borderwidth=1,
        ),
    )

    fig.update_xaxes(
        # dtick="M3",
        tickformat="%Y-%m",
        ticks="outside",
    )
    fig.update_yaxes(tickformat=".2f")
    # fig.update_traces(hovertemplate="%{x}  %{y:.2f}<extra></extra>")
    fig.update_traces(hovertemplate="(%{x:'%Y-%m-%d'}, %{y:.2f}<extra>%{meta}</extra>)")

    return fig
