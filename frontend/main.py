from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request

from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.templating import Jinja2Templates

BASE_PATH = Path(__file__).resolve().parent


app = FastAPI(title="Dashboard",)
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))
app.mount("/static", StaticFiles(directory="static"), name="static")


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.get("/", status_code=200)
async def get(request: Request):

    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, },
    )


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
