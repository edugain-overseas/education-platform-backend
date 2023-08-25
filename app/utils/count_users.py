from sqlalchemy.orm import Session

from app.crud.group_chat_crud import (select_curator_in_group_db,
                                      select_student_in_group_db)
from app.crud.subject_chat_crud import (select_students_for_subject_db,
                                        select_teachers_for_subject_db)


def select_users_in_group(group_name: str, db: Session) -> list[tuple]:
    users = []
    students = select_student_in_group_db(db=db, group_name=group_name)
    for student in students:
        users.append(student)

    curators = select_curator_in_group_db(db=db, group_name=group_name)
    for curator in curators:
        users.append(curator)

    return users


def select_users_in_subject(subject_id: int, db: Session) -> list[tuple]:
    users = []
    students = select_students_for_subject_db(db=db, subject_id=subject_id)
    for student in students:
        users.append(student)

    teachers = select_teachers_for_subject_db(db=db, subject_id=subject_id)
    for teacher in teachers:
        users.append(teacher)

    return users


def set_keyword_for_users_data(users: list) -> list[dict]:
    users_info = []
    fields = ['user_id', 'is_active', 'username', 'user_type', 'name', 'surname', 'image_path']

    for user in users:
        user_dict = dict(zip(fields, user))
        users_info.append(user_dict)

    return users_info
