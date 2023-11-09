from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.crud.lesson_crud import select_lesson_by_subject_db
from app.crud.student_crud import get_student_info_db, get_student_schedule_db
from app.crud.subject_crud import select_dop_subjects, select_subject_by_group_id_db
from app.crud.user_crud import (delete_student_db, delete_user_db, select_all_students_db, select_student_by_id_db,
                                select_student_by_user_id_db, select_students_by_course_id_db,
                                select_students_by_group_id_db, select_students_by_specializations_id_db,
                                select_user_by_id_db, update_student_info_db, update_student_photo_path_db)
from app.models import User
from app.schemas.user_schemas import StudentUpdate
from app.session import get_db
from app.utils.save_images import save_student_avatar
from app.utils.token import get_current_user

router = APIRouter()


@router.get("/student/info/me")
async def get_student_info(
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    user_info_list = get_student_info_db(db=db, user_id=user.id)

    field_list = [
        'student_id',
        'student_name',
        'student_surname',
        'image_path',
        'student_educational_program',
        'student_qualification',
        'student_subject_area',
        'field_of_study',
        'course_number',
        'semester_number',
        'group_name',
        'group_id'
    ]

    user_info = zip(field_list, user_info_list[0])

    return user_info


@router.get("/student/my/schedule")
async def get_student_schedule(
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    result = get_student_schedule_db(db=db, student_id=user.student[0].id)
    return result


@router.put("/student/update/photo")
async def update_student_avatar(
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if not user.student:
        raise HTTPException(status_code=403, detail="Only students can update their avatars")

    student = select_student_by_user_id_db(db=db, user_id=user.id)

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    file_path = save_student_avatar(photo=file)
    update_student_photo_path_db(
        db=db,
        student=student,
        new_path=file_path
    )

    return {
        "message": "Avatar updated successfully",
        "photo_path": file_path
    }


@router.put("/student/{student_id}/update/")
async def update_student_info(
        student_id: int,
        student_data: StudentUpdate,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.student or user.moder or user.teacher:
        student = select_student_by_user_id_db(db=db, user_id=student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        update_student_info_db(
            db=db,
            student=student,
            student_data=student_data
        )

        return {"message": "Student information updated successfully"}
    else:
        raise HTTPException(
            status_code=403,
            detail="Only students can update their information"
        )


@router.get("/students")
async def get_students(
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    students = select_all_students_db(db=db)
    return {"students": students}


@router.get("/student/{student_id}")
async def get_student(
        student_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    student = select_student_by_id_db(db=db, student_id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.get("/students/course/{course_id}")
async def get_students_in_course(
        course_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    students = select_students_by_course_id_db(db=db, course_id=course_id)
    if not students:
        raise HTTPException(status_code=404, detail="Students not found")
    return {"students": students}


@router.get("/students/group/{group_id}")
async def get_students_in_group(
        group_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    students = select_students_by_group_id_db(db=db, group_id=group_id)
    if not students:
        raise HTTPException(status_code=404, detail="Students not found")
    return {"students": students}


@router.get("/students/specialization/{specialization_id}")
async def get_students_in_specialization(
        specialization_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)):
    students = select_students_by_specializations_id_db(db=db, specialization_id=specialization_id)
    if not students:
        raise HTTPException(status_code=404, detail="Students not found")
    return {"students": students}


@router.delete("/student/{student_id}")
async def delete_student(
        student_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    student = select_student_by_id_db(db=db, student_id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    user_data = select_user_by_id_db(db=db, user_id=student.user_id)

    delete_student_db(db=db, student=student)
    delete_user_db(db=db, user=user_data)
    return {"massage": "Student has been successful deleted"}


@router.get("/student/get-register/{student_id}")
async def get_student_register(
        student_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    student = select_student_by_id_db(db=db, student_id=student_id)
    result = []
    main_subjects = select_subject_by_group_id_db(db=db, group_id=student.group_id)
    for subject in main_subjects:
        lessons = select_lesson_by_subject_db(db=db, subject_id=subject.subject_id)
        subject_register = {
            "subjectId": subject.subject_id,
            "subjectName": subject.subject_title,
            "subjectLessons": lessons
        }
        result.append(subject_register)

    dop_subjects = select_dop_subjects(db=db, student_id=student_id)
    for subject in dop_subjects:
        lessons = select_lesson_by_subject_db(db=db, subject_id=subject[0])
        dop_subject_register = {
            "dopSubjectId": subject[0],
            "dopSubjectName": subject[1],
            "dopSubjectLessons": lessons
        }
        result.append(dop_subject_register)

    return result
