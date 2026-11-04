
import pytest
import coupon_validator
from coupon_validator import coupon_discount, best_discount, is_expired


# 1. Invalid cart condition
def test_invalid_cart_zero():
    with pytest.raises(ValueError):
        coupon_discount("WELCOME10", 0, True, "mon")


def test_invalid_cart_negative():
    with pytest.raises(ValueError):
        coupon_discount("WELCOME10", -100, True, "mon")


# 2. WELCOME10 branches
def test_welcome10_true_branch():
    assert coupon_discount("WELCOME10", 200, True, "mon") == 20


def test_welcome10_false_branch():
    assert coupon_discount("WELCOME10", 200, False, "mon") == 0


# 3. WEEKEND20 branches
def test_weekend20_saturday_high_cart():
    assert coupon_discount("WEEKEND20", 600, True, "sat") == 120


def test_weekend20_sunday_low_cart():
    assert coupon_discount("WEEKEND20", 300, True, "sun") == 50


def test_weekend20_weekday():
    assert coupon_discount("WEEKEND20", 600, True, "mon") == 0


def test_weekend20_cart_exactly_500():
    assert coupon_discount("WEEKEND20", 500, True, "sat") == 100


# 4. FLAT100 branches
def test_flat100_above_300():
    assert coupon_discount("FLAT100", 500, False, "mon") == 100


def test_flat100_exactly_300():
    assert coupon_discount("FLAT100", 300, False, "mon") == 0


# 5. Unknown coupon branch
def test_unknown_coupon():
    assert coupon_discount("INVALID", 500, True, "sat") == 0


# 6. best_discount loop and comparison branches
def test_best_discount_empty_codes():
    assert best_discount([], 500, True, "mon") == 0


def test_best_discount_updates_best():
    assert best_discount(
        ["WELCOME10", "FLAT100"], 500, True, "mon"
    ) == 100


def test_best_discount_does_not_update_best():
    assert best_discount(
        ["FLAT100", "WELCOME10"], 500, True, "mon"
    ) == 100


# 7. best_discount cap branches
def test_best_discount_cap_applied(monkeypatch):
    monkeypatch.setattr(
        coupon_validator,
        "coupon_discount",
        lambda *args: 100
    )

    assert best_discount(["TEST"], 100, True, "mon") == 40


def test_best_discount_cap_not_applied():
    assert best_discount(
        ["WELCOME10"], 500, True, "mon"
    ) == 50


# 8. Expiration branches
def test_expiration_nonpositive_validity():
    assert is_expired(10, 5, 0) is True


def test_expiration_negative_validity():
    assert is_expired(10, 5, -1) is True


def test_expiration_still_valid():
    assert is_expired(12, 10, 5) is False


def test_expiration_exact_boundary():
    assert is_expired(15, 10, 5) is False


def test_expiration_past_boundary():
    assert is_expired(16, 10, 5) is True
