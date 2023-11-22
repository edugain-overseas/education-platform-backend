from typing import Dict, List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.websockets import WebSocket, WebSocketDisconnect, WebSocketState
from sqlalchemy.orm import Session

from app.crud.subject_chat_crud import (get_messages_for_subject_chat_by_pagination_db, select_last_answer_db,
                                        select_last_message_db, select_message_by_id_db, select_recipient_by_message_id,
                                        update_read_by_for_answer_db, update_read_by_for_message_db)
from app.models import User
from app.session import get_db
from app.utils.save_images import delete_file, save_subject_chat_file
from app.utils.subject_chat import (delete_answer_data_to_db, delete_message_data_to_db, get_data_about_latest_messages,
                                    save_answer_data_to_db, save_message_data_to_db, set_subject_chat_last_answer_dict,
                                    set_subject_chat_last_message_dict, set_subject_chat_last_messages_dict,
                                    update_answer_data_to_db, update_message_data_to_db)
from app.utils.token import get_current_user

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.connections = {}

    @staticmethod
    def create_connection(websocket: WebSocket, user: User):
        connection = {"websocket": websocket, "user": user.id, "user_type": str(user.user_type.type)}
        return connection

    async def add_connection(self, subject_id: int, connection: Dict):
        if subject_id not in self.connections:
            self.connections[subject_id] = []
        self.connections[subject_id].append(connection)
        await self.total_active_users(subject_id=subject_id)

    async def remove_connection(self, subject_id: int, connection: Dict):
        if subject_id in self.connections:
            self.connections[subject_id].remove(connection)
            await self.total_active_users(subject_id=subject_id)

    async def check_user_connection(self, subject_id: int,  user_id: int):
        if subject_id in self.connections:
            for connection in self.connections[subject_id]:
                if connection["user"] == user_id:
                    await connection["websocket"].close()

    async def total_active_users(self, subject_id: int):
        total_json = {
            "totalActive": len(self.connections[subject_id]),
            "idsActiveUsers": [connection["user"] for connection in self.connections[subject_id]]
        }
        await self.send_message_to_everyone(subject_id=subject_id, message=total_json)

    @staticmethod
    async def send_first_message(db: Session, websocket: WebSocket, subject_id: int, user: User):
        last_messages = get_data_about_latest_messages(db=db, subject_id=subject_id, user=user)
        await websocket.send_json(last_messages)

    async def send_message_to_user(self, user_id: int, subject_id: int, message: Dict):
        if subject_id in self.connections:
            for connection in self.connections[subject_id]:
                if connection["user"] == user_id:
                    await connection["websocket"].send_json(message)

    async def send_message_to_users(self, user_ids: List[int], subject_id: int, message: Dict):
        if subject_id in self.connections:
            for connection in self.connections[subject_id]:
                if connection["user"] in user_ids:
                    await connection["websocket"].send_json(message)

    async def send_message_to_everyone(self, subject_id: int, message: Dict):
        if subject_id in self.connections:
            for connection in self.connections[subject_id]:
                if (connection["websocket"].application_state == WebSocketState.CONNECTED
                        and connection["websocket"].client_state == WebSocketState.CONNECTED):
                    await connection["websocket"].send_json(message)
                else:
                    continue


manager = ConnectionManager()


