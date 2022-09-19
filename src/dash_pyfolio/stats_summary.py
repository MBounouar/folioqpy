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
    """Fetches rows from a Smalltable.

    Retrieves rows pertaining to the given keys from the Table instance
    represented by table_handle.  String keys will be UTF-8 encoded.

    Args:
      table_handle:
        An open `smalltable.Table` instance.
      keys:
        A sequence of strings representing the key of each table row to
        fetch.  String keys will be UTF-8 encoded.
      require_all_keys:
        If True only rows with values set for all keys will be returned.

    Returns:
      A dict mapping keys to the corresponding table row data
      fetched. Each row is represented as a tuple of strings. For
      example:

      {b'Serak': ('Rigel VII', 'Preparer'),
       b'Zim': ('Irk', 'Invader'),
       b'Lrrr': ('Omicron Persei 8', 'Emperor')}

      Returned keys are always bytes.  If a key from the keys argument is
      missing from the dictionary, then that row was not found in the
      table (and require_all_keys must have been False).

    Raises:
      IOError: An error occurred accessing the smalltable.
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
