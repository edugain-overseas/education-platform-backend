from sqlalchemy.orm import Session

from app.crud.group_chat_crud import (select_curator_in_group_db,
                                      select_student_in_group_db)


def select_users_in_group(group_name: str, db: Session) -> list[tuple]:
    users = []
    students = select_student_in_group_db(db=db, group_name=group_name)
    for student in students:
        users.append(student)

    curators = select_curator_in_group_db(db=db, group_name=group_name)
    for curator in curators:
        users.append(curator)

    # moderators = select_moder_db(db=db)
    # for moderator in moderators:
    #     users.append(moderator)

    return users


def get_total_in_group_chat(users: list) -> tuple:

    total_in_chat = len(users)
    total_active = 0

    for user in users:
        if user[1] is True:
            total_active += 1

    return total_in_chat, total_active


def set_keyword_for_users_data(users: list) -> list[dict]:
    users_info = []
    fields = ['UserId', 'IsActive', 'Username', 'UserType', 'Name', 'Surname', 'ImagePath']

    for user in users:
        user_dict = dict(zip(fields, user))
        if len(user) <= 6:
            user_dict['ImagePath'] = None
        users_info.append(user_dict)

    return users_info
