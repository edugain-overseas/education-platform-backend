from sqlalchemy.orm import Session

from app.models import Lecture, LectureAttribute, LectureValue, Lesson
from app.schemas.lecture_schemas import LectureTextCreate


def create_lecture_db(db: Session, lesson_id: int):
    new_lecture = Lecture(lesson_id=lesson_id)
    db.add(new_lecture)
    db.commit()
    db.refresh(new_lecture)
    return new_lecture


def set_text_attr_for_lecture_db(db: Session, item: LectureTextCreate, lecture_id: int):
    for attribute in item.attributes:

        attribute_model = LectureAttribute(
            attr_type=attribute.attr_type,
            attr_title=attribute.attr_title,
            attr_number=attribute.attr_number,
            download_allowed=attribute.download_allowed,
            lecture_id=lecture_id
        )
        db.add(attribute_model)
        db.flush()

        value_model = LectureValue(
            value=attribute.value,
            lecture_id=lecture_id,
            lecture_attribute_id=attribute_model.id
        )

        db.add(value_model)

    db.commit()


def set_file_attr_for_lecture_db(
        db: Session,
        attr_type: str,
        attr_title: str,
        attr_number: int,
        download_allowed: bool,
        lecture_id: int,
        file_path: str,

):
    attribute_model = LectureAttribute(
        attr_type=attr_type,
        attr_title=attr_title,
        attr_number=attr_number,
        download_allowed=download_allowed,
        lecture_id=lecture_id
    )
    db.add(attribute_model)
    db.flush()

    value_model = LectureValue(
        value=file_path,
        lecture_id=lecture_id,
        lecture_attribute_id=attribute_model.id
    )

    db.add(value_model)
    db.commit()


def get_lecture_info_db(db: Session, lesson_id: int):
    result = db.query(
        Lesson.title,
        Lesson.description,
        Lesson.lesson_date,
        Lesson.lesson_end,
        LectureAttribute.attr_number,
        LectureAttribute.download_allowed,
        LectureAttribute.attr_type,
        LectureAttribute.attr_title,
        LectureValue.value
    )\
        .join(Lecture, Lecture.lesson_id == Lesson.id)\
        .join(LectureAttribute, LectureAttribute.lecture_id == Lecture.id)\
        .join(LectureValue, LectureValue.lecture_attribute_id == LectureAttribute.id)\
        .filter(Lesson.id == lesson_id).all()

    return result
