from sqlalchemy.orm import Session

from app.models import (Lesson, OrdinaryLesson, OrdinaryLessonAttribute,
                        OrdinaryLessonValue)
from app.schemas.lecture_schemas import LectureTextCreate


def create_ordinary_lesson_db(db: Session, lesson_id: int):
    new_ordinary_lesson = OrdinaryLesson(lesson_id=lesson_id)
    db.add(new_ordinary_lesson)
    db.commit()
    db.refresh(new_ordinary_lesson)
    return new_ordinary_lesson


def set_text_attr_for_lecture_db(db: Session, item: LectureTextCreate, lecture_id: int):
    for attribute in item.attributes:

        attribute_model = OrdinaryLessonAttribute(
            attribute_name=attribute.name,
            ordinary_lesson_id=lecture_id
        )
        db.add(attribute_model)
        db.flush()

        value_model = OrdinaryLessonValue(
            value=attribute.value,
            ordinary_lesson_id=lecture_id,
            ordinary_lesson_attribute_id=attribute_model.id
        )

        db.add(value_model)

    db.commit()


def set_file_attr_for_lecture_db(db: Session, file_path: str, name: str, lecture_id: int):
    attribute_model = OrdinaryLessonAttribute(
        attribute_name=name,
        ordinary_lesson_id=lecture_id
    )
    db.add(attribute_model)
    db.flush()

    value_model = OrdinaryLessonValue(
        value=file_path,
        ordinary_lesson_id=lecture_id,
        ordinary_lesson_attribute_id=attribute_model.id
    )

    db.add(value_model)
    db.commit()


def get_lecture_info_db(db: Session, lesson_id: int):
    result = db.query(
        Lesson.title,
        Lesson.description,
        Lesson.lesson_date,
        Lesson.number,
        OrdinaryLessonAttribute.attribute_name,
        OrdinaryLessonValue.value
    )\
        .join(OrdinaryLesson, OrdinaryLesson.lesson_id == Lesson.id)\
        .join(OrdinaryLessonAttribute, OrdinaryLessonAttribute.ordinary_lesson_id == OrdinaryLesson.id)\
        .join(OrdinaryLessonValue, OrdinaryLessonValue.ordinary_lesson_attribute_id == OrdinaryLessonAttribute.id)\
        .filter(Lesson.id == lesson_id).all()

    return result
