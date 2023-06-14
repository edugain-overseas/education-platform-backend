from sqlalchemy.orm import Session

from app.models import \
    User, \
    Student, \
    Teacher, \
    Group, \
    Course, \
    Lesson, \
    Subject, \
    SubjectTeacherAssociation, \
    Specialization


def get_student_info_db(db: Session, user_id: int):
    userinfo = db.query(
        Student.id,
        Student.name,
        Student.surname,
        Student.educational_program,
        Student.qualification,
        Student.subject_area,
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
    student_schedule = db.query(
        Subject.title,
        Lesson.lesson_date,
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
    ).filter(Group.group_name == group_name).all()

    return student_schedule
