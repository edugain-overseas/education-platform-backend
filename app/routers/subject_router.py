import json
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.crud.group_crud import select_group_curator_db, select_group_students_db
from app.crud.lesson_crud import get_lessons_by_subject_id_db, select_three_next_lesson_db
from app.crud.subject_crud import (create_new_subject_db, create_or_update_participant_comment_db,
                                   create_subject_icon_db, create_subject_instruction_category_db,
                                   create_subject_instruction_db, create_subject_instruction_file_db,
                                   create_subject_instruction_link_db, create_subject_item_db, delete_subject_db,
                                   delete_subject_icon_db, delete_subject_instruction_category_db,
                                   delete_subject_instruction_db, delete_subject_instruction_file_db,
                                   delete_subject_instruction_link_db, select_all_subjects_db, select_dop_subjects,
                                   select_subject_by_id_db, select_subject_exam_date, select_subject_icon_db,
                                   select_subject_icons_db, select_subject_instruction_category_db,
                                   select_subject_instruction_db, select_subject_instructions_db,
                                   select_subject_item_db, select_subjects_by_course_db, select_subjects_by_group_db,
                                   select_subjects_by_specialization_db, select_teachers_for_subject_db,
                                   set_teacher_for_subject_db, sign_student_for_addition_subject_db,
                                   update_subject_image_path_db, update_subject_info_db,
                                   update_subject_instruction_category_db, update_subject_instruction_db,
                                   update_subject_item_text_db, update_subject_logo_path_db)
from app.models import User
from app.schemas.subject_schemas import (SubjectCreate, SubjectInstructionAttachFile, SubjectInstructionAttachLink,
                                         SubjectInstructionCategoryCreate, SubjectInstructionCategoryUpdate,
                                         SubjectInstructionCreate, SubjectInstructionUpdate, SubjectUpdate)
from app.session import get_db
from app.utils.save_images import (delete_file, save_subject_avatar, save_subject_icon, save_subject_instructions,
                                   save_subject_logo, save_subject_program)
from app.utils.subject_utils import set_subjects_lessons_structure
from app.utils.token import get_current_user
from app.utils.check_lecture import checking_lecture


router = APIRouter()


