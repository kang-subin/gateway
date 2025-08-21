
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict
import uuid

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        # {세션ID(UUID): WebSocket 객체}
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket) -> str:
        """클라이언트 연결 수락 + 세션ID 발급"""
        await websocket.accept()
        session_id = str(uuid.uuid4())   # 세션을 구분할 고유 UUID
        self.active_connections[session_id] = websocket
        return session_id

    def disconnect(self, session_id: str):
        """클라이언트 연결 해제"""
        if session_id in self.active_connections:
            del self.active_connections[session_id]

    async def send_to_one(self, session_id: str, message: str):
        """특정 세션(클라이언트)에게만 메시지 전송"""
        if session_id in self.active_connections:
            websocket = self.active_connections[session_id]
            await websocket.send_text(message)

    async def broadcast(self, message: str):
        """모든 세션(클라이언트)에게 메시지 브로드캐스트"""
        for connection in self.active_connections.values():
            await connection.send_text(message)


# 매니저 객체 생성
manager = ConnectionManager()


# =====================
# 웹소켓 엔드포인트
# =====================
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # 클라이언트 연결 수락 + 세션 ID 발급
    session_id = await manager.connect(websocket)
    try:
        while True:
            # 클라이언트 → 서버로부터 텍스트 메시지 수신
            data = await websocket.receive_text()

            # 1) 자기 자신에게 echo
            await
