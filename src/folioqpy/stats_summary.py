import scipy as sp
import pandas as pd
import numpy as np

from .portfolio_data import Portfolio
from .stats.var import value_at_risk
from .stats.qstats import (
    cum_returns,
    annual_return,
    cum_returns_final,
    annual_volatility,
    sharpe_ratio,
    calmar_ratio,
    stability_of_timeseries,
    max_drawdown,
    omega_ratio,
    sortino_ratio,
    tail_ratio,
    get_top_drawdowns,
)

STAT_FUNC_NAMES = {
    "Annual return": [annual_return, ".1%"],
    "Cumulative returns": [cum_returns_final, ".1%"],
    "Annual volatility": [annual_volatility, ".1%"],
    "Sharpe ratio": [sharpe_ratio, ".2f"],
    "Calmar ratio": [calmar_ratio, ".2f"],
    "Stability": [stability_of_timeseries, ".2f"],
    "Max drawdown": [max_drawdown, ".1%"],
    "Omega ratio": [omega_ratio, ".2f"],
    "Sortino ratio": [sortino_ratio, ".2f"],
    "Skew": [sp.stats.skew, ".2f"],
    "Kurtosis": [sp.stats.kurtosis, ".2f"],
    "Tail ratio": [tail_ratio, ".2f"],
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

    Parameters
    ----------
    portfolio : Portfolio
        Instance of Portfolio

    Returns
    -------
    pd.DataFrame

    """

    stats = pd.DataFrame(
        index=STAT_FUNC_NAMES.keys(),
        columns=[portfolio.name],
    ).rename_axis("Metric")

    for func_name, (stat_func, _) in STAT_FUNC_NAMES.items():
        stats.loc[func_name, portfolio.name] = stat_func(
            portfolio.returns[portfolio.name]
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


def top_drawdown_table(
    portfolio: Portfolio,
    top: int = 5,
) -> pd.DataFrame:
    """Top Drawdowns table.

    Parameters
    ----------
    portfolio : Portfolio
        Portfolio instance
    top : int, optional
        Number of drawdown periods to find, by default 5

    Returns
    -------
    pd.DataFrame

    """

    returns = portfolio.returns[portfolio.name]
    df_cum = cum_returns(returns, 1.0)
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
