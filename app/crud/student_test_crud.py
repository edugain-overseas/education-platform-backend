from sqlalchemy.orm import Session

from app.models import (StudentTest, StudentTestAnswer, StudentTestMatching,
                        TestQuestion, TestAnswer, TestMatchingLeft, TestMatchingRight)


def create_student_test_db(db: Session, test_id: int, student_id: int):
    student_test = StudentTest(
        score=0,
        number_attempt=1,
        test_id=test_id,
        student_id=student_id
    )
    db.add(student_test)
    db.commit()
    db.refresh(student_test)
    return student_test


def select_student_test_db(db: Session, student_id: id, test_id: int):
    return db.query(StudentTest).filter(
        StudentTest.student_id == student_id,
        StudentTest.test_id == test_id
    ).first()


def update_student_test_score_db(db: Session, student_test: StudentTest, score: int):
    student_test.score = score
    db.commit()
    db.refresh(student_test)
    return student_test


def select_correct_answer_db(db: Session, question_id: int):
    correct_answer_id = db.query(TestAnswer.id.label("id")).filter(
        TestAnswer.is_correct == 1,
        TestAnswer.question_id == question_id
    ).first()
    return correct_answer_id.id


def select_correct_answers_db(db: Session, question_id: int):
    answers_id = db.query(TestAnswer.id.label("id")).filter(
        TestAnswer.is_correct == 1,
        TestAnswer.question_id == question_id
    ).all()
    correct_answers_ids = [answer.id for answer in answers_id]
    return correct_answers_ids


def create_student_test_answer_db(
        db: Session,
        score: int,
        student_id: int,
        question_id: int,
        answer_id: int,
        student_test_id: int
):
    student_test_answer = StudentTestAnswer(
        score=score,
        student_id=student_id,
        question_id=question_id,
        answer_id=answer_id,
        student_test_id=student_test_id
    )

    db.add(student_test_answer)
    db.commit()
    db.refresh(student_test_answer)


def create_student_test_matching_db(
        db: Session,
        score: int,
        student_id: int,
        question_id: int,
        left_option_id: int,
        right_option_id: int,
        student_test_id: int
):
    student_test_matching = StudentTestMatching(
        score=score,
        student_id=student_id,
        question_id=question_id,
        left_option_id=left_option_id,
        right_option_id=right_option_id,
        student_test_id=student_test_id
    )

    db.add(student_test_matching)
    db.commit()
    db.refresh(student_test_matching)


def select_count_correct_answers_db(db: Session, question_id: int):
    count_correct_answers = db.query(TestAnswer).filter(
        TestAnswer.question_id == question_id,
        TestAnswer.is_correct == 1
    ).count()
    return count_correct_answers


def select_correct_right_option_db(db: Session, left_option_id: int):
    right_option = db.query(TestMatchingLeft.right_id.label("right_id")).filter(
        TestMatchingLeft.id == left_option_id).first()
    return right_option.right_id
