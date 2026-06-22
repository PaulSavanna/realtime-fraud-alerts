import time
from unittest.mock import patch, AsyncMock

import pytest
from backend.generator import transactions


@pytest.fixture(autouse=True)
def reset_transactions():
    transactions.clear()
    yield
    transactions.clear()


def _make_fake_tx(id=1, user_id=1, amount=100.0):
    return {
        "id": id,
        "user_id": user_id,
        "amount": amount,
        "timestamp": time.time(),
        "status": "normal",
    }


class TestTransactionFormat:
    def test_has_required_fields(self):
        tx = _make_fake_tx()
        for field in ("id", "user_id", "amount", "timestamp", "status"):
            assert field in tx

    def test_id_is_int(self):
        assert isinstance(_make_fake_tx(id=42)["id"], int)

    def test_amount_is_float(self):
        assert isinstance(_make_fake_tx(amount=99.99)["amount"], float)

    def test_timestamp_is_numeric(self):
        assert isinstance(_make_fake_tx()["timestamp"], (int, float))

    def test_status_is_valid(self):
        for status in ("normal", "suspicious"):
            tx = _make_fake_tx()
            tx["status"] = status
            assert tx["status"] in ("normal", "suspicious")
