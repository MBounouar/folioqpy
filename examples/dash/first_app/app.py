import pandas as pd
import yfinance as yf
from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP
from folioqpy.portfolio_data import SimplePortfolio

from components.layout import create_layout

meta = yf.Ticker("META").history("max")
spy = yf.Ticker("SPY").history("max")

spy.index = spy.index.tz_localize("utc")
meta.index = meta.index.tz_localize("utc")
spy_ret = spy.Close.pct_change().to_frame().rename({"Close": "SPY"}, axis=1)
meta_ret = meta.Close.pct_change().to_frame().rename({"Close": "META"}, axis=1)

df = pd.concat([meta_ret, spy_ret], axis=1).dropna(how="any", axis=0)

pf_data = SimplePortfolio(
    returns=df.loc["2019":],
    # name="Test Portfolio",
    live_start_date="2020-1-1",
)


# load the data and create the data manager
app = Dash(external_stylesheets=[BOOTSTRAP], use_pages=False)
app.title = "folioqpy"

server = app.server

app.layout = create_layout(app, pf_data)
app.run(debug=True)
