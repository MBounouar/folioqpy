from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from src.components.layout import create_layout
from src.data.loader import load_transaction_data

import yfinance as yf


spy = yf.Ticker("SPY").history("max")
spy.index = spy.index.tz_localize("utc")
spy = spy.Close.pct_change()

fb = yf.Ticker("IBM")
history = fb.history("max")
history.index = history.index.tz_localize("utc")

returns = history.Close.pct_change()


DATA_PATH = "./data/transactions.csv"

# load the data and create the data manager
data = load_transaction_data(DATA_PATH)

app = Dash(external_stylesheets=[BOOTSTRAP], use_pages=False)
app.title = "dash-pyfolio"

server = app.server

app.layout = create_layout(app, data)
app.run(debug=True)
