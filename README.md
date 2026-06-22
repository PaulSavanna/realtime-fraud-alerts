# Realtime Fraud Alerts

Real-time dashboard for monitoring suspicious transactions using WebSocket push-based architecture.

## Problem

Fraud detection systems need immediate alerting — every second counts. Traditional polling adds latency and wastes bandwidth. This project demonstrates a push-based approach where suspicious transactions are detected and delivered to the dashboard in real-time.

## Key Features

- **Real-time transaction streaming** via WebSocket (sub-second delivery)
- **Rule-based fraud detection** — amount threshold + frequency analysis
- **Batched UI updates** — 300ms batching prevents render lag under high load
- **Auto-reconnect** with exponential backoff on connection drops
- **Live transaction chart** — transactions/min and suspicious/min over time

## Tech Stack

- **Backend:** Python 3.11, FastAPI, Uvicorn, WebSockets
- **Frontend:** Vanilla HTML/JS, Chart.js
- **Containerization:** Docker, Docker Compose

## Architecture

```
┌──────────────┐    WebSocket     ┌──────────────┐
│   Frontend   │◄────────────────│   Backend    │
│  (Browser)   │   push events   │  (FastAPI)   │
└──────────────┘                  └──────┬───────┘
                                         │
                                    ┌────▼────┐
                                    │ Generator│
                                    │ (async)  │
                                    └────┬────┘
                                         │
                                    ┌────▼────┐
                                    │  Rules  │
                                    │  Engine │
                                    └─────────┘

Flow: Generator creates transactions → Rules check each one →
      WebSocket broadcasts to all connected clients →
      Frontend batches and renders
```

## Quick Start

```bash
# With Docker
docker-compose up

# Without Docker
pip install -r requirements.txt
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

Open http://localhost:8000

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/transactions` | GET | Last 50 transactions (JSON) |
| `/ws` | WebSocket | Real-time transaction stream |

### Example: GET /transactions

```json
{
  "transactions": [
    {
      "id": 42,
      "user_id": 7,
      "amount": 1250.50,
      "timestamp": 1719062400.0,
      "status": "suspicious"
    }
  ]
}
```

### WebSocket Protocol

Connect to `ws://localhost:8000/ws`. Server pushes JSON objects:

```json
{"id": 43, "user_id": 12, "amount": 45.20, "timestamp": 1719062401.0, "status": "normal"}
```

## Detection Rules

1. **Amount rule:** Transaction amount > $1,000 → suspicious
2. **Frequency rule:** More than 5 transactions from the same user within 60 seconds → suspicious
3. **Combined:** Either rule triggers → transaction flagged

## Running Tests

```bash
pip install -r requirements-dev.txt
pytest -v
```

## CI

GitHub Actions runs on every push/PR:
- Install dependencies
- Run pytest suite
- Build Docker image and verify container starts

## Known Limitations

- Simple threshold-based rules produce false positives
- No persistent storage — history lost on restart
- Single instance only — no horizontal scaling
- No authentication or rate limiting

## License

MIT — see [LICENSE](LICENSE)
