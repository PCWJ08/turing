from fastapi import WebSocket

class ConnectionManager:
    """负责管理WebSocket连接，并给新进来的人分发序号"""
    def __init__(self):
        self.active_connections = []
        self.user_count = 0  # 🌟 计数器

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.user_count += 1
        return self.user_count  # 返回这是第几个连进来的人

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for conn in list(self.active_connections):
            try:
                await conn.send_text(message)
            except Exception:
                self.disconnect(conn)

manager = ConnectionManager()