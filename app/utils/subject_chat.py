from typing import Dict

from sqlalchemy.orm import Session

from app.crud.subject_chat_crud import (create_subject_attach_file_db, create_subject_chat_answer,
                                        create_subject_chat_message, create_subject_recipient_db, delete_answer_db,
                                        delete_attached_file_db, delete_message_db,
                                        get_last_messages_for_subject_chat_db, select_answer_by_id_db,
                                        select_message_by_id_db, update_answer_text_db,
                                        update_message_text_and_fixed_db, update_message_type_and_recipient_db)
from app.models import SubjectChat, SubjectChatAnswer, User
from app.utils.count_users import select_users_in_subject, set_keyword_for_users_data
from app.utils.save_images import delete_file


def set_subject_chat_last_messages_dict(messages_obj):
    messages_data = {"messages": []}

    for message in messages_obj:
        message_data = {
            "messageId": message.id,
            "messageText": message.message,
            "messageType": message.message_type.value,
            "messageFixed": message.fixed,
            "messageDatetime": message.datetime_message.strftime("%d.%m.%Y %H:%M:%S"),
            "subjectId": message.subject_id,
            "senderId": message.sender_id,
            "senderType": message.sender_type.value,
            "readBy": message.read_by.split(", ") if message.read_by else [],
            "answers": [],
            "attachFiles": []
        }

        for answer in message.subject_chat_answer:
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


def set_subject_chat_last_message_dict(message_obj):
    attach_files = []

    if message_obj.fileIds:
        file_ids = message_obj.fileIds.split(",") if message_obj.fileIds else []
        file_paths = message_obj.filePaths.split(",") if message_obj.filePaths else []
        mime_types = message_obj.mimeTypes.split(",") if message_obj.mimeTypes else []
        file_names = message_obj.fileNames.split(",") if message_obj.fileNames else []
        file_sizes = message_obj.fileSizes.split(",") if message_obj.fileSizes else []

        for file_id, file_path, mime_type, file_name, file_size in zip(
                file_ids, file_paths, mime_types, file_names, file_sizes
        ):
            attach_files.append({
                "fileId": int(file_id),
                "filePath": file_path,
                "mimeType": mime_type,
                "fileName": file_name,
                "fileSize": file_size
            })

    message = {
        "messageId": message_obj.id,
        "messageText": message_obj.message,
        "messageType": message_obj.message_type.value,
        "messageFixed": message_obj.fixed,
        "messageDatetime": message_obj.datetime_message.strftime("%d.%m.%Y %H:%M:%S"),
        "subjectId": message_obj.subject_id,
        "senderId": message_obj.sender_id,
        "senderType": message_obj.sender_type.value,
        "readBy": message_obj.read_by.split(", ") if message_obj.read_by else [],
        "attachFiles": attach_files
    }

    return message


def set_updated_subject_message_dict(message_obj: SubjectChat):
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
    if message_obj.subject_chat_answer:
        for answer in message_obj.subject_chat_answer:
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
        "subjectId": message_obj.subject_id,
        "senderId": message_obj.sender_id,
        "senderType": message_obj.sender_type,
        "fixed": message_obj.fixed,
        "deleted": message_obj.deleted,
        "readBy": message_obj.read_by.split(",") if message_obj.read_by else [],
        "recipient": [rec.recipient_id for rec in message_obj.subject_recipient]
        if message_obj.subject_recipient else [],
        "attachFiles": attach_file,
        "answers": answers
    }
    return message


def set_updated_subject_answer_dict(answer_obj: SubjectChatAnswer):
    attach_file = []
    if answer_obj.attach_file:
        for file in answer_obj.attach_file:
            file_obj = {
                "fileId": file.id,
                "filePath": file.file_path,
                "mimeType": file.mime_type,
                "fileName": file.filename,
                "fileSize": file.size
            }
            attach_file.append(file_obj)

    answer = {
        "answerId": answer_obj.id,
        "answer": answer_obj.message,
        "answerDatetime": answer_obj.datetime_message.strftime("%d.%m.%Y %H:%M:%S"),
        "senderId": answer_obj.sender_id,
        "senderType": answer_obj.sender_type,
        "readBy": answer_obj.read_by.split(",") if answer_obj.read_by else [],
        "deleted": answer_obj.deleted,
        "attachFiles": attach_file
    }
    return answer


def set_subject_chat_last_answer_dict(answer_obj):
    attach_files = []

    if answer_obj:
        file_ids = answer_obj.fileIds.split(",") if answer_obj.fileIds else []
        file_paths = answer_obj.filePaths.split(",") if answer_obj.filePaths else []
        mime_types = answer_obj.mimeTypes.split(",") if answer_obj.mimeTypes else []
        file_names = answer_obj.fileNames.split(",") if answer_obj.fileNames else []
        file_sizes = answer_obj.fileSizes.split(",") if answer_obj.fileSizes else []

        for file_id, file_path, mime_type, file_name, file_size in zip(
                file_ids, file_paths, mime_types, file_names, file_sizes
        ):
            attach_files.append({
                "fileId": int(file_id),
                "filePath": file_path,
                "mimeType": mime_type,
                "fileName": file_name,
                "fileSize": file_size
            })

    answer = {
        "answerId": answer_obj[0].id,
        "answerText": answer_obj[0].message,
        "answerDatetime": answer_obj[0].datetime_message.strftime("%d.%m.%Y %H:%M:%S"),
        "messageId": answer_obj[0].subject_chat.id,
        "senderId": answer_obj[0].sender_id,
        "senderType": answer_obj[0].sender_type,
        "readBy": answer_obj[0].read_by.split(", ") if answer_obj[0].read_by else [],
        "attachFiles": attach_files
    }
    return answer


