from fastapi import APIRouter, File, Depends, UploadFile, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models import User
from app.session import get_db
from app.utils.save_images import save_lesson_file
from app.utils.token import get_current_user
from app.schemas.lecture_schemas import LectureTextCreate
from app.crud.lecture_crud import *


router = APIRouter()


@router.post("/lecture/create")
async def create_lecture(
        lesson_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.teacher:
        return create_ordinary_lesson_db(db=db, lesson_id=lesson_id)
    else:
        raise HTTPException(
            status_code=403,
            detail="Permission denied"
        )


@router.post("/lecture/text/{lecture_id}")
async def add_text_attr_for_lecture(
        lecture_id: int,
        item: LectureTextCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.teacher:
        set_text_attr_for_lecture_db(db=db, item=item, lecture_id=lecture_id)
        return {"message": f"Text for lecture {lecture_id } has been saved"}
    else:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.post("/lecture/file/{lecture_id}")
async def add_file_attr_for_lecture(
        lecture_id: int,
        files: List[UploadFile] = File(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.teacher:
        for file in files:
            file_path, name = save_lesson_file(file)
            set_file_attr_for_lecture_db(
                db=db,
                file_path=file_path,
                name=name,
                lecture_id=lecture_id
            )

        return {"message": f"File for lecture {lecture_id} has been saved"}
    else:
        raise HTTPException(status_code=403, detail="Permission denied")
