"""Consistent decimal rounding for manuscript rates and intervals."""

from decimal import Decimal, ROUND_HALF_UP


def decimal_text(value, places=4):
    rounded = Decimal(str(value)).quantize(
        Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP
    )
    if rounded.is_zero():
        rounded = abs(rounded)
    return f"{rounded:.{places}f}"


def rate_interval_text(row):
    return (f"{decimal_text(row['rejection_rate'])} "
            f"[{decimal_text(row['rejection_low'])}, "
            f"{decimal_text(row['rejection_high'])}]")
