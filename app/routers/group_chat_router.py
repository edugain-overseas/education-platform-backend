from typing import Dict, List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.websockets import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.crud.group_chat_crud import (get_last_answer_db, get_last_message_db, select_message_by_id_db,
                                      select_messages_by_pagination_db, select_recipient_by_message_id,
                                      update_answer_read_by_db, update_message_read_by_db)
from app.crud.group_crud import select_group_by_name_db
from app.models import User
from app.session import get_db
from app.utils.group_chat import (create_last_message_data, delete_answer_data, delete_message_data,
                                  save_answer_data_to_db, save_message_data_to_db, set_last_answer_dict,
                                  set_last_message_dict, set_last_messages_dict, update_answer_data_to_db,
                                  update_message_data_to_db)
from app.utils.save_images import delete_file, save_group_chat_file
from app.utils.token import get_current_user

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.connections = {}

    def create_connection(self, websocket: WebSocket, user: User):
        connection = {
            "websocket": websocket,
            "user": user.id,
            "user_type": str(user.user_type.type)
        }
        return connection

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
            "totalActive": total_active,
            "idsActiveUsers": active_users
        }
        await self.send_message_to_group(group_name=group_name, message=total_json)

    @staticmethod
    async def send_first_message(db: Session, websocket: WebSocket, group_id: int, user: User):
        messages_data = create_last_message_data(db=db, group_id=group_id, user=user)
        await websocket.send_json(messages_data)

    async def send_message_to_user(self, group_name: str, user_id: int, message: Dict):
        if group_name in self.connections:
            connections = self.connections[group_name]
            for connection in connections:
                if connection["user"] == user_id:
                    await connection["websocket"].send_json(message)

    async def send_message_to_users(self, group_name: str, user_ids: List[int], message: Dict):
        if group_name in self.connections:
            connections = self.connections[group_name]
            for connection in connections:
                if connection["user"] in user_ids:
                    await connection["websocket"].send_json(message)

    async def send_message_to_group(self, group_name: str, message: Dict):
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
    user = get_current_user(db=db, token=token)
    group_id = select_group_by_name_db(db=db, group_name=group_name)[0]

    try:
        await websocket.accept()
        connection = manager.create_connection(websocket, user)
        await manager.add_connection(group_name, connection)
        print(manager.connections)
        await manager.send_first_message(db=db, websocket=websocket, group_id=group_id, user=user)

        while True:
            data = await websocket.receive_json()

            if data.get("type") == "message":
                save_message_data_to_db(db=db, group_id=group_id, data=data)
                message_obj = get_last_message_db(db=db, group_id=group_id, sender_id=data.get("senderId"))
                message_to_send = set_last_message_dict(message_obj)

                if data.get("messageType") == "everyone":
                    await manager.send_message_to_group(group_name=group_name, message=message_to_send)
                elif data.get("messageType") == "several":
                    await manager.send_message_to_users(
                        group_name=group_name,
                        user_ids=data.get("recipient"),
                        message=message_to_send)
                    await websocket.send_json(message_to_send)
                else:
                    await manager.send_message_to_user(
                        group_name=group_name,
                        user_id=data.get("recipient"),
                        message=message_to_send
                    )
                    await websocket.send_json(message_to_send)

            elif data.get("type") == "answer":
                save_answer_data_to_db(db=db, data=data)
                answer_obj = get_last_answer_db(db=db, sender_id=data.get("senderId"))
                answer_to_send = set_last_answer_dict(answer_obj)

                message_obj = select_message_by_id_db(db=db, message_id=data.get("messageId"))

                if message_obj.message_type == "alone":
                    await manager.send_message_to_user(
                        group_name=group_name,
                        user_id=message_obj.sender_id,
                        message=answer_to_send
                    )
                    await websocket.send_json(answer_to_send)

                elif message_obj.message_type == "several":
                    recipients = select_recipient_by_message_id(db=db, message_id=message_obj.id)
                    user_ids = [recipient.recipient_id for recipient in recipients]

                    await manager.send_message_to_users(
                        group_name=group_name,
                        user_ids=user_ids,
                        message=answer_to_send
                    )
                    await manager.send_message_to_user(
                        group_name=group_name,
                        user_id=message_obj.sender_id,
                        message=answer_to_send
                    )

                else:
                    await manager.send_message_to_group(
                        group_name=group_name,
                        message=answer_to_send
                    )
            elif data.get("type") == "deleteMessage":
                info = delete_message_data(db=db, data=data)
                message = f"Message with id {data.get('messageId')} have been deleted"
                if info["messageType"] == "everyone":
                    await manager.send_message_to_group(group_name=group_name, message={"message": message})
                else:
                    await websocket.send_json({"message": message})
                    await manager.send_message_to_users(
                        group_name=group_name,
                        user_ids=info['recipient'],
                        message={"message": message}
                    )

            elif data.get("type") == "deleteAnswer":
                info = delete_answer_data(db=db, data=data)
                message = f"Answer with id {data.get('answerId')} have been deleted"
                if info["messageType"] == "everyone":
                    await manager.send_message_to_group(group_name=group_name, message={"message": message})
                elif info["messageType"] == "alone":
                    await manager.send_message_to_user(
                        group_name=group_name,
                        user_id=info["messageSenderId"],
                        message={"message": message}
                    )
                    await manager.send_message_to_user(
                        group_name=group_name,
                        user_id=data['senderId'],
                        message={"message": message}
                    )
                else:
                    await manager.send_message_to_user(
                        group_name=group_name,
                        user_id=info["messageSenderId"],
                        message={"message": message}
                    )
                    await manager.send_message_to_users(
                        group_name=group_name,
                        user_ids=info["recipients"],
                        message={"message": message}
                    )

            elif data.get("type") == "updateMessage":
                update_message = update_message_data_to_db(db=db, data=data)
                if update_message["messageType"] == "everyone":
                    await manager.send_message_to_group(group_name=group_name, message=update_message)
                elif update_message["messageType"] == "alone":
                    await websocket.send_json(update_message)
                    await manager.send_message_to_user(
                        group_name=group_name,
                        user_id=data["recipient"],
                        message=update_message
                    )
                else:
                    await websocket.send_json(update_message)
                    await manager.send_message_to_users(
                        group_name=group_name,
                        user_ids=data["recipient"],
                        message=update_message
                    )

            elif data.get("type") == "updateAnswer":
                result_after_update = update_answer_data_to_db(db=db, data=data)
                if result_after_update["messageType"] == "everyone":
                    await manager.send_message_to_group(
                        group_name=group_name,
                        message=result_after_update["answerData"]
                    )
                elif result_after_update["messageType"] == "alone":
                    await manager.send_message_to_user(
                        group_name=group_name,
                        user_id=result_after_update["messageSenderId"],
                        message=result_after_update["answerData"]
                    )
                    await manager.send_message_to_user(
                        group_name=group_name,
                        user_id=data['senderId'],
                        message=result_after_update["answerData"]
                    )
                else:
                    await manager.send_message_to_user(
                        group_name=group_name,
                        user_id=result_after_update["messageSenderId"],
                        message=result_after_update["answerData"]
                    )
                    await manager.send_message_to_users(
                        group_name=group_name,
                        user_ids=result_after_update["messageRecipient"],
                        message=result_after_update["answerData"]
                    )

    except WebSocketDisconnect:
        await manager.remove_connection(group_name=group_name, connection=connection)
        print(manager.connections)

    except Exception as e:
        print(f'Exception – {e}')


