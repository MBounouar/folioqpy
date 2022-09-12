from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from dash_pyfolio.components.layout import create_layout
from dash_pyfolio.portfolio_data import Portfolio
import yfinance as yf


spy = yf.Ticker("SPY").history("max")
spy.index = spy.index.tz_localize("utc")
spy_ret = spy.Close.pct_change()

pf_data = Portfolio(
    name="Test Portfolio",
    returns=spy_ret,
    live_start_date="2000-1-1",
)


# load the data and create the data manager

app = Dash(external_stylesheets=[BOOTSTRAP], use_pages=False)
app.title = "dash-pyfolio"

server = app.server

app.layout = create_layout(app, pf_data)
app.run(debug=True)
