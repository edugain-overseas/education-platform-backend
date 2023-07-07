from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.group_crud import (create_group_db, select_group_by_id_db,
                                 select_groups_by_curator_id_db,
                                 select_groups_by_specialization_id_db,
                                 select_groups_db, update_group_db)
from app.models import User
from app.schemas.group_schemas import Group as GroupBase
from app.schemas.group_schemas import GroupCreate, GroupUpdate
from app.session import get_db
from app.utils.token import get_current_user

router = APIRouter()


@router.post("/group/create", response_model=GroupBase)
async def create_group(
        group_data: GroupCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.teacher or current_user.moder:
        new_group = create_group_db(db=db, group_data=group_data)
        return new_group
    else:
        raise HTTPException(
            status_code=403,
            detail="Permission denied. Only moders and teachers can create new groups")


@router.put("/group/{group_id}/update")
async def update_group(
        group_id: int,
        group_data: GroupUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.teacher or current_user.moder:
        group = select_group_by_id_db(db=db, group_id=group_id)
        update_group_db(db=db, group_data=group_data, group=group)
        return {"massage": "Group have been successful updated"}
    else:
        raise HTTPException(
            status_code=403,
            detail="Permission denied. Only moders and teachers can update group")


@router.get("/groups", response_model=List[GroupBase])
async def get_groups(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    groups = select_groups_db(db=db)
    return groups


@router.get("/group/{group_id}", response_model=GroupBase)
async def get_group_by_id(
        group_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    group = select_group_by_id_db(db=db, group_id=group_id)
    return group


# @router.get("/group/teacher/{teacher_id}")
# async def get_groups_by_teacher_id(
#         teacher_id: int,
#         db: Session = Depends(get_db),
#         current_user: User = Depends(get_current_user)
# ):
#     groups = select_groups_by_teacher_id_db(db=db, teacher_id=teacher_id)
#     return groups


@router.get("/group/curator/{curator_id}")
async def get_groups_by_curator_id(
        curator_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    groups = select_groups_by_curator_id_db(db=db, curator_id=curator_id)
    return groups


@router.get("/group/specialization/{specialization_id}")
async def get_groups_by_specialization_id(
        specialization_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    groups = select_groups_by_specialization_id_db(db=db, specialization_id=specialization_id)
    return groups
