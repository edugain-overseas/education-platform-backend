from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.websockets import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.crud.subject_chat_crud import (create_subject_attach_file_db, create_subject_chat_answer,
                                        create_subject_chat_message, create_subject_recipient_db,
                                        get_last_messages_for_subject_chat_db,
                                        get_messages_for_subject_chat_by_pagination_db, select_last_answer_db,
                                        select_last_message_db, select_message_by_id_db, select_recipient_by_message_id,
                                        update_read_by_for_answer_db, update_read_by_for_message_db)
from app.models import User
from app.session import get_db
from app.utils.count_users import select_users_in_subject, set_keyword_for_users_data
from app.utils.save_images import delete_file, save_subject_chat_file
from app.utils.subject_chat import (set_subject_chat_last_answer_dict, set_subject_chat_last_message_dict,
                                    set_subject_chat_last_messages_dict)
from app.utils.token import get_current_user, get_user_by_token

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.connections = {}

    async def add_connection(self, subject_id: int, connection):
        if subject_id not in self.connections:
            self.connections[subject_id] = []
        self.connections[subject_id].append(connection)
        await self.total_active_users(subject_id=subject_id)

    async def remove_connection(self, subject_id: int, connection):
        if subject_id in self.connections:
            self.connections[subject_id].remove(connection)
            await self.total_active_users(subject_id=subject_id)

    async def total_active_users(self, subject_id: int):
        total_active = len(self.connections[subject_id])
        connections = self.connections[subject_id]
        active_users = []

        for connection in connections:
            active_users.append(connection['user'])

        total_json = {
            "total_active": total_active,
            "id_active_users": active_users
        }
        await self.send_message_to_group(subject_id=subject_id, message=total_json)

    async def send_message_to_user(self, subject_id: int, user_id: int, message):
        if subject_id in self.connections:
            connections = self.connections[subject_id]
            for connection in connections:
                if connection["user"] == user_id:
                    await connection["websocket"].send_json(message)

    async def send_message_to_users(self, subject_id: int, user_ids: List[int], message):
        if subject_id in self.connections:
            connections = self.connections[subject_id]
            for connection in connections:
                if connection["user"] in user_ids:
                    await connection["websocket"].send_json(message)

    async def send_message_to_group(self, subject_id: int, message):
        if subject_id in self.connections:
            connections = self.connections[subject_id]
            for connection in connections:
                await connection["websocket"].send_json(message)


manager = ConnectionManager()


