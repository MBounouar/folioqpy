from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash_pyfolio.portfolio_data import Portfolio
from . import navbar
import dash_pyfolio.plotting as dplt
from dash_pyfolio.basic_components import simple_render

from . import ids


def create_layout(
    app: Dash,
    pf_data: Portfolio,
) -> html.Div:
    # This is a vary basic way to render plots using currying
    render = simple_render(app, pf_data, input_id=ids.DASH_APPLICATION)

    return html.Div(
        children=[
            # Input is set as dummy value to render charts
            dcc.Input(id=ids.DASH_APPLICATION, value="dummy"),
            navbar.render(app),
            html.Hr(),
            dbc.Tabs(
                [
                    dbc.Tab(
                        label="Overview",
                        children=[
                            render(
                                dplt.show_perf_stats, output_id=ids.PERF_STATS_TABLE
                            ),
                            render(
                                dplt.show_top_drawdown, output_id=ids.TOP_DRAWDOWN_TABLE
                            ),
                            render(
                                dplt.plot_returns,
                                output_id=ids.RETURNS_CHART,
                            ),
                            render(
                                dplt.plot_annual_returns,
                                output_id=ids.ANNUAL_RETURNS_BAR_CHART,
                            ),
                            render(
                                dplt.plot_drawdown_underwater,
                                output_id=ids.DRAWDOWN_RETURNS_CHART,
                            ),
                            render(
                                dplt.plot_monthly_returns_heatmap,
                                output_id=ids.MONTHLY_RETURNS_HEATMAP,
                            ),
                            render(
                                dplt.plot_rolling_volatility,
                                output_id=ids.ROLLING_VOLATILITY_CHART,
                            ),
                            render(
                                dplt.plot_monthly_returns_dist,
                                output_id=ids.MONNTLY_RETURNS_DIST,
                            ),
                            render(
                                dplt.plot_cumulative_returns,
                                output_id=ids.CUMULATIVE_RETURNS_CHART,
                            ),
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
