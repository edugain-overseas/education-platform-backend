from datetime import datetime
from typing import Dict, List

from sqlalchemy import desc, select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql.expression import func

from app.models import (MessageTypeOption, Student, Subject, SubjectChat,
                        SubjectChatAnswer, SubjectChatAttachFile,
                        SubjectRecipient, SubjectTeacherAssociation, Teacher,
                        User, UserType, UserTypeOption)


def select_students_for_subject_db(db: Session, subject_id: int):
    students = db.query(
        User.id,
        User.is_active,
        User.username,
        UserType.type,
        Student.name,
        Student.surname,
        Student.image_path
    ).select_from(Subject).join(
        Student, Student.group_id == Subject.group_id).join(
        User, User.id == Student.user_id).join(
        UserType, UserType.id == User.user_type_id).filter(
        Subject.id == subject_id).all()

    return students


def select_teachers_for_subject_db(db: Session, subject_id: int):
    teachers = db.query(
        User.id,
        User.is_active,
        User.username,
        UserType.type,
        Teacher.name,
        Teacher.surname,
        Teacher.image_path
    ).select_from(Subject).join(
        SubjectTeacherAssociation, SubjectTeacherAssociation.subject_id == Subject.id).join(
        Teacher, Teacher.id == SubjectTeacherAssociation.teacher_id).join(
        User, User.id == Teacher.user_id).join(
        UserType, UserType.id == User.user_type_id).filter(
        Subject.id == subject_id).all()

    return teachers


def create_subject_chat_message(
        db: Session,
        message: str,
        datetime_message: datetime,
        fixed: bool,
        sender_id: int,
        sender_type: UserTypeOption,
        subject_id: int,
        message_type: MessageTypeOption
):
    new_message = SubjectChat(
        message=message,
        datetime_message=datetime_message,
        fixed=fixed,
        sender_id=sender_id,
        sender_type=sender_type,
        subject_id=subject_id,
        message_type=message_type
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message


def create_subject_chat_answer(
        db: Session,
        message: str,
        datetime_message: datetime,
        subject_chat_id: int,
        sender_id: int,
        sender_type: str,
):
    new_answer = SubjectChatAnswer(
        message=message,
        datetime_message=datetime_message,
        subject_chat_id=subject_chat_id,
        sender_id=sender_id,
        sender_type=sender_type
    )

    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)
    return new_answer


def create_subject_attach_file_db(
    db: Session,
    attach_files: List[Dict[str, str]],
    subject_chat_answer: int = None,
    subject_chat_message: int = None
):
    attach_file_objs = []
    for attach_file in attach_files:
        if subject_chat_answer is not None:
            attach_file_obj = SubjectChatAttachFile(
                chat_answer=subject_chat_answer,
                file_path=attach_file['path'],
                mime_type=attach_file['mime-type']
            )

        elif subject_chat_message is not None:
            attach_file_obj = SubjectChatAttachFile(
                chat_message=subject_chat_message,
                file_path=attach_file['path'],
                mime_type=attach_file['mime-type']
            )
        else:
            continue

        db.add(attach_file_obj)
        attach_file_objs.append(attach_file_obj)

    db.commit()
    for attach_file_obj in attach_file_objs:
        db.refresh(attach_file_obj)

    return


def create_subject_recipient_db(
        db: Session,
        subject_chat_id: int,
        recipient: List[int] or int
):
    if isinstance(recipient, list):
        for recip in recipient:
            rec_obj = SubjectRecipient(
                subject_chat_id=subject_chat_id,
                recipient_id=recip
            )
            db.add(rec_obj)
            db.commit()
            db.refresh(rec_obj)
        return
    else:
        recipient_obj = SubjectRecipient(
            subject_chat_id=subject_chat_id,
            recipient_id=recipient
        )
        db.add(recipient_obj)
        db.commit()
        db.refresh(recipient_obj)
        return


def get_last_messages_for_subject_chat_db(
        db: Session,
        subject_id: int,
        recipient_id: int,
        limit: int = 10
):

    query_everyone = db.query(SubjectChat)\
        .filter(SubjectChat.subject_id == subject_id)\
        .filter(SubjectChat.message_type == "everyone")\
        .order_by(desc(SubjectChat.datetime_message))\
        .limit(limit)\
        .options(joinedload(SubjectChat.subject_chat_answer))\
        .options(joinedload(SubjectChat.attach_file))
    messages_everyone = query_everyone.all()

    query_personal = db.query(SubjectChat)\
        .join(SubjectRecipient, SubjectChat.id == SubjectRecipient.subject_chat_id)\
        .filter(SubjectChat.subject_id == subject_id)\
        .filter(SubjectRecipient.recipient_id == recipient_id)\
        .filter(SubjectChat.message_type.in_(["alone", "several"]))\
        .order_by(desc(SubjectChat.datetime_message))\
        .limit(limit)\
        .options(joinedload(SubjectChat.subject_chat_answer))\
        .options(joinedload(SubjectChat.attach_file))
    messages_personal = query_personal.all()

    query_sent_personal = db.query(SubjectChat) \
        .filter(SubjectChat.subject_id == subject_id) \
        .filter(SubjectChat.sender_id == recipient_id) \
        .filter(SubjectChat.message_type.in_(["alone", "several"])) \
        .order_by(desc(SubjectChat.datetime_message)) \
        .limit(limit) \
        .options(joinedload(SubjectChat.subject_chat_answer)) \
        .options(joinedload(SubjectChat.attach_file))
    messages_sent_personal = query_sent_personal.all()

    all_messages = messages_everyone + messages_personal + messages_sent_personal
    all_messages.sort(key=lambda x: x.datetime_message, reverse=True)
    selected_messages = all_messages[:limit]

    return selected_messages


