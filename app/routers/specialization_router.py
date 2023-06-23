from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.specialization_crud import (
    create_specialization_db, delete_specialization_db,
    select_specialization_by_id_db, select_specializations_by_course_id_db,
    select_specializations_db, update_specialization_title_db)
from app.models import User
from app.schemas.specialization_schemas import \
    Specialization as SpecializationBase
from app.schemas.specialization_schemas import SpecializationCreate
from app.session import get_db
from app.utils.token import get_current_user

router = APIRouter()


@router.post("/specialization/create")
async def create_specialization(
        specialization_data: SpecializationCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if not current_user.moder:
        raise HTTPException(status_code=403, detail="Only moderators can create a new specialization")
    return create_specialization_db(db=db, data=specialization_data)


@router.put("/specialization/{specialization_id}/update")
async def update_specialization(
        specialization_id: int,
        title: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if not current_user.moder:
        raise HTTPException(status_code=403, detail="Only moderators can update specialization")
    specialization = select_specialization_by_id_db(db=db, spec_id=specialization_id)
    update_specialization_title_db(db=db, title=title, specialization=specialization)
    return {"message": "Title for specialization have been successful updated"}


@router.get("/specializations", response_model=List[SpecializationBase])
async def get_specializations(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if not current_user.moder:
        raise HTTPException(status_code=403, detail="Only moderators can view the list of specializations")
    specializations = select_specializations_db(db=db)
    return specializations


@router.get("/specialization/{specialization_id}", response_model=SpecializationBase)
async def get_specialization_by_id(
        specialization_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if not current_user.moder:
        raise HTTPException(status_code=403, detail="Only moderators can view specialization")

    specialization = select_specialization_by_id_db(db=db, spec_id=specialization_id)
    return specialization


@router.get("/specializations/course-{course_id}", response_model=List[SpecializationBase])
async def get_specialization_by_course_id(
        course_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if not current_user.moder:
        raise HTTPException(status_code=403, detail="Only moderators can view the list of specializations")

    specializations = select_specializations_by_course_id_db(db=db, course_id=course_id)
    return specializations


@router.delete("/specialization/delete")
async def delete_specialization(
        specialization_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if not current_user.moder:
        raise HTTPException(status_code=403, detail="Only moderators can view specialization")

    specialization = select_specialization_by_id_db(db=db, spec_id=specialization_id)
    delete_specialization_db(db=db, specialization=specialization)
    return {"massage": "Specialization have been successful deleted"}
