from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.crud.test_lesson_crud import (create_feedback_answer_db, create_test_answer_db, create_test_db,
                                       create_test_feedback_db, create_test_matching_db, create_test_question_db,
                                       select_feedback_answer_db, select_test_answer_db, select_test_db,
                                       select_test_feedback_db, select_test_info_db, select_test_matching_left_db,
                                       select_test_matching_right_db, select_test_question_db, update_test_answer_db,
                                       update_test_db, update_test_matching_left_db, update_test_matching_right_db,
                                       update_test_question_db)
from app.models import User
from app.schemas.test_lesson_schemas import (FeedbackAnswer, TesMatchingBase, TestAnswerBase, TestAnswerUpdate,
                                             TestConfigBase, TestConfigUpdate, TestMatchingLeftUpdate,
                                             TestMatchingRightUpdate, TestQuestionBase, TestQuestionFeedback,
                                             TestQuestionUpdate)
from app.session import get_db
from app.utils.save_images import save_lesson_file
from app.utils.token import get_current_user

router = APIRouter()


@router.post("/test/create")
async def create_test(
        test_data: TestConfigBase,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return create_test_db(db=db, test_data=test_data)


@router.put("/test/update")
async def update_test(
        test_lesson_id: int,
        test_data: TestConfigUpdate,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    test = select_test_db(db=db, test_id=test_lesson_id)
    return update_test_db(db=db, test=test, test_data=test_data)


@router.get("/test/{lesson_id}")
async def get_test_info(
        lesson_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return select_test_info_db(db=db, lesson_id=lesson_id)


@router.post("/test/create/question")
async def create_test_question(
        question_data: TestQuestionBase,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return create_test_question_db(db=db, question_data=question_data)


@router.put("/test/update/question")
async def update_test_question(
        question_id: int,
        question_data: TestQuestionUpdate,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    test_question = select_test_question_db(db=db, question_id=question_id)
    return update_test_question_db(db=db, question=test_question, question_data=question_data)


@router.post("/test/create/answer")
async def create_test_answer(
        answer_data: TestAnswerBase,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return create_test_answer_db(db=db, answer_data=answer_data)


@router.put("/test/update/answer")
async def update_test_answer(
        answer_id: int,
        answer_data: TestAnswerUpdate,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    test_answer = select_test_answer_db(db=db, answer_id=answer_id)
    return update_test_answer_db(db=db, answer=test_answer, answer_data=answer_data)


@router.post("/test/create/matching")
async def create_test_matching(
        matching_data: TesMatchingBase,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return create_test_matching_db(db=db, matching_data=matching_data)


@router.put("/test/update//matching_left")
async def update_test_matching_left(
        matching_left_id: int,
        matching_left_data: TestMatchingLeftUpdate,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    test_matching_left = select_test_matching_left_db(db=db, left_option_id=matching_left_id)
    return update_test_matching_left_db(
        db=db,
        test_matching_left=test_matching_left,
        matching_left_data=matching_left_data
    )


@router.put("/test/update//matching_right")
async def update_test_matching_right(
        matching_right_id: int,
        matching_right_data: TestMatchingRightUpdate,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    test_matching_right = select_test_matching_right_db(db=db, right_option_id=matching_right_id)
    return update_test_matching_right_db(
        db=db,
        test_matching_right=test_matching_right,
        matching_right_data=matching_right_data
    )


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


@router.post("/test/feedback")
async def create_test_feedback(
        test_feedback_data: TestQuestionFeedback,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.student:
        return create_test_feedback_db(db=db, feedback_data=test_feedback_data)
    else:
        raise HTTPException(
            status_code=401,
            detail='Permission denied'
        )


@router.get("/test/feedback/question/{question_id}")
async def get_test_feedback_by_question(
        question_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return select_test_feedback_db(db=db, question_id=question_id)


@router.get("/test/feedback/student/{student_id}")
async def get_test_feedback_by_student(
        student_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return select_test_feedback_db(db=db, student_id=student_id)


@router.post("/feedback/answer")
async def create_test_feedback_answer(
        answer_data: FeedbackAnswer,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher:
        return create_feedback_answer_db(db=db, answer_data=answer_data)
    else:
        raise HTTPException(
            status_code=401,
            detail="Permission denied"
        )


@router.get("/feedback/answer/teacher/{teacher_id}")
async def get_feedback_answer_by_teacher(
        teacher_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return select_feedback_answer_db(db=db, teacher_id=teacher_id)


@router.get("/feedback/answer/{feedback_id}")
async def get_feedback_answer(
        feedback_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return select_feedback_answer_db(db=db, test_feedback_id=feedback_id)