@router.post("/group-chat/attachment-file")
async def attach_file_to_chat(
        file: UploadFile = File(...),
        user: User = Depends(get_current_user)
):
    if user.student or user.curator or user.moder:
        file_path = save_group_chat_file(file=file)
        return {
            "filePath": file_path,
            "fileName": file.filename,
            "fileSize": file.size
        }
    return HTTPException(status_code="403", detail="Teacher can't use group chat")


@router.delete("/group-chat/delete-file")
async def delete_file_from_chat(
        file_path: str,
        user: User = Depends(get_current_user)
):
    if user.student or user.curator or user.moder:
        return delete_file(file_path=file_path)
    return HTTPException(status_code="403", detail="Teacher can't use group chat")


@router.post("/read-message/{message_id}")
async def read_chat_message(
        message_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return update_message_read_by_db(db=db, message_id=message_id, user_id=user.id)


@router.post("/read-answer/{answer_id}")
async def read_chat_answer(
        answer_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return update_answer_read_by_db(db=db, answer_id=answer_id, user_id=user.id)


@router.get("/next-messages/{group_name}/{last_message_id}")
async def get_chat_messages(
        group_name: str,
        last_message_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    group_id = select_group_by_name_db(db=db, group_name=group_name)[0]

    messages_obj = select_messages_by_pagination_db(
        db=db,
        group_id=group_id,
        recipient_id=user.id,
        last_message_id=last_message_id
    )

    result = set_last_messages_dict(messages_obj=messages_obj)
    return result
