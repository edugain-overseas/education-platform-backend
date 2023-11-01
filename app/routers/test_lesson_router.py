from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.crud.lesson_crud import get_lesson_info_db
from app.crud.test_lesson_crud import (create_test_answer_db, create_test_answer_with_photo_db, create_test_db,
                                       create_test_matching_db, create_test_question_db,
                                       create_test_question_with_photo_db, delete_answer_db, delete_matching_left_db,
                                       delete_matching_right_db, delete_test_question_db, select_matching_left_db,
                                       select_matching_right_db, select_mathing_left_by_right_id_db,
                                       select_question_type_id, select_test_answer_db, select_test_db,
                                       select_test_info_db, select_test_question_db, set_none_for_left_option_db,
                                       update_test_db, update_test_question_db)
from app.models import User
from app.schemas.test_lesson_schemas import QuestionBase, TestConfigBase, TestConfigUpdate
from app.session import get_db
from app.utils.save_images import delete_file, save_lesson_file
from app.utils.token import get_current_user


router = APIRouter()


@router.post("/test/")
async def create_test_config(
        test_data: TestConfigBase,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.moder or user.teacher:
        return create_test_db(db=db, test_data=test_data)
    else:
        raise HTTPException(status_code=401, detail="Permission denied")


@router.put("/test/")
async def update_test_config(
        test_id: int,
        test_data: TestConfigUpdate,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.moder or user.teacher:
        test = select_test_db(db=db, test_id=test_id)
        return update_test_db(db=db, test=test, test_data=test_data)
    else:
        raise HTTPException(status_code=401, detail="Permission denied")


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


@router.put("/test/question")
async def update_question(
        question_id: int,
        data: QuestionBase,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.moder or user.teacher:
        question = select_test_question_db(db=db, question_id=question_id)
        update_test_question_db(
            db=db,
            question=question,
            text=data.questionText,
            number=data.questionNumber,
            score=data.questionScore,
            hided=data.hided,
            image_path=data.imagePath
        )

        if data.questionType == "matching":
            for right in question.matching_right:
                delete_matching_right_db(db=db, right_option=right)
            for left in question.matching_left:
                delete_matching_left_db(db=db, left_option=left)

        else:
            for answer in question.test_answer:
                if answer.image_path:
                    delete_file(answer.image_path)
                delete_answer_db(db=db, answer=answer)

        if data.questionType == "answer_with_photo":
            for new_answer in data.questionAnswers:
                create_test_answer_with_photo_db(
                    db=db,
                    answer_text=new_answer.answerText,
                    is_correct=new_answer.isCorrect,
                    image_path=new_answer.imagePath,
                    question_id=question_id
                )
        elif data.questionType in ["test", "boolean", "multiple_choice", "question_with_photo"]:
            for new_answer in data.questionAnswers:
                create_test_answer_db(
                    db=db,
                    answer_text=new_answer.answerText,
                    is_correct=new_answer.isCorrect,
                    question_id=question_id
                )
        else:
            for matching in data.questionAnswers:
                create_test_matching_db(
                    db=db,
                    right_text=matching.rightText,
                    left_text=matching.leftText,
                    question_id=question_id
                )
        return {"message": "Question data have been updated"}
    else:
        raise HTTPException(status_code=401, detail="Permission denied")


@router.delete("/test/delete-question")
async def delete_question(
        question_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.moder or user.teacher:
        question = select_test_question_db(db=db, question_id=question_id)
        if question.question_type == "matching":
            for left in question.matching_left:
                delete_matching_left_db(db=db, left_option=left)
            for right in question.matching_right:
                delete_matching_right_db(db=db, right_option=right)
            delete_test_question_db(db=db, question=question)
        elif question.question_type == "question_with_photo":
            delete_file(question.image_path)
            for answer in question.test_answer:
                delete_answer_db(db=db, answer=answer)
            delete_test_question_db(db=db, question=question)
        elif question.question_type == "answer_with_photo":
            for answer in question.test_answer:
                delete_file(answer.image_path)
                delete_answer_db(db=db, answer=answer)
            delete_test_question_db(db=db, question=question)
        else:
            for answer in question.test_answer:
                delete_answer_db(db=db, answer=answer)
            delete_test_question_db(db=db, question=question)
        return {"message": "Question have been deleted"}
    else:
        raise HTTPException(status_code=401, detail="Permission denied")


@router.delete("/test/delete-answer")
async def delete_answer(
        answer_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.moder or user.teacher:
        answer = select_test_answer_db(db=db, answer_id=answer_id)
        if answer.image_path:
            delete_file(answer.image_path)
        delete_answer_db(db=db, answer=answer)
        return {"message": "Answer have been deleted"}
    else:
        raise HTTPException(status_code=401, detail="Permission denied")


@router.delete("/test/delete-matching-left")
async def delete_matching_left(
        left_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.moder or user.teacher:
        left_option = select_matching_left_db(db=db, left_id=left_id)
        delete_matching_left_db(db=db, left_option=left_option)
        return {"message": "Left option have been deleted"}
    else:
        raise HTTPException(status_code=401, detail="Permission denied")


@router.delete("/test/delete/matching-right")
async def delete_matching_right(
        right_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.moder or user.teacher:
        right_option = select_matching_right_db(db=db, right_id=right_id)
        left_option = select_mathing_left_by_right_id_db(db=db, right_id=right_id)
        set_none_for_left_option_db(db=db, left_option=left_option)
        delete_matching_right_db(db=db, right_option=right_option)
        return {"message": "Right option have been deleted"}
    else:
        raise HTTPException(status_code=401, detail="Permission denied")


@router.get("/test/{lesson_id}")
async def get_test_info(
        lesson_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    lesson_base = get_lesson_info_db(db=db, lesson_id=lesson_id)

    result = {
        "lessonTitle": lesson_base.lessonTitle,
        "lessonDescription": lesson_base.lessonDescription,
        "lessonDate": lesson_base.lessonDate,
        "lessonEnd": lesson_base.lessonEnd,
    }

    test_info = select_test_info_db(db=db, lesson_id=lesson_id)

    if test_info is None:
        return result

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
        raise HTTPException(status_code=401, detail="Permission denied")
