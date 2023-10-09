from sqlalchemy.orm import Session

from app.models import Curator, Group, ParticipantComment, Student, User
from app.schemas.group_schemas import GroupCreate, GroupUpdate


def create_group_db(db: Session, group_data: GroupCreate):
    new_group = Group(
        group_name=group_data.group_name,
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


def select_group_curator_db(db: Session, group_id: int):
    curator_data = db.query(
        Curator.id,
        Curator.name,
        Curator.surname,
        Curator.email,
        Curator.image_path,
        User.last_active
    )\
        .join(Group, Group.curator_id == Curator.id)\
        .join(User, Curator.user_id == User.id)\
        .filter(Group.id == group_id)\
        .first()

    fields = ['id', 'name', 'surname', 'email', 'image_path', 'last_active']
    curator = dict(zip(fields, curator_data))

    return curator


def select_group_students_db(db: Session, group_id: int, subject_id: int):
    students = db.query(
        Student.id,
        Student.name,
        Student.surname,
        Student.email,
        Student.image_path,
        User.last_active
    )\
        .join(User, Student.user_id == User.id)\
        .filter(Student.group_id == group_id)\
        .all()

    students_list = []

    for student in students:
        participant_comment = db.query(ParticipantComment).\
            filter(ParticipantComment.student_id == student.id and
                   ParticipantComment.student_id == subject_id).first()

        student_data = {
            "id": student.id,
            "name": student.name,
            "surname": student.surname,
            "email": student.email,
            "image_path": student.image_path,
            "last_active": student.last_active,
            "participant_comment": participant_comment.comment if participant_comment else None
        }

        students_list.append(student_data)

    return students_list
