import uuid
from typing import Optional
from websocket_service.infra.redis_client import RedisClient


# redis에 세션 등록/조회/관리 책임
class SessionService:
    def __init__(self, redis_client: RedisClient):
        self.redis = redis_client

    async def create_session(self, user_id: str, session_id: str):
        await self.redis.set(f"session:{session_id}", {"user_id": user_id})

    async def get_user(self, session_id: str) -> Optional[str]:
        data = await self.redis.get(f"session:{session_id}")
        return data.get("user_id") if data else None

    async def remove_session(self, session_id: str):
        await self.redis.delete(f"session:{session_id}")
