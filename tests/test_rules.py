import time
from unittest.mock import patch

import pytest
from backend.rules import (
    AMOUNT_THRESHOLD,
    FREQUENCY_THRESHOLD,
    FREQUENCY_WINDOW,
    check_amount,
    check_frequency,
    check_suspicious,
    user_transactions,
)


@pytest.fixture(autouse=True)
def reset_frequency_state():
    user_transactions.clear()
    yield
    user_transactions.clear()


class TestCheckAmount:
    def test_below_threshold(self):
        assert check_amount({"amount": 500}) is False

    def test_above_threshold(self):
        assert check_amount({"amount": 1500}) is True

    def test_exact_threshold(self):
        assert check_amount({"amount": AMOUNT_THRESHOLD}) is False

    def test_just_above_threshold(self):
        assert check_amount({"amount": AMOUNT_THRESHOLD + 0.01}) is True

    def test_zero_amount(self):
        assert check_amount({"amount": 0}) is False

    def test_negative_amount(self):
        assert check_amount({"amount": -100}) is False

    def test_very_large_amount(self):
        assert check_amount({"amount": 999999.99}) is True


class TestCheckFrequency:
    def test_single_transaction_not_suspicious(self):
        tx = {"user_id": 1, "amount": 50}
        assert check_frequency(tx) is False

    def test_beyond_frequency_threshold(self):
        tx = {"user_id": 1, "amount": 50}
        for _ in range(FREQUENCY_THRESHOLD + 1):
            check_frequency(tx)
        assert check_frequency(tx) is True

    def test_exactly_at_frequency_threshold(self):
        tx = {"user_id": 999, "amount": 50}
        for _ in range(FREQUENCY_THRESHOLD):
            assert check_frequency(tx) is False

    def test_old_transactions_outside_window_are_purged(self):
        tx = {"user_id": 1, "amount": 50}
        for _ in range(FREQUENCY_THRESHOLD + 1):
            check_frequency(tx)

        with patch("backend.rules.time") as mock_time:
            mock_time.time.return_value = time.time() + FREQUENCY_WINDOW + 1
            result = check_frequency(tx)

        assert result is False

    def test_separate_users_are_independent(self):
        tx1 = {"user_id": 1, "amount": 50}
        tx2 = {"user_id": 2, "amount": 50}

        for _ in range(FREQUENCY_THRESHOLD + 1):
            check_frequency(tx1)

        assert check_frequency(tx1) is True
        assert check_frequency(tx2) is False


class TestCheckSuspicious:
    def test_suspicious_by_amount(self):
        tx = {"amount": 1500, "user_id": 1}
        assert check_suspicious(tx) is True

    def test_suspicious_by_frequency(self):
        tx = {"amount": 50, "user_id": 1}
        for _ in range(FREQUENCY_THRESHOLD + 1):
            check_suspicious(tx)
        assert check_suspicious(tx) is True

    def test_normal_transaction(self):
        tx = {"amount": 50, "user_id": 1}
        assert check_suspicious(tx) is False

    def test_boundary_amount_is_normal(self):
        tx = {"amount": AMOUNT_THRESHOLD, "user_id": 1}
        assert check_suspicious(tx) is False
