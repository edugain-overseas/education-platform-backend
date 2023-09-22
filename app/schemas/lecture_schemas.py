from enum import Enum
from typing import List

from pydantic import BaseModel


class AttributeType(str, Enum):
    title = "title"
    text = "text"
    present = "present"
    audio = "audio"
    picture = "picture"
    file = "file"
    link = "link"
    homework = "homework"


class AttributeTextBase(BaseModel):
    attr_type: AttributeType
    attr_title: str
    attr_number: int
    download_allowed: bool
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
