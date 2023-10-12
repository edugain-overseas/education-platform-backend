from typing import Dict, List, Tuple

from sqlalchemy.orm import Session

from app.crud.group_chat_crud import select_curator_in_group_db, select_student_in_group_db
from app.crud.subject_chat_crud import select_students_for_subject_db, select_teachers_for_subject_db


def select_users_in_group(group_id: int, db: Session) -> List[Tuple]:
    users = []
    students = select_student_in_group_db(db=db, group_id=group_id)
    for student in students:
        users.append(student)

    curators = select_curator_in_group_db(db=db, group_id=group_id)
    for curator in curators:
        users.append(curator)

    return users


def select_users_in_subject(subject_id: int, db: Session) -> List[Tuple]:
    users = []
    students = select_students_for_subject_db(db=db, subject_id=subject_id)
    for student in students:
        users.append(student)

    teachers = select_teachers_for_subject_db(db=db, subject_id=subject_id)
    for teacher in teachers:
        users.append(teacher)

    return users


def set_keyword_for_users_data(users: List) -> List[Dict]:
    users_info = []
    fields = ['userId', 'isActive', 'username', 'userType', 'name', 'surname', 'imagePath']

    for user in users:
        user_dict = dict(zip(fields, user))
        users_info.append(user_dict)

    return users_info
