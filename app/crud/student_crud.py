from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models import Course, Group, Lesson, Student, StudentAdditionalSubject, Subject, Teacher, User


def get_student_info_db(db: Session, user_id: int):
    user_info = db.query(
        Student.id,
        Student.name,
        Student.surname,
        Student.image_path,
        Student.educational_program,
        Student.qualification,
        Student.subject_area,
        Student.field_of_study,
        Course.course_number,
        Course.semester_number,
        Group.group_name,
        Group.id
    ).join(
        User, Student.user_id == User.id
    ).join(
        Course, Student.course_id == Course.id
    ).join(
        Group, Student.group_id == Group.id
    ).filter(
        User.id == user_id
    ).all()
    return user_info


def get_student_schedule_db(db: Session, student_id: int):
    today = datetime.now().date()
    end_date = today + timedelta(days=10)
    result = []

    base_subjects = db.query(
        Subject.title,
        Lesson.title,
        Lesson.lesson_date,
        Lesson.lesson_end,
        Teacher.name,
        Teacher.surname
    ).select_from(
        Student
    ).join(
        Group, Student.group_id == Group.id
    ).join(
        Subject, Group.id == Subject.group_id
    ).join(
        Lesson, Subject.id == Lesson.subject_id
    ).join(
        Teacher, Lesson.teacher_id == Teacher.id
    ).filter(
        Student.id == student_id,
        Lesson.lesson_date >= today,
        Lesson.lesson_date <= end_date
    ).all()

    for subject in base_subjects:
        result.append({
            'subject_name': subject[0],
            'lesson_name': subject[1],
            'lesson_date': subject[2],
            'lesson_end': subject[3],
            'teacher_name': subject[4],
            'teacher_surname': subject[5]
        })

    additional_subjects = db.query(
        Subject.title,
        Lesson.title,
        Lesson.lesson_date,
        Lesson.lesson_end,
        Teacher.name,
        Teacher.surname
    ).select_from(
        Student
    ).join(
        StudentAdditionalSubject, Student.id == StudentAdditionalSubject.student_id
    ).join(
        Subject, StudentAdditionalSubject.subject_id == Subject.id
    ).join(
        Lesson, Subject.id == Lesson.subject_id
    ).join(
        Teacher, Lesson.teacher_id == Teacher.id
    ).filter(
        Student.id == student_id,
        Lesson.lesson_date >= today,
        Lesson.lesson_date <= end_date
    ).all()

    for add_subject in additional_subjects:
        result.append({
            'subject_name': add_subject[0],
            'lesson_name': add_subject[1],
            'lesson_date': add_subject[2],
            'lesson_end': add_subject[3],
            'teacher_name': add_subject[4],
            'teacher_surname': add_subject[5]
        })

    return result