def get_data_about_latest_messages(db: Session, subject_id: int, user: User):
    users = select_users_in_subject(db=db, subject_id=subject_id)
    user_info = set_keyword_for_users_data(users=users)
    messages_obj = get_last_messages_for_subject_chat_db(db=db, subject_id=subject_id, recipient_id=user.id)
    last_messages = set_subject_chat_last_messages_dict(messages_obj=messages_obj)
    last_messages["userInfo"] = user_info
    return last_messages


def save_message_data_to_db(db: Session, subject_id: int, data: Dict):
    new_message = create_subject_chat_message(
        db=db,
        message=data.get("message"),
        message_type=data.get("messageType"),
        fixed=data.get("fixed"),
        sender_id=data.get("senderId"),
        sender_type=data.get("senderType"),
        subject_id=subject_id,
    )

    if data.get("attachFiles") is not None:
        create_subject_attach_file_db(db=db, attach_files=data.get("attachFiles"), subject_chat_message=new_message.id)

    if data.get("recipient") is not None:
        create_subject_recipient_db(db=db, subject_chat_id=new_message.id, recipient=data.get("recipient"))


def save_answer_data_to_db(db: Session, data: Dict):
    new_answer = create_subject_chat_answer(
        db=db,
        message=data.get("message"),
        subject_chat_id=data.get("messageId"),
        sender_id=data.get("senderId"),
        sender_type=data.get("senderType")
    )

    if data.get("attachFiles") is not None:
        create_subject_attach_file_db(db=db, attach_files=data.get("attachFiles"), subject_chat_answer=new_answer.id)


def update_message_data_to_db(db: Session, data: Dict):
    message = select_message_by_id_db(db=db, message_id=data.get("messageId"))

    if len(message.attach_file) >= 1:
        for attach_file in message.attach_file:
            delete_file(file_path=attach_file.file_path)
            delete_attached_file_db(db=db, file_id=attach_file.id)

    if data.get("attachFiles") is not None:
        create_subject_attach_file_db(db=db, attach_files=data.get("attachFiles"),
                                      subject_chat_message=data.get("messageId"))

    if data.get("message") != message.message or data.get("fixed") != message.fixed:
        update_message_text_and_fixed_db(db=db, new_text=data.get("message"),
                                         fixed=data.get("fixed"), message=message)

    if message.message_type == data.get("messageType"):
        message_data = set_updated_subject_message_dict(message)
        return message_data
    else:
        update_message_type_and_recipient_db(db=db, message_type=data.get("messageType"),
                                             recipients=data.get("recipient"), message=message)
        message_data = set_updated_subject_message_dict(message)
        return message_data


def update_answer_data_to_db(db: Session, data: Dict):
    answer = select_answer_by_id_db(db=db, answer_id=data.get("answerId"))

    if len(answer.attach_file) >= 1:
        for attach_file in answer.attach_file:
            delete_file(attach_file.file_path)
            delete_attached_file_db(db=db, file_id=attach_file.id)

    if data.get("attachFiles") is not None:
        create_subject_attach_file_db(db=db, attach_files=data.get("attachFiles"),
                                      subject_chat_answer=data.get("answerId"))

    message = answer.subject_chat
    result = {
        "messageType": message.message_type,
        "messageSenderId": message.sender_id,
        "messageRecipient": [rec.recipient_id for rec in message.subject_recipient]
        if message.subject_recipient else []
    }

    if answer.message == data.get("answerText"):
        result["answerData"] = set_updated_subject_answer_dict(answer)
        return result
    else:
        update_answer_text_db(db=db, answer_text=data.get("answerText"), answer=answer)
        result["answerData"] = set_updated_subject_answer_dict(answer)
        return result


def delete_message_data_to_db(db: Session, data: Dict):
    message = select_message_by_id_db(db=db, message_id=data.get("messageId"))
    message = delete_message_db(db=db, message=message)

    if message.message_type == "everyone":
        return {"messageType": "everyone"}
    else:
        return {"messageType": "other",
                "recipient": [recipient.recipient_id for recipient in message.subject_recipient]}


def delete_answer_data_to_db(db: Session, data: Dict):
    answer = select_answer_by_id_db(db=db, answer_id=data.get("answerId"))
    answer = delete_answer_db(db=db, answer=answer)
    message = answer.subject_chat

    if message.message_type == "everyone":
        return {"messageType": "everyone"}

    elif message.message_type == "alone":
        return {"messageType": "alone", "messageSenderId": message.sender_id}

    else:
        return {"messageType": "several", "messageSenderId": message.sender_id,
                "recipients": [recipient.recipient_id for recipient in message.subject_recipient]}
