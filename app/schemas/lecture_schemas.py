from typing import List, Optional

from pydantic import BaseModel

from app.enums import LectureAttributeType


class AttributeBase(BaseModel):
    attributeType: LectureAttributeType
    attributeTitle: str
    attributeNumber: int
    attributeText: Optional[str] = ""
    hided: Optional[bool] = False


class AttributeFile(AttributeBase):
    fileName: str
    filePath: str
    fileSize: int
    downloadAllowed: bool


class Link(BaseModel):
    link: str
    anchor: str


class UpdateLink(BaseModel):
    link: Optional[str] = None
    anchor: Optional[str] = None


class File(BaseModel):
    fileName: str
    filePath: str
    fileSize: int
    downloadAllowed: bool


class UpdateFile(BaseModel):
    fileName: Optional[str] = None
    filePath: Optional[str] = None
    fileSize: Optional[int] = None
    downloadAllowed: Optional[bool] = None


class AttributeFiles(AttributeBase):
    attributeFiles: List[File]


class AttributeLinks(AttributeBase):
    attributeLinks: List[Link]


class AttributeHomeWork(AttributeBase):
    attributeFiles: Optional[List[File]] = None
    attributeLinks: Optional[List[Link]] = None


class UpdateAttributeBase(BaseModel):
    attributeTitle: Optional[str] = None
    attributeNumber: Optional[int] = None
    attributeText: Optional[str] = None
    hided: Optional[bool] = None


class UpdateAttributeFile(UpdateAttributeBase):
    fileName: Optional[str] = None
    filePath: Optional[str] = None
    fileSize: Optional[int] = None
    downloadAllowed: Optional[bool] = None


class UpdateAttributeFiles(UpdateAttributeBase):
    attributeFiles: Optional[List[File]] = None


class UpdateAttributeLinks(UpdateAttributeBase):
    attributeLinks: Optional[List[Link]] = None


class UpdateAttributeHomeWork(UpdateAttributeBase):
    attributeFiles: Optional[List[File]] = None
    attributeLinks: Optional[List[Link]] = None
