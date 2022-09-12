import pandas as pd
from typing import Union


def get_utc_timestamp(
    dt: Union[pd.Timestamp, pd.DatetimeIndex]
) -> Union[pd.Timestamp, pd.DatetimeIndex]:
    """
    Returns the Timestamp/DatetimeIndex
    with either localized or converted to UTC.

    Parameters
    ----------
    dt : Timestamp/DatetimeIndex
        the date(s) to be converted

    Returns
    -------
    same type as input
        date(s) converted to UTC
    """

    dt = pd.to_datetime(dt)
    try:
        dt = dt.tz_localize("UTC")
    except TypeError:
        dt = dt.tz_convert("UTC")
    return dt
