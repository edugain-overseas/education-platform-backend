from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.crud.lecture_crud import (create_lecture_db, get_lecture_info_db,
                                   set_file_attr_for_lecture_db,
                                   set_text_attr_for_lecture_db)
from app.models import User
from app.schemas.lecture_schemas import LectureTextCreate
from app.session import get_db
from app.utils.save_images import save_lesson_file
from app.utils.token import get_current_user

router = APIRouter()


@router.post("/lecture/create")
async def create_lecture(
        lesson_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        return create_lecture_db(db=db, lesson_id=lesson_id)
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
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        set_text_attr_for_lecture_db(db=db, item=item, lecture_id=lecture_id)
        return {"message": f"Text for lecture {lecture_id } has been saved"}
    else:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.post("/lecture/file/{lecture_id}")
async def add_file_attr_for_lecture(
        lecture_id: int,
        attr_title: str,
        attr_number: int,
        download_allowed: bool,
        files: List[UploadFile] = File(...),
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        for file in files:
            file_path, file_extension = save_lesson_file(file)
            set_file_attr_for_lecture_db(
                db=db,
                attr_type=file_extension,
                attr_title=attr_title,
                attr_number=attr_number,
                download_allowed=download_allowed,
                lecture_id=lecture_id,
                file_path=file_path
            )

        return {"message": f"File for lecture {lecture_id} has been saved"}
    else:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.get("/lecture/{lesson_id}")
async def get_lecture(
        lesson_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    lectures = get_lecture_info_db(db=db, lesson_id=lesson_id)
    result = []
    for lecture in lectures:
        result.append({
            "lesson title": lecture[0],
            "lesson description": lecture[1],
            "lesson date": lecture[2],
            "lesson end": lecture[3],
            "attribute number": lecture[4],
            "download allowed": lecture[5],
            "attribute type": lecture[6],
            "attribute title": lecture[7],
            "value": lecture[8]
        })

    return result
