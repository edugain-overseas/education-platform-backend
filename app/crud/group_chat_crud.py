from datetime import datetime
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models import User, UserType, Student, Curator, Moder, Group, GroupChat, GroupChatAnswer


def select_student_in_group_db(db: Session, group_name: str):
    students = db.query(
        User.id,
        User.is_active,
        User.username,
        UserType.type
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
        UserType.type
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
        sender_type: str,
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
