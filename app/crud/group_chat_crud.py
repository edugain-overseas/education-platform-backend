from datetime import datetime
from typing import Dict, List

from sqlalchemy import desc, select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql.expression import func

from app.enums import UserTypeOption, MessageTypeOption
from app.models import (Curator, Group, GroupChat, GroupChatAnswer, GroupChatAttachFile, MessageRecipient,
                        Moder, Student, User, UserType)


def select_student_in_group_db(db: Session, group_id: int):
    students = db.query(
        User.id,
        User.is_active,
        User.username,
        UserType.type,
        Student.name,
        Student.surname,
        Student.image_path
    )\
        .select_from(Group)\
        .join(Student, Student.group_id == Group.id)\
        .join(User, User.id == Student.user_id)\
        .join(UserType, UserType.id == User.user_type_id)\
        .filter(Group.id == group_id)\
        .all()

    return students


def select_moder_db(db: Session):
    moderators = db.query(
        User.id,
        User.is_active,
        User.username,
        UserType.type
    )\
        .select_from(Moder)\
        .join(User, User.id == Moder.user_id)\
        .join(UserType, UserType.id == User.user_type_id)\
        .all()

    return moderators


def select_curator_in_group_db(db: Session, group_id: int):
    curator = db.query(
        User.id,
        User.is_active,
        User.username,
        UserType.type,
        Curator.name,
        Curator.surname,
        Curator.image_path
    )\
        .select_from(Group)\
        .join(Curator, Curator.id == Group.curator_id)\
        .join(User, User.id == Curator.user_id)\
        .join(UserType, UserType.id == User.user_type_id)\
        .filter(Group.id == group_id)\
        .all()

    return curator


def create_group_chat_massage(
        db: Session,
        message: str,
        fixed: bool,
        sender_id: int,
        sender_type: UserTypeOption,
        group_id: int,
        message_type: MessageTypeOption
):
    new_message = GroupChat(
        message=message,
        datetime_message=datetime.utcnow(),
        fixed=fixed,
        sender_id=sender_id,
        sender_type=sender_type,
        group_id=group_id,
        message_type=message_type,
        deleted=False
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message


def create_group_chat_answer(
        db: Session,
        message: str,
        group_chat_id: int,
        sender_id: int,
        sender_type: str,
):
    new_answer = GroupChatAnswer(
        message=message,
        datetime_message=datetime.utcnow(),
        group_chat_id=group_chat_id,
        sender_id=sender_id,
        sender_type=sender_type,
        deleted=False
    )
    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)
    return new_answer


def create_attach_file_db(
        db: Session,
        attach_files: List[Dict[str, str]],
        chat_answer: int = None,
        chat_message: int = None
):
    attach_file_objs = []
    for attach_file in attach_files:
        if chat_message is not None:
            attach_file_obj = GroupChatAttachFile(
                chat_message=chat_message,
                file_path=attach_file['path'],
                mime_type=attach_file['type'],
                filename=attach_file['filename'],
                size=attach_file['size']
            )

        elif chat_answer is not None:
            attach_file_obj = GroupChatAttachFile(
                chat_answer=chat_answer,
                file_path=attach_file['path'],
                mime_type=attach_file['type'],
                filename=attach_file['filename'],
                size=attach_file['size']
            )
        else:
            continue

        db.add(attach_file_obj)
        attach_file_objs.append(attach_file_obj)

    db.commit()
    for attach_file_obj in attach_file_objs:
        db.refresh(attach_file_obj)


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


def select_last_messages_db(
        db: Session,
        group_id: int,
        recipient_id: int,
        limit: int = 10
):

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


def select_messages_by_pagination_db(
        db: Session,
        group_id: int,
        recipient_id: int,
        last_message_id: int,
        limit: int = 10
):
    query_everyone = db.query(GroupChat) \
        .filter(GroupChat.group_id == group_id) \
        .filter(GroupChat.message_type == "everyone") \
        .filter(GroupChat.id < last_message_id) \
        .order_by(desc(GroupChat.datetime_message)) \
        .limit(limit) \
        .options(joinedload(GroupChat.group_chat_answer)) \
        .options(joinedload(GroupChat.attach_file))
    messages_everyone = query_everyone.all()

    query_personal = db.query(GroupChat) \
        .join(MessageRecipient, GroupChat.id == MessageRecipient.group_chat_id) \
        .filter(GroupChat.group_id == group_id) \
        .filter(MessageRecipient.recipient_id == recipient_id) \
        .filter(GroupChat.id < last_message_id) \
        .filter(GroupChat.message_type.in_(["alone", "several"])) \
        .order_by(desc(GroupChat.datetime_message)) \
        .limit(limit) \
        .options(joinedload(GroupChat.group_chat_answer)) \
        .options(joinedload(GroupChat.attach_file))
    messages_personal = query_personal.all()

    query_sent_personal = db.query(GroupChat) \
        .filter(GroupChat.group_id == group_id) \
        .filter(GroupChat.sender_id == recipient_id) \
        .filter(GroupChat.message_type.in_(["alone", "several"])) \
        .filter(GroupChat.id < last_message_id) \
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


