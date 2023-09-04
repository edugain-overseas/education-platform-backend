import os
from datetime import datetime

from fastapi import UploadFile

STUDENT_AVATAR_FOLDER = 'static/images/student-avatar'
TEACHER_AVATAR_FOLDER = 'static/images/teacher-avatar'
SUBJECT_AVATAR_FOLDER = 'static/images/subject-photo'
SUBJECT_LOGO_FOLDER = 'static/images/subject-logo'
SUBJECT_PROGRAM_FOLDER = 'static/subject-files/program/'
SUBJECT_ICON_FOLDER = 'static/subject-files/icons'


def save_student_avatar(photo: UploadFile, name, surname) -> str:
    filename = f'{name}-{surname}–{photo.filename}'
    file_path = os.path.join(STUDENT_AVATAR_FOLDER, filename)
    os.makedirs(STUDENT_AVATAR_FOLDER, exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(photo.file.read())

    return file_path


def save_teacher_avatar(photo: UploadFile) -> str:
    file_path = os.path.join(TEACHER_AVATAR_FOLDER, photo.filename)
    os.makedirs(TEACHER_AVATAR_FOLDER, exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(photo.file.read())

    return file_path


def save_subject_avatar(photo: UploadFile, subject_title) -> str:
    filename = f'{subject_title}-{photo.filename}'
    file_path = os.path.join(SUBJECT_AVATAR_FOLDER, filename)
    os.makedirs(SUBJECT_AVATAR_FOLDER, exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(photo.file.read())

    return file_path


def save_subject_logo(photo: UploadFile, subject_title) -> str:
    filename = f'{subject_title}-{photo.filename}'
    file_path = os.path.join(SUBJECT_LOGO_FOLDER, filename)
    os.makedirs(SUBJECT_LOGO_FOLDER, exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(photo.file.read())

    return file_path


def save_lesson_file(file: UploadFile) -> tuple:
    folder = 'static/lesson-files/' + datetime.now().strftime("%d-%m-%Y")
    file_extension = os.path.splitext(file.filename)[1].lstrip(".")
    file_path = os.path.join(folder, file.filename)
    os.makedirs(folder, exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path, file_extension


def save_group_chat_file(file: UploadFile):
    folder = 'static/chat-files/' + datetime.now().strftime("%d-%m-%Y")
    file_path = os.path.join(folder, file.filename)
    os.makedirs(folder, exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path


def save_subject_chat_file(file: UploadFile):
    folder = 'static/subject-files/chat/' + datetime.now().strftime("%d-%m-%Y")
    file_path = os.path.join(folder, file.filename)
    os.makedirs(folder, exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path


def save_subject_program(file: UploadFile):
    file_path = os.path.join(SUBJECT_PROGRAM_FOLDER, file.filename)
    os.makedirs(SUBJECT_PROGRAM_FOLDER, exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path


def save_subject_icon(file: UploadFile):
    file_path = os.path.join(SUBJECT_ICON_FOLDER, file.filename)
    os.makedirs(SUBJECT_ICON_FOLDER, exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path


def delete_chat_file(file_path: str):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return {"message": f"File {file_path} successfully deleted"}
        else:
            return {"message": f"File {file_path} not found."}
    except Exception as e:
        return {"message": f"Error while deleting file: {str(e)}"}
