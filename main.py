import random

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routers.group_chat_router import router as group_chat_router
from app.routers.group_router import router as group_router
from app.routers.lecture_router import router as lecture_router
from app.routers.lesson_router import router as lesson_router
from app.routers.module_router import router as module_router
from app.routers.specialization_router import router as specialization_router
from app.routers.student_router import router as student_router
from app.routers.subject_chat_router import router as subject_chat_router
from app.routers.subject_router import router as subject_router
from app.routers.teacher_router import router as teacher_router
from app.routers.test_lesson_router import router as test_router
from app.routers.user_router import router as user_router
from app.routers.student_test_router import router as student_test_router

from app.setting import API_PREFIX

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(user_router, prefix=API_PREFIX, tags=['User'])
app.include_router(student_router, prefix=API_PREFIX, tags=['Student'])
app.include_router(student_test_router, prefix=API_PREFIX, tags=['StudentTest'])
app.include_router(teacher_router, prefix=API_PREFIX, tags=['Teacher'])

app.include_router(specialization_router, prefix=API_PREFIX, tags=['Specialization'])
app.include_router(group_router, prefix=API_PREFIX, tags=['Group'])
app.include_router(subject_router, prefix=API_PREFIX, tags=['Subject'])
app.include_router(module_router, prefix=API_PREFIX, tags=['Module'])
app.include_router(lesson_router, prefix=API_PREFIX, tags=['Lesson'])
app.include_router(lecture_router, prefix=API_PREFIX, tags=['Lecture'])
app.include_router(test_router, prefix=API_PREFIX, tags=['TestLesson'])

app.include_router(group_chat_router, prefix=API_PREFIX, tags=['GroupChat'])
app.include_router(subject_chat_router, prefix=API_PREFIX, tags=['SubjectChat'])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


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


@app.get("/")
async def root():
    return {"message": "Server working"}


@app.get("/get_image")
async def get_image(file_path: str):
    return FileResponse(file_path)


@app.get("/generate_room_id")
async def generate_uuid():
    room_id = random.randint(100000, 999999)
    return {"room_id": room_id}


@app.websocket("/room/{room_id}")
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


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
