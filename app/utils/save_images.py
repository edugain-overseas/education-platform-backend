from fastapi import UploadFile
from datetime import datetime
import os


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
    current_date = datetime.now().strftime("%d-%m-%Y")
    folder = 'static/lesson-files/' + current_date
    file_extension = os.path.splitext(file.filename)[1].lstrip(".")
    file_path = os.path.join(folder, file.filename)
    os.makedirs(folder, exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path, file_extension