@router.websocket("/ws/subject/{subject_id}/{token}")
async def subject_chat_socket(
    subject_id: int,
    token: str,
    websocket: WebSocket,
    db: Session = Depends(get_db)
):
    user = get_current_user(db=db, token=token)

    try:
        await manager.check_user_connection(subject_id=subject_id, user_id=user.id)

        await websocket.accept()
        connection = manager.create_connection(websocket=websocket, user=user)
        await manager.add_connection(subject_id=subject_id, connection=connection)
        await manager.send_first_message(db=db, websocket=websocket, subject_id=subject_id, user=user)

        while True:
            data = await websocket.receive_json()

            if data.get("type") == "message":
                save_message_data_to_db(db=db, subject_id=subject_id, data=data)
                message_obj = select_last_message_db(db=db, subject_id=subject_id, sender_id=data.get("senderId"))
                message_to_send = set_subject_chat_last_message_dict(message_obj)

                if data.get("messageType") == "alone":
                    await websocket.send_json(message_to_send)
                    await manager.send_message_to_user(user_id=data.get("recipient"), subject_id=subject_id,
                                                       message=message_to_send)

                elif data.get("messageType") == "several":
                    await websocket.send_json(message_to_send)
                    await manager.send_message_to_users(user_ids=data.get("recipient"), subject_id=subject_id,
                                                        message=message_to_send)

                else:
                    await manager.send_message_to_everyone(subject_id=subject_id, message=message_to_send)

            elif data.get("type") == "answer":
                save_answer_data_to_db(db=db, data=data)
                answer_obj = select_last_answer_db(db=db, sender_id=data.get("senderId"))
                answer_to_send = set_subject_chat_last_answer_dict(answer_obj)
                message_obj = select_message_by_id_db(db=db, message_id=data.get("messageId"))

                if message_obj.message_type == "alone":
                    await websocket.send_json(answer_to_send)
                    await manager.send_message_to_user(user_id=message_obj.sender_id, subject_id=subject_id,
                                                       message=answer_to_send)

                elif message_obj.message_type == "several":
                    recipients = select_recipient_by_message_id(db=db, message_id=message_obj.id)
                    user_ids = [recipient.recipient_id for recipient in recipients]
                    await manager.send_message_to_users(user_ids=user_ids, subject_id=subject_id,
                                                        message=answer_to_send)
                    await manager.send_message_to_user(user_id=message_obj.sender_id, subject_id=subject_id,
                                                       message=answer_to_send)

                else:
                    await manager.send_message_to_everyone(subject_id=subject_id, message=answer_to_send)

            elif data.get("type") == "updateMessage":
                updated_message = update_message_data_to_db(db=db, data=data)

                if updated_message["messageType"] == "alone":
                    await websocket.send_json(updated_message)
                    await manager.send_message_to_user(user_id=data.get("recipient"), subject_id=subject_id,
                                                       message=updated_message)

                elif updated_message["messageType"] == "several":
                    await websocket.send_json(updated_message)
                    await manager.send_message_to_users(user_ids=data.get("recipient"), subject_id=subject_id,
                                                        message=updated_message)

                else:
                    await manager.send_message_to_everyone(subject_id=subject_id, message=updated_message)

            elif data.get("type") == "deleteMessage":
                info = delete_message_data_to_db(db=db, data=data)
                message_to_send = f'Message with id {data.get("messageId")} have been deleted'

                if info["messageType"] == "everyone":
                    await manager.send_message_to_everyone(subject_id=subject_id, message={"message": message_to_send})

                else:
                    await websocket.send_json({"message": message_to_send})
                    await manager.send_message_to_users(subject_id=subject_id, user_ids=info["recipient"],
                                                        message={"message": message_to_send})

            elif data.get("type") == "updateAnswer":
                updated_answer = update_answer_data_to_db(db=db, data=data)

                if updated_answer["messageType"] == "alone":
                    await manager.send_message_to_user(subject_id=subject_id, user_id=updated_answer["messageSenderId"],
                                                       message=updated_answer["answerData"])
                    await manager.send_message_to_user(subject_id=subject_id, user_id=data.get("senderId"),
                                                       message=updated_answer["answerData"])

                elif updated_answer["messageType"] == "several":
                    await manager.send_message_to_user(subject_id=subject_id, user_id=updated_answer["messageSenderId"],
                                                       message=updated_answer["answerData"])
                    await manager.send_message_to_users(subject_id=subject_id,
                                                        user_ids=updated_answer["messageRecipient"],
                                                        message=updated_answer["answerData"])
                else:
                    await manager.send_message_to_everyone(subject_id=subject_id, message=updated_answer["answerData"])

            elif data.get("type") == "deleteAnswer":
                info = delete_answer_data_to_db(db=db, data=data)
                message_to_send = f'Answer with id {data.get("answerId")} have been deleted'

                if info["messageType"] == "alone":
                    await manager.send_message_to_user(subject_id=subject_id, user_id=info["messageSenderId"],
                                                       message={"message": message_to_send})
                    await manager.send_message_to_user(subject_id=subject_id, user_id=data['senderId'],
                                                       message={"message": message_to_send})

                elif info["messageType"] == "several":
                    await manager.send_message_to_user(subject_id=subject_id, user_id=info["messageSenderId"],
                                                       message={"message": message_to_send})
                    await manager.send_message_to_users(subject_id=subject_id, user_ids=info["recipients"],
                                                        message={"message": message_to_send})

                else:
                    await manager.send_message_to_everyone(subject_id=subject_id, message={"message": message_to_send})

    except WebSocketDisconnect:
        manager.connections[subject_id].remove(connection)
    finally:
        await manager.total_active_users(subject_id=subject_id)


@router.post("/subject_chat/attachment-file")
async def attach_file_to_chat(
        file: UploadFile = File(...),
        user: User = Depends(get_current_user)
):
    if user.student or user.teacher or user.moder:
        file_path = save_subject_chat_file(file=file)
        return {
            "filePath": file_path,
            "fileName": file.filename,
            "fileSize": file.size
        }
    return HTTPException(status_code=403, detail="Curator can't use group chat")


@router.delete("/subject_chat/delete-file")
async def delete_file_from_chat(
        file_path: str,
        user: User = Depends(get_current_user)
):
    if user.student or user.teacher or user.moder:
        return delete_file(file_path=file_path)
    return HTTPException(status_code=403, detail="Curator can't use group chat")


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
