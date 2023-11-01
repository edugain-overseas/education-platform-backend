from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models import (Group, ParticipantComment, StudentAdditionalSubject, Subject, SubjectIcon, SubjectInstruction,
                        SubjectInstructionCategory, SubjectInstructionFiles, SubjectInstructionLink, SubjectItem,
                        SubjectTeacherAssociation, Teacher, User)
from app.schemas.subject_schemas import (SubjectCreate, SubjectInstructionAttachFile, SubjectInstructionAttachLink,
                                         SubjectInstructionCategoryCreate, SubjectInstructionCategoryUpdate,
                                         SubjectInstructionCreate, SubjectInstructionUpdate, SubjectUpdate)
from app.utils.save_images import delete_file


def create_new_subject_db(db: Session, subject: SubjectCreate):
    is_published = subject.is_published if subject.is_published is not None else False
    exam_date = subject.exam_date if subject.exam_date is not None else None

    new_subject = Subject(
        title=subject.title,
        specialization_id=subject.specialization_id,
        course_id=subject.course_id,
        group_id=subject.group_id,
        description=subject.description,
        # image_path=None,
        # logo_path=None,
        is_published=is_published,
        quantity_lecture=subject.quantity_lecture,
        quantity_seminar=subject.quantity_seminar,
        quantity_test=subject.quantity_test,
        quantity_module=subject.quantity_module,
        score=subject.score,
        exam_date=exam_date
    )

    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)
    return new_subject


