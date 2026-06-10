AMOUNT_THRESHOLD = 1000

def check_amount(tx: dict) -> bool:
    """Правило: сумма выше порога"""
    return tx["amount"] > AMOUNT_THRESHOLD
