import empyrical as ep
import scipy as sp
import pandas as pd
import numpy as np
from typing import Union

from .portfolio_data import Portfolio
from .stats import value_at_risk


STAT_FUNC_NAMES = {
    "Annual return": [ep.annual_return, ".1%"],
    "Cumulative returns": [ep.cum_returns_final, ".1%"],
    "Annual volatility": [ep.annual_volatility, ".1%"],
    "Sharpe ratio": [ep.sharpe_ratio, ".2f"],
    "Calmar ratio": [ep.calmar_ratio, ".2f"],
    "Stability": [ep.stability_of_timeseries, ".2f"],
    "Max drawdown": [ep.max_drawdown, ".1%"],
    "Omega ratio": [ep.omega_ratio, ".2f"],
    "Sortino ratio": [ep.sortino_ratio, ".2f"],
    "Skew": [sp.stats.skew, ".2f"],
    "Kurtosis": [sp.stats.kurtosis, ".2f"],
    "Tail ratio": [ep.tail_ratio, ".2f"],
    # "Common sense ratio": ,
    "Daily value at risk": [value_at_risk, ".1%"],
    # "alpha": "Alpha",
    # "beta": "Beta",
}


def perf_stats(
    portfolio: Portfolio,
    # factor_returns=None,
    # positions=None,
    # transactions=None,
    # turnover_denom="AGB",
) -> pd.DataFrame:
    """Returns some performance metrics of the strategy.


    Args:
      portfolio:
        A Portfolio instance.

    Returns:
      A pandas DataFrame

    """

    stats = pd.DataFrame(
        index=STAT_FUNC_NAMES.keys(),
        columns=[portfolio.portfolio_name],
    ).rename_axis("Metric")
    for func_name, (stat_func, _) in STAT_FUNC_NAMES.items():
        stats.loc[func_name, portfolio.portfolio_name] = stat_func(
            portfolio.returns[portfolio.portfolio_name]
        )

    # if positions is not None:
    #     stats["Gross leverage"] = gross_lev(positions).mean()
    #     if transactions is not None:
    #         stats["Daily turnover"] = get_turnover(
    #             positions, transactions, turnover_denom
    #         ).mean()
    # if factor_returns is not None:
    #     for stat_func in FACTOR_STAT_FUNCS:
    #         res = stat_func(returns, factor_returns)
    #         stats[STAT_FUNC_NAMES[stat_func.__name__]] = res

    stats = stats.reset_index()
    return stats


def get_max_drawdown_underwater(underwater):
    """
    Determines peak, valley, and recovery dates given an 'underwater'
    DataFrame.

    An underwater DataFrame is a DataFrame that has precomputed
    rolling drawdown.

    Parameters
    ----------
    underwater : pd.Series
       Underwater returns (rolling drawdown) of a strategy.

    Returns
    -------
    peak : datetime
        The maximum drawdown's peak.
    valley : datetime
        The maximum drawdown's valley.
    recovery : datetime
        The maximum drawdown's recovery.
    """

    valley = underwater.idxmin()  # end of the period
    # Find first 0
    peak = underwater[:valley][underwater[:valley] == 0].index[-1]
    # Find last 0
    try:
        recovery = underwater[valley:][underwater[valley:] == 0].index[0]
    except IndexError:
        recovery = np.nan  # drawdown not recovered
    return peak, valley, recovery


def get_top_drawdowns(df_cum, top=10):
    """
    Finds top drawdowns, sorted by drawdown amount.

    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    top : int, optional
        The amount of top drawdowns to find (default 10).

    Returns
    -------
    drawdowns : list
        List of drawdown peaks, valleys, and recoveries. See get_max_drawdown.
    """

    running_max = np.maximum.accumulate(df_cum)
    underwater = df_cum / running_max - 1

    drawdowns = []
    for _ in range(top):
        peak, valley, recovery = get_max_drawdown_underwater(underwater)
        # Slice out draw-down period
        if not pd.isnull(recovery):
            underwater.drop(underwater[peak:recovery].index[1:-1], inplace=True)
        else:
            # drawdown has not ended yet
            underwater = underwater.loc[:peak]

        drawdowns.append((peak, valley, recovery))
        if (len(underwater) == 0) or (np.min(underwater) == 0):
            break

    return drawdowns


