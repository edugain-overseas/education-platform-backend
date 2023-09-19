from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.lesson_crud import (create_new_lesson_db, delete_lesson_db, select_all_lessons_db, select_lesson_by_id_db,
                                  select_lesson_by_module_db, select_lesson_by_subject_db, select_lesson_by_type_db,
                                  update_lesson_db)
from app.models import User
from app.schemas.lesson_schemas import LessonBase, LessonUpdate
from app.session import get_db
from app.utils.token import get_current_user

router = APIRouter()


@router.post("/lesson/create")
async def create_lesson(
        lesson_data: LessonBase,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        new_lesson = create_new_lesson_db(db=db, lesson_data=lesson_data)
        return new_lesson
    else:
        raise HTTPException(
            status_code=403,
            detail="Permission denied"
        )


@router.put("/lesson/{lesson_id}/update")
async def update_lesson(
        lesson_id: int,
        lesson_data: LessonUpdate,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        lesson = select_lesson_by_id_db(db=db, lesson_id=lesson_id)
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        update_lesson_db(db=db, lesson=lesson, lesson_data=lesson_data)
        return {"massage": "Lesson have been successful updated"}
    else:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.get("/lessons")
async def get_lessons(
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder or user.student:
        return {"lessons": select_all_lessons_db(db=db)}
    raise HTTPException(status_code=403, detail="Permission denied")


@router.get("/lesson/{lesson_id}")
async def get_lesson(
        lesson_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder or user.student:
        return select_lesson_by_id_db(db=db, lesson_id=lesson_id)
    raise HTTPException(status_code=403, detail="Permission denied")


@router.get("/lessons/module/{module_id}")
async def get_lesson_by_module(
        module_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder or user.student:
        return {"lessons": select_lesson_by_module_db(db=db, module_id=module_id)}
    raise HTTPException(status_code=403, detail="Permission denied")


@router.get("/lessons/subject/{subject_id}")
async def get_lesson_by_subject(
        subject_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder or user.student:
        return {"lessons": select_lesson_by_subject_db(db=db, subject_id=subject_id)}
    raise HTTPException(status_code=403, detail="Permission denied")


@router.get("/lessons/type/{type_id}")
async def get_lesson_by_type(
        type_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder or user.student:
        return {"lessons": select_lesson_by_type_db(db=db, type_id=type_id)}
    raise HTTPException(status_code=403, detail="Permission denied")


@router.delete("/lesson/{lesson_id}/delete")
async def delete_lesson(
        lesson_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        lesson = select_lesson_by_id_db(db=db, lesson_id=lesson_id)
        if not lesson:
            raise HTTPException(status_code=404, detail="Lessons not found")
        delete_lesson_db(db=db, lesson=lesson)
        return {"massage": "Lesson have been successful deleted"}
    else:
        raise HTTPException(status_code=403, detail="Permission denied")
