import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import Dash, html

from . import ids


def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.NAVBAR_COLLAPSE, "is_open"),
        [Input(ids.NAVBAR_TOGGLER, "n_clicks")],
        [State(ids.NAVBAR_COLLAPSE, "is_open")],
    )
    def toggle_navbar_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    return dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(dbc.NavbarBrand(app.title, className="ms-2")),
                        ],
                        # align="center",
                        # className="g-0",
                    ),
                    href="https://github.com/MBounouar/dash-pyfolio",
                    style={"textDecoration": "none"},
                ),
                dbc.NavbarToggler(id=ids.NAVBAR_TOGGLER, n_clicks=0),
                dbc.Collapse(
                    dbc.Nav(
                        # nav_items
                        navbar=True,
                        className="ms-5",
                    ),
                    id=ids.NAVBAR_COLLAPSE,
                    # is_open=False,
                    navbar=True,
                ),
            ],
            fluid=True,
        ),
        color="dark",
        dark=True,
        fixed="top",
        className="mb-5",
    )
