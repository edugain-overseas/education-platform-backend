import random

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


@router.get("/generate_room_id")
async def generate_uuid():
    room_id = random.randint(100000, 999999)
    return {"room_id": room_id}


class RoomConnectionManager:
    def __init__(self):
        self.websocket_connections = []

    def initialize_room(self, room_id):
        for connection in self.websocket_connections:
            if room_id in connection:
                return

        room_data = {
            room_id: [],
            "room_connection": []
        }
        self.websocket_connections.append(room_data)

    def add_new_user(self, room_id: int, user_id: int, websocket: WebSocket):
        for connection in self.websocket_connections:
            if room_id in connection:
                connection[room_id].append(
                    {
                        "userId": user_id,
                        "websocket": websocket
                    }
                )
                connection["room_connection"].append(user_id)
                return

    def remove_user(self, room_id: int, websocket: WebSocket):
        for connection in self.websocket_connections:
            if room_id in connection:
                for user in connection[room_id]:
                    if user["websocket"] == websocket:
                        user_id = user["userId"]
                        connection[room_id].remove(user)
                        connection["room_connection"].remove(user_id)
                        return

    async def send_list_user(self, room_id: int, user_id: int):
        for connection in self.websocket_connections:
            if room_id in connection:
                connection_list = [conn_id for conn_id in connection["room_connection"] if conn_id != user_id]
                for user in connection[room_id]:
                    if user["userId"] == user_id:
                        await user["websocket"].send_json(
                            {
                                "eventType": "all users",
                                "data": connection_list
                            }
                        )

    async def send_offer(
            self,
            room_id: int,
            sender: int,
            recipient: int,
            signal: dict
    ):
        for connection in self.websocket_connections:
            if room_id in connection:
                for user in connection[room_id]:
                    if user["userId"] == recipient:
                        await user["websocket"].send_json(
                            {
                                "eventType": "user joined",
                                "data": {
                                    "callerId": sender,
                                    "signal": signal
                                }
                            }
                        )
                        break

    async def send_answer(
            self,
            room_id: int,
            sender: int,
            recipient: int,
            signal: dict
    ):
        for connection in self.websocket_connections:
            if room_id in connection:
                for user in connection[room_id]:
                    if user["userId"] == recipient:
                        await user["websocket"].send_json(
                            {
                                "eventType": "receiving returned signal",
                                "data": {
                                    "id": sender,
                                    "signal": signal
                                }
                            }
                        )
                        break


manager = RoomConnectionManager()


@router.websocket("/room/{room_id}")
async def connect_to_room(
       websocket: WebSocket,
       room_id: int
):
    manager.initialize_room(room_id=room_id)

    try:
        await websocket.accept()

        while True:
            data = await websocket.receive_json()

            if data.get("eventType") == "join room":
                user_id = data.get("data").get("userId")
                manager.add_new_user(room_id=room_id, user_id=user_id, websocket=websocket)
                await manager.send_list_user(room_id=room_id, user_id=user_id)

            elif data.get("eventType") == "sending signal":
                signal = data.get("data").get("signal")
                recipient = data.get("data").get("userToSignal")
                sender = data.get("data").get("callerId")
                await manager.send_offer(room_id=room_id, sender=sender, recipient=recipient, signal=signal)

            elif data.get("eventType") == "returning signal":
                signal = data.get("data").get("signal")
                sender = data.get("data").get("userId")
                recipient = data.get("data").get("callerId")
                await manager.send_answer(room_id=room_id, sender=sender, recipient=recipient, signal=signal)
            else:
                await websocket.send_text("Wrong eventType")

            print(manager.websocket_connections)

    except WebSocketDisconnect as e:
        print(f"Ошибка {e}")
        manager.remove_user(room_id=room_id, websocket=websocket)
        print(manager.websocket_connections)

    finally:
        await websocket.close()
