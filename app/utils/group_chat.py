from typing import List, Dict
from sqlalchemy.orm import Session

from app.crud.group_chat_crud import (select_last_messages_db, create_group_chat_massage, create_attach_file_db,
                                      create_recipient_db, create_group_chat_answer, delete_message_db,
                                      delete_answer_db, select_message_by_id_db, select_answer_by_id_db,
                                      delete_attached_file_db, update_message_text_and_fixed_db, update_message_type_db)
from app.models import User
from app.utils.count_users import set_keyword_for_users_data, select_users_in_group
from app.utils.save_images import delete_file


def set_last_messages_dict(messages_obj):
    messages_data = {"messages": []}

    for message in messages_obj:
        message_data = {
            "messageId": message.id,
            "messageText": message.message,
            "messageType": message.message_type.value,
            "messageFixed": message.fixed,
            "messageDatetime": message.datetime_message.strftime("%d.%m.%Y %H:%M:%S"),
            "groupId": message.group_id,
            "senderId": message.sender_id,
            "senderType": message.sender_type.value,
            "readBy": message.read_by.split(", ") if message.read_by else [],
            "answers": [],
            "attachFiles": []
        }

        for answer in message.group_chat_answer:

            answer_data = {
                "answerId": answer.id,
                "answer": answer.message,
                "answerDatetime": answer.datetime_message.strftime("%d.%m.%Y %H:%M:%S"),
                "senderId": answer.sender_id,
                "senderType": answer.sender_type.value,
                "readBy": answer.read_by.split(", ") if answer.read_by else [],
                "attachFiles": []
            }

            for file in answer.attach_file:
                file_data = {
                    "fileId": file.id,
                    "filePath": file.file_path,
                    "mimeType": file.mime_type,
                    "fileName": file.filename,
                    "fileSize": file.size
                }
                answer_data["attachFiles"].append(file_data)

            message_data["answers"].append(answer_data)

        for file in message.attach_file:
            file_data = {
                "fileId": file.id,
                "filePath": file.file_path,
                "mimeType": file.mime_type,
                "fileName": file.filename,
                "fileSize": file.size
            }
            message_data["attachFiles"].append(file_data)

        messages_data["messages"].append(message_data)
    return messages_data


def set_last_message_dict(message_obj):
    attach_files = []
    if message_obj.fileIds:
        file_ids = message_obj.fileIds.split(",") if message_obj.fileIds else []
        file_paths = message_obj.filePaths.split(",") if message_obj.filePaths else []
        mime_types = message_obj.mimeTypes.split(",") if message_obj.mimeTypes else []
        file_names = message_obj.fileNames.split(",") if message_obj.fileNames else []
        file_sizes = message_obj.fileSizes.split(",") if message_obj.fileSizes else []

        for file_id, file_path, mime_type, filename, file_size in zip(
                file_ids, file_paths, mime_types, file_names, file_sizes
        ):
            attach_files.append({
                "fileId": int(file_id),
                "filePath": file_path,
                "mimeType": mime_type,
                "fileName": filename,
                "fileSize": file_size,
            })

    message = {
        "messageId": message_obj.id,
        "messageText": message_obj.message,
        "messageType": message_obj.message_type.value,
        "messageFixed": message_obj.fixed,
        "messageDatetime": message_obj.datetime_message.strftime("%d.%m.%Y %H:%M:%S"),
        "groupId": message_obj.group_id,
        "senderId": message_obj.sender_id,
        "senderType": message_obj.sender_type.value,
        "readBy": message_obj.read_by.split(", ") if message_obj.read_by else [],
        "attachFiles": attach_files
    }

    return message


def set_last_answer_dict(answer_obj):
    attach_files = []

    if answer_obj:
        file_ids = answer_obj.fileIds.split(",") if answer_obj.fileIds else []
        file_paths = answer_obj.filePaths.split(",") if answer_obj.filePaths else []
        mime_types = answer_obj.mimeTypes.split(",") if answer_obj.mimeTypes else []
        file_names = answer_obj.fileNames.split(",") if answer_obj.fileNames else []
        file_sizes = answer_obj.fileSizes.split(",") if answer_obj.fileSizes else []

        for file_id, file_path, mime_type, filename, file_size in zip(
                file_ids, file_paths, mime_types, file_names, file_sizes
        ):
            attach_files.append({
                "fileId": int(file_id),
                "filePath": file_path,
                "mimeType": mime_type,
                "fileName": filename,
                "fileSize": file_size
            })

    answer = {
        "answerId": answer_obj[0].id,
        "answerText": answer_obj[0].message,
        "answerDatetime": answer_obj[0].datetime_message.strftime("%d.%m.%Y %H:%M:%S"),
        "messageId": answer_obj[0].group_chat.id,
        "senderId": answer_obj[0].sender_id,
        "senderType": answer_obj[0].sender_type,
        "readBy": answer_obj[0].read_by.split(",") if answer_obj[0].read_by else [],
        "attachFiles": attach_files
    }

    return answer


