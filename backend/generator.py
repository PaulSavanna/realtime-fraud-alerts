import random
import time
from threading import Thread

transactions = []

def generate_batch(count=10):
    """Генерация пачки транзакций"""
    for _ in range(count):
        tx = {
            "id": len(transactions) + 1,
            "user_id": random.randint(1, 100),
            "amount": round(random.expovariate(1/100), 2),
            "timestamp": time.time(),
            "status": "normal"
        }
        transactions.append(tx)
    return transactions

def start_generator(interval=2):
    """Запуск генератора в фоне"""
    def _run():
        while True:
            generate_batch(random.randint(1, 3))
            time.sleep(interval)
    Thread(target=_run, daemon=True).start()