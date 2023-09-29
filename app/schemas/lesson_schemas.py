from datetime import datetime, time
from typing import Optional

from pydantic import BaseModel

from app.models import LessonTypeOption


class LessonBase(BaseModel):
    number: int
    title: str
    description: str
    is_published: Optional[bool] = False
    lesson_date: datetime
    lesson_end: time
    lesson_type: LessonTypeOption
    module_id: int
    subject_id: int
    teacher_id: int


class Lesson(LessonBase):
    id: int

    class Config:
        orm_mode = True


class LessonUpdate(BaseModel):
    number: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    is_published: Optional[bool] = None
    lesson_date: Optional[datetime] = None
    lesson_end: Optional[time] = None
    lesson_type: Optional[LessonTypeOption] = None
    module_id: Optional[int] = None
    subject_id: Optional[int] = None
    teacher_id: Optional[int] = None
