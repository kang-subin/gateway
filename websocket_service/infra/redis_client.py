import aioredis
import json
from typing import Any


class RedisClient:
    def __init__(self, url: str = "redis://localhost:6379/0", namespace: str = "app", default_ttl: int = 3600):
        self.url = url
        self.namespace = namespace
        self.ttl = default_ttl
        self.redis: aioredis.Redis | None = None

    async def connect(self):
        self.redis = await aioredis.from_url(
            self.url,
            decode_responses=True
        )
        print("[Redis] Connected")

    async def disconnect(self):
        if self.redis:
            await self.redis.close()
            print("[Redis] Disconnected")

    def _key(self, key: str) -> str:
        return f"{self.namespace}:{key}"

    async def set(self, key: str, value: Any, expire: int = None):
        if not self.redis:
            raise RuntimeError("Redis is not connected")
        data = json.dumps(value, ensure_ascii=False)
        await self.redis.set(self._key(key), data, ex=expire or self.ttl)

    async def get(self, key: str) -> Any:
        if not self.redis:
            raise RuntimeError("Redis is not connected")
        raw = await self.redis.get(self._key(key))
        return json.loads(raw) if raw else None

    async def delete(self, key: str):
        if not self.redis:
            raise RuntimeError("Redis is not connected")
        await self.redis.delete(self._key(key))

