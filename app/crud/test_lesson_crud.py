from sqlalchemy.orm import Session

from app.models import QuestionType, TestAnswer, TestLesson, TestMatchingLeft, TestMatchingRight, TestQuestion
from app.schemas.test_lesson_schemas import TestConfigBase, TestConfigUpdate
from app.utils.lesson_utils import set_test_answer_info, set_test_question_info, set_test_answer_for_teacher_info


def create_test_db(db: Session, test_data: TestConfigBase):
    new_test = TestLesson(**test_data.dict())
    db.add(new_test)
    db.commit()
    db.refresh(new_test)
    return new_test


def select_test_db(db: Session, test_id: int):
    return db.query(TestLesson).filter(TestLesson.id == test_id).first()


def select_test_by_lesson_id_db(db: Session, lesson_id: int):
    return db.query(TestLesson).filter(TestLesson.lesson_id == lesson_id).first()


def select_question_type_id(db: Session, question_type: str):
    question_type = db.query(QuestionType.id.label("id")).filter(QuestionType.type == question_type).first()
    return question_type.id


def select_answers_db(db: Session, question_id: int):
    return db.query(TestAnswer).filter(TestAnswer.question_id == question_id).all()


def select_test_info_db(db: Session, test_id: int):
    test_questions = db.query(TestQuestion).filter(TestQuestion.test_lesson_id == test_id).all()
    result = []

    if test_questions is None:
        return result

    for question in test_questions:
        question_info = set_test_question_info(question=question)

        if question.question_type.type in ["test", "boolean"]:
            answers = select_answers_db(db=db, question_id=question.id)

            for answer in answers:
                answer_info = set_test_answer_info(answer)
                question_info["questionAnswers"].append(answer_info)

        elif question.question_type.type == "multiple_choice":
            answers = select_answers_db(db=db, question_id=question.id)
            counter = 0

            for answer in answers:
                if answer.is_correct:
                    counter += 1
                answer_info = set_test_answer_info(answer)
                question_info["questionAnswers"].append(answer_info)
            question_info["quantityCorrectAnswers"] = counter

        elif question.question_type.type == "matching":
            left_options = db.query(TestMatchingLeft).filter(TestMatchingLeft.question_id == question.id).all()
            right_options = db.query(TestMatchingRight).filter(TestMatchingRight.question_id == question.id).all()
            question_info["questionAnswers"] = {
                "left": [
                    {"value": left_option.text,
                     "id": left_option.id
                     } for left_option in left_options],
                "right": [
                    {"value": right_option.text,
                     "id": right_option.id
                     } for right_option in right_options]
            }

        elif question.question_type.type == "answer_with_photo":
            answers = select_answers_db(db=db, question_id=question.id)

            for answer in answers:
                answer_info = set_test_answer_info(answer)
                question_info["questionAnswers"].append(answer_info)

        else:
            question_info["imagePath"] = question.image_path
            answers = select_answers_db(db=db, question_id=question.id)

            for answer in answers:
                answer_info = set_test_answer_info(answer)
                question_info["questionAnswers"].append(answer_info)

        result.append(question_info)
    return result


def select_test_info_for_teacher_db(db: Session, test_id: int):
    test_questions = db.query(TestQuestion).filter(TestQuestion.test_lesson_id == test_id).all()
    result = []

    if test_questions is None:
        return result

    for question in test_questions:
        question_info = set_test_question_info(question=question)

        if question.question_type.type in ["test", "boolean"]:
            answers = select_answers_db(db=db, question_id=question.id)

            for answer in answers:
                answer_info = set_test_answer_for_teacher_info(answer)
                question_info["questionAnswers"].append(answer_info)

        elif question.question_type.type == "multiple_choice":
            answers = select_answers_db(db=db, question_id=question.id)
            counter = 0

            for answer in answers:
                if answer.is_correct:
                    counter += 1
                answer_info = set_test_answer_for_teacher_info(answer)
                question_info["questionAnswers"].append(answer_info)
            question_info["quantityCorrectAnswers"] = counter

        elif question.question_type.type == "matching":
            left_options = db.query(TestMatchingLeft).filter(TestMatchingLeft.question_id == question.id).all()
            right_options = db.query(TestMatchingRight).filter(TestMatchingRight.question_id == question.id).all()

            question_info["questionAnswers"] = {
                "left": [{
                    "value": left_option.text,
                    "id": left_option.id,
                    "rightId": left_option.right_id
                } for left_option in left_options],

                "right": [{
                    "value": right_option.text,
                    "id": right_option.id
                } for right_option in right_options]
            }

        elif question.question_type.type == "answer_with_photo":
            answers = select_answers_db(db=db, question_id=question.id)

            for answer in answers:
                answer_info = set_test_answer_for_teacher_info(answer)
                question_info["questionAnswers"].append(answer_info)

        else:
            question_info["imagePath"] = question.image_path
            answers = select_answers_db(db=db, question_id=question.id)

            for answer in answers:
                answer_info = set_test_answer_info(answer)
                question_info["questionAnswers"].append(answer_info)

        result.append(question_info)
    return result


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


def set_test_question_path_db(db: Session, image_path: str):
    question = db.query(TestQuestion).filter(TestQuestion.image_path == image_path).first()
    question.image_path = None
    db.commit()
    db.refresh(question)
    return


def delete_test_question_db(db: Session, question: TestQuestion):
    db.delete(question)
    db.commit()


def update_test_question_db(
        db: Session,
        question: TestQuestion,
        text: str,
        number: int,
        score: int,
        hided: bool,
        image_path: str = None
):
    question.question_text = text
    question.question_number = number
    question.question_score = score
    question.hided = hided

    if image_path:
        question.image_path = image_path

    db.commit()
    db.refresh(question)
    return question


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


def set_test_answer_path_db(db: Session, image_path: str):
    answer = db.query(TestAnswer).filter(TestAnswer.image_path == image_path).first()
    answer.image_path = None
    db.commit()
    db.refresh(answer)
    return


def update_test_answer_db(
        db: Session,
        answer: TestAnswer,
        text: str,
        is_correct: bool,
        image_path: str = None
):
    answer.answer_text = text
    answer.is_correct = is_correct
    if image_path:
        answer.image_path = image_path

    db.commit()
    db.refresh(answer)
    return answer


def delete_answer_db(db: Session, answer: TestAnswer):
    db.delete(answer)
    db.commit()


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


def select_matching_right_db(db: Session, right_id: int):
    return db.query(TestMatchingRight).filter(TestMatchingRight.id == right_id).first()


def select_matching_left_db(db: Session, left_id: int):
    return db.query(TestMatchingLeft).filter(TestMatchingLeft.id == left_id).first()


def select_mathing_left_by_right_id_db(db: Session, right_id: int):
    return db.query(TestMatchingLeft).filter(TestMatchingLeft.right_id == right_id).first()


def delete_matching_right_db(db: Session, right_option: TestMatchingRight):
    db.delete(right_option)
    db.commit()


def delete_matching_left_db(db: Session, left_option: TestMatchingLeft):
    db.delete(left_option)
    db.commit()


def set_none_for_left_option_db(db: Session, left_option: TestMatchingLeft):
    left_option.right_id = None
    db.commit()
    db.refresh(left_option)
