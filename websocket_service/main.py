from fastapi import FastAPI
from websocket_service.controller import websocket_controller

app = FastAPI()

app.include_router(websocket_controller.router)
