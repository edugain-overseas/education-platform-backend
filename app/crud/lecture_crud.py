from sqlalchemy.orm import Session

from app.models import Lecture, LectureAttribute, LectureFile, LectureValue, Lesson
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
            attr_subtitle=attribute.attr_subtitle,
            attr_number=attribute.attr_number,
            lecture_id=lecture_id
        )
        db.add(attribute_model)
        db.flush()

        value_model = LectureValue(
            value=attribute.value,
            lecture_attribute_id=attribute_model.id
        )

        db.add(value_model)

    db.commit()


def set_file_attr_for_lecture_db(
        db: Session,
        attr_type: str,
        attr_title: str,
        attr_subtitle: str,
        attr_number: int,
        lecture_id: int,
        filename: str,
        file_path: str,
        file_size: int,
        download_allowed: bool

):
    attribute_model = LectureAttribute(
        attr_type=attr_type,
        attr_title=attr_title,
        attr_subtitle=attr_subtitle,
        attr_number=attr_number,
        lecture_id=lecture_id
    )
    db.add(attribute_model)
    db.flush()

    value_model = LectureFile(
        filename=filename,
        file_path=file_path,
        file_size=file_size,
        download_allowed=download_allowed,
        lecture_attribute_id=attribute_model.id
    )

    db.add(value_model)
    db.commit()


def get_lesson_info_db(db: Session, lesson_id: int):
    result = db.query(
        Lesson.title.label("lessonTitle"),
        Lesson.description.label("lessonDescription"),
        Lesson.lesson_date.label("lessonDate"),
        Lesson.lesson_end.label("lessonEnd"),
    )\
        .filter(Lesson.id == lesson_id)\
        .first()

    return result


def get_lecture_db(db: Session, lesson_id: int):
    return db.query(Lecture).filter(Lecture.lesson_id == lesson_id).first()


def get_lecture_text_attribute_db(db: Session, lecture_id: int):
    result = db.query(
        LectureAttribute.id.label("attributeId"),
        LectureAttribute.attr_type.label("attributeType"),
        LectureAttribute.attr_number.label("attributeNumber"),
        LectureAttribute.attr_title.label("attributeTitle"),
        LectureAttribute.attr_subtitle.label("attributeSubTitle"),
        LectureValue.value.label("attributeValue")
    )\
        .join(LectureValue, LectureValue.lecture_attribute_id == LectureAttribute.id) \
        .filter(LectureAttribute.lecture_id == lecture_id) \
        .all()

    return result


def get_lecture_file_attribute_db(db: Session, lecture_id: int):
    result = db.query(
        LectureAttribute.id.label("attributeId"),
        LectureAttribute.attr_type.label("attributeType"),
        LectureAttribute.attr_number.label("attributeNumber"),
        LectureAttribute.attr_title.label("attributeTitle"),
        LectureAttribute.attr_subtitle.label("attributeSubTitle"),
        LectureFile.filename.label("fileName"),
        LectureFile.file_size.label("fileSize"),
        LectureFile.file_path.label("filePath"),
        LectureFile.download_allowed.label("downloadAllowed"),
    )\
        .join(LectureFile, LectureFile.lecture_attribute_id == LectureAttribute.id) \
        .filter(LectureAttribute.lecture_id == lecture_id) \
        .all()

    return result
