from fastapi import UploadFile
import os


def save_student_avatar(photo: UploadFile, name, surname) -> str:
    folder = 'static/images/student-avatar'
    filename = f'{name}-{surname}–{photo.filename}'
    file_path = os.path.join(folder, filename)

    with open(file_path, "wb") as f:
        f.write(photo.file.read())

    return file_path
