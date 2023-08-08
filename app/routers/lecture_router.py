# from typing import List
#
# from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
# from sqlalchemy.orm import Session
#
# from app.crud.lecture_crud import (create_ordinary_lesson_db,
#                                    get_lecture_info_db,
#                                    set_file_attr_for_lecture_db,
#                                    set_text_attr_for_lecture_db)
# from app.models import User
# from app.schemas.lecture_schemas import LectureTextCreate
# from app.session import get_db
# from app.utils.save_images import save_lesson_file
# from app.utils.token import get_current_user
#
# router = APIRouter()
#
#
# @router.post("/lecture/create")
# async def create_lecture(
#         lesson_id: int,
#         db: Session = Depends(get_db),
#         current_user: User = Depends(get_current_user)
# ):
#     if current_user.teacher:
#         return create_ordinary_lesson_db(db=db, lesson_id=lesson_id)
#     else:
#         raise HTTPException(
#             status_code=403,
#             detail="Permission denied"
#         )
#
#
# @router.post("/lecture/text/{lecture_id}")
# async def add_text_attr_for_lecture(
#         lecture_id: int,
#         item: LectureTextCreate,
#         db: Session = Depends(get_db),
#         current_user: User = Depends(get_current_user)
# ):
#     if current_user.teacher:
#         set_text_attr_for_lecture_db(db=db, item=item, lecture_id=lecture_id)
#         return {"message": f"Text for lecture {lecture_id } has been saved"}
#     else:
#         raise HTTPException(status_code=403, detail="Permission denied")
#
#
# @router.post("/lecture/file/{lecture_id}")
# async def add_file_attr_for_lecture(
#         lecture_id: int,
#         attr_number: int,
#         download: bool,
#         files: List[UploadFile] = File(...),
#         db: Session = Depends(get_db),
#         current_user: User = Depends(get_current_user)
# ):
#     if current_user.teacher:
#         for file in files:
#             file_path, name = save_lesson_file(file)
#             set_file_attr_for_lecture_db(
#                 db=db,
#                 file_path=file_path,
#                 name=name,
#                 lecture_id=lecture_id,
#                 attr_number=attr_number,
#                 download=download
#             )
#
#         return {"message": f"File for lecture {lecture_id} has been saved"}
#     else:
#         raise HTTPException(status_code=403, detail="Permission denied")
#
#
# @router.get("/lecture/{lesson_id}")
# async def get_lecture(
#         lesson_id: int,
#         db: Session = Depends(get_db),
#         current_user: User = Depends(get_current_user)
# ):
#     lectures = get_lecture_info_db(db=db, lesson_id=lesson_id)
#     result = []
#     for lecture in lectures:
#         result.append({
#             "Lesson Title": lecture[0],
#             "Description": lecture[1],
#             "Lesson Date": lecture[2],
#             "Lesson End": lecture[3],
#             "Attribute Number": lecture[4],
#             "Download": lecture[5],
#             "Attribute": lecture[6],
#             "Value": lecture[7]
#         })
#
#     return result
