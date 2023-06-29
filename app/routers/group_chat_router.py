from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi.websockets import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.crud.group_chat_crud import (create_group_chat_answer,
                                      create_group_chat_massage,
                                      get_last_messages_db)
from app.crud.group_crud import select_group_by_name_db
# from app.models import User
from app.session import get_db
from app.utils.count_users import (get_total_in_group_chat,
                                   select_users_in_group,
                                   set_keyword_for_users_data)
# from app.utils.token import get_current_user


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


@router.websocket("/ws/{group_name}")
async def websocket_endpoint(
        group_name: str,
        websocket: WebSocket,
        db: Session = Depends(get_db),
        # current_user: User = Depends(get_current_user)
):

    group_id = select_group_by_name_db(db=db, group_name=group_name)
    await websocket.accept()

    connection = {"websocket": websocket}
    manager.add_connection(group_name, connection)

    users = select_users_in_group(group_name=group_name, db=db)
    total_in_chat, total_active = get_total_in_group_chat(users)
    user_info = set_keyword_for_users_data(users)

    try:
        last_messages = get_last_messages_db(db=db, group_id=group_id[0])
        last_messages['total_in_chat'] = total_in_chat
        last_messages['total_active'] = total_active
        last_messages['user_info'] = user_info
        await websocket.send_json(last_messages)

        while True:
            data = await websocket.receive_json()
            data_type = data.get("type")

            if data_type == "message":
                create_group_chat_massage(
                    db=db,
                    message=data.get("message"),
                    datetime_message=datetime.utcnow(),
                    sender_id=data.get("sender_id"),
                    sender_type=data.get("sender_type"),
                    fixed=data.get("fixed"),
                    group_id=group_id[0]
                )

            elif data_type == "answer":
                create_group_chat_answer(
                    db=db,
                    message=data.get("message"),
                    datetime_message=datetime.utcnow(),
                    group_chat_id=data.get("message_id"),
                    sender_id=data.get("sender_id"),
                    sender_type=data.get("sender_type")
                )
            else:
                await websocket.send_text(data='You entered an invalid value for the type field')

            last_messages = get_last_messages_db(db=db, group_id=group_id[0])
            await manager.send_message_to_group(group_name, last_messages)

    except WebSocketDisconnect:
        manager.remove_connection(group_name=group_name, connection=connection)
