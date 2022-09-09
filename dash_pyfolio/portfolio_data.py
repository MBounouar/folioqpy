from dataclasses import dataclass, field

# from typing import Protocol
from typing import Union
import pandas as pd
from dash_pyfolio.utils import get_utc_timestamp


@dataclass
class Portfolio:
    name: str
    returns: pd.Series = field(repr=False)
    live_start_date: Union[pd.Timestamp, str] = field(default=None)

    def __post_init__(self) -> None:
        if self.live_start_date is not None:
            self.live_start_date = get_utc_timestamp(self.live_start_date)
