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
    print("🚀 启动群聊永动机...")
    asyncio.create_task(game_ai.auto_chat_loop())

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    # 🌟 1. 连接建立，获取当前是第几个进来的
    seq = await manager.connect(websocket)
    
    # 🌟 2. 分配名字
    if seq == 1:
        assigned_name = "圆周率"
    else:
        assigned_name = f"圆周率_{seq}"
        
    # 🌟 3. 把名字偷偷发给这个特定的前端
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
                
                # 只要是圆周率开头（包含圆周率_2等），都算真人
                is_human = sender.startswith("圆周率")
                await game_ai.process_message(sender, content, is_human)
                    
    except WebSocketDisconnect:
        manager.disconnect(websocket)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/")
async def index():
    return FileResponse(str(STATIC_DIR / "index.html"))