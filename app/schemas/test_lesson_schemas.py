from datetime import datetime, time
from typing import Optional

from pydantic import BaseModel, validator


class TestConfigBase(BaseModel):
    is_published: bool
    set_timer: Optional[bool] = False
    timer: Optional[time] = None
    attempts: int = 1
    show_answer: Optional[bool] = False
    deadline: Optional[datetime] = None
    lesson_id: int


class TestConfig(TestConfigBase):
    id: int

    class Config:
        orm_mode = True


class TestConfigUpdate(BaseModel):
    is_published: Optional[bool] = None
    set_timer: Optional[bool] = None
    timer: Optional[time] = None
    attempts: Optional[int] = None
    show_answer: Optional[bool] = None
    deadline: Optional[datetime] = None


class TestQuestionBase(BaseModel):
    question_text: str
    question_number: int
    question_score: int
    question_type_id: int
    test_lesson_id: int

    @validator("question_score")
    def validate_question_score(cls, value):
        if value < 1:
            raise ValueError("question_score should be greater than 0")
        if value > 200:
            raise ValueError("question_score cannot be greater than 200")
        return value


class TestQuestionUpdate(BaseModel):
    question_text: Optional[str] = None
    question_number: Optional[int] = None
    question_score: Optional[int] = None
    question_type_id: Optional[int] = None


class TestAnswerBase(BaseModel):
    answer_text: str
    is_correct: bool
    question_id: int


class TestAnswerUpdate(BaseModel):
    answer_text: Optional[str] = None
    is_correct: Optional[bool] = None
    question_id: Optional[int] = None


class TesMatchingBase(BaseModel):
    left_text: str
    right_text: str
    question_id: int


class TestMatchingLeftUpdate(BaseModel):
    text: Optional[str] = None
    right_id: Optional[int] = None
    question_id: Optional[int] = None


class TestMatchingRightUpdate(BaseModel):
    text: Optional[str] = None
    question_id: Optional[int] = None
