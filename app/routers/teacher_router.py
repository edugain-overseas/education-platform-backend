from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.crud.teacher_crud import (get_teacher_by_user_id_db, get_teacher_info_db, get_teacher_lessons_db,
                                   get_teacher_subjects_db, update_teacher_image_db)
from app.models import User
from app.session import get_db
from app.utils.save_images import save_teacher_avatar
from app.utils.token import get_current_user

router = APIRouter()


@router.get("/teacher/info/me")
async def get_teacher_info(
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    teacher_info_list = get_teacher_info_db(db=db, user_id=user.id)
    field_list = [
        'teacher_id',
        'teacher_name',
        'teacher_surname',
        'image_path',
        'teacher_email'
    ]

    teacher_info = dict(zip(field_list, teacher_info_list))

    subjects = get_teacher_subjects_db(db=db, user_id=user.id)
    teacher_info['subject_info'] = subjects

    return teacher_info


@router.get("/teacher/my/schedule")
async def get_my_schedule(
        teacher_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    lessons = get_teacher_lessons_db(db=db, teacher_id=teacher_id)
    result = []

    for lesson in lessons:
        schedule_data = {
            'subject_name': lesson[0],
            'lesson_name': lesson[1],
            'lesson_date': lesson[2],
            'lesson_end': lesson[3],
            'group_name': lesson[4]
        }
        result.append(schedule_data)

    return result


@router.put("/teacher/update-image")
async def update_teacher_image(
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    teacher = get_teacher_by_user_id_db(db=db, user_id=user.id)
    image_path = save_teacher_avatar(photo=file)
    update_teacher_image_db(db=db, teacher=teacher, image_path=image_path)
    return {
        "message": "Avatar updated successfully",
        "photo_path": image_path
    }
