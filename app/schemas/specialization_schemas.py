from pydantic import BaseModel


class SpecializationCreate(BaseModel):
    title: str
    course_id: int


class Specialization(SpecializationCreate):
    id: int

    class Config:
        orm_mode = True
