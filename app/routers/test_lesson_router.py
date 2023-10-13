from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.crud.test_lesson_crud import (create_feedback_answer_db, create_test_answer_db, create_test_db,
                                       create_test_feedback_db, create_test_matching_db, create_test_question_db,
                                       select_feedback_answer_db, select_test_answer_db, select_test_db,
                                       select_test_feedback_db, select_test_info_db, select_test_question_db,
                                       select_question_type_id, update_test_db,
                                       create_test_answer_with_photo_db, create_test_question_with_photo_db)
from app.models import User
from app.schemas.test_lesson_schemas import (FeedbackAnswer, QuestionBase,
                                             TestConfigBase, TestConfigUpdate, TestQuestionFeedback)
from app.session import get_db
from app.utils.save_images import save_lesson_file
from app.utils.token import get_current_user

router = APIRouter()


@router.post("/test/create")
async def create_test_config(
        test_data: TestConfigBase,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return create_test_db(db=db, test_data=test_data)


@router.post("/test/create-data/{test_id}")
async def create_test_data(
        test_id: int,
        data: List[QuestionBase],
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    for question_data in data:
        if question_data.questionType in ["boolean", "test", "multiple_choice"]:
            question_type_id = select_question_type_id(db=db, question_type=question_data.questionType)

            question = create_test_question_db(
                db=db,
                question_text=question_data.questionText,
                question_number=question_data.questionNumber,
                question_score=question_data.questionScore,
                question_type_id=question_type_id,
                test_lesson_id=test_id,
                hided=question_data.hided
            )

            for answer_data in question_data.questionAnswers:
                create_test_answer_db(
                    db=db,
                    answer_text=answer_data.answerText,
                    is_correct=answer_data.isCorrect,
                    question_id=question.id
                )
        elif question_data.questionType == "answer_with_photo":
            question_type_id = select_question_type_id(db=db, question_type=question_data.questionType)

            question = create_test_question_db(
                db=db,
                question_text=question_data.questionText,
                question_number=question_data.questionNumber,
                question_score=question_data.questionScore,
                question_type_id=question_type_id,
                test_lesson_id=test_id,
                hided=question_data.hided
            )

            for answer_data in question_data.questionAnswers:
                create_test_answer_with_photo_db(
                    db=db,
                    answer_text=answer_data.answerText,
                    is_correct=answer_data.isCorrect,
                    question_id=question.id,
                    image_path=answer_data.imagePath
                )

        elif question_data.questionType == "question_with_photo":
            question_type_id = select_question_type_id(db=db, question_type=question_data.questionType)

            question = create_test_question_with_photo_db(
                db=db,
                question_text=question_data.questionText,
                question_number=question_data.questionNumber,
                question_score=question_data.questionScore,
                question_type_id=question_type_id,
                test_lesson_id=test_id,
                hided=question_data.hided,
                image_path=question_data.imagePath
            )

            for answer_data in question_data.questionAnswers:
                create_test_answer_db(
                    db=db,
                    answer_text=answer_data.answerText,
                    is_correct=answer_data.isCorrect,
                    question_id=question.id
                )

        elif question_data.questionType == "matching":
            question_type_id = select_question_type_id(db=db, question_type=question_data.questionType)

            question = create_test_question_db(
                db=db,
                question_text=question_data.questionText,
                question_number=question_data.questionNumber,
                question_score=question_data.questionScore,
                question_type_id=question_type_id,
                test_lesson_id=test_id,
                hided=question_data.hided
            )

            for answer_data in question_data.questionAnswers:
                create_test_matching_db(
                    db=db,
                    right_text=answer_data.rightText,
                    left_text=answer_data.leftText,
                    question_id=question.id
                )

    return {"Message": "Test data have been saved"}


@router.put("/test/update")
async def update_test(
        test_id: int,
        test_data: TestConfigUpdate,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    test = select_test_db(db=db, test_id=test_id)
    return update_test_db(db=db, test=test, test_data=test_data)


@router.get("/test/{lesson_id}")
async def get_test_info(
        lesson_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    test_info = select_test_info_db(db=db, lesson_id=lesson_id)

    if test_info is None:
        raise HTTPException(status_code=404, detail="Test not found")
    return test_info


@router.post("/test/upload/image")
async def upload_test_image(
        file: UploadFile = File(...),
        user: User = Depends(get_current_user)
):
    if user.moder or user.teacher:
        file_path = save_lesson_file(file=file)
        return {"filePath": file_path}
    else:
        raise HTTPException(
            status_code=401,
            detail="Permission denied"
        )


# @router.post("/test/feedback")
# async def create_test_feedback(
#         test_feedback_data: TestQuestionFeedback,
#         db: Session = Depends(get_db),
#         user: User = Depends(get_current_user)
# ):
#     if user.student:
#         return create_test_feedback_db(db=db, feedback_data=test_feedback_data)
#     else:
#         raise HTTPException(
#             status_code=401,
#             detail='Permission denied'
#         )


# @router.get("/test/feedback/question/{question_id}")
# async def get_test_feedback_by_question(
#         question_id: int,
#         db: Session = Depends(get_db),
#         user: User = Depends(get_current_user)
# ):
#     return select_test_feedback_db(db=db, question_id=question_id)


# @router.get("/test/feedback/student/{student_id}")
# async def get_test_feedback_by_student(
#         student_id: int,
#         db: Session = Depends(get_db),
#         user: User = Depends(get_current_user)
# ):
#     return select_test_feedback_db(db=db, student_id=student_id)


# @router.post("/feedback/answer")
# async def create_test_feedback_answer(
#         answer_data: FeedbackAnswer,
#         db: Session = Depends(get_db),
#         user: User = Depends(get_current_user)
# ):
#     if user.teacher:
#         return create_feedback_answer_db(db=db, answer_data=answer_data)
#     else:
#         raise HTTPException(
#             status_code=401,
#             detail="Permission denied"
#         )


# @router.get("/feedback/answer/teacher/{teacher_id}")
# async def get_feedback_answer_by_teacher(
#         teacher_id: int,
#         db: Session = Depends(get_db),
#         user: User = Depends(get_current_user)
# ):
#     return select_feedback_answer_db(db=db, teacher_id=teacher_id)


# @router.get("/feedback/answer/{feedback_id}")
# async def get_feedback_answer(
#         feedback_id: int,
#         db: Session = Depends(get_db),
#         user: User = Depends(get_current_user)
# ):
#     return select_feedback_answer_db(db=db, test_feedback_id=feedback_id)


# @router.post("/student-test/create")
# async def create_student_test(
#         student_id: int,
#         test_id: int,
#         db: Session = Depends(get_db),
#         user: User = Depends(get_current_user)
# ):
#     pass


# @router.get("/student-test/{student_id}")
# async def check_student_test(
#         student_id: int,
#         test_id: int,
#         db: Session = Depends(get_db),
#         user: User = Depends(get_current_user)
# ):
#     pass


