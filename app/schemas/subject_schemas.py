from datetime import date
from typing import Optional

from pydantic import BaseModel


class SubjectCreate(BaseModel):
    title: str
    description: str
    specialization_id: int
    course_id: int
    # image_path: Optional[str] = None
    # logo_path: Optional[str] = None
    is_published: Optional[bool] = None
    quantity_lecture: Optional[int] = None
    quantity_seminar: Optional[int] = None
    quantity_test: Optional[int] = None
    quantity_webinar: Optional[int] = None
    score: Optional[int] = None
    exam_date: Optional[date] = None


class Subject(SubjectCreate):
    id: int

    class Config:
        orm_mode = True


class SubjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    specialization_id: Optional[int] = None
    course_id: Optional[int] = None
    is_published: Optional[bool] = None
    quantity_lecture: Optional[int] = None
    quantity_seminar: Optional[int] = None
    quantity_test: Optional[int] = None
    quantity_webinar: Optional[int] = None
    score: Optional[int] = None
    exam_date: Optional[date] = None
