from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.crud.lecture_crud import (create_lecture_db, set_file_attr_for_lecture_db,
                                   set_text_attr_for_lecture_db, get_lesson_info_db, get_lecture_db,
                                   get_lecture_text_attribute_db, get_lecture_file_attribute_db)
from app.models import User, LectureAttributeType
from app.schemas.lecture_schemas import LectureTextCreate, AttributeBase
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
        attr_type: LectureAttributeType,
        attr_title: str,
        attr_number: int,
        download_allowed: bool,
        attr_subtitle: str = None,
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        file_path = save_lesson_file(file)
        set_file_attr_for_lecture_db(
            db=db,
            attr_type=attr_type,
            attr_title=attr_title,
            attr_subtitle=attr_subtitle,
            attr_number=attr_number,
            download_allowed=download_allowed,
            lecture_id=lecture_id,
            filename=file.filename,
            file_path=file_path,
            file_size=file.size
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
    lecture_base = get_lesson_info_db(db=db, lesson_id=lesson_id)

    result = {
        "lessonTitle": lecture_base.lessonTitle,
        "lessonDescription": lecture_base.lessonDescription,
        "lessonDate": lecture_base.lessonDate,
        "lessonEnd": lecture_base.lessonEnd,
        "lectureInfo": []
    }

    lecture = get_lecture_db(db=db, lesson_id=lesson_id)
    if lecture is None:
        return result

    text_attrs = get_lecture_text_attribute_db(db=db, lecture_id=lecture.id)
    for attr in text_attrs:
        text_attr = {
            "attributeId": attr.attributeId,
            "attributeNumber": attr.attributeNumber,
            "attributeType": attr.attributeType,
            "attributeTitle": attr.attributeTitle,
            "attributeSubTitle": attr.attributeSubTitle,
            "attributeValue": attr.attributeValue
        }
        result["lectureInfo"].append(text_attr)

    file_attrs = get_lecture_file_attribute_db(db=db, lecture_id=lecture.id)
    for attr in file_attrs:
        file_attr = {
            "attributeId": attr.attributeId,
            "attributeNumber": attr.attributeNumber,
            "attributeType": attr.attributeType,
            "attributeTitle": attr.attributeTitle,
            "attributeSubTitle": attr.attributeSubTitle,
            "fileName": attr.fileName,
            "fileSize": attr.fileSize,
            "filePath": attr.filePath,
            "downloadAllowed": attr.downloadAllowed
        }
        result["lectureInfo"].append(file_attr)

    return result
