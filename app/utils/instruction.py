from typing import Dict, List

from fastapi import UploadFile

from app.models import SubjectInstruction, SubjectInstructionCategory, SubjectInstructionFiles, SubjectInstructionLink
from app.utils.save_images import save_subject_instructions


def save_subject_instruction_file(files: List[UploadFile]) -> List:
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


def save_subject_instruction_link(link: SubjectInstructionLink) -> List:
    result = {"number": link.number, "id": link.id,
              "link": link.link, "subject_instruction_id": link.subject_instruction_id}

    return result


def set_instruction_category(category: SubjectInstructionCategory) -> Dict:
    subject_instructions = {
        "courseNumber": 1,
        "category": category.category_name,
        "categoryId": category.id,
        "categoryNumber": category.number,
        "categoryIsView": category.is_view,
        "instructions": []
    }
    return subject_instructions


def set_instruction(instruction: SubjectInstruction) -> Dict:
    instruction_dict = {
        "instructionId": instruction.id,
        "number": instruction.number,
        "title": instruction.title,
        "subTitle": instruction.subtitle,
        "text": instruction.text,
        "isView": instruction.is_view,
        "files": [],
        "links": []
    }

    return instruction_dict


def set_instruction_file(instruction_file: SubjectInstructionFiles) -> Dict:
    file_dict = {
        "fileId": instruction_file.id,
        "filePath": instruction_file.file_path,
        "fileType": instruction_file.file_type,
        "fileName": instruction_file.filename,
        "fileSize": instruction_file.file_size,
        "number": instruction_file.number
    }
    return file_dict


def set_instruction_link(instruction_link: SubjectInstructionLink) -> Dict:
    link_dict = {
        "linkId": instruction_link.id,
        "link": instruction_link.link,
        "number": instruction_link.number
    }
    return link_dict
