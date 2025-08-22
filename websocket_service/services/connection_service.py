from typing import Dict, Optional

from fastapi import WebSocket


# 웹소켓 등록/조회/삭제 책임
class ConnectionService:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, session_id: str, websocket: WebSocket) -> str:
        await websocket.accept()
        self.active_connections[session_id] = websocket
        return session_id

    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]

    def get(self, session_id: str) -> Optional[WebSocket]:
        return self.active_connections.get(session_id)

    def all(self) -> Dict[str, WebSocket]:
        return self.active_connections

    def all_ids(self) -> list[str]:
        return list(self.active_connections.keys())
