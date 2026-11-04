
import pytest
import coupon_validator
from coupon_validator import coupon_discount, best_discount, is_expired


# 1. WELCOME10 coupon tests
def test_welcome10_new_user():
    assert coupon_discount("WELCOME10", 200, True, "mon") == 20


def test_welcome10_existing_user():
    assert coupon_discount("WELCOME10", 200, False, "mon") == 0


# 2. WEEKEND20 coupon tests
def test_weekend20_high_cart():
    assert coupon_discount("WEEKEND20", 600, True, "sat") == 120


def test_weekend20_low_cart():
    assert coupon_discount("WEEKEND20", 300, True, "sun") == 50


def test_weekend20_weekday():
    assert coupon_discount("WEEKEND20", 600, True, "mon") == 0


# 3. FLAT100 coupon tests
def test_flat100_eligible():
    assert coupon_discount("FLAT100", 500, False, "mon") == 100


def test_flat100_not_eligible():
    assert coupon_discount("FLAT100", 300, False, "mon") == 0


# 4. Invalid/unknown coupon test
def test_unknown_coupon():
    assert coupon_discount("INVALID", 200, True, "mon") == 0


# 5. Best discount tests
def test_best_discount_selects_highest():
    result = best_discount(
        ["FLAT100", "WELCOME10"], 400, True, "mon"
    )
    assert result == 100


def test_best_discount_empty_list():
    assert best_discount([], 200, True, "mon") == 0


def test_best_discount_applies_cap(monkeypatch):
    monkeypatch.setattr(
        coupon_validator,
        "coupon_discount",
        lambda *args: 100
    )

    result = best_discount(["TEST"], 100, True, "mon")
    assert result == 40


# 6. Coupon expiration tests
def test_expired_zero_validity():
    assert is_expired(10, 5, 0) is True


def test_expired_negative_validity():
    assert is_expired(10, 5, -2) is True


def test_coupon_not_expired():
    assert is_expired(12, 10, 5) is False


def test_coupon_expired():
    assert is_expired(20, 10, 5) is True
