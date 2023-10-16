from typing import List, Optional, Union

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


class AttributeText(AttributeTextBase):
    id: int

    class Config:
        orm_mode = True


class LectureText(LectureTextBase):
    id: int
    attributes: List[AttributeText] = []

    class Config:
        orm_mode = True


class TextAttribute(BaseModel):
    attributeId: int
    attributeNumber: int
    attributeType: LectureAttributeType
    attributeTitle: str
    attributeSubTitle: str
    attributeValue: str


class FileAttribute(BaseModel):
    attributeId: int
    attributeNumber: int
    attributeType: LectureAttributeType
    attributeTitle: str
    attributeSubTitle: str
    fileName: str
    fileSize: int
    filePath: str
    downloadAllowed: bool


class LectureUpdate(BaseModel):
    lectureInfo: List[Union[TextAttribute, FileAttribute]]
