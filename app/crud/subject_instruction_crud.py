from sqlalchemy.orm import Session

from app.models import SubjectInstruction, SubjectInstructionCategory, SubjectInstructionFiles, SubjectInstructionLink
from app.schemas.subject_instruction_schemas import (SubjectInstructionAttachFile, SubjectInstructionAttachLink,
                                                     SubjectInstructionCategoryCreate, SubjectInstructionCategoryUpdate,
                                                     SubjectInstructionCreate, SubjectInstructionUpdate)
from app.utils.instruction import set_instruction, set_instruction_category, set_instruction_file, set_instruction_link
from app.utils.save_images import delete_file


def create_subject_instruction_category_db(
        db: Session,
        subject_category: SubjectInstructionCategoryCreate
):
    new_category = SubjectInstructionCategory(**subject_category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


def select_subject_instruction_category_db(db: Session, instruction_category_id: int):
    res = db.query(
        SubjectInstructionCategory
    )\
        .filter(SubjectInstructionCategory.id == instruction_category_id)\
        .first()
    return res


def update_subject_instruction_category_db(
        db: Session,
        instruction_category: SubjectInstructionCategory,
        instruction_category_data: SubjectInstructionCategoryUpdate
):
    for field, value in instruction_category_data:
        if value is not None:
            setattr(instruction_category, field, value)

    db.commit()
    db.refresh(instruction_category)
    return instruction_category


def create_subject_instruction_db(
        db: Session,
        instruction_data: SubjectInstructionCreate
):
    new_instruction = SubjectInstruction(**instruction_data.dict())
    db.add(new_instruction)
    db.commit()
    db.refresh(new_instruction)
    return new_instruction


def create_subject_instruction_file_db(
        db: Session,
        file_data: SubjectInstructionAttachFile
):
    new_instruction_file = SubjectInstructionFiles(**file_data.dict())
    db.add(new_instruction_file)
    db.commit()
    db.refresh(new_instruction_file)
    return new_instruction_file


def select_subject_instruction_db(instruction_id: int, db: Session):
    instruction = db.query(SubjectInstruction).filter(SubjectInstruction.id == instruction_id).first()
    return instruction


def select_subject_instruction_file_db(db: Session, file_id: int):
    instruction_file = db.query(
        SubjectInstructionFiles
    )\
        .filter(SubjectInstructionFiles.id == file_id)\
        .first()
    return instruction_file


def delete_subject_instruction_file_db(db: Session, file_path: str):
    instruction_file = db.query(
        SubjectInstructionFiles
    )\
        .filter(SubjectInstructionFiles.file_path == file_path)\
        .first()
    db.delete(instruction_file)
    db.commit()


def select_subject_instructions_db(subject_id: int, db: Session):
    instruction_categories = (
        db.query(
            SubjectInstructionCategory.id,
            SubjectInstructionCategory.category_name,
            SubjectInstructionCategory.is_view,
            SubjectInstructionCategory.number
        )
        .filter(SubjectInstructionCategory.subject_id == subject_id)
        .all()
    )

    result = []

    for category in instruction_categories:
        subject_instructions = set_instruction_category(category=category)

        instructions = db.query(
            SubjectInstruction
        )\
            .filter(SubjectInstruction.subject_category_id == category.id)\
            .all()

        for instruction in instructions:
            instruction_dict = set_instruction(instruction=instruction)

            if len(instruction.subject_instruction_files) > 0:
                for file in instruction.subject_instruction_files:
                    file_dict = set_instruction_file(instruction_file=file)
                    instruction_dict["files"].append(file_dict)

            if len(instruction.subject_instruction_link) > 0:
                for link in instruction.subject_instruction_link:
                    link_dict = set_instruction_link(instruction_link=link)
                    instruction_dict["links"].append(link_dict)

            subject_instructions["instructions"].append(instruction_dict)
        result.append(subject_instructions)
    return result


def update_subject_instruction_db(
        db: Session,
        instruction: SubjectInstruction,
        instruction_data: SubjectInstructionUpdate
):
    for field, value in instruction_data:
        if value is not None:
            setattr(instruction, field, value)

    db.commit()
    db.refresh(instruction)
    return instruction


def delete_subject_instruction_db(db: Session, instruction: SubjectInstruction):
    instruction_files = db.query(
        SubjectInstructionFiles
    )\
        .filter(SubjectInstructionFiles.subject_instruction_id == instruction.id)\
        .all()

    if instruction_files is not None:
        for file in instruction_files:
            delete_file(file_path=file.file)
            db.delete(file)
            db.commit()

    db.delete(instruction)
    db.commit()


def delete_subject_instruction_category_db(db: Session, instruction_category: SubjectInstructionCategory):
    instructions = db.query(
        SubjectInstruction
    )\
        .filter(SubjectInstruction.subject_category_id == instruction_category.id)\
        .all()

    for instruction in instructions:
        delete_subject_instruction_db(db=db, instruction=instruction)

    db.delete(instruction_category)
    db.commit()


def create_subject_instruction_link_db(db: Session, link_data: SubjectInstructionAttachLink):
    new_link = SubjectInstructionLink(**link_data.dict())
    db.add(new_link)
    db.commit()
    db.refresh(new_link)
    return new_link


def delete_subject_instruction_link_db(db: Session, link_id: int):
    instruction_link = db.query(SubjectInstructionLink).filter(SubjectInstructionLink.id == link_id).first()
    db.delete(instruction_link)
    db.commit()
