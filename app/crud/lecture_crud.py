from sqlalchemy.orm import Session

from app.enums import LectureAttributeType
from app.models import Lecture, LectureAttribute, LectureFile, LectureLink, StudentLecture


def create_lecture_db(db: Session, lesson_id: int) -> object:
    new_lecture = Lecture(lesson_id=lesson_id)
    db.add(new_lecture)
    db.commit()
    db.refresh(new_lecture)
    return new_lecture


def get_lecture_db(db: Session, lesson_id: int):
    return db.query(Lecture).filter(Lecture.lesson_id == lesson_id).first()


def create_attribute_base_db(
        db: Session,
        lecture_id: int,
        attr_type: LectureAttributeType,
        attr_title: str,
        attr_text: str,
        attr_number: int,
        hided: bool
):
    attribute = LectureAttribute(
        attr_type=attr_type,
        attr_title=attr_title,
        attr_text=attr_text,
        attr_number=attr_number,
        hided=hided,
        lecture_id=lecture_id
    )
    db.add(attribute)
    db.commit()
    db.refresh(attribute)
    return attribute


def update_attribute_db(
        db: Session,
        attribute: LectureAttribute,
        title: str = None,
        text: str = None,
        number: int = None,
        hided: bool = None
):
    if title is not None:
        attribute.attr_title = title
    if text is not None:
        attribute.attr_text = text
    if number is not None:
        attribute.attr_number = number
    if hided is not None:
        attribute.hided = hided

    db.commit()
    db.refresh(attribute)
    return attribute


def delete_attribute_db(db: Session, attribute: LectureAttribute):
    db.delete(attribute)
    db.commit()


def create_attribute_file_db(
        db: Session,
        attribute_id: int,
        filename: str,
        file_path: str,
        file_size: int,
        download_allowed: bool
):
    file = LectureFile(
        filename=filename,
        file_path=file_path,
        file_size=file_size,
        download_allowed=download_allowed,
        lecture_attribute_id=attribute_id
    )
    db.add(file)
    db.commit()
    db.refresh(file)


def create_attribute_file_with_description_db(
        db: Session,
        attribute_id: int,
        filename: str,
        file_path: str,
        file_size: int,
        file_description: str,
        download_allowed: bool
):
    file = LectureFile(
        filename=filename,
        file_path=file_path,
        file_size=file_size,
        file_description=file_description,
        download_allowed=download_allowed,
        lecture_attribute_id=attribute_id
    )
    db.add(file)
    db.commit()
    db.refresh(file)


def update_attribute_file_db(
        db: Session,
        file: LectureFile,
        file_path: str = None,
        filename: str = None,
        file_size: str = None,
        download_allowed: bool = None
):
    if file_path is not None:
        file.file_path = file_path
    if filename is not None:
        file.filename = filename
    if file_size is not None:
        file.file_size = file_size
    if download_allowed is not None:
        file.download_allowed = download_allowed
    db.commit()
    db.refresh(file)


def delete_attribute_file_db(db: Session, file: LectureFile):
    db.delete(file)
    db.commit()


def create_attribute_link_db(db: Session, attribute_id: int, link: str, anchor: str):
    link = LectureLink(link=link, anchor=anchor, lecture_attribute_id=attribute_id)
    db.add(link)
    db.commit()
    db.refresh(link)


def update_attribute_link_db(db: Session, attr_link: LectureLink, link: str = None, anchor: str = None):
    if link is not None:
        attr_link.link = link
    if anchor is not None:
        attr_link.anchor = anchor
    db.commit()
    db.refresh(link)


def delete_attribute_link_db(db: Session, link: LectureLink):
    db.delete(link)
    db.commit()


def get_lecture_attributes_db(db: Session, lecture_id: int):
    return db.query(LectureAttribute).filter(LectureAttribute.lecture_id == lecture_id).all()


def get_lecture_text_attribute_db(db: Session, lecture_id: int):
    result = db.query(
        LectureAttribute.id.label("attributeId"),
        LectureAttribute.attr_type.label("attributeType"),
        LectureAttribute.attr_number.label("attributeNumber"),
        LectureAttribute.attr_title.label("attributeTitle"),
        LectureAttribute.attr_text.label("attributeText"),
        LectureAttribute.hided.label("hided")
    )\
        .filter(LectureAttribute.lecture_id == lecture_id) \
        .all()

    return result


def get_attribute_db(db: Session, attr_id: int):
    return db.query(LectureAttribute).filter(LectureAttribute.id == attr_id).first()


def get_attribute_file_db(db: Session, file_id: int):
    return db.query(LectureFile).filter(LectureFile.id == file_id).first()


def get_attribute_link_db(db: Session, link_id: int):
    return db.query(LectureLink).filter(LectureLink.id == link_id).first()


def check_lecture_db(db: Session, student_id: int, lecture_id: int):
    new_row = StudentLecture(
        check=True,
        student_id=student_id,
        lecture_id=lecture_id
    )
    db.add(new_row)
    db.commit()
    db.refresh(new_row)
    return new_row
