import pandas as pd
import yfinance as yf
from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP
from folioqpy.portfolio_data import SimplePortfolio

from components.layout import create_layout

spy = yf.Ticker("META").history("max")
aapl = yf.Ticker("IBM").history("max")

spy.index = spy.index.tz_localize("utc")
aapl.index = aapl.index.tz_localize("utc")
spy_ret = spy.Close.pct_change().to_frame().rename({"Close": "SPY"}, axis=1)
aapl_ret = aapl.Close.pct_change().to_frame().rename({"Close": "AAPL"}, axis=1)

df = pd.concat([spy_ret, aapl_ret], axis=1).dropna(how="any", axis=0)

pf_data = SimplePortfolio(
    returns=df.loc["2019":],
    # portfolio_name="Test Portfolio",
    live_start_date="2020-1-1",
)


# load the data and create the data manager
app = Dash(external_stylesheets=[BOOTSTRAP], use_pages=False)
app.title = "folioqpy"

server = app.server

app.layout = create_layout(app, pf_data)
app.run(debug=True)
