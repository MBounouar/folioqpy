import numpy as np
import pandas as pd
import pytest

from dash_pyfolio.stats_summary import top_drawdown_table
from dash_pyfolio.portfolio_data import SimplePortfolio

DECIMAL_PLACES = 8


class TestDrawdown:
    def test_max_drawdown_begins_first_day(self):
        drawdown_list = np.array([100, 90, 75]) / 10.0
        dt = pd.date_range("2000-1-3", periods=3, freq="D")

        drawdown_df = pd.Series(drawdown_list, index=dt, name="PF").to_frame()
        rets = drawdown_df.pct_change()
        pf = SimplePortfolio(returns=rets)
        drawdowns = top_drawdown_table(pf, top=1)
        assert drawdowns.loc[0, "Net drawdown in %"] == 0.25

    @pytest.mark.parametrize(
        "first_expected_peak,first_expected_valley,first_expected_recovery,first_net_drawdown,second_expected_peak,second_expected_valley,second_expected_recovery,second_net_drawdown",
        [
            (
                pd.Timestamp("2000-01-08"),
                pd.Timestamp("2000-01-09"),
                pd.Timestamp("2000-01-13"),
                0.5,
                pd.Timestamp("2000-01-20"),
                pd.Timestamp("2000-01-22"),
                None,
                0.4,
            )
        ],
    )
    def test_drawdown_table_relative(
        self,
        first_expected_peak,
        first_expected_valley,
        first_expected_recovery,
        first_net_drawdown,
        second_expected_peak,
        second_expected_valley,
        second_expected_recovery,
        second_net_drawdown,
    ):

        drawdown_list = np.array(
            [
                100,
                110,
                120,
                150,
                180,
                200,
                100,
                120,
                160,
                180,
                200,
                300,
                400,
                500,
                600,
                800,
                900,
                1000,
                650,
                600,
            ]
        ) * (1 / 10.0)

        dt = pd.date_range("2000-1-3", periods=20, freq="D")

        drawdown_df = pd.Series(drawdown_list, index=dt, name="PF").to_frame()
        rets = drawdown_df.pct_change()
        pf = SimplePortfolio(returns=rets)
        drawdowns = top_drawdown_table(pf, top=2)

        assert drawdowns.loc[0, "Net drawdown in %"] == first_net_drawdown

        assert drawdowns.loc[0, "Peak date"] == first_expected_peak
        assert drawdowns.loc[0, "Valley date"] == first_expected_valley
        assert drawdowns.loc[0, "Recovery date"] == first_expected_recovery
        assert drawdowns.loc[1, "Net drawdown in %"] == second_net_drawdown
        assert drawdowns.loc[1, "Peak date"] == second_expected_peak
        assert drawdowns.loc[1, "Valley date"] == second_expected_valley
        assert pd.isnull(drawdowns.loc[1, "Recovery date"])

    # px_list_1 = np.array([100, 120, 100, 80, 70, 110, 180, 150]) / 100.0  # Simple
    # px_list_2 = (
    #     np.array([100, 120, 100, 80, 70, 80, 90, 90]) / 100.0
    # )  # Ends in drawdown
    # dt = pd.date_range("2000-1-3", periods=8, freq="D")

    # @parameterized.expand(
    #     [
    #         (
    #             pd.Series(px_list_1, index=dt),
    #             pd.Timestamp("2000-1-4"),
    #             pd.Timestamp("2000-1-7"),
    #             pd.Timestamp("2000-1-9"),
    #         ),
    #         (
    #             pd.Series(px_list_2, index=dt),
    #             pd.Timestamp("2000-1-4"),
    #             pd.Timestamp("2000-1-7"),
    #             None,
    #         ),
    #     ]
    # )
    # def test_get_max_drawdown(
    #     self, px, expected_peak, expected_valley, expected_recovery
    # ):
    #     rets = px.pct_change().iloc[1:]

    #     peak, valley, recovery = timeseries.get_max_drawdown(rets)
    #     # Need to use isnull because the result can be NaN, NaT, etc.
    #     self.assertTrue(pd.isnull(peak)) if expected_peak is None else self.assertEqual(
    #         peak, expected_peak
    #     )
    #     self.assertTrue(
    #         pd.isnull(valley)
    #     ) if expected_valley is None else self.assertEqual(valley, expected_valley)
    #     self.assertTrue(
    #         pd.isnull(recovery)
    #     ) if expected_recovery is None else self.assertEqual(
    #         recovery, expected_recovery
    #     )

    # @parameterized.expand(
    #     [
    #         (
    #             pd.Series(px_list_2, index=dt),
    #             pd.Timestamp("2000-1-4"),
    #             pd.Timestamp("2000-1-7"),
    #             None,
    #             None,
    #         ),
    #         (
    #             pd.Series(px_list_1, index=dt),
    #             pd.Timestamp("2000-1-4"),
    #             pd.Timestamp("2000-1-7"),
    #             pd.Timestamp("2000-1-9"),
    #             4,
    #         ),
    #     ]
    # )
    # def test_gen_drawdown_table(
    #     self,
    #     px,
    #     expected_peak,
    #     expected_valley,
    #     expected_recovery,
    #     expected_duration,
    # ):
    #     rets = px.pct_change().iloc[1:]

    #     drawdowns = timeseries.gen_drawdown_table(rets, top=1)
    #     self.assertTrue(
    #         pd.isnull(drawdowns.loc[0, "Peak date"])
    #     ) if expected_peak is None else self.assertEqual(
    #         drawdowns.loc[0, "Peak date"], expected_peak
    #     )
    #     self.assertTrue(
    #         pd.isnull(drawdowns.loc[0, "Valley date"])
    #     ) if expected_valley is None else self.assertEqual(
    #         drawdowns.loc[0, "Valley date"], expected_valley
    #     )
    #     self.assertTrue(
    #         pd.isnull(drawdowns.loc[0, "Recovery date"])
    #     ) if expected_recovery is None else self.assertEqual(
    #         drawdowns.loc[0, "Recovery date"], expected_recovery
    #     )
    #     self.assertTrue(
    #         pd.isnull(drawdowns.loc[0, "Duration"])
    #     ) if expected_duration is None else self.assertEqual(
    #         drawdowns.loc[0, "Duration"], expected_duration
    #     )

    # def test_drawdown_overlaps(self):
    #     rand = np.random.RandomState(1337)
    #     n_samples = 252 * 5
    #     spy_returns = pd.Series(
    #         rand.standard_t(3.1, n_samples),
    #         pd.date_range("2005-01-02", periods=n_samples),
    #     )
    #     spy_drawdowns = timeseries.gen_drawdown_table(spy_returns, top=20).sort_values(
    #         by="Peak date"
    #     )
    #     # Compare the recovery date of each drawdown with the peak of the next
    #     # Last pair might contain a NaT if drawdown didn't finish, so ignore it
    #     pairs = list(
    #         zip(
    #             spy_drawdowns["Recovery date"],
    #             spy_drawdowns["Peak date"].shift(-1),
    #         )
    #     )[:-1]
    #     self.assertGreater(len(pairs), 0)
    #     for recovery, peak in pairs:
    #         if not pd.isnull(recovery):
    #             self.assertLessEqual(recovery, peak)

    # @parameterized.expand(
    #     [
    #         (
    #             pd.Series(px_list_1, index=dt),
    #             1,
    #             [
    #                 (
    #                     pd.Timestamp("2000-01-03 00:00:00"),
    #                     pd.Timestamp("2000-01-03 00:00:00"),
    #                     pd.Timestamp("2000-01-03 00:00:00"),
    #                 )
    #             ],
    #         )
    #     ]
    # )
    # def test_top_drawdowns(self, returns, top, expected):
    #     self.assertEqual(timeseries.get_top_drawdowns(returns, top=top), expected)
