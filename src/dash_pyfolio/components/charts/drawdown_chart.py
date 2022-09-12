# import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash_pyfolio.plotting import plot_drawdown_underwater

from .. import ids


def render(app: Dash, pf_data) -> html.Div:
    @app.callback(
        Output(ids.DRAWDOWN_RETURNS_CHART, "children"),
        Input(ids.DASH_APPLICATION, "children"),
    )
    def update_drawdown_chart(value) -> html.Div:
        fig = plot_drawdown_underwater(pf_data)
        return html.Div(
            dcc.Graph(
                figure=fig,
                config={"displaylogo": False},
            ),
            id=ids.DRAWDOWN_RETURNS_CHART,
        )

    return html.Div(id=ids.DRAWDOWN_RETURNS_CHART)
