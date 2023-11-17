from typing import Optional

from pydantic import BaseModel


class SubjectInstructionCreate(BaseModel):
    subject_id: int
    number: int
    title: str
    text: str
    subtitle: str
    subject_category_id: int
    is_view: bool


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
    number: int


class SubjectInstructionAttachLink(BaseModel):
    subject_instruction_id: int
    link: str
    number: int
