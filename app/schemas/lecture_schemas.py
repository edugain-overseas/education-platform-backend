from typing import List

from pydantic import BaseModel


class AttributeTextBase(BaseModel):
    name: str
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
