from fastapi import APIRouter, UploadFile, File, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.models import User
from app.session import get_db
from app.schemas.user_schemas import StudentCreate, TeacherCreate, ModerCreate, CuratorCreate
from app.utils.password import hash_password, check_password
from app.utils.token import create_access_token, get_current_user
from app.utils.save_images import save_student_avatar

from app.crud.user_crud import \
    create_new_user_db, \
    create_new_student_db, \
    create_new_teacher_db, \
    create_new_moder_db, \
    create_new_curator_db, \
    select_user_type_id_db, \
    select_user_by_username_db, \
    select_student_by_user_id_db, \
    update_user_token_db, \
    update_student_photo_path_db


SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

router = APIRouter()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')


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
        user_id=new_user.id
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
        user_type_id=user_type.id)

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
        user_type_id=user_type.id)

    new_curator = create_new_curator_db(
        db=db,
        name=data.name,
        surname=data.surname,
        lastname=data.lastname,
        user_id=new_user.id
    )

    return {
        "status": "new curator have been successful created",
        "curator_info": new_curator
    }


@router.post("/auth/token")
async def login_with_jwt_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):
    user = select_user_by_username_db(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    if not check_password(form_data.password, user.hashed_pass):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires)

    update_user_token_db(db=db, user=user, token=access_token)

    return {
        "access_token": access_token,
        "token_type": "bearer",
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
        current_user: User = Depends(get_current_user)):
    if not current_user.student:
        raise HTTPException(status_code=403, detail="Only students can update their avatars")

    student = select_student_by_user_id_db(db=db, user_id=current_user.id)

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    file_path = save_student_avatar(file, student.name, student.surname)
    update_student_photo_path_db(db=db, student=student, new_path=file_path)
    return {"message": "Avatar updated successfully"}

