from enum import IntEnum

APPROX_BDAYS_PER_MONTH = 21
APPROX_BDAYS_PER_YEAR = 252
MONTHS_PER_YEAR = 12
WEEKS_PER_YEAR = 52
QTRS_PER_YEAR = 4


class AnnualizationFactor(IntEnum):  # pragma: no cover
    DAILY = APPROX_BDAYS_PER_YEAR
    WEEKLY = WEEKS_PER_YEAR
    MONTHLY = MONTHS_PER_YEAR
    QUARTERLY = QTRS_PER_YEAR
    YEARLY = 1

    def __str__(self):
        return f"{self.name.lower()}"

    @classmethod
    def from_period(cls, period):
        if isinstance(period, str):
            if period not in cls.periods():
                raise ValueError(
                    f"Invalid Period: {period}. "
                    "Can only be '{}'.".format("', '".join(cls.periods()))
                )
            return getattr(cls, period.upper())

        elif isinstance(period, int):
            return period

        else:
            raise ValueError(
                f"Invalid Period: {period}. "
                "Can only be '{}'. Or integer".format("', '".join(cls.periods()))
            )

    @classmethod
    def periods(cls):
        return [x.name.lower() for x in cls]


DAILY = AnnualizationFactor.DAILY
WEEKLY = AnnualizationFactor.WEEKLY
MONTHLY = AnnualizationFactor.MONTHLY
QUARTERLY = AnnualizationFactor.QUARTERLY
YEARLY = AnnualizationFactor.YEARLY
