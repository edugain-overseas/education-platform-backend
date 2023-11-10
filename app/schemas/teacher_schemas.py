from typing import Dict, List

from pydantic import BaseModel

from app.enums import LessonTypeOption


class TeacherTemplateSchemas(BaseModel):
    name: str
    template: List[Dict]
    basis: LessonTypeOption
    teacher_id: int
