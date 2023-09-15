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


def select_test_info_db(db: Session, lesson_id: int):
    test_lesson = (
        db.query(TestLesson)
        .filter(TestLesson.lesson_id == lesson_id)
        .first()
    )

    if not test_lesson:
        return None

    test_questions = (
        db.query(TestQuestion)
        .filter(TestQuestion.test_lesson_id == test_lesson.id)
        .all()
    )

    test_info = {
        "testId": test_lesson.id,
        "isPublished": test_lesson.is_published,
        "setTimer": test_lesson.set_timer,
        "timer": test_lesson.timer,
        "attempts": test_lesson.attempts,
        "showAnswer": test_lesson.show_answer,
        "deadline": str(test_lesson.deadline),
        "lessonId": test_lesson.lesson_id,
        "testQuestions": []
    }

    for question in test_questions:
        question_info = {
            "questionType": question.question_type.type_name,
            "questionText": question.question_text,
            "questionScore": question.question_score,
            "questionNumber": question.question_number,
            "questionAnswers": []
        }

        if question.question_type.type_name == "test":
            answers = (
                db.query(TestAnswer)
                .filter(TestAnswer.question_id == question.id)
                .all()
            )
            for answer in answers:
                question_info["questionAnswers"].append({
                    "answerTest": answer.answer_text,
                    "isCorrect": answer.is_correct
                })

        elif question.question_type.type_name == "matching":
            left_options = (
                db.query(TestMatchingLeft)
                .filter(TestMatchingLeft.question_id == question.id)
                .all()
            )
            right_options = (
                db.query(TestMatchingRight)
                .filter(TestMatchingRight.question_id == question.id)
                .all()
            )

            matching_pairs = list(zip(left_options, right_options))
            for left, right in matching_pairs:
                question_info["questionAnswers"].append({
                    "matchingLeft": left.text,
                    "matchingRight": right.text
                })

        test_info["testQuestions"].append(question_info)

    return test_info


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
