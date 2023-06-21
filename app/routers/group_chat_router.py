from fastapi import APIRouter, Depends, HTTPException
from fastapi.websockets import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from app.session import get_db
from app.utils.token import get_current_user
from app.crud.group_crud import select_group_by_name_db
from app.crud.group_chat_crud import *


router = APIRouter()


class GroupChatAnswer(BaseModel):
    message: str
    datetime_message: datetime
    sender_id: int
    sender_type: str


class ConnectionManager:
    def __init__(self):
        self.connections = []

    def add_connection(self, connection):
        self.connections.append(connection)

    def remove_connection(self, connection):
        self.connections.remove(connection)

    async def send_message(self, message):
        for connection in self.connections:
            await connection["websocket"].send_json(message)


manager = ConnectionManager()


@router.get("/group_chat/{group_chat_id}/last")
async def get_last_massage(
        group_chat_id: int,
        db: Session = Depends(get_db)
):
    messages = select_last_message_db(db=db, group_id=group_chat_id)
    return messages


@router.get("/group_chat/{group_id}/last10")
async def get_last_messages(
        group_id: int,
        db: Session = Depends(get_db)
):
    group_chat_messages = select_last_messages_db(db=db, group_id=group_id)
    data_for_frontend = {"messages": []}

    for message in group_chat_messages:
        message_data = {
            "message_id": message.id,
            "message_text": message.message,
            "message_datetime": message.datetime_message.strftime("%d.%m.%Y %H:%M:%S"),
            "group_id": message.group_id,
            "sender_id": message.sender_id,
            "sender_type": message.sender_type.value,
            "answers": [],
        }

        for answer in message.group_chat_answer:
            answer_data = {
                "answer_id": answer.id,
                "answer": answer.message,
                "answer_datetime": answer.datetime_message.strftime("%d.%m.%Y %H:%M:%S"),
                "sender_id": answer.sender_id,
                "sender_type": answer.sender_type.value,
            }
            message_data["answers"].append(answer_data)

        data_for_frontend["messages"].append(message_data)

    return data_for_frontend


@router.websocket("/ws/{group_name}")
async def websocket_endpoint(
        group_name: str,
        websocket: WebSocket,
        db: Session = Depends(get_db)
):
    await websocket.accept()

    # Собираем всех пользователей
    users = []
    students = select_student_in_group_db(db=db, group_name=group_name)
    for student in students:
        users.append(student)

    moderators = select_moder_db(db=db)
    for moderator in moderators:
        users.append(moderator)

    curators = select_curator_in_group_db(db=db, group_name=group_name)
    for curator in curators:
        users.append(curator)

    # Создаем массив соединений для пользователей группы
    connections = []

    for user in users:
        if user[1] is True:
            connection = {
                "user_id": user[0],
                "websocket": websocket
            }
            connections.append(connection)
            manager.add_connection(connection)

    try:
        while True:
            data = await websocket.receive_json()
            message = data.get("message")
            message_date = data.get("datetime_message")
            sender_id = data.get("sender_id")
            sender_type = data.get("sender_type")
            fixed = data.get("fixed")
            group_id = select_group_by_name_db(db=db, group_name=group_name)

            datetime_message = datetime.strptime(message_date, "%Y-%m-%d %H:%M:%S")

            new_message = create_group_chat_massage(
                db=db,
                message=message,
                datetime_message=datetime_message,
                sender_id=sender_id,
                sender_type=sender_type,
                fixed=fixed,
                group_id=group_id[0]
            )

            await manager.send_message(message)

    except WebSocketDisconnect:
        # Удаляем соединение пользователя при отключении
        for connection in connections:
            if connection["websocket"] == websocket:
                connections.remove(connection)
                manager.remove_connection(connection)
                break


@router.post("/create/group-chat-answer/{message_id}")
async def create_answer(
        message_id: int,
        answer: GroupChatAnswer,
        db: Session = Depends(get_db)

):
    new_message = create_group_chat_answer(
        db=db,
        message=answer.message,
        datetime_message=answer.datetime_message,
        sender_id=answer.sender_id,
        sender_type=answer.sender_type,
        group_chat_id=message_id

    )
    return new_message
