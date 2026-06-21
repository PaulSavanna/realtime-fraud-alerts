from collections import defaultdict
import time

AMOUNT_THRESHOLD = 1000

def check_amount(tx: dict) -> bool:
    """Правило: сумма выше порога"""
    return tx["amount"] > AMOUNT_THRESHOLD

user_transactions = defaultdict(list)
FREQUENCY_THRESHOLD = 5
FREQUENCY_WINDOW = 60

def check_frequency(tx: dict) -> bool:
    """Правило: много транзакций от одного пользователя за короткое время"""
    user_id = tx["user_id"]
    now = time.time()
    user_transactions[user_id].append(now)
    user_transactions[user_id] = [
        t for t in user_transactions[user_id]
        if now - t < FREQUENCY_WINDOW
    ]
    return len(user_transactions[user_id]) > FREQUENCY_THRESHOLD