def set_updated_message(message_obj):
    attach_file = []
    if message_obj.attach_file:
        for file in message_obj.attach_file:
            file_obj = {
                "fileId": file.id,
                "filePath": file.file_path,
                "mimeType": file.mime_type,
                "fileName": file.filename,
                "fileSize": file.size
            }
            attach_file.append(file_obj)

    answers = []
    if message_obj.group_chat_answer:
        for answer in message_obj.group_chat_answer:
            answer_attach_files = []
            if answer.attach_file:
                for answer_file in answer.attach_file:
                    answer_file_obj = {
                        "fileId": answer_file.id,
                        "filePath": answer_file.file_path,
                        "mimeType": answer_file.mime_type,
                        "fileName": answer_file.filename,
                        "fileSize": answer_file.size
                    }
                    answer_attach_files.append(answer_file_obj)

            answer_obj = {
                "answerId": answer.id,
                "answer": answer.message,
                "answerDatetime": answer.datetime_message.strftime("%d.%m.%Y %H:%M:%S"),
                "senderId": answer.sender_id,
                "senderType": answer.sender_type,
                "readBy": answer.read_by.split(",") if answer.read_by else [],
                "deleted": answer.deleted,
                "attachFiles": answer_attach_files
            }
            answers.append(answer_obj)

    message = {
        "messageId": message_obj.id,
        "messageText": message_obj.message,
        "messageType": message_obj.message_type,
        "messageDatetime": message_obj.datetime_message.strftime("%d.%m.%Y %H:%M:%S"),
        "groupId": message_obj.group_id,
        "senderId": message_obj.sender_id,
        "senderType": message_obj.sender_type,
        "fixed": message_obj.fixed,
        "deleted": message_obj.deleted,
        "readBy": message_obj.read_by.split(",") if message_obj.read_by else [],
        "recipient": [rec.recipient_id for rec in message_obj.recipient] if message_obj.recipient else [],
        "attachFiles": attach_file,
        "answers": answers
    }
    return message


def create_last_message_data(db: Session, group_id: int, user: User):
    users = select_users_in_group(group_id=group_id, db=db)
    user_info = set_keyword_for_users_data(users)

    messages_obj = select_last_messages_db(
        db=db,
        group_id=group_id,
        recipient_id=user.id
    )

    last_messages = set_last_messages_dict(messages_obj=messages_obj)
    last_messages['userInfo'] = user_info
    return last_messages


def save_message_data_to_db(db: Session, group_id: int, data: Dict):
    new_message = create_group_chat_massage(
        db=db,
        message=data.get("message"),
        message_type=data.get("messageType"),
        fixed=data.get("fixed"),
        group_id=group_id,
        sender_id=data.get("senderId"),
        sender_type=data.get("senderType")
    )

    if data.get("attachFiles"):
        create_attach_file_db(db=db, attach_files=data.get("attachFiles"), chat_message=new_message.id)

    if data.get("recipient") is not None:
        create_recipient_db(db=db, recipient=data.get("recipient"), group_chat_id=new_message.id)


def save_answer_data_to_db(db: Session, data: Dict):
    new_answer = create_group_chat_answer(
        db=db,
        message=data.get("message"),
        group_chat_id=data.get("messageId"),
        sender_id=data.get("senderId"),
        sender_type=data.get("senderType")
    )

    if data.get("attachFiles") is not None:
        create_attach_file_db(
            db=db,
            attach_files=data.get("attachFiles"),
            chat_answer=new_answer.id
        )


def delete_message_data(db: Session, data: Dict):
    chat_message = select_message_by_id_db(db=db, message_id=data.get("messageId"))
    chat_message = delete_message_db(db=db, message=chat_message)

    if chat_message.message_type == "everyone":
        return {"messageType": "everyone"}
    else:
        return {
            "messageType": "other",
            "recipient": [recipient.recipient_id for recipient in chat_message.recipient]
        }


def delete_answer_data(db: Session, data: Dict):
    answer = select_answer_by_id_db(db=db, answer_id=data.get("answerId"))
    answer = delete_answer_db(db=db, answer=answer)
    message = answer.group_chat
    if message.message_type == "everyone":
        return {"messageType": "everyone"}
    elif message.message_type == "alone":
        return {
            "messageType": "alone",
            "messageSenderId": message.sender_id,
        }
    else:
        return {
            "messageType": "several",
            "messageSenderId": message.sender_id,
            "recipients": [recipient.recipient_id for recipient in message.recipient]
        }


def update_message_data_to_db(db: Session, data: Dict):
    message = select_message_by_id_db(db=db, message_id=data["messageId"])

    if len(message.attach_file) >= 1:
        for attach_file in message.attach_file:
            delete_file(file_path=attach_file.file_path)
            delete_attached_file_db(db=db, file_id=attach_file.id)

    if data['attachFiles']:
        create_attach_file_db(db=db, attach_files=data["attachFiles"], chat_message=data["messageId"])

    if data["message"] != message.message or data["fixed"] != message.fixed:
        update_message_text_and_fixed_db(
            db=db,
            new_text=data["message"],
            fixed=data["fixed"],
            message=message
        )

    if message.message_type == data["messageType"]:
        message_data = set_updated_message(message)
        return message_data
    else:
        update_message_type_db(
            db=db,
            message_type=data["messageType"],
            recipients=data["recipient"],
            message=message
        )
        message_data = set_updated_message(message)
        return message_data


def update_answer_data_to_db(db: Session, data: Dict):
    pass
