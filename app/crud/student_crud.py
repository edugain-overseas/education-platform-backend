from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models import (Course, Group, Lesson, Student, Subject,
                        SubjectTeacherAssociation, Teacher, User)


def get_student_info_db(db: Session, user_id: int):
    userinfo = db.query(
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
        Group.group_name
    ).join(
        User, Student.user_id == User.id
    ).join(
        Course, Student.course_id == Course.id
    ).join(
        Group, Student.group_id == Group.id
    ).filter(User.id == user_id).all()
    return userinfo


def get_student_schedule_db(db: Session, group_name: str):
    today = datetime.now().date()
    end_date = today + timedelta(days=10)

    student_schedule = db.query(
        Subject.title,
        Lesson.lesson_date,
        Lesson.lesson_end,
        Teacher.name,
        Teacher.surname
    ).join(
        Subject, Subject.id == Lesson.subject_id
    ).join(
        SubjectTeacherAssociation, SubjectTeacherAssociation.subject_id == Subject.id
    ).join(
        Teacher, Teacher.id == SubjectTeacherAssociation.teacher_id
    ).join(
        Group, Group.specialization_id == Subject.specialization_id
    ).filter(
        Group.group_name == group_name,
        Lesson.lesson_date >= today,
        Lesson.lesson_date <= end_date
    ).all()

    return student_schedule
