from datetime import datetime, time
from typing import Optional, List, Union

from pydantic import BaseModel, validator

from app.enums import QuestionTypeOption


class TestConfigBase(BaseModel):
    is_published: bool
    min_score: Optional[int] = None
    set_timer: Optional[bool] = False
    timer: Optional[time] = None
    attempts: Optional[int] = 1
    show_answer: Optional[bool] = False
    shuffle_answer: Optional[bool] = False
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
    min_score: Optional[int] = None
    shuffle_answer: Optional[bool] = None


class AnswerBase(BaseModel):
    answerText: str
    isCorrect: bool
    imagePath: Optional[str] = None


class MatchingBase(BaseModel):
    rightText: str
    leftText: str


class QuestionBase(BaseModel):
    questionText: str
    questionNumber: int
    questionScore: int
    questionType: QuestionTypeOption
    hided: bool
    imagePath: Optional[str] = None
    questionAnswers: List[Union[AnswerBase, MatchingBase]]

    @validator("questionScore")
    def validate_question_score(cls, value):
        if value < 1:
            raise ValueError("questionScore should be greater than 0")
        if value > 200:
            raise ValueError("questionScore cannot be greater than 200")
        return value


class TestQuestionFeedback(BaseModel):
    text: str
    student_id: int
    question_id: int


class FeedbackAnswer(BaseModel):
    answer: str
    teacher_id: int
    test_feedback_id: int
