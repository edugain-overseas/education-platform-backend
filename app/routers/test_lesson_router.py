from fastapi import Depends, APIRouter, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.models import User
from app.crud.test_lesson_crud import (create_test_db, select_test_db, update_test_db,
                                       create_test_question_db, create_test_answer_db,
                                       create_test_matching_db)
from app.schemas.test_lesson_schemas import (TestConfigBase, TestConfigUpdate, TestQuestionBase,
                                             TestAnswerBase, TesMatchingBase)
from app.session import get_db
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


@router.post("/test/create/question")
async def create_test_question(
        question_data: TestQuestionBase,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return create_test_question_db(db=db, question_data=question_data)


@router.post("/test/create/answer")
async def create_test_answer(
        answer_data: TestAnswerBase,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return create_test_answer_db(db=db, answer_data=answer_data)


@router.post("/test/create/matching")
async def create_test_matching(
        matching_data: TesMatchingBase,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return create_test_matching_db(db=db, matching_data=matching_data)
