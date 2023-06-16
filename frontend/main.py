"""FastAPI server """
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_PATH = Path(__file__).resolve().parent

app = FastAPI(title="Dashboard", )
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))
app.mount("/static", StaticFiles(directory="static"), name="static")


class ConnectionManager:
    """
    Manages WebSocket connections and broadcast messages to connected clients.

    Attributes:
        active_connections (list[WebSocket]): A list of currently active WebSocket connections.

    Methods:
        __init__(): Initializes the ConnectionManager object.
        connect(websocket: WebSocket): Connects a new WebSocket client.
        disconnect(websocket: WebSocket): Disconnects a WebSocket client.
        send_personal_message(message: str, websocket: WebSocket): Sends a personal message to a specific WebSocket client.
        broadcast(message: str): Broadcasts a message to all connected WebSocket clients.
    """

    def __init__(self):
        """
           Initializes the ConnectionManager object.
           The active_connections attribute is initialized as an empty list.
       """
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """
        Connects a new WebSocket client.

        Args:
            websocket (WebSocket): The WebSocket connection to be added.

        Usage:
            connection_manager = ConnectionManager()
            await connection_manager.connect(websocket)
        """
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """
        Disconnects a WebSocket client.

        Args:
            websocket (WebSocket): The WebSocket connection to be removed.

        Usage:
            connection_manager = ConnectionManager()
            connection_manager.disconnect(websocket)
        """
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """
        Sends a personal message to a specific WebSocket client.

        Args:
            message (str): The message to be sent.
            websocket (WebSocket): The WebSocket connection to receive the message.

        Usage:
            connection_manager = ConnectionManager()
            await connection_manager.send_personal_message("Hello!", websocket)
        """
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        """
        Broadcasts a message to all connected WebSocket clients.

        Args:
            message (str): The message to be broadcasted.

        Usage:
            connection_manager = ConnectionManager()
            await connection_manager.broadcast("Important announcement!")
        """
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
