from typing import Optional
from fastapi import WebSocket
import uuid

from websocket_service.services.session_service import SessionService
from websocket_service.services.connection_service import ConnectionService
from websocket_service.services.broadcast_service import BroadcastService

class Manager:
    def __init__(self,
                 session_service: SessionService,
                 connection_service: ConnectionService,
                 broadcast_service: BroadcastService):
        self.session_service = session_service
        self.connection_service = connection_service
        self.broadcast_service = broadcast_service
    # -----------------------------
    # 연결 / 세션 관리
    # -----------------------------
    async def connect_user(self, websocket: WebSocket, user_id: str) -> str:
        session_id = str(uuid.uuid4())   # Manager가 UUID 발급
        await self.session_service.create_session(user_id, session_id)  # Redis 저장
        await self.connection_service.connect(session_id, websocket)   # 로컬 저장
        return session_id

    async def disconnect_user(self, session_id: str):
        await self.session_service.remove_session(session_id)   # 1) Redis 삭제
        self.connection_service.disconnect(session_id)          # 2) 로컬 삭제

    # -----------------------------
    # 조회 기능
    # -----------------------------
    async def get_user(self, session_id: str) -> Optional[str]:
        return await self.session_service.get_user(session_id) # 레디스 조회

    def get_connection(self, session_id: str) -> Optional[WebSocket]:
        return self.connection_service.get(session_id) # 웹소켓 객체 조희

    # -----------------------------
    # 메시징 기능
    # -----------------------------
    async def send_to_user(self, session_id: str, message: str):
        conn = self.get_connection(session_id)
        if conn:
            await self.broadcast_service.send(conn, message)

    async def broadcast_to_all(self, message: str):
        connections = self.connection_service.all()
        await self.broadcast_service.broadcast(connections, message)

    # -----------------------------
    # 보정 (Recovery) 기능
    # -----------------------------
