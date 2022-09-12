from dataclasses import dataclass, field

# from typing import Protocol
from typing import Union
import pandas as pd
from dash_pyfolio.utils import get_utc_timestamp
import empyrical as ep


@dataclass
class Portfolio:
    name: str
    returns: pd.Series = field(repr=False)
    live_start_date: Union[pd.Timestamp, str] = field(default=None)

    benchmark_name: str = field(repr=False, default="Benchmark")
    benchmark_returns: pd.Series = field(repr=False, default=None)

    def __post_init__(self) -> None:
        if self.live_start_date is not None:
            self.live_start_date = get_utc_timestamp(self.live_start_date)
        self.cum_returns = ep.cum_returns(self.returns, 1.0)

    @property
    def back_returns(self) -> pd.Series:
        if self.live_start_date:
            return self.returns.loc[self.returns.index < self.live_start_date]
        return self.returns

    @property
    def cum_back_returns(self) -> pd.Series:
        if self.live_start_date:
            return self.cum_returns.loc[self.cum_returns.index < self.live_start_date]
        return self.cum_returns

    @property
    def live_returns(self) -> Union[None, pd.Series]:
        if self.live_start_date:
            return self.returns.loc[self.returns.index >= self.live_start_date]

    @property
    def cum_live_returns(self) -> pd.Series:
        if self.live_start_date:
            return self.cum_returns.loc[self.cum_returns.index >= self.live_start_date]
