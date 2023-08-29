from sqlalchemy.orm import Session, joinedload

from app.models import (User, Teacher, SubjectTeacherAssociation,
                        GroupTeacherAssociation, Group, Subject)


def get_teacher_info_db(db: Session, user_id: int):
    teacher_info = db.query(
        Teacher.id,
        Teacher.name,
        Teacher.surname,
        Teacher.image_path,
        Teacher.email
    ).filter(
        Teacher.user_id == user_id
    ).first()

    return teacher_info


def get_teacher_subjects_db(db: Session, user_id: int):
    subjects = db.query(
        Subject.id, Subject.title, Subject.image_path, Subject.group_id, Group.group_name
    ).join(
        SubjectTeacherAssociation,
        Subject.id == SubjectTeacherAssociation.subject_id
    ).join(
        Teacher, Teacher.id == SubjectTeacherAssociation.teacher_id
    ).join(
        Group, Subject.group_id == Group.id
    ).filter(
        Teacher.user_id == user_id
    ).all()

    field_list = [
        'subject_id',
        'subject_title',
        'image_path',
        'group_id',
        'group_name'
    ]

    result_list = []

    for subject in subjects:
        teacher_subject = dict(zip(field_list, subject))
        result_list.append(teacher_subject)

    return result_list
