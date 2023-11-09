import os
from datetime import datetime

from fastapi import UploadFile

STUDENT_AVATAR_FOLDER = 'static/images/student-avatar/'
TEACHER_AVATAR_FOLDER = 'static/images/teacher-avatar/'
SUBJECT_AVATAR_FOLDER = 'static/images/subject/photo/'
SUBJECT_LOGO_FOLDER = 'static/images/subject/logo/'
SUBJECT_PROGRAM_FOLDER = 'static/images/subject/program/'
SUBJECT_ICON_FOLDER = 'static/images/subject/icons/'
SUBJECT_INSTRUCTION_FOLDER = 'static/images/subject/instruction/'
LESSON_FILE_FOLDER = 'static/images/lesson-files/'
SUBJECT_CHAT_FOLDER = 'static/chat/subject/'
GROUP_CHAT_FOLDER = 'static/chat/group/'


def save_student_avatar(photo: UploadFile) -> str:
    file_path = os.path.join(STUDENT_AVATAR_FOLDER, photo.filename)
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


def save_lesson_file(file: UploadFile) -> str:
    folder = LESSON_FILE_FOLDER + datetime.now().strftime("%d-%m-%Y")
    filename = generate_unique_filename(file.filename)
    file_path = os.path.join(folder, filename)
    os.makedirs(folder, exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path


def save_group_chat_file(file: UploadFile) -> str:
    folder = GROUP_CHAT_FOLDER + datetime.now().strftime("%d-%m-%Y")
    file_path = os.path.join(folder, file.filename)
    os.makedirs(folder, exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path


def save_subject_chat_file(file: UploadFile) -> str:
    folder = SUBJECT_CHAT_FOLDER + datetime.now().strftime("%d-%m-%Y")
    file_path = os.path.join(folder, file.filename)
    os.makedirs(folder, exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path


def save_subject_program(file: UploadFile) -> str:
    file_path = os.path.join(SUBJECT_PROGRAM_FOLDER, file.filename)
    os.makedirs(SUBJECT_PROGRAM_FOLDER, exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path


def save_subject_icon(file: UploadFile) -> str:
    file_path = os.path.join(SUBJECT_ICON_FOLDER, file.filename)
    os.makedirs(SUBJECT_ICON_FOLDER, exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path


def save_subject_instructions(file: UploadFile) -> str:
    filename = generate_unique_filename(file.filename)
    file_path = os.path.join(SUBJECT_INSTRUCTION_FOLDER, filename)
    os.makedirs(SUBJECT_INSTRUCTION_FOLDER, exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path


def delete_file(file_path: str):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return {"message": f"File {file_path} successfully deleted"}
        else:
            return {"message": f"File {file_path} not found."}
    except Exception as e:
        return {"message": f"Error while deleting file: {str(e)}"}


def generate_unique_filename(original_filename: str):
    curr_time = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    filename, file_extension = original_filename.rsplit('.', 1)
    new_filename = f"{filename}-{curr_time}.{file_extension}"
    return new_filename
