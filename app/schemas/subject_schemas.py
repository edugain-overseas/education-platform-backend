import datetime
from typing import Optional

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
