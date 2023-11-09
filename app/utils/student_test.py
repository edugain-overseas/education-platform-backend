from sqlalchemy.orm import Session

from app.crud.student_test_crud import (create_student_test_answer_db, create_student_test_matching_db,
                                        select_correct_answer_db, select_correct_answers_db,
                                        select_correct_right_option_db, select_count_correct_answers_db)
from app.crud.subject_crud import (filling_journal, select_journal_row, select_lesson_id_and_subject_id_by_test_id_db,
                                   update_score_to_journal)
from app.models import TestQuestion
from app.schemas.student_test_schemas import MatchingField
from app.session import SessionLocal


def check_default_test(
        db: Session,
        student_answer_id: int,
        question: TestQuestion,
        student_id: int,
        student_test_id: int

):
    correct_answer_id = select_correct_answer_db(db=db, question_id=question.id)
    if correct_answer_id == student_answer_id:
        create_student_test_answer_db(
            db=db,
            score=question.question_score,
            student_id=student_id,
            question_id=question.id,
            answer_id=student_answer_id,
            student_test_id=student_test_id
        )
        return question.question_score
    else:
        create_student_test_answer_db(
            db=db,
            score=0,
            student_id=student_id,
            question_id=question.id,
            answer_id=student_answer_id,
            student_test_id=student_test_id
        )
        return 0


def check_multiple_test(
        db: Session,
        student_answers: list[int],
        question: TestQuestion,
        student_id: int,
        student_test_id: int

):
    correct_answers = select_correct_answers_db(db=db, question_id=question.id)
    question_score = question.question_score
    count_correct_answers = select_count_correct_answers_db(db=db, question_id=question.id)
    score_for_one_answer = question_score / count_correct_answers

    student_correct_answers = []
    student_wrong_answers = []

    for student_answer in student_answers:
        if student_answer in correct_answers:
            student_correct_answers.append(student_answer)
        else:
            student_wrong_answers.append(student_answer)

    student_score = ((len(student_correct_answers) * score_for_one_answer) -
                     (len(student_wrong_answers) * score_for_one_answer))

    counter = 1
    for answer_id in student_answers:
        if counter == 1:
            create_student_test_answer_db(
                db=db,
                score=int(student_score),
                student_id=student_id,
                question_id=question.id,
                answer_id=answer_id,
                student_test_id=student_test_id
            )
        else:
            create_student_test_answer_db(
                db=db,
                score=0,
                student_id=student_id,
                question_id=question.id,
                answer_id=answer_id,
                student_test_id=student_test_id
            )

    if student_score <= 0:
        return 0
    return int(student_score)


def check_matching_test(
        db: Session,
        matching: list[MatchingField],
        question: TestQuestion,
        student_id: int,
        student_test_id: int
):
    question_score = question.question_score
    count_matching = len(question.matching_left)
    score_one_match = question_score / count_matching
    student_correct_match = 0

    for match in matching:
        correct_right_id = select_correct_right_option_db(db=db, left_option_id=match.leftOptionId)
        if match.rightOptionId == correct_right_id:
            student_correct_match += 1
            create_student_test_matching_db(
                db=db,
                score=int(score_one_match),
                student_id=student_id,
                question_id=question.id,
                left_option_id=match.leftOptionId,
                right_option_id=match.rightOptionId,
                student_test_id=student_test_id
            )
        else:
            create_student_test_matching_db(
                db=db,
                score=0,
                student_id=student_id,
                question_id=question.id,
                left_option_id=match.leftOptionId,
                right_option_id=match.rightOptionId,
                student_test_id=student_test_id
            )

    student_score = student_correct_match * score_one_match
    return student_score


def write_score_to_journal(student_id: int, score: int, test_id: int):
    db = SessionLocal()
    data = select_lesson_id_and_subject_id_by_test_id_db(db=db, test_id=test_id)
    journal_data = select_journal_row(
        db=db,
        student_id=student_id,
        subject_id=data.subject_id,
        lesson_id=data.lesson_id
    )

    if journal_data is None:
        filling_journal(
            db=db,
            score=score,
            subject_id=data.subject_id,
            lesson_id=data.lesson_id,
            student_id=student_id
        )
    else:
        update_score_to_journal(db=db, journal_row=journal_data, score=score)
