from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi.websockets import WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.crud.group_chat_crud import (create_group_chat_answer,
                                      create_group_chat_massage,
                                      select_curator_in_group_db,
                                      select_last_messages_db, select_moder_db,
                                      select_student_in_group_db,
                                      select_student_name_and_photo_db,
                                      select_curator_name_db)
from app.crud.group_crud import select_group_by_name_db
from app.models import User
from app.session import get_db
from app.utils.token import get_current_user


router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.connections = {}

    def add_connection(self, group_name: str, connection):
        if group_name not in self.connections:
            self.connections[group_name] = []
        self.connections[group_name].append(connection)

    def remove_connection(self, group_name: str, connection):
        if group_name in self.connections:
            self.connections[group_name].remove(connection)

    async def send_message_to_group(self, group_name: str, message):
        if group_name in self.connections:
            connections = self.connections[group_name]
            for connection in connections:
                await connection["websocket"].send_json(message)


manager = ConnectionManager()


def get_last_messages(group_id: int, db: Session = Depends(get_db)):
    group_chat_messages = select_last_messages_db(db=db, group_id=group_id)
    data_for_frontend = {"messages": []}

    for message in group_chat_messages:
        message_data = {
            "message_id": message.id,
            "message_text": message.message,
            "message_fixed": message.fixed,
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


def select_users(group_name: str, db: Session = Depends(get_db)):
    users = []
    users_info = []
    students = select_student_in_group_db(db=db, group_name=group_name)
    for student in students:
        users.append(student)
        student_info = select_student_name_and_photo_db(db=db, user_id=student[0])
        users_info.append(student_info)

    curators = select_curator_in_group_db(db=db, group_name=group_name)
    for curator in curators:
        users.append(curator)
        curator_info = select_curator_name_db(db=db, user_id=curator[0])
        users_info.append(curator_info)

    data = update_user_info(users_info)

    # moderators = select_moder_db(db=db)
    # for moderator in moderators:
    #     users.append(moderator)

    return users, data


def update_user_info(users_info):
    data = []
    fields = ['UserId', 'Name', 'Surname', 'ImagePath']

    for user in users_info:
        user_dict = dict(zip(fields, user))
        if len(user) <= 3:
            user_dict['ImagePath'] = None
        data.append(user_dict)

    return data


def select_count(users: list):

    total_in_chat = len(users)
    total_active = 0

    for user in users:
        if user[1] is True:
            total_active += 1

    return total_in_chat, total_active


@router.websocket("/ws/{group_name}")
async def websocket_endpoint(
        group_name: str,
        websocket: WebSocket,
        db: Session = Depends(get_db),
        # current_user: User = Depends(get_current_user)
):

    await websocket.accept()

    group_id = select_group_by_name_db(db=db, group_name=group_name)
    connection = {
        "websocket": websocket
    }
    manager.add_connection(group_name, connection)

    print(manager.connections)
    users, data = select_users(group_name=group_name, db=db)
    total_in_chat, total_active = select_count(users)

    try:
        last_messages = get_last_messages(db=db, group_id=group_id[0])
        last_messages['total_in_chat'] = total_in_chat
        last_messages['total_active'] = total_active
        last_messages['user_info'] = data
        await websocket.send_json(last_messages)

        while True:
            data = await websocket.receive_json()
            if data.get("type") == "message":
                message = data.get("message")
                sender_id = data.get("sender_id")
                sender_type = data.get("sender_type")
                fixed = data.get("fixed")
                datetime_message = datetime.utcnow()

                create_group_chat_massage(
                    db=db,
                    message=message,
                    datetime_message=datetime_message,
                    sender_id=sender_id,
                    sender_type=sender_type,
                    fixed=fixed,
                    group_id=group_id[0]
                )

            if data.get("type") == "answer":
                message = data.get("message")
                message_id = data.get("message_id")
                sender_id = data.get("sender_id")
                sender_type = data.get("sender_type")
                datetime_message = datetime.utcnow()

                create_group_chat_answer(
                    db=db,
                    message=message,
                    datetime_message=datetime_message,
                    group_chat_id=message_id,
                    sender_id=sender_id,
                    sender_type=sender_type
                )

            last_messages = get_last_messages(db=db, group_id=group_id[0])
            await manager.send_message_to_group(group_name, last_messages)

    except WebSocketDisconnect:
        manager.remove_connection(group_name=group_name, connection=connection)
