# import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash_pyfolio.plotting import plot_returns

from .. import ids


def render(app: Dash, pf_data) -> html.Div:
    @app.callback(
        Output(ids.RETURNS_CHART, "children"),
        Input(ids.DASH_APPLICATION, "children"),
    )
    def update_returns_chart(years) -> html.Div:
        fig = plot_returns(pf_data)
        return html.Div(
            dcc.Graph(
                figure=fig,
                config={"displaylogo": False},
            ),
            id=ids.RETURNS_CHART,
        )

    return html.Div(id=ids.RETURNS_CHART)
