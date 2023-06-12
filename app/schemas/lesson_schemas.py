from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LessonBase(BaseModel):
    number: int
    title: str
    description: str
    is_published: Optional[bool] = False
    lesson_date: datetime
    lesson_type_id: int
    module_id: int
    subject_id: int


class Lesson(LessonBase):
    id: int

    # @validator('lesson_type_id')
    # def check_lesson_type(self, lesson_type_id):
    #     if lesson_type_id > 5:
    #         raise ValueError("Lesson type must be integer greater than 1 and less than 5")
    #     return lesson_type_id

    class Config:
        orm_mode = True


class LessonUpdate(BaseModel):
    number: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    is_published: Optional[bool] = None
    lesson_date: Optional[datetime] = None
    lesson_type_id: Optional[int] = None
    module_id: Optional[int] = None
    subject_id: Optional[int] = None

