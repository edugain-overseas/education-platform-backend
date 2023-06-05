from sqlalchemy.orm import Session

from app.models import Specialization
from app.schemas.specialization_schemas import SpecializationCreate


def create_specialization_db(db: Session, data: SpecializationCreate):
    specialization = Specialization(title=data.title, course_id=data.course_id)
    db.add(specialization)
    db.commit()
    db.refresh(specialization)
    return specialization


def update_specialization_title_db(db: Session, title: str, specialization: Specialization):
    specialization.title = title
    db.commit()
    db.refresh(specialization)


def select_specialization_by_id_db(db: Session, spec_id: int):
    return db.query(Specialization).filter(Specialization.id == spec_id).first()


def select_specializations_by_course_id_db(db: Session, course_id: int):
    return db.query(Specialization).filter(Specialization.course_id == course_id).all()


def select_specializations_db(db: Session):
    return db.query(Specialization).all()


def delete_specialization_db(db: Session, specialization: Specialization):
    db.delete(specialization)
    db.commit()
