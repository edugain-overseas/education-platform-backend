from datetime import datetime
from typing import List, Union

from sqlalchemy import desc, select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql.expression import func

from app.models import (Curator, Group, GroupChat, GroupChatAnswer,
                        GroupChatAttachFile, MessageRecipient,
                        MessageTypeOption, Moder, Student, User, UserType,
                        UserTypeOption)


def select_student_in_group_db(db: Session, group_name: str):
    students = db.query(
        User.id,
        User.is_active,
        User.username,
        UserType.type,
        Student.name,
        Student.surname,
        Student.image_path
    ).select_from(Group).join(
        Student, Student.group_id == Group.id).join(
        User, User.id == Student.user_id).join(
        UserType, UserType.id == User.user_type_id).filter(
        Group.group_name == group_name).all()

    return students


def select_moder_db(db: Session):
    moderators = db.query(
        User.id,
        User.is_active,
        User.username,
        UserType.type
    ).select_from(Moder).join(
        User, User.id == Moder.user_id).join(
        UserType, UserType.id == User.user_type_id).all()

    return moderators


def select_curator_in_group_db(db: Session, group_name: str):
    curator = db.query(
        User.id,
        User.is_active,
        User.username,
        UserType.type,
        Curator.name,
        Curator.surname,
        Curator.image_path
    ).select_from(Group).join(
        Curator, Curator.id == Group.curator_id).join(
        User, User.id == Curator.user_id).join(
        UserType, UserType.id == User.user_type_id).filter(
        Group.group_name == group_name).all()

    return curator


def create_group_chat_massage(
        db: Session,
        message: str,
        datetime_message: datetime,
        fixed: bool,
        sender_id: int,
        sender_type: UserTypeOption,
        group_id: int,
        message_type: MessageTypeOption
):
    new_message = GroupChat(
        message=message,
        datetime_message=datetime_message,
        fixed=fixed,
        sender_id=sender_id,
        sender_type=sender_type,
        group_id=group_id,
        message_type=message_type
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message


def create_group_chat_answer(
        db: Session,
        message: str,
        datetime_message: datetime,
        group_chat_id: int,
        sender_id: int,
        sender_type: str,
):
    new_answer = GroupChatAnswer(
        message=message,
        datetime_message=datetime_message,
        group_chat_id=group_chat_id,
        sender_id=sender_id,
        sender_type=sender_type
    )
    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)
    return new_answer


def create_attach_file_db(
        db: Session,
        attach_files: Union[List[str], str],
        chat_answer: int = None,
        chat_message: int = None
):
    if isinstance(attach_files, str):
        attach_files = [attach_files]

    attach_file_objs = []
    for attach_file in attach_files:
        if chat_message is not None:
            attach_file_obj = GroupChatAttachFile(chat_message=chat_message, file_path=attach_file)
        elif chat_answer is not None:
            attach_file_obj = GroupChatAttachFile(chat_answer=chat_answer, file_path=attach_file)
        else:
            continue

        db.add(attach_file_obj)
        attach_file_objs.append(attach_file_obj)

    db.commit()
    for attach_file_obj in attach_file_objs:
        db.refresh(attach_file_obj)

    return attach_file_objs


def create_recipient_db(
        db: Session,
        group_chat_id: int,
        recipient: List[int] or int
):
    if isinstance(recipient, list):
        for rec in recipient:
            rec_obj = MessageRecipient(
                group_chat_id=group_chat_id,
                recipient_id=rec
            )
            db.add(rec_obj)
            db.commit()
            db.refresh(rec_obj)
        return
    else:
        recipient_obj = MessageRecipient(
            group_chat_id=group_chat_id,
            recipient_id=recipient
        )
        db.add(recipient_obj)
        db.commit()
        db.refresh(recipient_obj)
        return


def select_last_messages_db(db: Session, group_id: int, recipient_id: int, limit: int = 10):

    query_everyone = db.query(GroupChat)\
        .filter(GroupChat.group_id == group_id)\
        .filter(GroupChat.message_type == "everyone")\
        .order_by(desc(GroupChat.datetime_message))\
        .limit(limit)\
        .options(joinedload(GroupChat.group_chat_answer))\
        .options(joinedload(GroupChat.attach_file))
    messages_everyone = query_everyone.all()

    query_personal = db.query(GroupChat)\
        .join(MessageRecipient, GroupChat.id == MessageRecipient.group_chat_id)\
        .filter(GroupChat.group_id == group_id)\
        .filter(MessageRecipient.recipient_id == recipient_id)\
        .filter(GroupChat.message_type.in_(["alone", "several"]))\
        .order_by(desc(GroupChat.datetime_message))\
        .limit(limit)\
        .options(joinedload(GroupChat.group_chat_answer))\
        .options(joinedload(GroupChat.attach_file))
    messages_personal = query_personal.all()

    query_sent_personal = db.query(GroupChat) \
        .filter(GroupChat.group_id == group_id) \
        .filter(GroupChat.sender_id == recipient_id) \
        .filter(GroupChat.message_type.in_(["alone", "several"])) \
        .order_by(desc(GroupChat.datetime_message)) \
        .limit(limit) \
        .options(joinedload(GroupChat.group_chat_answer)) \
        .options(joinedload(GroupChat.attach_file))
    messages_sent_personal = query_sent_personal.all()

    all_messages = messages_everyone + messages_personal + messages_sent_personal
    all_messages.sort(key=lambda x: x.datetime_message, reverse=True)
    selected_messages = all_messages[:limit]

    return selected_messages


