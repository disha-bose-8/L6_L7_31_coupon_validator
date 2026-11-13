
from datetime import date
from hypothesis import given, strategies as st
from coupon_validator import split_code, most_expensive, expiry_days


# Fuzz tests: functions should handle unexpected inputs without crashing

@given(st.one_of(st.text(), st.none()))
def test_split_code_no_crash(s):
    split_code(s)


@given(st.one_of(st.text(), st.none()))
def test_most_expensive_no_crash(s):
    most_expensive(s)


@given(st.one_of(st.text(), st.none()))
def test_expiry_days_no_crash(s):
    expiry_days(s)


# Property tests: verify correct results for valid inputs

@given(
    prefix=st.text(
        alphabet=st.characters(whitelist_categories=("Lu", "Ll")),
        min_size=1,
        max_size=10
    ),
    value=st.integers(min_value=0, max_value=999999)
)
def test_split_code_valid(prefix, value):
    result = split_code(f"{prefix}-{value}")
    assert result == (prefix.upper(), value)


@given(
    prices=st.lists(
        st.floats(
            min_value=0,
            max_value=1000000,
            allow_nan=False,
            allow_infinity=False
        ),
        min_size=1,
        max_size=20
    )
)
def test_most_expensive_valid(prices):
    csv_input = ",".join(str(p) for p in prices)
    assert most_expensive(csv_input) == max(prices)


@given(target_date=st.dates(
    min_value=date(1900, 1, 1),
    max_value=date(2100, 12, 31)
))
def test_expiry_days_valid(target_date):
    result = expiry_days(target_date.isoformat())
    expected = (target_date - date.today()).days
    assert result == expected
