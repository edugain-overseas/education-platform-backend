from sqlalchemy.orm import Session

from app.models import Lesson
from app.schemas.lesson_schemas import LessonUpdate, Lesson as LessonSchemas


def create_new_lesson_db(db: Session, lesson_data: LessonSchemas):
    new_lesson = Lesson(
        number=lesson_data.number,
        title=lesson_data.title,
        description=lesson_data.description,
        is_published=lesson_data.is_published,
        lesson_date=lesson_data.lesson_date,
        lesson_type_id=lesson_data.lesson_type_id,
        module_id=lesson_data.module_id,
        subject_id=lesson_data.subject_id
    )

    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)
    return new_lesson


def update_lesson_db(db: Session, lesson: Lesson, lesson_data: LessonUpdate):
    for filed, value in lesson_data:
        if value:
            setattr(lesson, filed, value)

    db.commit()
    db.refresh(lesson)


def select_all_lessons_db(db: Session):
    return db.query(Lesson).all()


def select_lesson_by_id_db(db: Session, lesson_id: int):
    return db.query(Lesson).filter(Lesson.id == lesson_id).first()


def select_lesson_by_module_db(db: Session, module_id: int):
    return db.query(Lesson).filter(Lesson.module_id == module_id).all()


def select_lesson_by_subject_db(db: Session, subject_id: int):
    return db.query(Lesson).filter(Lesson.subject_id == subject_id).all()


def select_published_lesson_db(db: Session):
    return db.query(Lesson).filter(Lesson.is_published == 1).all()


def select_lesson_by_type_db(db: Session, type_id: int):
    return db.query(Lesson).filter(Lesson.lesson_type_id == type_id).all()


def delete_lesson_db(db: Session, lesson: Lesson):
    db.delete(lesson)
    db.commit()
