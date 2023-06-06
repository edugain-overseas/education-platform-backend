from pydantic import BaseModel
from typing import Optional


class SubjectCreate(BaseModel):
    title: str
    description: str
    teacher_id: int
    specialization_id: int
    course_id: int


class Subject(SubjectCreate):
    id: int
    image_path: str

    class Config:
        orm_mode = True


class SubjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    teacher_id: Optional[int] = None
    specialization_id: Optional[int] = None
    course_id: Optional[int] = None
