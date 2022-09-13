from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from dash_pyfolio.components.layout import create_layout
from dash_pyfolio.portfolio_data import Portfolio
import yfinance as yf
import pandas as pd


spy = yf.Ticker("META").history("max")
aapl = yf.Ticker("IBM").history("max")

spy.index = spy.index.tz_localize("utc")
aapl.index = aapl.index.tz_localize("utc")
spy_ret = spy.Close.pct_change().to_frame().rename({"Close": "SPY"}, axis=1)
aapl_ret = aapl.Close.pct_change().to_frame().rename({"Close": "AAPL"}, axis=1)

df = pd.concat([spy_ret, aapl_ret], axis=1).dropna(how="any", axis=0)

pf_data = Portfolio(
    returns=df.loc["2019":],
    # portfolio_name="Test Portfolio",
    live_start_date="2020-1-1",
)


# load the data and create the data manager

app = Dash(external_stylesheets=[BOOTSTRAP], use_pages=False)
app.title = "dash-pyfolio"

server = app.server

app.layout = create_layout(app, pf_data)
app.run(debug=True)
