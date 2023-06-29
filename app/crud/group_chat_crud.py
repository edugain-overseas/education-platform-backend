from datetime import datetime

from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload

from app.models import (Curator, Group, GroupChat, GroupChatAnswer, Moder,
                        Student, User, UserType, UserTypeOption)


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
        Curator.surname
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
        group_id: int
):
    new_message = GroupChat(
        message=message,
        datetime_message=datetime_message,
        fixed=fixed,
        sender_id=sender_id,
        sender_type=sender_type,
        group_id=group_id
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


def select_last_message_db(db: Session, group_id: int, limit: int = None):
    if limit is None:
        messages = db.query(
            GroupChat).filter(GroupChat.group_id == group_id).order_by(
            desc(GroupChat.datetime_message)).limit(10).all()
        return messages
    else:
        messages = db.query(
            GroupChat).filter(GroupChat.group_id == group_id).order_by(
            desc(GroupChat.datetime_message)).limit(limit).all()
        return messages


def select_last_messages_db(db: Session, group_id: int, limit: int = 10):
    query = db.query(
        GroupChat)\
        .filter(GroupChat.group_id == group_id)\
        .order_by(
        desc(GroupChat.datetime_message))\
        .limit(10)\
        .options(joinedload(GroupChat.group_chat_answer))

    group_chat_messages = query.all()
    return group_chat_messages


def select_student_name_and_photo_db(db: Session, user_id: int):
    return db.query(Student.user_id, Student.name, Student.surname, Student.image_path).\
        filter(Student.user_id == user_id).first()


def select_curator_name_db(db: Session, user_id):
    return db.query(Curator.user_id, Curator.name, Curator.surname)\
        .filter(Curator.user_id == user_id).first()


def get_last_messages_db(group_id: int, db: Session):
    group_chat_messages = select_last_messages_db(db=db, group_id=group_id)
    messages_data = {"messages": []}

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

        messages_data["messages"].append(message_data)

    return messages_data
