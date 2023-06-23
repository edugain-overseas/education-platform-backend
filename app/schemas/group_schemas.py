from typing import Optional

from pydantic import BaseModel


class GroupCreate(BaseModel):
    group_name: str
    teacher_id: int
    curator_id: int
    specialization_id: int


class Group(GroupCreate):
    id: int

    class Config:
        orm_mode = True


class GroupUpdate(BaseModel):
    group_name: Optional[str] = None
    teacher_id: Optional[int] = None
    curator_id: Optional[int] = None
    specialization_id: Optional[int] = None

    class Config:
        orm_mode = True