def select_message_by_id_db(db: Session, message_id: int):
    return db.query(GroupChat).filter(GroupChat.id == message_id).first()


def select_recipient_by_message_id(db: Session, message_id: int):
    return db.query(MessageRecipient).filter(MessageRecipient.group_chat_id == message_id).all()


def get_last_messages_db(group_id: int, recipient_id: int, db: Session):
    group_chat_messages = select_last_messages_db(db=db, group_id=group_id, recipient_id=recipient_id)
    messages_data = {"messages": []}

    for message in group_chat_messages:
        message_data = {
            "message_id": message.id,
            "message_text": message.message,
            "message_type": message.message_type.value,
            "message_fixed": message.fixed,
            "message_datetime": message.datetime_message.strftime("%d.%m.%Y %H:%M:%S"),
            "group_id": message.group_id,
            "sender_id": message.sender_id,
            "sender_type": message.sender_type.value,
            "read_by": message.read_by.split(", ") if message.read_by else [],
            "answers": [],
            "attach_files": []
        }

        for answer in message.group_chat_answer:
            answer_data = {
                "answer_id": answer.id,
                "answer": answer.message,
                "answer_datetime": answer.datetime_message.strftime("%d.%m.%Y %H:%M:%S"),
                "sender_id": answer.sender_id,
                "sender_type": answer.sender_type.value,
                "read_by": answer.read_by.split(", ") if answer.read_by else []
            }
            message_data["answers"].append(answer_data)

        for file in message.attach_file:
            file_data = {
                "fileId": file.id,
                "file_path": file.file_path
            }
            message_data["attach_files"].append(file_data)

        messages_data["messages"].append(message_data)
    return messages_data


def get_last_message_db(db: Session, group_id: int, sender_id: int):
    subquery = select(GroupChat.id).filter(GroupChat.sender_id == sender_id,
                                           GroupChat.group_id == group_id)

    query = db.query(
        GroupChat.id,
        GroupChat.message,
        GroupChat.datetime_message,
        GroupChat.fixed,
        GroupChat.message_type,
        GroupChat.group_id,
        GroupChat.sender_id,
        GroupChat.sender_type,
        GroupChat.read_by,
        func.group_concat(GroupChatAttachFile.file_path).label("file_paths")
    ).join(GroupChatAttachFile, GroupChatAttachFile.chat_message == GroupChat.id, isouter=True)\
        .filter(GroupChat.id.in_(subquery.scalar_subquery())).group_by(
        GroupChat.id,
        GroupChat.message,
        GroupChat.datetime_message,
        GroupChat.fixed,
        GroupChat.message_type,
        GroupChat.group_id,
        GroupChat.sender_id,
        GroupChat.sender_type
    ).order_by(desc(GroupChat.datetime_message)).limit(1)

    result = query.first()

    message = {
        "message_id": result.id,
        "message_text": result.message,
        "message_type": result.message_type.value,
        "message_fixed": result.fixed,
        "message_datetime": result.datetime_message.strftime("%d.%m.%Y %H:%M:%S"),
        "group_id": result.group_id,
        "sender_id": result.sender_id,
        "sender_type": result.sender_type.value,
        "read_by": result.read_by.split(", ") if result.read_by else [],
        "attach_files": result.file_paths.split(",") if result.file_paths else []
    }

    return message


def get_last_answer_db(db: Session, sender_id: int):
    query = db.query(
        GroupChatAnswer,
        func.group_concat(GroupChatAttachFile.file_path).label("file_paths")
    ).join(GroupChatAttachFile, GroupChatAttachFile.chat_answer == GroupChatAnswer.id, isouter=True)\
        .filter(GroupChatAnswer.sender_id == sender_id)\
        .order_by(desc(GroupChatAnswer.datetime_message)).limit(1)

    result = query.first()
    answer = {
        "answer_id": result[0].id,
        "answer_text": result[0].message,
        "answer_datetime": result[0].datetime_message.strftime("%d.%m.%Y %H:%M:%S"),
        "message_id": result[0].group_chat.id,
        "sender_id": result[0].sender_id,
        "sender_type": result[0].sender_type,
        "read_by": result[0].read_by.split(", ") if result[0].read_by else [],
        "attach_files": result[1].split(",") if result.file_paths else []
    }

    return answer


def update_message_read_by_db(db: Session, message_id: int, user_id: int):
    message = db.query(GroupChat).filter(GroupChat.id == message_id).first()
    if message.read_by is not None:
        read_by_list = list(map(int, message.read_by.split(", ")))
        read_by_list.append(user_id)
        read_by_str = ", ".join(map(str, read_by_list))
        message.read_by = read_by_str
        db.commit()
        db.refresh(message)
        return message
    message.read_by = str(user_id)
    db.commit()
    db.refresh(message)
    return message


def update_answer_read_by_db(db: Session, answer_id: int, user_id: int):
    answer = db.query(GroupChatAnswer).filter(GroupChatAnswer.id == answer_id).first()
    if answer.read_by is not None:
        read_by_list = list(map(int, answer.read_by.split(", ")))
        read_by_list.append(user_id)
        read_by_str = ", ".join(map(str, read_by_list))
        answer.read_by = read_by_str
        db.commit()
        db.refresh(answer)
        return answer
    answer.read_by = str(user_id)
    db.commit()
    db.refresh(answer)
    return answer
