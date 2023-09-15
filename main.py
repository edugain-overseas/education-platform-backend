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
from app.setting import API_PREFIX


app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(user_router, prefix=API_PREFIX, tags=['User'])
app.include_router(student_router, prefix=API_PREFIX, tags=['Student'])
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


# class RoomConnectionManager:
#     def __init__(self):
#         self.websocket_connections = {}
#
#     def set_new_connection(self, websocket: WebSocket):
#         connection = {
#             "user_id": None,
#             "user_type": None,
#             "websocket": websocket,
#             "signal": None
#         }
#
#         return connection
#
#     def check_len(self, room_id):
#         if room_id in self.websocket_connections:
#             room_connections = self.websocket_connections[room_id]
#             return len(room_connections)
#
#     def add_new_connection(self, room_id: int, connection: dict):
#         if room_id not in self.websocket_connections:
#             self.websocket_connections[room_id] = []
#         self.websocket_connections[room_id].append(connection)
#
#     def find_connection(self, room_id: int, websocket: WebSocket):
#         if room_id in self.websocket_connections:
#             room_connections = self.websocket_connections[room_id]
#             for connection in room_connections:
#                 if connection["websocket"] == websocket:
#                     return connection
#             print('Я не нашел нужный сокет')
#             return None
#
#     def find_teacher_connection(self, room_id: int):
#         if room_id in self.websocket_connections:
#             room_connections = self.websocket_connections[room_id]
#             for connection in room_connections:
#                 if connection["user_type"] == "teacher":
#                     return connection
#
#     def update_connection(self, connection: dict, user_id: int, user_type: str, signal: dict):
#         connection["user_id"] = user_id
#         connection["user_type"] = user_type
#         connection["signal"] = signal
#         return connection
#
#     def remove_connection(self, room_id: int, websocket: WebSocket):
#         if room_id in self.websocket_connections:
#             room_connections = self.websocket_connections[room_id]
#             for connection in room_connections:
#                 if connection["websocket"] == websocket:
#                     room_connections.remove(connection)
#                     return True
#                 return False
#
#     async def send_signal_to_students(self, room_id, signal):
#         if room_id in self.websocket_connections:
#             room_connections = self.websocket_connections[room_id]
#             for connection in room_connections:
#                 if connection["user_type"] == "student" and connection["signal"] is None:
#                     await connection["websocket"].send_json(signal)
#                 elif connection["user_type"] is None:
#                     await connection["websocket"].send_json(signal)
#
#     async def send_signal_to_teacher(self, room_id, signal):
#         if room_id in self.websocket_connections:
#             room_connections = self.websocket_connections[room_id]
#             for connection in room_connections:
#                 if connection["user_type"] == "teacher":
#                     await connection["websocket"].send_json(signal)

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


# @app.websocket("/room/{room_id}")
# async def connect_to_room(
#        websocket: WebSocket,
#        room_id: int
# ):
#     try:
#         await websocket.accept()
#         new_connection = manager.set_new_connection(websocket=websocket)
#         manager.add_new_connection(room_id=room_id, connection=new_connection)
#
#         print(len(manager.websocket_connections[room_id]))
#         print(manager.websocket_connections[room_id])
#
#         if manager.check_len(room_id=room_id) >= 2:
#             teacher_connection = manager.find_teacher_connection(room_id=room_id)
#             await manager.send_signal_to_students(room_id=room_id, signal=teacher_connection["signal"])
#             print('Отправил siganal студенту')
#
#         while True:
#             data = await websocket.receive_json()
#             print(data)
#             connection = manager.find_connection(room_id=room_id, websocket=websocket)
#             user_id = data.get('from')
#             user_type = data.get('fromUserType')
#             signal = data.get('signal')
#
#             manager.update_connection(
#                 connection=connection,
#                 user_id=user_id,
#                 user_type=user_type,
#                 signal=signal
#             )
#
#             if user_type == "student" and signal["type"] == "answer":
#                 await manager.send_signal_to_teacher(room_id=room_id, signal=signal)
#                 print(connection)
#
#             print(manager.websocket_connections)
#
#     except WebSocketDisconnect as e:
#         print(f"Код ответа – {e}")
#         manager.remove_connection(room_id=room_id, websocket=websocket)
#         print(manager.websocket_connections)
#
#     finally:
#         await websocket.close()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


# 1) Get
# data.eventType: str = "join room"
# data.data.userId: int

# 2) Send
# eventType: str = "all user"
# data: list

# 3) Get
# data.eventType: str = "sending signal"
# data.data.userToSignal: int - кому отправляем оффер
# data.data.callerId: int - кто отправляет оффер
# data.data.signal: dict{"sdp": "...", "type": "..."}

# 4) Send
# eventType: str = "user joined"
# data.signal: dict{"sdp": "...", "type": "..."}
# data.callerId: int

# 5) Get
# data.eventType: str = "returning signal"
# data.data.signal: dict{"sdp": "...", "type": "..."}
# data.data.callerId: int - кому
# data.data.userId: int - от кого

# 6) Send
# eventType: str = "receiving returned signal"
# signal: dict{"sdp": "...", "type": "..."}
# callerId: int


