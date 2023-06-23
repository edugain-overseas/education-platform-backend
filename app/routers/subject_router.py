from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.crud.subject_crud import (create_new_subject_db, delete_subject_db,
                                   select_all_subjects_db,
                                   select_subject_by_id_db,
                                   select_subjects_by_course_db,
                                   select_subjects_by_specialization_db,
                                   set_teacher_for_subject_db,
                                   update_subject_image_path_db,
                                   update_subject_info_db,
                                   update_subject_logo_path_db)
from app.models import User
from app.schemas.subject_schemas import SubjectCreate, SubjectUpdate
from app.session import get_db
from app.utils.save_images import save_subject_avatar, save_subject_logo
from app.utils.token import get_current_user

router = APIRouter()


@router.post("/subject/create")
async def create_subject(
        new_subject: SubjectCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.teacher or current_user.moder:
        new_subject = create_new_subject_db(db=db, subject=new_subject)
        return new_subject
    else:
        raise HTTPException(
            status_code=403,
            detail="Permission denied. Only moders and teachers can create new subject"
        )


@router.put("/subject/update/{subject_id}/info")
async def update_subject_info(
        subject_id: int,
        subject_data: SubjectUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.teacher or current_user.moder:
        subject = select_subject_by_id_db(db=db, subject_id=subject_id)
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")
        update_subject_info_db(db=db, subject=subject, subject_data=subject_data)
        return {"massage": "Subject information have been successful updated"}
    else:
        raise HTTPException(
            status_code=403,
            detail="Permission denied. Only moders and teachers can update subject info"
        )


@router.put("/subject/update/{subject_id}/photo")
async def update_subject_photo(
        subject_id: int,
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.teacher or current_user.moder:
        subject = select_subject_by_id_db(db=db, subject_id=subject_id)
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")
        subject_photo_path = save_subject_avatar(photo=file, subject_title=subject.title)
        update_subject_image_path_db(db=db, subject=subject, new_path=subject_photo_path)
        return {"massage": "Subject photo have been successful updated"}
    else:
        raise HTTPException(
            status_code=403,
            detail="Permission denied. Only moders and teachers can update subject photo"
        )


@router.put("/subject/update/{subject_id}/logo")
async def update_subject_logo(
        subject_id: int,
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.teacher or current_user.moder:
        subject = select_subject_by_id_db(db=db, subject_id=subject_id)
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")
        subject_logo_path = save_subject_logo(photo=file, subject_title=subject.title)
        update_subject_logo_path_db(db=db, subject=subject, new_path=subject_logo_path)
        return {"massage": "Subject photo have been successful updated"}
    else:
        raise HTTPException(
            status_code=403,
            detail="Permission denied. Only moders and teachers can update subject photo"
        )


@router.get("/subjects")
async def get_subjects(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.teacher or current_user.moder:
        subjects = select_all_subjects_db(db=db)
        if not subjects:
            raise HTTPException(status_code=404, detail="Subjects not found")
        return {"subjects": subjects}
    else:
        raise HTTPException(
            status_code=403,
            detail="Permission denied. Only moders and teachers can view all subjects"
        )


@router.get("/subject/{subject_id}")
async def get_subject_by_id(
        subject_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.teacher or current_user.moder:
        subject = select_subject_by_id_db(db=db, subject_id=subject_id)
        if not subject:
            raise HTTPException(status_code=404, detail="Subjects not found")
        return subject
    else:
        raise HTTPException(
            status_code=403,
            detail="Permission denied. Only moders and teachers can view subject"
        )


@router.get("/subject/course/{course_id}")
async def get_subject_by_course(
        course_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.teacher or current_user.moder:
        subjects = select_subjects_by_course_db(db=db, course_id=course_id)
        if not subjects:
            raise HTTPException(status_code=404, detail="Subjects not found")
        return subjects
    else:
        raise HTTPException(
            status_code=403,
            detail="Permission denied. Only moders and teachers can view subject"
        )


@router.get("/subject/specialization/{specialization_id}")
async def get_subject_by_specialization(
        specialization_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.teacher or current_user.moder:
        subjects = select_subjects_by_specialization_db(db=db, specialization_id=specialization_id)
        if not subjects:
            raise HTTPException(status_code=404, detail="Subjects not found")
        return subjects
    else:
        raise HTTPException(
            status_code=403,
            detail="Permission denied. Only moders and teachers can view subject"
        )


@router.delete("/subject/delete/{subject_id}")
async def delete_subject(
        subject_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.teacher or current_user.moder:
        subject = select_subject_by_id_db(db=db, subject_id=subject_id)
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")
        delete_subject_db(db=db, subject=subject)
        return {"massage": "Subject have been successful deleted"}
    else:
        raise HTTPException(
            status_code=403,
            detail="Permission denied. Only moders and teachers can delete subject"
        )


@router.post("/subject/{subject_id}/add-teacher")
async def add_teacher_for_subject(
        subject_id: int,
        teacher_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.teacher or current_user.moder:
        set_teacher_for_subject_db(db=db, teacher_id=teacher_id, subject_id=subject_id)
        return {"massage": "Added new teacher for subject"}
    else:
        raise HTTPException(
            status_code=403,
            detail="Permission denied."
        )