def create_subject_item_db(db: Session, subject_id: int, item: str):
    new_item = SubjectItem(
        text=item,
        subject_id=subject_id
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


def create_subject_icon_db(
        db: Session,
        subject_id: int | None,
        is_default: bool,
        icon_path: str
):
    new_icon = SubjectIcon(
        icon_path=icon_path,
        is_default=is_default,
        subject_id=subject_id
    )

    db.add(new_icon)
    db.commit()
    db.refresh(new_icon)
    return new_icon


def select_all_subjects_db(db: Session):
    return db.query(Subject).all()


def select_subject_by_id_db(db: Session, subject_id: int):
    return db.query(Subject).filter(Subject.id == subject_id).first()


def select_subjects_by_specialization_db(db: Session, specialization_id: int):
    return db.query(Subject).filter(Subject.specialization_id == specialization_id).all()


def select_subjects_by_course_db(db: Session, course_id: int):
    return db.query(Subject).filter(Subject.course_id == course_id).all()


def select_subject_by_group_id_db(db: Session, group_id: int):
    query = db.query(
        Subject.id.label("subject_id"),
        Subject.title.label("subject_title")
    )\
        .join(Group, Group.id == Subject.group_id)\
        .filter(Group.id == group_id)
    return query.all()


def select_subjects_by_group_db(db: Session, group_name: str):
    query = db.query(
        Subject.id,
        Subject.title,
        Subject.image_path
    )\
        .join(Group, Group.specialization_id == Subject.specialization_id)\
        .filter(Group.group_name == group_name)

    return query.all()


def update_subject_image_path_db(db: Session, subject: Subject, new_path: str):
    subject.image_path = new_path
    db.commit()
    db.refresh(subject)


def update_subject_logo_path_db(db: Session, subject: Subject, new_path: str):
    subject.logo_path = new_path
    db.commit()
    db.refresh(subject)


def update_subject_info_db(db: Session, subject: Subject, subject_data: SubjectUpdate):
    if subject_data.is_published is None:
        subject_data.is_published = True

    for field, value in subject_data:
        if value is not None:
            setattr(subject, field, value)

    db.commit()
    db.refresh(subject)
    return subject


def update_subject_item_text_db(db: Session, subject_item: SubjectItem, text: str):
    subject_item.text = text
    db.commit()
    db.refresh(subject_item)
    return subject_item


def delete_subject_db(db: Session, subject: Subject):
    db.delete(subject)
    db.commit()


def set_teacher_for_subject_db(db: Session, teacher_id: int, subject_id: int):
    new_association = SubjectTeacherAssociation(
        teacher_id=teacher_id,
        subject_id=subject_id
    )

    db.add(new_association)
    db.commit()
    db.refresh(new_association)


def select_teachers_for_subject_db(db: Session, subject_id: int):
    teachers = db.query(
        Teacher.id, Teacher.name, Teacher.surname,
        Teacher.email, Teacher.image_path, User.last_active) \
        .join(SubjectTeacherAssociation, SubjectTeacherAssociation.teacher_id == Teacher.id) \
        .join(User, Teacher.user_id == User.id) \
        .filter(SubjectTeacherAssociation.subject_id == subject_id) \
        .all()

    teachers_list = []

    for teacher in teachers:
        teacher_dict = {
            "id": teacher.id,
            "name": teacher.name,
            "surname": teacher.surname,
            "email": teacher.email,
            "image_path": teacher.image_path,
            "last_active": teacher.last_active
        }
        teachers_list.append(teacher_dict)

    return teachers_list


def sign_student_for_addition_subject_db(db: Session, subject_id: int, student_id: int):
    student_addition_subject = StudentAdditionalSubject(
        subject_id=subject_id,
        student_id=student_id
    )

    db.add(student_addition_subject)
    db.commit()
    db.refresh(student_addition_subject)
    return student_addition_subject


def select_dop_subjects(db: Session, student_id: int):
    subjects = db.query(
        Subject.id,
        Subject.title,
        Subject.image_path)\
        .join(StudentAdditionalSubject, StudentAdditionalSubject.subject_id == Subject.id)\
        .filter(StudentAdditionalSubject.student_id == student_id)\
        .all()

    return subjects


def select_subject_exam_date(db: Session, subject_id: int):
    exam_date = db.query(Subject.exam_date).filter(Subject.id == subject_id).first()
    return exam_date[0].strftime('%Y-%m-%d')


def select_subject_item_db(db: Session, subject_id: int):
    return db.query(SubjectItem).filter(SubjectItem.subject_id == subject_id).first()


def select_subject_icons_db(db: Session, subject_id: int):
    icons = db.query(SubjectIcon).filter(
        or_(
            SubjectIcon.is_default,
            SubjectIcon.subject_id == subject_id
        )
    ).all()

    return icons


def select_subject_icon_db(db: Session, icon_path: str):
    icon = db.query(SubjectIcon).filter(SubjectIcon.icon_path == icon_path).first()
    return icon


def delete_subject_icon_db(db: Session, subject_icon: SubjectIcon):
    db.delete(subject_icon)
    db.commit()


def create_or_update_participant_comment_db(
        db: Session,
        subject_id: int,
        student_id: int,
        comment: str
):
    part_comment = db.query(ParticipantComment).filter(
        ParticipantComment.subject_id == subject_id,
        ParticipantComment.student_id == student_id).first()

    if part_comment:
        part_comment.comment = comment
        db.commit()
        db.refresh(part_comment)
        return part_comment
    else:
        new_comment = ParticipantComment(
            subject_id=subject_id,
            student_id=student_id,
            comment=comment
        )
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        return new_comment


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
    return db.query(
        SubjectInstructionCategory
    ).filter(SubjectInstructionCategory.id == instruction_category_id).first()


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


def delete_subject_instruction_file_db(db: Session, file_path: str):
    instruction = db.query(SubjectInstructionFiles).filter(SubjectInstructionFiles.file == file_path).first()
    db.delete(instruction)
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
        subject_instructions = {
            "courseNumber": 1,
            "category": category.category_name,
            "categoryId": category.id,
            "categoryNumber": category.number,
            "categoryIsView": category.is_view,
            "instructions": []
        }

        instructions = (
            db.query(
                SubjectInstruction.id,
                SubjectInstruction.number,
                SubjectInstruction.title,
                SubjectInstruction.subtitle,
                SubjectInstruction.text,
                SubjectInstruction.is_view,
                func.group_concat(SubjectInstructionFiles.file_path).label("filesPath"),
                func.group_concat(SubjectInstructionFiles.file_type).label("filesType"),
                func.group_concat(SubjectInstructionFiles.filename).label("filesName"),
                func.group_concat(SubjectInstructionFiles.file_size).label("filesSize"),
                func.group_concat(SubjectInstructionFiles.number).label("numbers"),
                func.group_concat(SubjectInstructionLink.link).label("links"),
                func.group_concat(SubjectInstructionLink.number).label("link_numbers")
            )
            .outerjoin(
                SubjectInstructionFiles,
                SubjectInstruction.id == SubjectInstructionFiles.subject_instruction_id
            )
            .outerjoin(
                SubjectInstructionLink,
                SubjectInstruction.id == SubjectInstructionLink.subject_instruction_id
            )
            .filter(SubjectInstruction.subject_category_id == category.id)
            .group_by(
                SubjectInstruction.id,
                SubjectInstruction.number,
                SubjectInstruction.title,
                SubjectInstruction.subtitle,
                SubjectInstruction.text,
                SubjectInstruction.is_view
            )
            .all()
        )

        for row in instructions:
            instruction_dict = {
                "instructionId": row.id,
                "number": row.number,
                "title": row.title,
                "subTitle": row.subtitle,
                "text": row.text,
                "isView": row.is_view,
                "files": [
                    {
                        "filePath": filepath,
                        "fileType": filetype,
                        "fileName": filename,
                        "fileSize": filesize,
                        "number": number
                    } for filepath, filetype, filename, filesize, number in zip(
                        row.filesPath.split(','),
                        row.filesType.split(','),
                        row.filesName.split(','),
                        row.filesSize.split(','),
                        row.numbers.split(','),
                    )
                ] if row.filesPath else [],
                "links": [
                    {
                        "link": link,
                        "number": number
                    } for link, number in zip(
                        row.links.split(','),
                        row.link_numbers.split(',')
                    )
                ] if row.links else []
            }

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
    ).filter(
        SubjectInstructionFiles.subject_instruction_id == instruction.id
    ).all()

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
    ).filter(
        SubjectInstruction.subject_category_id == instruction_category.id
    ).all()

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
