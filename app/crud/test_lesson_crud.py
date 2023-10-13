from sqlalchemy.orm import Session

from app.models import (Lesson, TestAnswer, TestFeedback, TestFeedbackAnswer, TestLesson, TestMatchingLeft,
                        TestMatchingRight, TestQuestion, QuestionType)
from app.schemas.test_lesson_schemas import FeedbackAnswer,TestConfigBase, TestConfigUpdate,  TestQuestionFeedback


def create_test_db(db: Session, test_data: TestConfigBase):
    new_test = TestLesson(**test_data.dict())
    db.add(new_test)
    db.commit()
    db.refresh(new_test)
    return new_test


def select_test_db(db: Session, test_id: int):
    return db.query(TestLesson).filter(TestLesson.id == test_id).first()


def select_question_type_id(db: Session, question_type: str):
    question_type = db.query(QuestionType.id.label("id")).filter(QuestionType.type == question_type).first()
    return question_type.id


def select_test_info_db(db: Session, lesson_id: int):
    lesson_info = db.query(
        Lesson.title.label("lesson_title"),
        Lesson.description.label("lesson_description")
    )\
        .filter(Lesson.id == lesson_id)\
        .first()

    test_lesson = db.query(TestLesson).filter(TestLesson.lesson_id == lesson_id).first()

    if not test_lesson:
        return None

    test_questions = db.query(TestQuestion).filter(TestQuestion.test_lesson_id == test_lesson.id).all()

    test_info = {
        "lessonTitle": lesson_info.lesson_title,
        "lessonDescription": lesson_info.lesson_description,
        "lessonId": test_lesson.lesson_id,
        "testId": test_lesson.id,
        "isPublished": test_lesson.is_published,
        "setTimer": test_lesson.set_timer,
        "timer": test_lesson.timer,
        "attempts": test_lesson.attempts,
        "showAnswer": test_lesson.show_answer,
        "minScore": test_lesson.min_score,
        "shuffleAnswer": test_lesson.shuffle_answer,
        "deadline": str(test_lesson.deadline),
        "testQuestions": []
    }

    for question in test_questions:
        question_info = {
            "questionId": question.id,
            "questionType": question.question_type.type,
            "questionText": question.question_text,
            "questionScore": question.question_score,
            "questionNumber": question.question_number,
            "questionAnswers": []
        }

        if question.question_type.type in ["test", "boolean"]:
            answers = db.query(TestAnswer).filter(TestAnswer.question_id == question.id).all()

            for answer in answers:
                question_info["questionAnswers"].append({
                    "answerId": answer.id,
                    "answerText": answer.answer_text,
                })

        elif question.question_type.type == "multiple_choice":
            answers = db.query(TestAnswer).filter(TestAnswer.question_id == question.id).all()
            counter = 0

            for answer in answers:
                if answer.is_correct:
                    counter += 1

                question_info["questionAnswers"].append({
                    "answerId": answer.id,
                    "answerText": answer.answer_text,
                })

            question_info["quantityCorrectAnswers"] = counter

        elif question.question_type.type == "matching":
            left_options = db.query(TestMatchingLeft).filter(TestMatchingLeft.question_id == question.id).all()
            right_options = db.query(TestMatchingRight).filter(TestMatchingRight.question_id == question.id).all()

            question_info["questionAnswers"] = {
                "left": [{"value": left_option.text, "id": left_option.id} for left_option in left_options],
                "right": [{"value": right_option.text, "id": right_option.id} for right_option in right_options]
            }

        elif question.question_type.type == "answer_with_photo":
            answers = db.query(TestAnswer).filter(TestAnswer.question_id == question.id).all()

            for answer in answers:
                question_info["questionAnswers"].append({
                    "answerId": answer.id,
                    "answerText": answer.answer_text,
                    "imagePath": answer.image_path
                })

        else:
            question_info["imagePath"] = question.image_path
            answers = db.query(TestAnswer).filter(TestAnswer.question_id == question.id).all()
            for answer in answers:
                question_info["questionAnswers"].append({
                    "answerId": answer.id,
                    "answerText": answer.answer_text,
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


def create_test_question_db(
        db: Session,
        question_text: str,
        question_number: int,
        question_score: int,
        question_type_id: int,
        test_lesson_id: int,
        hided: bool
):
    question = TestQuestion(
        question_text=question_text,
        question_number=question_number,
        question_score=question_score,
        question_type_id=question_type_id,
        test_lesson_id=test_lesson_id,
        hided=hided
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


def create_test_question_with_photo_db(
        db: Session,
        question_text: str,
        question_number: int,
        question_score: int,
        question_type_id: int,
        test_lesson_id: int,
        hided: bool,
        image_path: str
):
    question = TestQuestion(
        question_text=question_text,
        question_number=question_number,
        question_score=question_score,
        question_type_id=question_type_id,
        test_lesson_id=test_lesson_id,
        hided=hided,
        image_path=image_path
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


def select_test_question_db(db: Session, question_id: int):
    return db.query(TestQuestion).filter(TestQuestion.id == question_id).first()


# def update_test_question_db(db: Session, question: TestQuestion, question_data: TestQuestionUpdate):
#     for field, value in question_data:
#         if value is not None:
#             setattr(question, field, value)
#     db.commit()
#     db.refresh(question)
#     return question


def create_test_answer_db(
        db: Session,
        answer_text: str,
        is_correct: bool,
        question_id: int
):
    answer = TestAnswer(
        answer_text=answer_text,
        is_correct=is_correct,
        question_id=question_id,
    )
    db.add(answer)
    db.commit()
    db.refresh(answer)
    return answer


def create_test_answer_with_photo_db(
        db: Session,
        answer_text: str,
        is_correct: bool,
        question_id: int,
        image_path: str
):
    answer = TestAnswer(
        answer_text=answer_text,
        is_correct=is_correct,
        question_id=question_id,
        image_path=image_path
    )
    db.add(answer)
    db.commit()
    db.refresh(answer)
    return answer


def select_test_answer_db(db: Session, answer_id: int):
    return db.query(TestAnswer).filter(TestAnswer.id == answer_id).first()


# def update_test_answer_db(db: Session, answer: TestAnswer, answer_data: TestAnswerUpdate):
#     for filed, value in answer_data:
#         if value is not None:
#             setattr(answer, filed, value)
#     db.commit()
#     db.refresh(answer)
#     return answer


def create_test_matching_db(db: Session, right_text: str, left_text: str, question_id: int):
    right_option = TestMatchingRight(
        text=right_text,
        question_id=question_id
    )

    db.add(right_option)
    db.commit()

    left_option = TestMatchingLeft(
        text=left_text,
        question_id=question_id,
        right_id=right_option.id
    )

    db.add(left_option)
    db.commit()
    db.refresh(right_option)
    db.refresh(left_option)

    return {"leftOption": left_option, "rightOption": right_option}


# def select_test_matching_left_db(db: Session, left_option_id: int):
#     return db.query(TestMatchingLeft).filter(TestMatchingLeft.id == left_option_id).first()
#
#
# def select_test_matching_right_db(db: Session, right_option_id: int):
#     return db.query(TestMatchingRight).filter(TestMatchingRight.id == right_option_id).first()


# def update_test_matching_left_db(
#         db: Session,
#         test_matching_left: TestMatchingLeft,
#         matching_left_data: TestMatchingLeftUpdate
# ):
#     for field, value in matching_left_data:
#         if value is not None:
#             setattr(test_matching_left, field, value)
#
#     db.commit()
#     db.refresh(test_matching_left)
#     return test_matching_left


# def update_test_matching_right_db(
#         db: Session,
#         test_matching_right: TestMatchingRight,
#         matching_right_data: TestMatchingRightUpdate
# ):
#     for field, value in matching_right_data:
#         if value is not None:
#             setattr(test_matching_right, field, value)
#
#     db.commit()
#     db.refresh(test_matching_right)
#     return test_matching_right


def create_test_feedback_db(db: Session, feedback_data: TestQuestionFeedback):
    new_feedback = TestFeedback(**feedback_data.dict())
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback


def select_test_feedback_db(db: Session, question_id: int = None, student_id: int = None):
    if student_id is None:
        return db.query(TestFeedback).filter(TestFeedback.question_id == question_id).all()
    else:
        return db.query(TestFeedback).filter(TestFeedback.student_id == student_id).all()


def create_feedback_answer_db(db: Session, answer_data: FeedbackAnswer):
    new_answer = TestFeedbackAnswer(**answer_data.dict())
    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)
    return new_answer


def select_feedback_answer_db(db: Session, teacher_id: int = None, test_feedback_id: int = None):
    if test_feedback_id is None:
        return db.query(TestFeedbackAnswer).filter(TestFeedbackAnswer.teacher_id == teacher_id).all()
    else:
        return db.query(TestFeedbackAnswer).filter(TestFeedbackAnswer.test_feedback_id == test_feedback_id).all()
