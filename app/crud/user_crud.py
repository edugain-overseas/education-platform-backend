from datetime import date, datetime

from sqlalchemy.orm import Session

from app.models import Curator, Moder, Student, Teacher, User, UserType
from app.schemas.user_schemas import StudentUpdate


def select_user_type_id_db(db: Session, user_type: str):
    return db.query(UserType).filter(UserType.type == user_type).first()


def select_user_type_by_user_id_db(db: Session, user_id: int):
    user_type = db.query(UserType.type).join(User).filter(User.id == user_id).first()
    return user_type


def select_user_by_username_db(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def select_user_by_id_db(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def select_all_students_db(db: Session):
    return db.query(Student).all()


def select_student_by_id_db(db: Student, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()


def select_student_by_user_id_db(db: Session, user_id: int):
    return db.query(Student).filter(Student.user_id == user_id).first()


def select_students_by_group_id_db(db: Student, group_id: int):
    return db.query(Student).filter(Student.group_id == group_id).all()


def select_students_by_course_id_db(db: Student, course_id: int):
    return db.query(Student).filter(Student.course_id == course_id).all()


def select_students_by_specializations_id_db(db: Session, specialization_id: int):
    return db.query(Student).filter(Student.specialization_id == specialization_id).all()


def update_user_token_db(db: Session, user: User, token: str, exp_token: datetime):
    user.token = token
    user.exp_token = exp_token
    user.is_active = True
    db.commit()
    db.refresh(user)


def update_student_photo_path_db(db: Session, student: Student, new_path: str):
    student.image_path = new_path
    db.commit()
    db.refresh(student)


def update_student_info_db(db: Session, student: Student, student_data: StudentUpdate):
    for field, value in student_data:
        if value:
            setattr(student, field, value)

    db.commit()
    db.refresh(student)


def create_new_user_db(db: Session, username: str, hashed_password: str, user_type_id: int):
    new_user = User(
        username=username,
        hashed_pass=hashed_password,
        user_type_id=user_type_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def create_new_student_db(
        db: Session,
        name: str,
        surname: str,
        lastname: str,
        phone: str,
        email: str,
        user_id: int
):
    new_student = Student(
        name=name,
        surname=surname,
        lastname=lastname,
        phone=phone,
        email=email,
        user_id=user_id,
        date_added=date.today()
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


def create_new_teacher_db(
        db: Session,
        name: str,
        surname: str,
        lastname: str,
        user_id: int,
        email: str
):
    new_teacher = Teacher(
        name=name,
        surname=surname,
        lastname=lastname,
        user_id=user_id,
        email=email
    )

    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    return new_teacher


def create_new_moder_db(db: Session, name: str, surname: str, lastname: str, user_id: int):
    new_moder = Moder(
        name=name,
        surname=surname,
        lastname=lastname,
        user_id=user_id
    )

    db.add(new_moder)
    db.commit()
    db.refresh(new_moder)
    return new_moder


def create_new_curator_db(
        db: Session,
        name: str,
        surname: str,
        lastname: str,
        user_id: int,
        email: str
):
    new_curator = Curator(
        name=name,
        surname=surname,
        lastname=lastname,
        user_id=user_id,
        email=email
    )

    db.add(new_curator)
    db.commit()
    db.refresh(new_curator)
    return new_curator


def delete_user_db(db: Session, user: User):
    db.delete(user)
    db.commit()


def delete_student_db(db: Session, student: Student):
    db.delete(student)
    db.commit()
