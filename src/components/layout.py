from dash import Dash, html
import dash_bootstrap_components as dbc
from dash_pyfolio.portfolio_data import Portfolio
from src.components.base import navbar
from src.components.charts import returns_chart
from . import ids


def create_layout(
    app: Dash,
    pf_data: Portfolio,
) -> html.Div:
    return html.Div(
        className="app-div",
        id=ids.DASH_APPLICATION,
        children=[
            navbar.render(app),
            html.Hr(),
            html.Hr(),
            dbc.Tabs(
                [
                    dbc.Tab(
                        label="First Chart",
                        children=[
                            returns_chart.render(app, pf_data),
                        ],
                    ),
                    # dbc.Tab(
                    #     label="Second Chart",
                    #     children=[
                    #         html.Div(
                    #             className="dropdown-container",
                    #             children=[
                    #                 year_dropdown.render(app, data),
                    #                 month_dropdown.render(app, data),
                    #                 category_dropdown.render(app, data),
                    #             ],
                    #         ),
                    #         pie_chart.render(app, data),
                    #         bar_chart.render(app, data),
                    #     ],
                    # ),
                ],
            ),
        ],
    )
