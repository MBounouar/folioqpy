import empyrical as ep
import scipy as sp
import pandas as pd

from .portfolio_data import Portfolio
from .stats import value_at_risk


STAT_FUNC_NAMES = {
    "Annual return": [ep.annual_return, ".1%"],
    "Cumulative returns": [ep.cum_returns_final, ".1%"],
    "Annual volatility": [ep.annual_volatility, ".1%"],
    "Sharpe ratio": [ep.sharpe_ratio, ".2f"],
    "Calmar ratio": [ep.calmar_ratio, ".2f"],
    "Stability": [ep.stability_of_timeseries, ".2f"],
    "Max drawdown": [ep.max_drawdown, ".2f"],
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
    # returns,
    # factor_returns=None,
    # positions=None,
    # transactions=None,
    # turnover_denom="AGB",
) -> pd.Series:
    """
    Calculates various performance metrics of a strategy, for use in
    plotting.show_perf_stats.

    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    factor_returns : pd.Series, optional
        Daily noncumulative returns of the benchmark factor to which betas are
        computed. Usually a benchmark such as market returns.
         - This is in the same style as returns.
         - If None, do not compute alpha, beta, and information ratio.
    positions : pd.DataFrame
        Daily net position values.
         - See full explanation in tears.create_full_tear_sheet.
    transactions : pd.DataFrame
        Prices and amounts of executed trades. One row per trade.
        - See full explanation in tears.create_full_tear_sheet.
    turnover_denom : str
        Either AGB or portfolio_value, default AGB.
        - See full explanation in txn.get_turnover.

    Returns
    -------
    pd.Series
        Performance metrics.
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
