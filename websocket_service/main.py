from fastapi import FastAPI
from websocket_service.controllers import websocket_controller

app = FastAPI()

app.include_router(websocket_controller.router)