def get_messages_for_subject_chat_by_pagination_db(
        db: Session,
        subject_id: int,
        recipient_id: int,
        last_message_id: int,
        limit: int = 10
):
    query_everyone = db.query(SubjectChat) \
        .filter(SubjectChat.subject_id == subject_id) \
        .filter(SubjectChat.message_type == "everyone") \
        .filter(SubjectChat.id < last_message_id) \
        .order_by(desc(SubjectChat.datetime_message)) \
        .limit(limit) \
        .options(joinedload(SubjectChat.subject_chat_answer)) \
        .options(joinedload(SubjectChat.attach_file))
    messages_everyone = query_everyone.all()

    query_personal = db.query(SubjectChat) \
        .join(SubjectRecipient, SubjectChat.id == SubjectRecipient.subject_chat_id) \
        .filter(SubjectChat.subject_id == subject_id) \
        .filter(SubjectRecipient.recipient_id == recipient_id) \
        .filter(SubjectChat.id < last_message_id) \
        .filter(SubjectChat.message_type.in_(["alone", "several"])) \
        .order_by(desc(SubjectChat.datetime_message)) \
        .limit(limit) \
        .options(joinedload(SubjectChat.subject_chat_answer)) \
        .options(joinedload(SubjectChat.attach_file))
    messages_personal = query_personal.all()

    query_sent_personal = db.query(SubjectChat) \
        .filter(SubjectChat.subject_id == subject_id) \
        .filter(SubjectChat.sender_id == recipient_id) \
        .filter(SubjectChat.message_type.in_(["alone", "several"])) \
        .filter(SubjectChat.id < last_message_id) \
        .order_by(desc(SubjectChat.datetime_message)) \
        .limit(limit) \
        .options(joinedload(SubjectChat.subject_chat_answer)) \
        .options(joinedload(SubjectChat.attach_file))
    messages_sent_personal = query_sent_personal.all()

    all_messages = messages_everyone + messages_personal + messages_sent_personal
    all_messages.sort(key=lambda x: x.datetime_message, reverse=True)
    selected_messages = all_messages[:limit]

    return selected_messages


def select_message_by_id_db(db: Session, message_id: int):
    return db.query(SubjectChat).filter(SubjectChat.id == message_id).first()


def select_recipient_by_message_id(db: Session, message_id: int):
    return db.query(SubjectRecipient).filter(SubjectRecipient.subject_chat_id == message_id).all()


def select_last_message_db(db: Session, subject_id: int, sender_id: int):
    subquery = select(
        SubjectChat.id).filter(
        SubjectChat.sender_id == sender_id,
        SubjectChat.subject_id == subject_id)

    message_obj = db.query(
            SubjectChat.id, SubjectChat.message, SubjectChat.datetime_message,
            SubjectChat.fixed, SubjectChat.message_type,
            SubjectChat.subject_id, SubjectChat.sender_id,
            SubjectChat.sender_type, SubjectChat.read_by,
            func.group_concat(SubjectChatAttachFile.id).label("fileIds"),
            func.group_concat(SubjectChatAttachFile.file_path).label("filePaths"),
            func.group_concat(SubjectChatAttachFile.mime_type).label("mimeTypes"))\
        .join(SubjectChatAttachFile, SubjectChatAttachFile.chat_message == SubjectChat.id, isouter=True)\
        .filter(SubjectChat.id.in_(subquery.scalar_subquery()))\
        .group_by(
            SubjectChat.id, SubjectChat.message, SubjectChat.datetime_message, SubjectChat.fixed,
            SubjectChat.message_type, SubjectChat.subject_id, SubjectChat.sender_id, SubjectChat.sender_type)\
        .order_by(desc(SubjectChat.datetime_message))\
        .limit(1) \
        .first()

    return message_obj


def select_last_answer_db(db: Session, sender_id: int):
    subquery = select(SubjectChatAnswer.id).filter(SubjectChatAnswer.sender_id == sender_id)

    answer_obj = db.query(
            SubjectChatAnswer,
            func.group_concat(SubjectChatAttachFile.id).label("fileIds"),
            func.group_concat(SubjectChatAttachFile.file_path).label("filePaths"),
            func.group_concat(SubjectChatAttachFile.mime_type).label("mimeTypes")) \
        .join(SubjectChatAttachFile, SubjectChatAttachFile.chat_answer == SubjectChatAnswer.id, isouter=True) \
        .filter(SubjectChatAnswer.id.in_(subquery.scalar_subquery())) \
        .group_by(SubjectChatAnswer.id) \
        .order_by(desc(SubjectChatAnswer.datetime_message)) \
        .limit(1) \
        .first()

    return answer_obj


def update_read_by_for_message_db(db: Session, message_id: int, user_id: int):
    message = db.query(SubjectChat).filter(SubjectChat.id == message_id).first()
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


def update_read_by_for_answer_db(db: Session, answer_id: int, user_id: int):
    answer = db.query(SubjectChatAnswer).filter(SubjectChatAnswer.id == answer_id).first()
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