def top_drawdown_table(portfolio: Portfolio, top: int = 5) -> pd.DataFrame:
    """Top Drawdown Table.

    Args:
        portfolio (Portfolio): _description_
        top (int, optional): Number of drawdown periods to find. Defaults to 5.

    Returns:
        pd.DataFrame: drawdowns
    """
    returns = portfolio.returns[portfolio.portfolio_name]
    df_cum = ep.cum_returns(returns, 1.0)
    drawdown_periods = get_top_drawdowns(df_cum, top=top)
    df_drawdowns = pd.DataFrame(
        index=range(top, 1),
        columns=[
            "Net drawdown in %",
            "Peak date",
            "Valley date",
            "Recovery date",
            "Duration",
        ],
    )

    for i, (peak, valley, recovery) in enumerate(drawdown_periods, 1):
        if pd.isnull(recovery):
            df_drawdowns.loc[i, "Recovery date"] = recovery
            df_drawdowns.loc[i, "Duration"] = np.nan
        else:
            df_drawdowns.loc[i, "Recovery date"] = recovery  # .strftime("%Y-%m-%d")

            # we add one day to replicate the behaviour
            df_drawdowns.loc[i, "Duration"] = 1 + np.busday_count(
                peak.asm8.astype("<M8[D]"), recovery.asm8.astype("<M8[D]")
            )
            # df_drawdowns.loc[i, "Duration"] = len(pd.date_range(peak, recovery, freq="B"))

        df_drawdowns.loc[i, "Peak date"] = peak  # .strftime("%Y-%m-%d")
        df_drawdowns.loc[i, "Valley date"] = valley  # .strftime("%Y-%m-%d")

        df_drawdowns.loc[i, "Net drawdown in %"] = (
            df_cum.loc[peak] - df_cum.loc[valley]
        ) / df_cum.loc[peak]

    df_drawdowns = df_drawdowns.rename_axis("Rank").reset_index()

    df_drawdowns[["Peak date", "Valley date", "Recovery date"]] = df_drawdowns[
        ["Peak date", "Valley date", "Recovery date"]
    ].astype("datetime64")

    return df_drawdowns


def drawdown_series(
    returns: Union[np.ndarray, pd.Series], out: np.ndarray = None
) -> Union[pd.Series, np.ndarray]:
    """Determines the series of drawdown of a strategy.

    Args:
        returns (Union[np.ndarray, pd.Series]):  Daily returns of the strategy, noncumulative.
        out (np.ndarray, optional): Array to use as output buffer. Defaults to None.

    Returns:
        Union[pd.Series, np.ndarray]: drawdown_series
    """
    allocated_output = out is None
    if allocated_output:
        out = np.empty(
            (returns.shape[0] + 1,) + returns.shape[1:],
            dtype="float64",
        )

    returns_1d = returns.ndim == 1

    if len(returns) < 1:
        out[()] = np.nan
        if returns_1d:
            out = out.item()
        return out

    returns_array = np.asanyarray(returns)

    out[0] = start = 100
    ep.cum_returns(returns_array, starting_value=start, out=out[1:])

    max_return = np.fmax.accumulate(out, axis=0)

    np.divide((out - max_return), max_return, out=out)

    if returns.ndim == 1 and isinstance(returns, pd.Series):
        out = pd.Series(out[1:], index=returns.index)
    elif isinstance(returns, pd.DataFrame):
        out = pd.DataFrame(
            out[1:],
            index=returns.index,
            columns=returns.columns,
        )

    return out
