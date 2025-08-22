from typing import Dict
from fastapi import WebSocket


class BroadcastService:
    async def broadcast(self, connections: Dict[str, WebSocket], message: str):
        disconnected = []
        for sid, conn in connections.items():
            try:
                await conn.send_text(message)
            except Exception:
                disconnected.append(sid)

        return disconnected

    async def send(self, conn: WebSocket, message: str):
        try:
            await conn.send_text(message)
        except Exception:
            return False
        return True
