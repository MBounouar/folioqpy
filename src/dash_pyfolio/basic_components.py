from typing import Any, Union

from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from toolz import curry

from dash_pyfolio.portfolio_data import Portfolio


@curry
def basic_plot_render(
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
    def update_plot(value) -> html.Div:
        return dcc.Graph(
            figure=fn(pf_data, **kwargs),
            config={"displaylogo": False},
        )

    return html.Div(id=output_id)
