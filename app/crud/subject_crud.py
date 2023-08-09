from sqlalchemy.orm import Session

from app.models import (Group, StudentAdditionalSubject, Subject, SubjectItem,
                        SubjectTeacherAssociation, Teacher)
from app.schemas.subject_schemas import SubjectCreate, SubjectUpdate


def create_new_subject_db(db: Session, subject: SubjectCreate):
    is_published = subject.is_published if subject.is_published is not None else False
    exam_date = subject.exam_date if subject.exam_date is not None else None

    new_subject = Subject(
        title=subject.title,
        specialization_id=subject.specialization_id,
        course_id=subject.course_id,
        group_id=subject.group_id,
        description=subject.description,
        image_path=None,
        logo_path=None,
        is_published=is_published,
        quantity_lecture=subject.quantity_lecture,
        quantity_seminar=subject.quantity_seminar,
        quantity_test=subject.quantity_test,
        quantity_module=subject.quantity_module,
        score=subject.score,
        exam_date=exam_date
    )

    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)
    return new_subject


def create_subject_item_db(db: Session, subject_id: int, item: str):
    new_item = SubjectItem(
        text=item,
        subject_id=subject_id
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


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
        Subject.image_path)\
        .join(Group, Group.specialization_id == Subject.specialization_id)\
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


def update_subject_item_text_db(db: Session, subject_item: SubjectItem, text: str):
    subject_item.text = text
    db.commit()
    db.refresh(subject_item)
    return subject_item


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
    teachers = db.query(
        Teacher.id, Teacher.name, Teacher.surname, Teacher.lastname, Teacher.email) \
        .join(SubjectTeacherAssociation, SubjectTeacherAssociation.teacher_id == Teacher.id) \
        .filter(SubjectTeacherAssociation.subject_id == subject_id) \
        .all()

    teachers_list = []

    for teacher in teachers:
        teacher_dict = {
            "id": teacher.id,
            "name": teacher.name,
            "surname": teacher.surname,
            "lastname": teacher.lastname,
            "email": teacher.email
        }
        teachers_list.append(teacher_dict)

    return teachers_list


def sign_student_for_addition_subject_db(db: Session, subject_id: int, student_id: int):
    student_addition_subject = StudentAdditionalSubject(
        subject_id=subject_id,
        student_id=student_id
    )

    db.add(student_addition_subject)
    db.commit()
    db.refresh(student_addition_subject)
    return student_addition_subject


def select_dop_subjects(db: Session, student_id: int):
    subjects = db.query(
        Subject.id,
        Subject.title,
        Subject.image_path)\
        .join(StudentAdditionalSubject, StudentAdditionalSubject.subject_id == Subject.id)\
        .filter(StudentAdditionalSubject.student_id == student_id)\
        .all()

    return subjects


def select_subject_exam_date(db: Session, subject_id: int):
    exam_date = db.query(Subject.exam_date).filter(subject_id == subject_id).first()
    return exam_date[0].strftime('%Y-%m-%d')


def select_subject_item_db(db: Session, subject_id: int):
    return db.query(SubjectItem).filter(SubjectItem.subject_id == subject_id).first()
