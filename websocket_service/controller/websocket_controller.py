from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from websocket_service.services.connection_manager import ConnectionManager

router = APIRouter()
manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    session_id = await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()

            await manager.send_to_one(session_id, f"나({session_id})가 보낸 메시지: {data}")

            await manager.broadcast(f"[{session_id}] {data}")

    except WebSocketDisconnect:
        manager.disconnect(session_id)
