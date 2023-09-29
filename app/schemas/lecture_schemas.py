from typing import List, Optional

from pydantic import BaseModel

from app.models import LectureAttributeType


class AttributeTextBase(BaseModel):
    attr_type: LectureAttributeType
    attr_title: str
    attr_subtitle: Optional[str] = None
    attr_number: int
    value: str


class LectureTextBase(BaseModel):
    attributes: List[AttributeTextBase]


class LectureTextCreate(LectureTextBase):
    pass


class LectureTextUpdate(LectureTextBase):
    pass


class AttributeText(AttributeTextBase):
    id: int

    class Config:
        orm_mode = True


class LectureText(LectureTextBase):
    id: int
    attributes: List[AttributeText] = []

    class Config:
        orm_mode = True


class AttributeBase(BaseModel):
    attr_type: LectureAttributeType
    attr_title: str
    attr_subtitle: Optional[str] = None
    attr_number: int
    download_allowed: bool
