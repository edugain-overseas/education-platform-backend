from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.crud.teacher_crud import get_teacher_info_db, get_teacher_subjects_db
from app.models import User
from app.session import get_db
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

