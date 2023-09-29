import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel


class SubjectCreate(BaseModel):
    title: str
    description: str
    specialization_id: int
    course_id: int
    group_id: int
    is_published: Optional[bool] = None
    quantity_lecture: Optional[int] = None
    quantity_seminar: Optional[int] = None
    quantity_test: Optional[int] = None
    quantity_module: Optional[int] = None
    score: Optional[int] = None
    exam_date: Optional[datetime.date] = None


class Subject(SubjectCreate):
    id: int

    class Config:
        orm_mode = True


class SubjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    specialization_id: Optional[int] = None
    course_id: Optional[int] = None
    group_id: Optional[int] = None
    is_published: Optional[bool] = None
    quantity_lecture: Optional[int] = None
    quantity_seminar: Optional[int] = None
    quantity_test: Optional[int] = None
    quantity_module: Optional[int] = None
    score: Optional[int] = None
    exam_date: Optional[datetime.date] = None


class SubjectInstructionCreate(BaseModel):
    subject_id: int
    number: int
    title: str
    text: str
    subtitle: str
    subject_category_id: int
    is_view: bool
    files: Optional[List[Dict[str, str]]] = None


class SubjectInstructionUpdate(BaseModel):
    number: Optional[int] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    text: Optional[str] = None
    subject_category_id: Optional[int] = None
    is_view: Optional[bool] = None


class SubjectInstructionCategoryCreate(BaseModel):
    category_name: str
    number: int
    is_view: bool
    subject_id: int


class SubjectInstructionCategoryUpdate(BaseModel):
    category_name: Optional[str] = None
    number: Optional[int] = None
    is_view: Optional[bool] = None


class SubjectInstructionAttachFile(BaseModel):
    subject_instruction_id: int
    file_path: str
    filename: str
    file_size: int
    file_type: str
