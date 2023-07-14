from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Lesson, LessonType, Subject
from app.schemas.lesson_schemas import Lesson as LessonSchemas
from app.schemas.lesson_schemas import LessonUpdate


def create_new_lesson_db(db: Session, lesson_data: LessonSchemas):
    new_lesson = Lesson(
        number=lesson_data.number,
        title=lesson_data.title,
        description=lesson_data.description,
        is_published=lesson_data.is_published,
        lesson_date=lesson_data.lesson_date,
        lesson_end=lesson_data.lesson_end,
        lesson_type_id=lesson_data.lesson_type_id,
        module_id=lesson_data.module_id,
        subject_id=lesson_data.subject_id,
        teacher_id=lesson_data.teacher_id
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


def select_three_next_lesson_db(db: Session, subject_id: int):
    today = datetime.today()

    query = db.query(Lesson.lesson_date, LessonType.type) \
        .join(Subject, Lesson.subject_id == Subject.id) \
        .join(LessonType, LessonType.id == Lesson.lesson_type_id) \
        .filter(Subject.id == subject_id) \
        .filter(Lesson.is_published == True) \
        .filter(Lesson.lesson_date >= today) \
        .order_by(Lesson.lesson_date).limit(3)

    lessons = query.all()
    lessons_list = []

    for lesson in lessons:
        lesson_dict = {
            "lesson_date": lesson.lesson_date,
            "lesson_type": lesson.type
        }
        lessons_list.append(lesson_dict)

    return lessons_list