def select_answer_by_id_db(db: Session, answer_id: int):
    return db.query(GroupChatAnswer).filter(GroupChatAnswer.id == answer_id).first()


def select_recipient_by_message_id(db: Session, message_id: int):
    return db.query(MessageRecipient).filter(MessageRecipient.group_chat_id == message_id).all()


def get_last_message_db(db: Session, group_id: int, sender_id: int):
    subquery = (select(GroupChat.id)
                .filter(GroupChat.sender_id == sender_id, GroupChat.group_id == group_id))

    message_obj = db.query(
        GroupChat.id,
        GroupChat.message,
        GroupChat.datetime_message,
        GroupChat.fixed,
        GroupChat.message_type,
        GroupChat.group_id,
        GroupChat.sender_id,
        GroupChat.sender_type,
        GroupChat.deleted,
        GroupChat.read_by,
        func.group_concat(GroupChatAttachFile.id).label("fileIds"),
        func.group_concat(GroupChatAttachFile.file_path).label("filePaths"),
        func.group_concat(GroupChatAttachFile.mime_type).label("mimeTypes"),
        func.group_concat(GroupChatAttachFile.filename).label("fileNames"),
        func.group_concat(GroupChatAttachFile.size).label("fileSizes")
    ) \
        .join(GroupChatAttachFile, GroupChatAttachFile.chat_message == GroupChat.id, isouter=True) \
        .filter(GroupChat.id.in_(subquery.scalar_subquery())) \
        .group_by(
        GroupChat.id,
        GroupChat.message,
        GroupChat.datetime_message,
        GroupChat.fixed,
        GroupChat.message_type,
        GroupChat.group_id,
        GroupChat.sender_id,
        GroupChat.sender_type
    ) \
        .order_by(desc(GroupChat.datetime_message)) \
        .limit(1) \
        .first()

    return message_obj


def get_last_answer_db(db: Session, sender_id: int):
    subquery = select(GroupChatAnswer.id).filter(GroupChatAnswer.sender_id == sender_id)

    answer_obj = db.query(
        GroupChatAnswer,
        func.group_concat(GroupChatAttachFile.id).label("fileIds"),
        func.group_concat(GroupChatAttachFile.file_path).label("filePaths"),
        func.group_concat(GroupChatAttachFile.mime_type).label("mimeTypes"),
        func.group_concat(GroupChatAttachFile.filename).label("fileNames"),
        func.group_concat(GroupChatAttachFile.size).label("fileSizes")
    )\
        .join(GroupChatAttachFile, GroupChatAttachFile.chat_answer == GroupChatAnswer.id, isouter=True) \
        .filter(GroupChatAnswer.id.in_(subquery.scalar_subquery())) \
        .group_by(GroupChatAnswer.id) \
        .order_by(desc(GroupChatAnswer.datetime_message)) \
        .limit(1) \
        .first()

    return answer_obj


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


def delete_message_db(db: Session, message: GroupChat):
    message.deleted = True
    db.commit()
    db.refresh(message)
    return message


def delete_answer_db(db: Session, answer: GroupChatAnswer):
    answer.deleted = True
    db.commit()
    db.refresh(answer)
    return answer


def update_message_text_and_fixed_db(db: Session, new_text: str, fixed: bool, message: GroupChat):
    message.message = new_text
    message.fixed = fixed
    db.commit()
    db.refresh(message)
    return message


def update_message_type_db(db: Session, message_type: str, recipients: List[int], message: GroupChat):
    db_recipients = db.query(MessageRecipient).filter(MessageRecipient.group_chat_id == message.id).all()
    for recipient in db_recipients:
        db.delete(recipient)
        db.commit()

    message.message_type = message_type
    db.commit()
    db.refresh(message)

    create_recipient_db(db=db, group_chat_id=message.id, recipient=recipients)
    return message


def update_answer_text_db(db: Session, answer_text: str, answer: GroupChatAnswer):
    answer.message = answer_text
    db.commit()
    db.refresh(answer)
    return answer


def delete_attached_file_db(db: Session, file_id: int):
    attach_file = db.query(GroupChatAttachFile).filter(GroupChatAttachFile.id == file_id).first()
    db.delete(attach_file)
    db.commit()
