import os
from datetime import datetime

from fastapi import UploadFile


def save_student_avatar(photo: UploadFile, name, surname) -> str:
    folder = 'static/images/student-avatar'
    filename = f'{name}-{surname}–{photo.filename}'
    file_path = os.path.join(folder, filename)

    with open(file_path, "wb") as f:
        f.write(photo.file.read())

    return file_path


def save_subject_avatar(photo: UploadFile, subject_title) -> str:
    folder = 'static/images/subject-photo'
    filename = f'{subject_title}-{photo.filename}'
    file_path = os.path.join(folder, filename)

    with open(file_path, "wb") as f:
        f.write(photo.file.read())

    return file_path


def save_subject_logo(photo: UploadFile, subject_title) -> str:
    folder = 'static/images/subject-logo'
    filename = f'{subject_title}-{photo.filename}'
    file_path = os.path.join(folder, filename)

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


def save_subject_program(file: UploadFile):
    folder = 'static/program/'
    file_path = os.path.join(folder, file.filename)
    os.makedirs(folder, exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path


def delete_group_chat_file(file_path: str):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return {"message": f"File {file_path} successfully deleted"}
        else:
            return {"message": f"File {file_path} not found."}
    except Exception as e:
        return {"message": f"Error while deleting file: {str(e)}"}