@router.post("/subject/create")
async def create_subject(
        new_subject: SubjectCreate,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        new_subject = create_new_subject_db(db=db, subject=new_subject)
        return new_subject
    else:
        raise HTTPException(
            status_code=403,
            detail="Permission denied. Only moders and teachers can create new subject"
        )


@router.put("/subject/{subject_id}/update/info")
async def update_subject_info(
        subject_id: int,
        subject_data: SubjectUpdate,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        subject = select_subject_by_id_db(db=db, subject_id=subject_id)
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")
        subject = update_subject_info_db(db=db, subject=subject, subject_data=subject_data)
        return subject
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
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        subject = select_subject_by_id_db(db=db, subject_id=subject_id)
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")
        subject_photo_path = save_subject_avatar(photo=file, subject_title=subject.title)
        update_subject_image_path_db(db=db, subject=subject, new_path=subject_photo_path)
        return {
            "massage": "Subject photo have been successful updated",
            "new_path": subject_photo_path
        }
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
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        subject = select_subject_by_id_db(db=db, subject_id=subject_id)
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")
        subject_logo_path = save_subject_logo(photo=file, subject_title=subject.title)
        update_subject_logo_path_db(db=db, subject=subject, new_path=subject_logo_path)
        return {
            "massage": "Subject photo have been successful updated",
            "new_path": subject_logo_path
        }
    else:
        raise HTTPException(
            status_code=403,
            detail="Permission denied. Only moders and teachers can update subject photo"
        )


@router.get("/subjects")
async def get_subjects(
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder or user.student:
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
        user: User = Depends(get_current_user)
):

    subject = select_subject_by_id_db(db=db, subject_id=subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subjects not found")
    return subject


@router.get("/subject/course/{course_id}")
async def get_subject_by_course(
        course_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder or user.student:
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
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder or user.student:
        subjects = select_subjects_by_specialization_db(db=db, specialization_id=specialization_id)
        if not subjects:
            raise HTTPException(status_code=404, detail="Subjects not found")
        return subjects
    else:
        raise HTTPException(
            status_code=403,
            detail="Permission denied. Only moders and teachers can view subject"
        )


@router.get("/subject/group/{group_name}", response_model=List[Dict[str, Any]])
async def get_subject_by_group(
        group_name: str,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    fields = ["id", "title", "image_path"]
    response_subject = []

    subjects = select_subjects_by_group_db(db=db, group_name=group_name)
    for subject in subjects:
        response_subject.append(dict(zip(fields, subject)))

    return response_subject


@router.delete("/subject/delete/{subject_id}")
async def delete_subject(
        subject_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
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
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        set_teacher_for_subject_db(db=db, teacher_id=teacher_id, subject_id=subject_id)
        return {"massage": "Added new teacher for subject"}
    else:
        raise HTTPException(
            status_code=403,
            detail="Permission denied."
        )


@router.get("/subject-tapes/{subject_id}")
async def get_subject_tapes(
        subject_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    subject_teachers = select_teachers_for_subject_db(db=db, subject_id=subject_id)
    next_lesson_date = select_three_next_lesson_db(db=db, subject_id=subject_id)
    subject_data = get_lessons_by_subject_id_db(db=db, subject_id=subject_id)
    subjects_lessons = set_subjects_lessons_structure(subject_data=subject_data)
    exam_date = select_subject_exam_date(db=db, subject_id=subject_id)

    if user.student:
        subjects_program = checking_lecture(db=db, student_id=user.student[0].id, subject_lessons=subjects_lessons)
        response_data = {
            "subject_teachers": subject_teachers,
            "subject_exam_date": exam_date,
            "next_lesson_date": next_lesson_date,
            "subjects_lessons": subjects_program,
        }
        return response_data
    else:
        response_data = {
            "subject_teachers": subject_teachers,
            "subject_exam_date": exam_date,
            "next_lesson_date": next_lesson_date,
            "subjects_lessons": subjects_lessons,
        }
        return response_data


@router.post("/add-dop-subject/{subject_id}/{student_id}")
async def set_additional_subject(
        subject_id: int,
        student_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    new_dop_subject = sign_student_for_addition_subject_db(
        db=db,
        subject_id=subject_id,
        student_id=student_id
    )
    return new_dop_subject


@router.get("/dop_subjects/{student_id}")
async def get_dop_subjects(
        student_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    fields = ["id", "title", "image_path"]
    response_subject = []

    subjects = select_dop_subjects(db=db, student_id=student_id)
    for subject in subjects:
        response_subject.append(dict(zip(fields, subject)))

    return response_subject


@router.get("/list-members")
async def get_list_subject_members(
        group_id: int,
        subject_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    teachers = select_teachers_for_subject_db(db=db, subject_id=subject_id)
    curator = select_group_curator_db(db=db, group_id=group_id)
    students = select_group_students_db(db=db, group_id=group_id, subject_id=subject_id)

    result = {
        "teachers": teachers,
        "curator": curator,
        "students": students
    }

    return result


@router.put("/update-comment", description="updating participant comment")
async def update_participant_comment(
        subject_id: int,
        student_id: int,
        comment: str,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder or user.curator:
        return create_or_update_participant_comment_db(
            db=db,
            subject_id=subject_id,
            student_id=student_id,
            comment=comment
        )
    else:
        raise HTTPException(
            status_code=403,
            detail="Permission denied."
        )


@router.post("/subject-item/create")
async def create_subject_item(
        subject_id: int,
        item: List[Dict],
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user),
):
    text_json = json.dumps(item)
    new_item = create_subject_item_db(db=db, subject_id=subject_id, item=text_json)
    return json.loads(new_item.text)


@router.put("/subject-item/update")
async def update_subject_item_text(
        subject_id: int,
        item: List[Dict],
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    subject_item = select_subject_item_db(db=db, subject_id=subject_id)
    text_json = json.dumps(item)
    updated_subject_item = update_subject_item_text_db(
        db=db,
        subject_item=subject_item,
        text=text_json
    )

    return json.loads(updated_subject_item.text)


@router.get("/subject-item/read")
async def get_subject_item(
        subject_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    subject_item = select_subject_item_db(db=db, subject_id=subject_id)
    if subject_item is None:
        return []
    json_data = json.loads(subject_item.text)
    subject_item.text = json_data
    return subject_item.text


@router.post("/subject-item/upload-program")
async def upload_subject_item_file(
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    file_path = save_subject_program(file=file)
    return {"file_path": file_path}


@router.post("/subject-item/upload-icon")
async def upload_subject_item_icon(
        is_default: bool,
        subject_id: Optional[int] = None,
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    icon_path = save_subject_icon(file=file)
    new_icon = create_subject_icon_db(
        db=db,
        icon_path=icon_path,
        is_default=is_default,
        subject_id=subject_id
    )
    return new_icon


@router.delete("/subject-item/delete-icon")
async def delete_subject_item_icon(
        icon_path: str,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    delete_file(file_path=icon_path)
    icon = select_subject_icon_db(db=db, icon_path=icon_path)
    delete_subject_icon_db(db=db, subject_icon=icon)
    return {"Message": "Icon has been deleted"}


@router.get("/subject-item/icons")
async def get_subject_item_icons(
        subject_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return select_subject_icons_db(db=db, subject_id=subject_id)


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
        result = []

        for file in files:
            file_path = save_subject_instructions(file=file)

            file_info_dict = {
                "filePath": file_path,
                "fileName": file.filename,
                "fileSize": file.size,
                "fileType": file.filename.split(".")[-1]
            }

            result.append(file_info_dict)

        return result
    else:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.delete("/subject/instruction/file/")
async def delete_subject_instruction_file(
        file_path: str,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        delete_subject_instruction_file_db(db=db, file_path=file_path)
        delete_file(file_path=file_path)
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
    result = []
    for link_data in links_data:
        new_link = create_subject_instruction_link_db(db=db, link_data=link_data)
        result.append(new_link)

    return result


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
