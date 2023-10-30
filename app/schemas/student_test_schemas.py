from typing import List, Union
from pydantic import BaseModel

from app.enums import QuestionTypeOption


class AnswerBase(BaseModel):
    questionId: int
    questionType: QuestionTypeOption


class AnswerTest(AnswerBase):
    answerId: int


class AnswersTest(AnswerBase):
    answersIds: List[int]


class MatchingField(BaseModel):
    leftOptionId: int
    rightOptionId: int


class MatchingTest(AnswerBase):
    matching: List[MatchingField]


class StudentTest(BaseModel):
    studentId: int
    testId: int
    studentAnswers: List[Union[AnswerTest, AnswersTest, MatchingTest]]