@router.websocket("/ws/subject/{subject_id}/{token}")
async def subject_chat_socket(
    subject_id: int,
    token: str,
    websocket: WebSocket,
    db: Session = Depends(get_db)
):
    user = get_user_by_token(db=db, token=token)
    try:
        await websocket.accept()
    except Exception as e:
        print(f"{e}")

    connection = {"websocket": websocket, "user": user.id}
    await manager.add_connection(subject_id, connection)
    print(manager.connections)

    users = select_users_in_subject(db=db, subject_id=subject_id)
    user_info = set_keyword_for_users_data(users=users)

    try:
        messages_obj = get_last_messages_for_subject_chat_db(db=db, subject_id=subject_id, recipient_id=user.id)
        last_messages = set_subject_chat_last_messages_dict(messages_obj=messages_obj)
        last_messages['user_info'] = user_info
        await websocket.send_json(last_messages)

        while True:
            data = await websocket.receive_json()
            data_type = data.get("type")

            # Logic to save new message in DataBase
            if data_type == "answer":
                new_answer = create_subject_chat_answer(
                    db=db,
                    message=data.get("message"),
                    datetime_message=datetime.utcnow(),
                    subject_chat_id=data.get("message_id"),
                    sender_id=data.get("sender_id"),
                    sender_type=data.get("sender_type")
                )

                if data.get("attach_file_path") is not None:
                    create_subject_attach_file_db(
                        db=db,
                        attach_files=data.get("attach_file_path"),
                        subject_chat_answer=new_answer.id
                    )

            elif data_type == "message":
                new_message = create_subject_chat_message(
                    db=db,
                    message=data.get("message"),
                    datetime_message=datetime.utcnow(),
                    message_type=data.get("message_type"),
                    fixed=data.get("fixed"),
                    subject_id=subject_id,
                    sender_id=data.get("sender_id"),
                    sender_type=data.get("sender_type")
                )

                if data.get("recipient") is not None:
                    create_subject_recipient_db(
                        db=db,
                        recipient=data.get("recipient"),
                        subject_chat_id=new_message.id
                    )

                if data.get("attach_file_path") is not None:
                    create_subject_attach_file_db(
                        db=db,
                        attach_files=data.get("attach_file_path"),
                        subject_chat_message=new_message.id
                    )

            # Logic to send new message in websocket
            if data.get("message_type") == "alone":
                message_obj = select_last_message_db(db=db, subject_id=subject_id, sender_id=data.get("sender_id"))
                message_to_send = set_subject_chat_last_message_dict(message_obj)
                await manager.send_message_to_user(
                    subject_id=subject_id,
                    user_id=data.get("recipient"),
                    message=message_to_send
                )
                await websocket.send_json(message_to_send)

            elif data.get("message_type") == "several":
                message_obj = select_last_message_db(db=db, subject_id=subject_id, sender_id=data.get("sender_id"))
                message_to_send = set_subject_chat_last_message_dict(message_obj)
                await manager.send_message_to_users(
                    subject_id=subject_id,
                    user_ids=data.get("recipient"),
                    message=message_to_send
                )
                await websocket.send_json(message_to_send)

            elif data.get("message_type") == "everyone":
                message_obj = select_last_message_db(db=db, subject_id=subject_id, sender_id=data.get("sender_id"))
                message_to_send = set_subject_chat_last_message_dict(message_obj)
                await manager.send_message_to_group(
                    subject_id=subject_id,
                    message=message_to_send
                )

            # Logic to send new answer in websocket
            else:
                answer_obj = select_last_answer_db(db=db, sender_id=data.get("sender_id"))
                answer_to_send = set_subject_chat_last_answer_dict(answer_obj)
                message_obj = select_message_by_id_db(db=db, message_id=data.get("message_id"))

                if message_obj.message_type == "alone":
                    await manager.send_message_to_user(
                        subject_id=subject_id,
                        user_id=message_obj.sender_id,
                        message=answer_to_send
                    )
                    await websocket.send_json(answer_to_send)

                elif message_obj.message_type == "several":
                    recipients = select_recipient_by_message_id(db=db, message_id=message_obj.id)

                    user_ids = []
                    for recipient in recipients:
                        user_ids.append(recipient.recipient_id)

                    await manager.send_message_to_users(
                        subject_id=subject_id,
                        user_ids=user_ids,
                        message=answer_to_send
                    )
                    await manager.send_message_to_user(
                        subject_id=subject_id,
                        user_id=message_obj.sender_id,
                        message=answer_to_send
                    )
                else:
                    await manager.send_message_to_group(
                        subject_id=subject_id,
                        message=answer_to_send
                    )

    except WebSocketDisconnect:
        await manager.remove_connection(subject_id=subject_id, connection=connection)


@router.post("/subject_chat/attachment-file")
async def attach_file_to_chat(
        file: UploadFile = File(...),
        user: User = Depends(get_current_user)
):
    if user.student or user.teacher or user.moder:
        file_path = save_subject_chat_file(file=file)
        return file_path
    return HTTPException(status_code="403", detail="Teacher can't use group chat")


@router.delete("/subject_chat/delete-file")
async def delete_file_from_chat(
        file_path: str,
        user: User = Depends(get_current_user)
):
    if user.student or user.teacher or user.moder:
        return delete_file(file_path=file_path)
    return HTTPException(status_code="403", detail="Teacher can't use group chat")


@router.post("/subject_chat/read_message/{message_id}")
async def read_chat_message(
        message_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return update_read_by_for_message_db(db=db, message_id=message_id, user_id=user.id)


@router.post("/subject_chat/read_answer/{answer_id}")
async def read_chat_answer(
        answer_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return update_read_by_for_answer_db(db=db, answer_id=answer_id, user_id=user.id)


@router.get("/subject_chat/next-messages/{subject_id}/{last_message_id}")
async def get_chat_messages(
        subject_id: int,
        last_message_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):

    messages_obj = get_messages_for_subject_chat_by_pagination_db(
        db=db,
        subject_id=subject_id,
        recipient_id=user.id,
        last_message_id=last_message_id
    )

    result = set_subject_chat_last_messages_dict(messages_obj=messages_obj)
    return result
