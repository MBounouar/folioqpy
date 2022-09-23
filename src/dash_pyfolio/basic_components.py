from typing import Any, Union

import plotly.graph_objects as go
from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output
from toolz import curry

from dash_pyfolio.portfolio_data import Portfolio


@curry
def simple_render(
    app: Dash,
    pf_data: Portfolio,
    fn: Any,
    output_id: str,
    input_id: str,
    **kwargs: dict[str, Any],
) -> html.Div:
    @app.callback(
        Output(output_id, "children"),
        Input(input_id, "value"),
    )
    def update_component(value) -> html.Div:
        obj = fn(pf_data, **kwargs)
        if isinstance(obj, go.Figure):
            return dcc.Graph(
                figure=obj,
                config={"displaylogo": False},
            )
        elif isinstance(obj, dash_table.DataTable):
            return obj
        else:
            raise Exception

    return html.Div(id=output_id)


@curry
def basic_table_render(
    app: Dash,
    pf_data: Portfolio,
    fn: Any,
    output_id: str,
    input_id: str,
    **kwargs: Union[str, int],
) -> html.Div:
    @app.callback(
        Output(output_id, "children"),
        Input(input_id, "value"),
    )
    def update_table(value) -> html.Div:
        return fn(pf_data, **kwargs)

    return html.Div(id=output_id)
