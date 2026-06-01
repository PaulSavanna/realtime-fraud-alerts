# Realtime Fraud Alerts

Dashboard для мониторинга подозрительных транзакций в реальном времени.

## Статус
Работает через polling (фронт опрашивает сервер каждые 2 секунды).
TODO: polling is wasteful and has delay, need to switch to push-based updates.

## Запуск
```bash
uvicorn backend.main:app --reload
```
Открой http://localhost:8000