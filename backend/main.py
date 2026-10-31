import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

import config
import game_ai
from ws_manager import manager

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR.parent / "static"

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(game_ai.auto_chat_loop())

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    seq = await manager.connect(websocket)
    assigned_name = "圆周率" if seq == 1 else f"圆周率_{seq}"
    
    try:
        await websocket.send_text(f"SYSTEM_INIT::{assigned_name}")
    except Exception:
        pass
        
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
            if "::" in data:
                parts = data.split("::")
                sender = parts[0]
                content = parts[1]
                print(f"[用户日志] {sender}: {content}",flush=True)
                is_human = sender.startswith("圆周率")
                await game_ai.process_message(sender, content, is_human)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/")
async def index():
    return FileResponse(str(STATIC_DIR / "index.html"))
