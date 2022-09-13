# import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash_pyfolio.plotting import plot_monthly_returns_dist

from .. import ids


def render(app: Dash, pf_data) -> html.Div:
    @app.callback(
        Output(ids.MONNTLY_RETURNS_DIST, "children"),
        Input(ids.DASH_APPLICATION, "value"),
    )
    def update_monthly_returns_dist(value) -> html.Div:
        return dcc.Graph(
            figure=plot_monthly_returns_dist(pf_data),
            config={"displaylogo": False},
        )

    return html.Div(id=ids.MONNTLY_RETURNS_DIST)
