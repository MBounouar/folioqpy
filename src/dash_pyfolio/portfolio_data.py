from dataclasses import dataclass, field

# import abc
from typing import Union
import pandas as pd
from dash_pyfolio.utils import get_utc_timestamp
import empyrical as ep


# @runtime_checkable
# class Portfolio(Protocol):
#     @abc.abstractproperty
#     def live_start_date(self):
#         ...


class Portfolio:
    pass


@dataclass
class SimplePortfolio(Portfolio):
    returns: pd.DataFrame = field(repr=False)
    base_currency: str = field(default="USD")
    portfolio_name: str = field(default=None)
    live_start_date: Union[pd.Timestamp, str] = field(default=None)
    benchmark_name: str = field(repr=False, default=None)
    risk_free_rate: Union[float, pd.Series] = field(repr=False, default=None)

    def __post_init__(self) -> None:
        if self.live_start_date is not None:
            self.live_start_date = get_utc_timestamp(self.live_start_date)
        if self.portfolio_name is None:
            self.portfolio_name = self.returns.columns[0]
        if self.benchmark_name is None and len(self.returns.columns) >= 2:
            self.benchmark_name = self.returns.columns[1]
        self.cum_returns = ep.cum_returns(self.returns, 1.0)
