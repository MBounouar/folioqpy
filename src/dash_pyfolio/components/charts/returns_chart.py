# import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash_pyfolio.plotting import plot_returns

from .. import ids


def render(app: Dash, pf_data) -> html.Div:
    @app.callback(
        Output(ids.RETURNS_CHART, "children"),
        Input(ids.DASH_APPLICATION, "value"),
    )
    def update_returns_chart(value) -> html.Div:
        return dcc.Graph(
            figure=plot_returns(pf_data),
            config={"displaylogo": False},
        )

    return html.Div(id=ids.RETURNS_CHART)
