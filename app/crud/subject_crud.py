from sqlalchemy.orm import Session

from app.models import Subject, SubjectTeacherAssociation, Group, Teacher
from app.schemas.subject_schemas import SubjectCreate, SubjectUpdate


def create_new_subject_db(db: Session, subject: SubjectCreate):
    is_published = subject.is_published if subject.is_published is not None else False
    exam_date = subject.exam_date if subject.exam_date is not None else None

    new_subject = Subject(
        title=subject.title,
        specialization_id=subject.specialization_id,
        course_id=subject.course_id,
        description=subject.description,
        image_path=None,
        logo_path=None,
        is_published=is_published,
        quantity_lecture=subject.quantity_lecture,
        quantity_seminar=subject.quantity_seminar,
        quantity_test=subject.quantity_test,
        quantity_webinar=subject.quantity_webinar,
        score=subject.score,
        exam_date=exam_date
    )

    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)
    return new_subject


def select_all_subjects_db(db: Session):
    return db.query(Subject).all()


def select_subject_by_id_db(db: Session, subject_id: int):
    return db.query(Subject).filter(Subject.id == subject_id).first()


def select_subjects_by_specialization_db(db: Session, specialization_id: int):
    return db.query(Subject).filter(Subject.specialization_id == specialization_id).all()


def select_subjects_by_course_db(db: Session, course_id: int):
    return db.query(Subject).filter(Subject.course_id == course_id).all()


def select_subjects_by_group_db(db: Session, group_name: str):
    query = db.query(
        Subject.id,
        Subject.title,
        Subject.image_path
    ).join(Group, Group.specialization_id == Subject.specialization_id)\
        .filter(Group.group_name == group_name)

    return query.all()


def update_subject_image_path_db(db: Session, subject: Subject, new_path: str):
    subject.image_path = new_path
    db.commit()
    db.refresh(subject)


def update_subject_logo_path_db(db: Session, subject: Subject, new_path: str):
    subject.logo_path = new_path
    db.commit()
    db.refresh(subject)


def update_subject_info_db(db: Session, subject: Subject, subject_data: SubjectUpdate):
    if subject_data.is_published is None:
        subject_data.is_published = False

    for field, value in subject_data:
        if value is not None:
            setattr(subject, field, value)

    db.commit()
    db.refresh(subject)


def delete_subject_db(db: Session, subject: Subject):
    db.delete(subject)
    db.commit()


def set_teacher_for_subject_db(db: Session, teacher_id: int, subject_id: int):
    new_association = SubjectTeacherAssociation(
        teacher_id=teacher_id,
        subject_id=subject_id
    )

    db.add(new_association)
    db.commit()
    db.refresh(new_association)


def select_teachers_for_subject_db(db: Session, subject_id: int):
    query = db.query(Teacher.id, Teacher.name, Teacher.surname, Teacher.lastname)\
        .join(SubjectTeacherAssociation, SubjectTeacherAssociation.teacher_id == Teacher.id)\
        .join(Subject, Subject.id == SubjectTeacherAssociation.subject_id)\
        .filter(Subject.id == subject_id)

    teachers = query.all()

    teachers_list = []

    for teacher in teachers:
        teacher_dict = {
            "id": teacher.id,
            "name": teacher.name,
            "surname": teacher.surname,
            "lastname": teacher.lastname
        }
        teachers_list.append(teacher_dict)

    return teachers_list
