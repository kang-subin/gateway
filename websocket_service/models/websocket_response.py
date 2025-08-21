from pydantic import BaseModel
from typing import Any, Dict

class WebSocketResponse(BaseModel):
    event: str
    sessionId: str
    data: Dict[str, Any]
