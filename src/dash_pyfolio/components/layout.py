from dash import Dash, html
import dash_bootstrap_components as dbc
from dash_pyfolio.portfolio_data import Portfolio
from dash_pyfolio.components.base import navbar
from dash_pyfolio.components.charts import (
    returns_chart,
    cumulative_returns_chart,
    rolling_volatility_chart,
    drawdown_chart,
    returns_heatmap,
)
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
            dbc.Tabs(
                [
                    dbc.Tab(
                        label="First Chart",
                        children=[
                            returns_chart.render(app, pf_data),
                            cumulative_returns_chart.render(app, pf_data),
                            drawdown_chart.render(app, pf_data),
                            returns_heatmap.render(app, pf_data),
                            rolling_volatility_chart.render(app, pf_data),
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
