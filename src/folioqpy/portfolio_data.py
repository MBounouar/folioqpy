from dataclasses import dataclass, field

# import abc
from typing import Union, Optional
import pandas as pd
from folioqpy.utils import get_utc_timestamp
import empyrical as ep


# @runtime_checkable
# class Portfolio(Protocol):
#     @abc.abstractproperty
#     def live_start_date(self):
#         ...

# import attrs


class Portfolio:
    pass
    # @abstractproperty
    # def portfolio_name(self):
    #     ...

    # @abstractproperty
    # def returns(self):
    #     ..


@dataclass
class SimplePortfolio(Portfolio):
    returns: pd.DataFrame = field(repr=False)
    base_currency: str = field(default="USD")
    portfolio_name: Optional[str] = field(default=None)
    live_start_date: Union[pd.Timestamp, str] = field(default=None)
    benchmark_name: Optional[str] = field(repr=False, default=None)
    risk_free_rate: Union[float, pd.Series] = field(repr=False, default=0.0)

    def __post_init__(self) -> None:
        if self.live_start_date is not None:
            self.live_start_date = get_utc_timestamp(self.live_start_date)
        if self.portfolio_name is None:
            self.portfolio_name = self.returns.columns[0]
        if self.benchmark_name is None and len(self.returns.columns) >= 2:
            self.benchmark_name = self.returns.columns[1]

    @classmethod
    def cum_returns(cls, returns, starting_value=1.0):
        return ep.cum_returns(returns, starting_value)
