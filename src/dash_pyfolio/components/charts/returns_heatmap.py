# import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash_pyfolio.plotting import plot_monthly_returns_heatmap

from .. import ids


def render(app: Dash, pf_data) -> html.Div:
    @app.callback(
        Output(ids.MONTHLY_RETURNS_HEATMAP, "children"),
        Input(ids.DASH_APPLICATION, "value"),
    )
    def update_heatmap_chart(value) -> html.Div:
        return dcc.Graph(
            figure=plot_monthly_returns_heatmap(pf_data),
            config={"displaylogo": False},
        )

    return html.Div(id=ids.MONTHLY_RETURNS_HEATMAP)
