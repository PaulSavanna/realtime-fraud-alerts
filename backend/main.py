import asyncio
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from backend.generator import transactions, generate_and_broadcast
from backend.ws import manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = None
    if not os.environ.get("TESTING"):
        task = asyncio.create_task(generate_and_broadcast())
    yield
    if task:
        task.cancel()


app = FastAPI(lifespan=lifespan)

@app.get("/transactions")
def get_transactions():
    return {"transactions": transactions[-50:]}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

frontend_dir = Path(__file__).parent.parent / "frontend"
app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")
