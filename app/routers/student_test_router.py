from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models import User
from app.session import get_db
from app.crud.student_test_crud import create_student_test_db, update_student_test_score_db
from app.crud.test_lesson_crud import select_test_question_db
from app.utils.token import get_current_user
from app.schemas.student_test_schemas import StudentTest
from app.utils.student_test import check_default_test, check_multiple_test, check_matching_test

router = APIRouter()


@router.post("/student-test/create")
async def create_student_test(
        data: StudentTest,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    student_test = create_student_test_db(db=db, test_id=data.testId, student_id=data.studentId)
    total_score = 0

    for student_answer in data.studentAnswers:
        question = select_test_question_db(db=db, question_id=student_answer.questionId)

        if student_answer.questionType == "matching":
            student_score = check_matching_test(
                db=db,
                matching=student_answer.matching,
                question=question,
                student_id=data.studentId,
                student_test_id=student_test.id
            )
            total_score += student_score

        elif student_answer.questionType == "multiple_choice":
            student_score = check_multiple_test(
                db=db,
                student_answers=student_answer.answersIds,
                question=question,
                student_id=data.studentId,
                student_test_id=student_test.id
            )
            total_score += student_score

        else:
            student_score = check_default_test(
                db=db,
                student_answer_id=student_answer.answerId,
                question=question,
                student_id=data.studentId,
                student_test_id=student_test.id
            )
            total_score += student_score

    update_student_test_score_db(db=db, student_test=student_test, score=total_score)
    return {"message": f"Оценка за тест {total_score} баллов"}