from fastapi import APIRouter, UploadFile, File, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.models import User
from app.session import get_db
from app.schemas.user_schemas import StudentCreate, StudentUpdate, TeacherCreate, ModerCreate, CuratorCreate
from app.utils.password import hash_password, check_password
from app.utils.token import create_access_token, get_current_user
from app.utils.save_images import save_student_avatar
from app.crud.user_crud import *


SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

router = APIRouter()


@router.post("/student/create")
async def create_student(data: StudentCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(data.password)
    user_type = select_user_type_id_db(db=db, user_type=data.usertype.value)

    new_user = create_new_user_db(
        db=db,
        username=data.username,
        hashed_password=hashed_password,
        user_type_id=user_type.id)

    new_student = create_new_student_db(
        db=db,
        name=data.name,
        surname=data.surname,
        lastname=data.lastname,
        phone=data.phone,
        email=data.email,
        user_id=new_user.id
    )

    return {
        "status": "new student have been successful created",
        "student_info": new_student
    }


@router.post("/teacher/create")
async def create_teacher(data: TeacherCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(data.password)
    user_type = select_user_type_id_db(db=db, user_type=data.usertype.value)

    new_user = create_new_user_db(
        db=db,
        username=data.username,
        hashed_password=hashed_password,
        user_type_id=user_type.id)

    new_teacher = create_new_teacher_db(
        db=db,
        name=data.name,
        surname=data.surname,
        lastname=data.lastname,
        email=data.email,
        user_id=new_user.id,
    )

    return {
        "status": "new teacher have been successful created",
        "teacher_info": new_teacher
    }


@router.post("/moder/create")
async def create_moder(data: ModerCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(data.password)
    user_type = select_user_type_id_db(db=db, user_type=data.usertype.value)

    new_user = create_new_user_db(
        db=db,
        username=data.username,
        hashed_password=hashed_password,
        user_type_id=user_type.id,
    )

    new_moder = create_new_moder_db(
        db=db,
        name=data.name,
        surname=data.surname,
        lastname=data.lastname,
        user_id=new_user.id
    )

    return {
        "status": "new moder have been successful created",
        "moder_info": new_moder
    }


@router.post("/curator/create")
async def create_curator(data: CuratorCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(data.password)
    user_type = select_user_type_id_db(db=db, user_type=data.usertype.value)

    new_user = create_new_user_db(
        db=db,
        username=data.username,
        hashed_password=hashed_password,
        user_type_id=user_type.id
    )

    new_curator = create_new_curator_db(
        db=db,
        name=data.name,
        surname=data.surname,
        lastname=data.lastname,
        email=data.email,
        user_id=new_user.id
    )

    return {
        "status": "new curator have been successful created",
        "curator_info": new_curator
    }


@router.post("/auth/token")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):
    user = select_user_by_username_db(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    if not check_password(form_data.password, user.hashed_pass):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    access_token, expire_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires)

    update_user_token_db(db=db, user=user, token=access_token, exp_token=expire_token)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expire_token": expire_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "type": user.user_type.type
        }
    }


@router.put("/student/update/photo")
async def update_student_avatar(
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if not current_user.student:
        raise HTTPException(status_code=403, detail="Only students can update their avatars")

    student = select_student_by_user_id_db(db=db, user_id=current_user.id)

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    file_path = save_student_avatar(file, student.name, student.surname)
    update_student_photo_path_db(db=db, student=student, new_path=file_path)
    return {"message": "Avatar updated successfully"}


@router.put("/student/update/info")
async def update_student_info(
        student_data: StudentUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.student or current_user.moder or current_user.teacher:
        student = select_student_by_user_id_db(db=db, user_id=current_user.id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        update_student_info_db(db=db, student=student, student_data=student_data)
        return {"message": "Student information updated successfully"}
    else:
        raise HTTPException(status_code=403, detail="Only students can update their information")


@router.get("/students")
async def get_students(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    students = select_all_students_db(db=db)
    return {"students": students}


@router.get("/student/{student_id}")
async def get_student(
        student_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    student = select_student_by_id_db(db=db, student_id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.get("/students/course/{course_id}")
async def get_students_in_course(
        course_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    students = select_students_by_course_id_db(db=db, course_id=course_id)
    if not students:
        raise HTTPException(status_code=404, detail="Students not found")
    return {"students": students}


@router.get("/students/group/{group_id}")
async def get_students_in_group(
        group_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    students = select_students_by_group_id_db(db=db, group_id=group_id)
    if not students:
        raise HTTPException(status_code=404, detail="Students not found")
    return {"students": students}


@router.get("/students/specialization/{specialization_id}")
async def get_students_in_specialization(
        specialization_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    students = select_students_by_specializations_id_db(db=db, specialization_id=specialization_id)
    if not students:
        raise HTTPException(status_code=404, detail="Students not found")
    return {"students": students}


@router.delete("/student/{student_id}")
async def delete_student(
        student_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    student = select_student_by_id_db(db=db, student_id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    user = select_user_by_id_db(db=db, user_id=student.user_id)

    delete_student_db(db=db, student=student)
    delete_user_db(db=db, user=user)
    return {"massage": "Student has been successful deleted"}
