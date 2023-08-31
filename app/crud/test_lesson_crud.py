from sqlalchemy.orm import Session

from app.models import (TestAnswer, TestLesson, TestMatchingLeft,
                        TestMatchingRight, TestQuestion)
from app.schemas.test_lesson_schemas import (TesMatchingBase, TestAnswerBase,
                                             TestConfigBase, TestConfigUpdate,
                                             TestQuestionBase)


def create_test_db(db: Session, test_data: TestConfigBase):
    new_test = TestLesson(**test_data.dict())
    db.add(new_test)
    db.commit()
    db.refresh(new_test)
    return new_test


def select_test_db(db: Session, test_id: int):
    return db.query(TestLesson).filter(TestLesson.id == test_id).first()


def update_test_db(db: Session, test: TestLesson, test_data: TestConfigUpdate):
    for field, value in test_data:
        if value is not None:
            setattr(test, field, value)

    test.timer = test_data.timer
    db.commit()
    db.refresh(test)
    return test


def create_test_question_db(db: Session, question_data: TestQuestionBase):
    new_question = TestQuestion(**question_data.dict())
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question


def create_test_answer_db(db: Session, answer_data: TestAnswerBase):
    new_answer = TestAnswer(**answer_data.dict())
    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)
    return new_answer


def create_test_matching_db(db: Session, matching_data: TesMatchingBase):
    right_option = TestMatchingRight(
        text=matching_data.right_text,
        question_id=matching_data.question_id
    )

    db.add(right_option)
    db.commit()

    left_option = TestMatchingLeft(
        text=matching_data.left_text,
        question_id=matching_data.question_id,
        right_id=right_option.id
    )

    db.add(left_option)
    db.commit()
    db.refresh(right_option)
    db.refresh(left_option)

    return left_option
