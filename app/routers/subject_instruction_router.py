from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.crud.subject_instruction_crud import (create_subject_instruction_category_db, create_subject_instruction_db,
                                               create_subject_instruction_file_db, create_subject_instruction_link_db,
                                               delete_subject_instruction_category_db, delete_subject_instruction_db,
                                               delete_subject_instruction_file_db, delete_subject_instruction_link_db,
                                               select_subject_instruction_category_db, select_subject_instruction_db,
                                               select_subject_instruction_file_db, select_subject_instructions_db,
                                               update_subject_instruction_category_db, update_subject_instruction_db)
from app.models import User
from app.schemas.subject_instruction_schemas import (SubjectInstructionAttachFile, SubjectInstructionAttachLink,
                                                     SubjectInstructionCategoryCreate, SubjectInstructionCategoryUpdate,
                                                     SubjectInstructionCreate, SubjectInstructionUpdate)
from app.session import get_db
from app.utils.instruction import save_subject_instruction_file, save_subject_instruction_link
from app.utils.save_images import delete_file
from app.utils.token import get_current_user

router = APIRouter()


@router.post("/subject/instruction/category")
async def create_subject_instruction_category(
        subject_category: SubjectInstructionCategoryCreate,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        return create_subject_instruction_category_db(db=db, subject_category=subject_category)
    else:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.put("/subject/instruction/category")
async def update_subject_instruction_category(
        instruction_category_id: int,
        instruction_category_data: SubjectInstructionCategoryUpdate,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        instruction_category = select_subject_instruction_category_db(
            db=db,
            instruction_category_id=instruction_category_id
        )
        return update_subject_instruction_category_db(
            db=db,
            instruction_category=instruction_category,
            instruction_category_data=instruction_category_data
        )
    else:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.delete("/subject/instruction/category")
async def delete_subject_instruction_category(
        instruction_category_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        instruction_category = select_subject_instruction_category_db(
            db=db,
            instruction_category_id=instruction_category_id
        )
        delete_subject_instruction_category_db(db=db, instruction_category=instruction_category)
        return {"message": "Instruction category has been deleted"}
    else:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.post("/subject/instruction/file")
async def upload_subject_instruction_file(
        files: list[UploadFile] = File(None),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        result = save_subject_instruction_file(files=files)
        return result
    else:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.delete("/subject/instruction/file")
async def delete_subject_instruction_file(
        file_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        instruction_file = select_subject_instruction_file_db(db=db, file_id=file_id)
        delete_file(file_path=instruction_file.file_path)
        delete_subject_instruction_file_db(db=db, file_path=instruction_file.file_path)
        return {"message": "File have been deleted"}
    else:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.post("/subjects/instruction/attach-file")
async def attach_file_for_instruction(
        file_data: SubjectInstructionAttachFile,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.moder or user.teacher:
        return create_subject_instruction_file_db(db=db, file_data=file_data)
    else:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.post("/subject/instruction/link")
async def attach_link_for_instruction(
        links_data: List[SubjectInstructionAttachLink],
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        result = []

        for link_data in links_data:
            new_link = create_subject_instruction_link_db(db=db, link_data=link_data)
            link = save_subject_instruction_link(link=new_link)
            result.append(link)
        return result
    else:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.delete("/subject/instruction/link")
async def delete_subject_instruction_link(
        instruction_link_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    delete_subject_instruction_link_db(db=db, link_id=instruction_link_id)
    return {"message": "Instruction link has been deleted"}


@router.post("/subject/instruction")
async def create_subject_instruction(
        instruction_data: SubjectInstructionCreate,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        instruction = create_subject_instruction_db(db=db, instruction_data=instruction_data)

        return {
            "instructionId": instruction.id,
            "number": instruction.number,
            "title": instruction.title,
            "subTitle": instruction.subtitle,
            "text": instruction.text,
            "subjectCategoryId": instruction.subject_category_id,
            "isView": instruction.is_view,
            "files": [],
            "links": []
        }

    else:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.put("/subject/instruction")
async def update_subject_instruction(
        instruction_id: int,
        instruction_data: SubjectInstructionUpdate,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.moder or user.teacher:
        instruction = select_subject_instruction_db(db=db, instruction_id=instruction_id)
        return update_subject_instruction_db(db=db, instruction=instruction, instruction_data=instruction_data)
    else:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.delete("/subject/instruction")
async def delete_subject_instruction(
    instruction_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        instruction = select_subject_instruction_db(db=db, instruction_id=instruction_id)
        delete_subject_instruction_db(db=db, instruction=instruction)
        return {"message": "Instruction has been deleted"}
    else:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.get("/subject/{subject_id}/instruction/")
async def get_subject_instruction(
        subject_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    instructions = select_subject_instructions_db(db=db, subject_id=subject_id)
    return instructions
