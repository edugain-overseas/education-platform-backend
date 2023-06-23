from typing import Optional

from pydantic import BaseModel


class ModuleBase(BaseModel):
    number: int
    name: str
    description: str
    subject_id: int


class CreateModule(ModuleBase):
    pass


class UpdateModule(BaseModel):
    number: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    subject_id: Optional[int] = None


class Module(ModuleBase):
    id: int

    class Config:
        orm_module = True
