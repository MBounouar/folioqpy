import pandas as pd
from typing import Union
import empyrical as ep
import numpy as np
from itertools import chain


def get_utc_timestamp(
    dt: Union[pd.Timestamp, pd.DatetimeIndex]
) -> Union[pd.Timestamp, pd.DatetimeIndex]:
    """Returns the Timestamp/DatetimeIndex with either localized or converted to UTC.

    Args:
        dt (Union[pd.Timestamp, pd.DatetimeIndex]): the date(s) to be converted

    Returns:
        Union[pd.Timestamp, pd.DatetimeIndex]: date(s) converted to UTC
    """

    dt = pd.to_datetime(dt)
    try:
        dt = dt.tz_localize("UTC")
    except TypeError:
        dt = dt.tz_convert("UTC")
    return dt


def simulate_paths(
    is_returns: pd.Series,
    num_days: int,
    starting_value=1,
    num_samples: int = 1000,
    random_seed: Union[int, None] = None,
) -> np.ndarray:
    """Generate alternate paths using available values from in-sample returns.

    Args:
        is_returns (pd.Series): Non-cumulative in-sample returns.
        num_days (int): Number of days to project the probability cone forward.
        num_samples (int, optional): Number of samples to draw from the in-sample daily returns.
        Each sample will be an array with length num_days.
        A higher number of samples will generate a more accurate
        bootstrap cone. Defaults to 1000.
        random_seed (Union[int, None], optional): Seed for the pseudorandom number generator used by the pandas
        sample method. Defaults to None.

    Returns:
        np.ndarray: samples

    """

    samples = np.empty((num_samples, num_days))
    seed = np.random.RandomState(seed=random_seed)
    for i in range(num_samples):
        samples[i, :] = is_returns.sample(num_days, replace=True, random_state=seed)

    return samples


def summarize_paths(samples, cone_std=(1.0, 1.5, 2.0), starting_value=1.0):
    """
    Gnerate the upper and lower bounds of an n standard deviation
    cone of forecasted cumulative returns.

    Parameters
    ----------
    samples : numpy.ndarray
        Alternative paths, or series of possible outcomes.
    cone_std : list of int/float
        Number of standard devations to use in the boundaries of
        the cone. If multiple values are passed, cone bounds will
        be generated for each value.

    Returns
    -------
    samples : pandas.core.frame.DataFrame
    """

    cum_samples = ep.cum_returns(samples.T, starting_value=starting_value).T

    cum_mean = cum_samples.mean(axis=0)
    cum_std = cum_samples.std(axis=0)

    if isinstance(cone_std, (float, int)):
        cone_std = [cone_std]

    df_columns = list(
        chain(*list(zip(np.array(cone_std, dtype=np.float64), -np.array(cone_std))))
    )
    cone_bounds = pd.DataFrame(columns=df_columns, index=range(len(cum_mean)))
    for num_std in cone_std:
        cone_bounds.loc[:, float(num_std)] = cum_mean + cum_std * num_std
        cone_bounds.loc[:, float(-num_std)] = cum_mean - cum_std * num_std

    return cone_bounds


def forecast_cone_bootstrap(
    is_returns,
    num_days,
    cone_std=(1.0, 1.5, 2.0),
    starting_value=1,
    num_samples=1000,
    random_seed=None,
):
    """
    Determines the upper and lower bounds of an n standard deviation
    cone of forecasted cumulative returns. Future cumulative mean and
    standard devation are computed by repeatedly sampling from the
    in-sample daily returns (i.e. bootstrap). This cone is non-parametric,
    meaning it does not assume that returns are normally distributed.

    Parameters
    ----------
    is_returns : pd.Series
        In-sample daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    num_days : int
        Number of days to project the probability cone forward.
    cone_std : int, float, or list of int/float
        Number of standard devations to use in the boundaries of
        the cone. If multiple values are passed, cone bounds will
        be generated for each value.
    starting_value : int or float
        Starting value of the out of sample period.
    num_samples : int
        Number of samples to draw from the in-sample daily returns.
        Each sample will be an array with length num_days.
        A higher number of samples will generate a more accurate
        bootstrap cone.
    random_seed : int
        Seed for the pseudorandom number generator used by the pandas
        sample method.

    Returns
    -------
    pd.DataFrame
        Contains upper and lower cone boundaries. Column names are
        strings corresponding to the number of standard devations
        above (positive) or below (negative) the projected mean
        cumulative returns.
    """

    samples = simulate_paths(
        is_returns=is_returns,
        num_days=num_days,
        starting_value=starting_value,
        num_samples=num_samples,
        random_seed=random_seed,
    )

    cone_bounds = summarize_paths(
        samples=samples,
        cone_std=cone_std,
        starting_value=starting_value,
    )

    return cone_bounds
