from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from backend.generator import transactions, start_generator

app = FastAPI()

@app.on_event("startup")
def startup():
    start_generator()

@app.get("/transactions")
def get_transactions():
    return {"transactions": transactions[-50:]}

frontend_dir = Path(__file__).parent.parent / "frontend"
app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")
