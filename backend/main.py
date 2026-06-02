from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import random
import time

app = FastAPI()

frontend_dir = Path(__file__).parent.parent / "frontend"
app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")

transactions = []

@app.get("/transactions")
def get_transactions():
    return {"transactions": transactions[-50:]}

@app.post("/generate")
def generate_transaction():
    tx = {
        "id": len(transactions) + 1,
        "user_id": random.randint(1, 100),
        "amount": round(random.uniform(1, 5000), 2),
        "timestamp": time.time(),
        "status": "normal"
    }
    transactions.append(tx)
    return tx
