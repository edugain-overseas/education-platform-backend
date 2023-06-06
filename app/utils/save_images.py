from fastapi import UploadFile
import os


def save_student_avatar(photo: UploadFile, name, surname) -> str:
    folder = 'static/images/student-avatar'
    filename = f'{name}-{surname}–{photo.filename}'
    file_path = os.path.join(folder, filename)

    with open(file_path, "wb") as f:
        f.write(photo.file.read())

    return file_path


def save_subject_avatar(photo: UploadFile, subject_title) -> str:
    folder = 'static/images/subject-avatar'
    filename = f'{subject_title}-{photo.filename}'
    file_path = os.path.join(folder, filename)

    with open(file_path, "wb") as f:
        f.write(photo.file.read())

    return file_path
