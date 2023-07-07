from enum import Enum
from typing import Optional

from pydantic import BaseModel


class UserType(str, Enum):
    student = 'student'
    moder = 'moder'
    teacher = 'teacher'
    curator = 'curator'


class StudentCreate(BaseModel):
    username: str
    password: str
    usertype: UserType
    name: str
    surname: str
    lastname: str
    phone: str
    email: str
    group_leader: Optional[bool] = None
    qualification: Optional[str] = None
    educational_program: Optional[str] = None
    subject_area: Optional[str] = None
    field_of_study: Optional[str] = None

    class Config:
        orm_mode = True


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    lastname: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    qualification: Optional[str] = None
    educational_program: Optional[str] = None
    subject_area: Optional[str] = None
    field_of_study: Optional[str] = None
    group_leader: Optional[bool] = None
    specialization_id: Optional[int] = None
    course_id: Optional[int] = None
    group_id: Optional[int] = None

    class Config:
        orm_mode = True


class TeacherCreate(BaseModel):
    username: str
    password: str
    usertype: UserType
    name: str
    surname: str
    lastname: str
    email: str

    class Config:
        orm_mode = True


class CuratorCreate(BaseModel):
    username: str
    password: str
    usertype: UserType
    name: str
    surname: str
    lastname: str
    email: str

    class Config:
        orm_mode = True


class ModerCreate(BaseModel):
    username: str
    password: str
    usertype: UserType
    name: str
    surname: str
    lastname: str

    class Config:
        orm_mode = True
