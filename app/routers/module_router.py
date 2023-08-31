from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.module_crud import (create_module_db, delete_module_db,
                                  select_module_by_id_db,
                                  select_modules_by_subject_id_db,
                                  select_modules_db, update_module_db)
from app.models import User
from app.schemas.module_schemas import CreateModule, UpdateModule
from app.session import get_db
from app.utils.token import get_current_user

router = APIRouter()


@router.post("/module/create")
async def create_module(
        module: CreateModule,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.moder or user.teacher:
        new_module = create_module_db(db=db, module=module)
        return new_module
    else:
        raise HTTPException(
            status_code=403,
            detail="Permission denied. Only moders and teachers can create new module"
        )


@router.put("/module/{module_id}/update")
async def update_module(
        module_id: int,
        module_data: UpdateModule,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.moder or user.teacher:
        module = select_module_by_id_db(db=db, module_id=module_id)
        if not module:
            raise HTTPException(status_code=404, detail="Module not found")
        update_module_db(db=db, module=module, module_data=module_data)
        return {"massage": "Module information have been successful updated"}
    else:
        raise HTTPException(
            status_code=403,
            detail="Permission denied. Only moders and teachers can update module"
        )


@router.get("/modules")
async def get_modules(
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder or user.student:
        modules = select_modules_db(db=db)
        if not modules:
            raise HTTPException(status_code=404, detail="Modules not found")
        return {"modules": modules}
    else:
        raise HTTPException(
            status_code=403,
            detail="Permission denied. Only moders and teacher can view list of modules"
        )


@router.get("/module/{module_id}")
async def get_module(
        module_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder or user.student:
        module = select_module_by_id_db(db=db, module_id=module_id)
        if not module:
            raise HTTPException(status_code=404, detail="Module not found")
        return module
    else:
        raise HTTPException(
            status_code=403,
            detail="Permission denied. Only moders and teacher can view module"
        )


@router.get("/module/subject/{subject_id}")
async def get_modules_by_subject(
        subject_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.teacher or current_user.moder:
        modules = select_modules_by_subject_id_db(db=db, subject_id=subject_id)
        if not modules:
            raise HTTPException(status_code=404, detail="Modules not found")
        return {"modules": modules}
    else:
        raise HTTPException(
            status_code=403,
            detail="Permission denied. Only moders and teacher can view list of modules"
        )


@router.delete("/module/{module_id}/delete")
async def delete_module(
        module_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.moder or user.teacher:
        module = select_module_by_id_db(db=db, module_id=module_id)
        if not module:
            raise HTTPException(status_code=404, detail="Module not found")
        delete_module_db(db=db, module=module)
        return {"massage": "Module have been successful deleted"}
    else:
        raise HTTPException(
            status_code=403,
            detail="Permission denied. Only moders and teacher can delete module"
        )
