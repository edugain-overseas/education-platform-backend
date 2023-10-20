from typing import List, Optional

from pydantic import BaseModel

from app.enums import LectureAttributeType


class AttributeBase(BaseModel):
    AttributeType: LectureAttributeType
    AttributeTitle: str
    AttributeNumber: int
    AttributeText: Optional[str] = ""
    hided: Optional[bool] = False


class AttributeFile(AttributeBase):
    filename: str
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
    filename: str
    filePath: str
    fileSize: int
    downloadAllowed: bool


class UpdateFile(BaseModel):
    filename: Optional[str] = None
    filePath: Optional[str] = None
    fileSize: Optional[int] = None
    downloadAllowed: Optional[bool] = None


class AttributeFiles(AttributeBase):
    AttributeFiles: List[File]


class AttributeLinks(AttributeBase):
    AttributeLinks: List[Link]


class AttributeHomeWork(AttributeBase):
    AttributeFiles: Optional[List[File]] = None
    AttributeLinks: Optional[List[Link]] = None


class UpdateAttributeBase(BaseModel):
    AttributeTitle: Optional[str] = None
    AttributeNumber: Optional[int] = None
    AttributeText: Optional[str] = None
    hided: Optional[bool] = None


class UpdateAttributeFile(UpdateAttributeBase):
    filename: Optional[str] = None
    filePath: Optional[str] = None
    fileSize: Optional[int] = None
    downloadAllowed: Optional[bool] = None


class UpdateAttributeFiles(UpdateAttributeBase):
    AttributeFiles: Optional[List[File]] = None


class UpdateAttributeLinks(UpdateAttributeBase):
    AttributeLinks: Optional[List[Link]] = None


class UpdateAttributeHomeWork(UpdateAttributeBase):
    AttributeFiles: Optional[List[File]] = None
    AttributeLinks: Optional[List[Link]] = None
