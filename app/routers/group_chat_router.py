from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.websockets import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.crud.group_chat_crud import (create_attach_file_db,
                                      create_group_chat_answer,
                                      create_group_chat_massage,
                                      create_recipient_db, get_last_answer_db,
                                      get_last_message_db,
                                      get_last_messages_db,
                                      select_message_by_id_db,
                                      select_recipient_by_message_id,
                                      update_answer_read_by_db,
                                      update_message_read_by_db)
from app.crud.group_crud import select_group_by_name_db
from app.models import User
from app.session import get_db
from app.utils.count_users import (select_users_in_group,
                                   set_keyword_for_users_data)
from app.utils.save_images import delete_group_chat_file, save_group_chat_file
from app.utils.token import get_current_user, get_user_by_token

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.connections = {}

    async def add_connection(self, group_name: str, connection):
        if group_name not in self.connections:
            self.connections[group_name] = []
        self.connections[group_name].append(connection)
        await self.total_active_users(group_name=group_name)

    async def remove_connection(self, group_name: str, connection):
        if group_name in self.connections:
            self.connections[group_name].remove(connection)
            await self.total_active_users(group_name=group_name)

    async def total_active_users(self, group_name: str):
        total_active = len(self.connections[group_name])
        connections = self.connections[group_name]
        active_users = []

        for connection in connections:
            active_users.append(connection['user'])

        total_json = {
            "total_active": total_active,
            "id_active_users": active_users
        }
        await self.send_message_to_group(group_name=group_name, message=total_json)

    async def send_message_to_user(self, group_name: str, user_id: int, message):
        if group_name in self.connections:
            connections = self.connections[group_name]
            for connection in connections:
                if connection["user"] == user_id:
                    await connection["websocket"].send_json(message)

    async def send_message_to_users(self, group_name: str, user_ids: List[int], message):
        if group_name in self.connections:
            connections = self.connections[group_name]
            for connection in connections:
                if connection["user"] in user_ids:
                    await connection["websocket"].send_json(message)

    async def send_message_to_group(self, group_name: str, message):
        if group_name in self.connections:
            connections = self.connections[group_name]
            for connection in connections:
                await connection["websocket"].send_json(message)


manager = ConnectionManager()


@router.websocket("/ws/{group_name}/{token}")
async def group_chat_socket(
        group_name: str,
        token: str,
        websocket: WebSocket,
        db: Session = Depends(get_db)
):
    user = get_user_by_token(db=db, token=token)
    try:
        group_id = select_group_by_name_db(db=db, group_name=group_name)
        await websocket.accept()
    except Exception as e:
        print(f'{e}')

    connection = {"websocket": websocket, "user": user.id}
    await manager.add_connection(group_name, connection)
    print(manager.connections)

    users = select_users_in_group(group_name=group_name, db=db)
    user_info = set_keyword_for_users_data(users)

    try:
        last_messages = get_last_messages_db(db=db, group_id=group_id[0], recipient_id=user.id)
        last_messages['user_info'] = user_info
        await websocket.send_json(last_messages)

        while True:
            data = await websocket.receive_json()
            data_type = data.get("type")

            # Логика сохранения нового сообщения в БД
            if data_type == "answer":
                new_answer = create_group_chat_answer(
                    db=db,
                    message=data.get("message"),
                    datetime_message=datetime.utcnow(),
                    group_chat_id=data.get("message_id"),
                    sender_id=data.get("sender_id"),
                    sender_type=data.get("sender_type")
                )

                if data.get("attach_file_path") is not None:
                    create_attach_file_db(
                        db=db,
                        attach_files=data.get("attach_file_path"),
                        chat_answer=new_answer.id
                    )

            elif data_type == "message":
                new_message = create_group_chat_massage(
                    db=db,
                    message=data.get("message"),
                    datetime_message=datetime.utcnow(),
                    message_type=data.get("message_type"),
                    fixed=data.get("fixed"),
                    group_id=group_id[0],
                    sender_id=data.get("sender_id"),
                    sender_type=data.get("sender_type")
                )

                if data.get("recipient") is not None:
                    create_recipient_db(
                        db=db,
                        recipient=data.get("recipient"),
                        group_chat_id=new_message.id
                    )

                if data.get("attach_file_path") is not None:
                    create_attach_file_db(
                        db=db,
                        attach_files=data.get("attach_file_path"),
                        chat_message=new_message.id
                    )

            # Логика отправки нового сообщения по сокету

            if data.get("message_type") == "alone":
                message = get_last_message_db(db=db, group_id=group_id[0], sender_id=data.get("sender_id"))
                await manager.send_message_to_user(
                    group_name=group_name,
                    user_id=data.get("recipient"),
                    message=message
                )
                await websocket.send_json(message)

            elif data.get("message_type") == "several":
                message = get_last_message_db(db=db, group_id=group_id[0], sender_id=data.get("sender_id"))
                await manager.send_message_to_users(
                    group_name=group_name,
                    user_ids=data.get("recipient"),
                    message=message
                )
                await websocket.send_json(message)

            elif data.get("message_type") == "everyone":
                message = get_last_message_db(db=db, group_id=group_id[0], sender_id=data.get("sender_id"))
                await manager.send_message_to_group(
                    group_name=group_name,
                    message=message
                )

            else:
                answer = get_last_answer_db(db=db, sender_id=data.get("sender_id"))
                message_obj = select_message_by_id_db(db=db, message_id=data.get("message_id"))

                if message_obj.message_type == "alone":
                    await manager.send_message_to_user(
                        group_name=group_name,
                        user_id=message_obj.sender_id,
                        message=answer
                    )
                    await websocket.send_json(answer)

                elif message_obj.message_type == "several":
                    recipients = select_recipient_by_message_id(db=db, message_id=message_obj.id)

                    user_ids = []
                    for recipient in recipients:
                        user_ids.append(recipient.recipient_id)

                    await manager.send_message_to_users(
                        group_name=group_name,
                        user_ids=user_ids,
                        message=answer
                    )
                    await manager.send_message_to_user(
                        group_name=group_name,
                        user_id=message_obj.sender_id,
                        message=answer
                    )

                else:
                    await manager.send_message_to_group(
                        group_name=group_name,
                        message=answer
                    )

    except WebSocketDisconnect:
        await manager.remove_connection(group_name=group_name, connection=connection)


@router.post("/group-chat/attachment-file")
async def attach_file_to_chat(
        file: UploadFile = File(...),
        current_user: User = Depends(get_current_user)
):
    if current_user.student or current_user.curator or current_user.moder:
        file_path = save_group_chat_file(file=file)
        return file_path
    return HTTPException(status_code="403", detail="Teacher can't use group chat")


@router.delete("/group-chat/delete-file")
async def delete_file_from_chat(
        file_path: str,
        current_user: User = Depends(get_current_user)
):
    if current_user.student or current_user.curator or current_user.moder:
        return delete_group_chat_file(file_path=file_path)
    return HTTPException(status_code="403", detail="Teacher can't use group chat")


@router.post("/read-message/{message_id}")
async def read_chat_message(
        message_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return update_message_read_by_db(db=db, message_id=message_id, user_id=current_user.id)


@router.post("/read-answer/{answer_id}")
async def read_chat_answer(
        answer_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return update_answer_read_by_db(db=db, answer_id=answer_id, user_id=current_user.id)
