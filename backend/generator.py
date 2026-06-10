import random
import time
import asyncio

from .rules import check_amount

transactions = []

async def generate_and_broadcast():
    """Генерация и рассылка через WebSocket"""
    from .ws import manager
    while True:
        count = random.randint(1, 3)
        for _ in range(count):
            tx = {
                "id": len(transactions) + 1,
                "user_id": random.randint(1, 100),
                "amount": round(random.expovariate(1/100), 2),
                "timestamp": time.time(),
                "status": "normal"
            }
            if check_amount(tx):
                tx["status"] = "suspicious"
            transactions.append(tx)
            await manager.broadcast(tx)
        await asyncio.sleep(random.uniform(1, 5))
