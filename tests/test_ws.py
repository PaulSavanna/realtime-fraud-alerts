import os
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.generator import transactions


os.environ["TESTING"] = "1"


@pytest.fixture
def client():
    transactions.clear()
    with TestClient(app) as c:
        yield c
    transactions.clear()


class TestTransactionsEndpoint:
    def test_returns_200(self, client):
        response = client.get("/transactions")
        assert response.status_code == 200

    def test_returns_transactions_key(self, client):
        data = client.get("/transactions").json()
        assert "transactions" in data

    def test_transactions_is_list(self, client):
        data = client.get("/transactions").json()
        assert isinstance(data["transactions"], list)

    def test_limit_to_50(self, client):
        data = client.get("/transactions").json()
        assert len(data["transactions"]) <= 50

    def test_empty_transactions_initially(self, client):
        data = client.get("/transactions").json()
        assert len(data["transactions"]) == 0


class TestWebSocketEndpoint:
    def test_ws_connects(self, client):
        with client.websocket_connect("/ws") as ws:
            assert ws is not None

    def test_ws_gets_initial_history(self, client):
        transactions.append({
            "id": 1, "user_id": 1, "amount": 100.0,
            "timestamp": 1000.0, "status": "normal"
        })
        with client.websocket_connect("/ws") as ws:
            tx = ws.receive_json()
            assert tx["id"] == 1
            assert tx["amount"] == 100.0

    def test_ws_gets_suspicious_transaction(self, client):
        transactions.append({
            "id": 2, "user_id": 2, "amount": 5000.0,
            "timestamp": 1000.0, "status": "suspicious"
        })
        with client.websocket_connect("/ws") as ws:
            tx = ws.receive_json()
            assert tx["status"] == "suspicious"

    def test_ws_transaction_types(self, client):
        transactions.append({
            "id": 3, "user_id": 3, "amount": 50.0,
            "timestamp": 1000.0, "status": "normal"
        })
        with client.websocket_connect("/ws") as ws:
            tx = ws.receive_json()
            assert isinstance(tx["id"], int)
            assert isinstance(tx["user_id"], int)
            assert isinstance(tx["amount"], (int, float))
            assert isinstance(tx["timestamp"], (int, float))

    def test_ws_gets_multiple_history_items(self, client):
        for i in range(5):
            transactions.append({
                "id": i, "user_id": i, "amount": float(i * 100),
                "timestamp": 1000.0 + i, "status": "normal"
            })
        with client.websocket_connect("/ws") as ws:
            received = []
            for _ in range(5):
                received.append(ws.receive_json())
            assert len(received) == 5
