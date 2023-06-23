from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.student_crud import get_student_info_db, get_student_schedule_db
from app.models import User
from app.session import get_db
from app.utils.token import get_current_user

router = APIRouter()


@router.get("/student/info/me")
async def get_student_info(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    user_info_list = get_student_info_db(db=db, user_id=current_user.id)

    field_list = [
        'student_id',
        'student_name',
        'student_surname',
        'image_path',
        'student_educational_program',
        'student_qualification',
        'student_subject_area',
        'course_number',
        'semester_number',
        'group_name'
    ]
    user_info = zip(field_list, user_info_list[0])

    return {"info": user_info}


@router.get("/student/my/schedule")
async def get_student_schedule(
        group_name: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    result = get_student_schedule_db(db=db, group_name=group_name)
    schedule_result_list = []

    for item in result:
        schedule_result_list.append({
            'subject_name': item[0],
            'lesson_date': item[1],
            'teacher_name': item[2],
            'teacher_surname': item[3]
        })
    return schedule_result_list


# @router.get("/student/my/image")
# async def get_student_photo(
#         db: Session = Depends(get_db),
#         current_user: User = Depends(get_current_user)
# ):
#     student = select_student_by_user_id_db(db=db, user_id=current_user.id)
#     if student and student.image_path:
#         image_path = f"static/images/student-avatar/{student.image_path}"
#         return {"image_path": image_path}
#     else:
#         return {"error": "Image not found"}
