import pytest
from backend.rules import check_amount, check_frequency, check_suspicious


def test_check_amount_normal():
    assert check_amount({"amount": 500}) == False


def test_check_amount_suspicious():
    assert check_amount({"amount": 1500}) == True


def test_check_suspicious():
    tx = {"amount": 1500, "user_id": 1}
    assert check_suspicious(tx) == True


def test_check_suspicious_normal():
    tx = {"amount": 50, "user_id": 1}
    assert check_suspicious(tx) == False
