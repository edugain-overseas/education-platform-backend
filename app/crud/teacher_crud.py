from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models import Group, Lesson, Subject, SubjectTeacherAssociation, Teacher


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

    result_list = []
    field_list = [
        'subject_id',
        'subject_title',
        'image_path',
        'group_id',
        'group_name'
    ]

    for subject in subjects:
        teacher_subject = dict(zip(field_list, subject))
        result_list.append(teacher_subject)

    return result_list


def get_teacher_lessons_db(db: Session, teacher_id: int):
    current_date = datetime.now().date()
    end_date = current_date + timedelta(days=10)

    lessons = db.query(
        Subject.title,
        Lesson.title,
        Lesson.lesson_date,
        Lesson.lesson_end,
        Group.group_name
    ).join(
        Lesson, Subject.id == Lesson.subject_id
    ).join(
        Group, Subject.group_id == Group.id
    ).filter(
        Lesson.teacher_id == teacher_id,
        Lesson.lesson_date >= current_date,
        Lesson.lesson_date < end_date
    ).all()

    return lessons


def get_teacher_by_user_id_db(db: Session, user_id: int):
    teacher = db.query(Teacher).filter(Teacher.user_id == user_id).first()
    return teacher


def update_teacher_image_db(db: Session, teacher: Teacher, image_path: str):
    teacher.image_path = image_path
    db.commit()
    db.refresh(teacher)
    return teacher
