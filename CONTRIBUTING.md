# Contributing

## Setup

**With Docker (recommended):**
```bash
git clone https://github.com/PaulSavanna/realtime-fraud-alerts
cd realtime-fraud-alerts
docker-compose up
```

Open http://localhost:8000

**Without Docker:**
```bash
pip install -r requirements.txt
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

## Running Tests

```bash
pip install -r requirements-dev.txt
pytest -v
```

## Code Style

This project uses [Ruff](https://docs.astral.sh/ruff/):

```bash
ruff check .
ruff format .
```

## Submitting Changes

1. Fork the repository
2. Create a branch: `git checkout -b feature/my-change`
3. Run `pytest -v` to make sure tests pass
4. Open a Pull Request with a clear description of the change
