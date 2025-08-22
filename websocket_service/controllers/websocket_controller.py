from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from websocket_service.services.connection_service import ConnectionService
from websocket_service.models.websocket_response import WebSocketResponse

router = APIRouter()
connection_service = ConnectionService()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    session_id = await connection_service.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()

            response = WebSocketResponse(
                event=data.get("event", "message"),
                sessionId=session_id,
                data=data
            )
    # 연결해제
    except WebSocketDisconnect:
        connection_service.disconnect(session_id)
