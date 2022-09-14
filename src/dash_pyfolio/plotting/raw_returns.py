import plotly.graph_objects as go
from dash_pyfolio.portfolio_data import Portfolio


def plot_returns(portfolio: Portfolio) -> go.Figure:
    fig = go.Figure()

    for i, name in enumerate(portfolio.returns.columns):

        if portfolio.live_start_date is not None and name == portfolio.portfolio_name:
            back_ret = portfolio.returns.loc[
                portfolio.returns.index < portfolio.live_start_date
            ]
            live_ret = portfolio.returns.loc[
                portfolio.returns.index >= portfolio.live_start_date
            ]
            fig.add_trace(
                go.Scatter(
                    name=f"{name}-Backtest",
                    meta=f"{name}-Backtest",
                    x=back_ret[name].index,
                    y=back_ret[name].values,
                    mode="lines",
                    line_color="#006400",
                ),
            )

            fig.add_trace(
                go.Scatter(
                    name=f"{name}-Live",
                    meta=f"{name}-Live",
                    x=live_ret[name].index,
                    y=live_ret[name].values,
                    mode="lines",
                    line=dict(color="#ff0000"),
                ),
            )
            continue
        else:
            fig.add_trace(
                go.Scatter(
                    name=name,
                    meta=name,
                    x=portfolio.returns[name].index,
                    y=portfolio.returns[name].values,
                    mode="lines",
                    visible="legendonly" if i > 0 else True,
                    # line_color="#006400",
                ),
            )

    fig.update_layout(
        title=dict(
            text="Returns",
            x=0.5,
            y=0.85,
            xanchor="center",
            yanchor="top",
        ),
        showlegend=True,
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

    fig.update_xaxes(
        tickformat="%Y-%m",
        ticks="outside",
    )
    fig.update_yaxes(tickformat=",.1%")
    fig.update_traces(
        hovertemplate="(%{x:'%Y-%m-%d'}, %{y:,.2%}<extra>%{meta}</extra>)"
    )

    return fig
