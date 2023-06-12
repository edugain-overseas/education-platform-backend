from sqlalchemy.orm import Session
from app.models import Subject
from app.schemas.subject_schemas import Subject as SubjectBase, SubjectCreate, SubjectUpdate


def create_new_subject_db(db: Session, subject: SubjectCreate):
    is_published = subject.is_published if subject.is_published is not None else False

    new_subject = Subject(
        title=subject.title,
        specialization_id=subject.specialization_id,
        course_id=subject.course_id,
        description=subject.description,
        image_path=subject.image_path,
        logo_path=subject.logo_path,
        is_published=is_published,
        quantity_lecture=subject.quantity_lecture,
        quantity_seminar=subject.quantity_seminar,
        quantity_test=subject.quantity_test,
        quantity_webinar=subject.quantity_webinar,
        score=subject.score
    )

    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)
    return new_subject


def select_all_subjects_db(db: Session):
    return db.query(Subject).all()


def select_subject_by_id_db(db: Session, subject_id: int):
    return db.query(Subject).filter(Subject.id == subject_id).first()


# def select_subjects_by_teacher_db(db: Session, teacher_id: int):
#     return db.query(Subject).filter(Subject.teacher_id == teacher_id).all()


def select_subjects_by_specialization_db(db: Session, specialization_id: int):
    return db.query(Subject).filter(Subject.specialization_id == specialization_id).all()


def select_subjects_by_course_db(db: Session, course_id: int):
    return db.query(Subject).filter(Subject.course_id == course_id).all()


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
