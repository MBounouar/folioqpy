# import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash_pyfolio.plotting import plot_rolling_volatility

from .. import ids


def render(app: Dash, pf_data) -> html.Div:
    @app.callback(
        Output(ids.ROLLING_VOLATILITY_CHART, "children"),
        Input(ids.DASH_APPLICATION, "children"),
    )
    def update_cum_returns_chart(value) -> html.Div:
        fig = plot_rolling_volatility(pf_data)
        return html.Div(
            dcc.Graph(
                figure=fig,
                config={"displaylogo": False},
            ),
            id=ids.ROLLING_VOLATILITY_CHART,
        )

    return html.Div(id=ids.ROLLING_VOLATILITY_CHART)
