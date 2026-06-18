"""Скрипт для демонстрации батчинга и реконнекта под нагрузкой"""
import asyncio
import websockets
import json
import random

async def stress_test():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as ws:
        print("Connected. Sending 100 rapid events...")
        for i in range(100):
            tx = {
                "id": i,
                "user_id": random.randint(1, 10),
                "amount": random.uniform(1, 5000),
                "status": "normal"
            }
            await ws.send(json.dumps(tx))
            await asyncio.sleep(0.01)
        print("Done. Check dashboard for updates.")

if __name__ == "__main__":
    asyncio.run(stress_test())
