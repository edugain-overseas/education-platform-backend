from sqlalchemy.orm import Session

from app.models import Group
from app.schemas.group_schemas import GroupCreate, GroupUpdate


def create_group_db(db: Session, group_data: GroupCreate):
    new_group = Group(
        group_name=group_data.group_name,
        teacher_id=group_data.teacher_id,
        curator_id=group_data.curator_id,
        specialization_id=group_data.specialization_id
    )
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group


def select_groups_db(db: Session):
    return db.query(Group).all()


def select_group_by_name_db(db: Session, group_name: str):
    return db.query(Group.id).filter(Group.group_name == group_name).first()


def select_group_by_id_db(db: Session, group_id: int):
    return db.query(Group).filter(Group.id == group_id).first()


def select_groups_by_teacher_id_db(db: Session, teacher_id: int):
    return db.query(Group).filter(Group.teacher_id == teacher_id).all()


def select_groups_by_curator_id_db(db: Session, curator_id: int):
    return db.query(Group).filter(Group.curator_id == curator_id).all()


def select_groups_by_specialization_id_db(db: Session, specialization_id: int):
    return db.query(Group).filter(Group.specialization_id == specialization_id).all()


def update_group_db(db: Session, group: Group, group_data: GroupUpdate):
    for field, value in group_data:
        if value:
            setattr(group, field, value)

    db.commit()
    db.refresh(group)


def delete_group_db(db: Session, group: Group):
    db.delete(group)
    db.commit()
