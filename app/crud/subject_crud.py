from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models import (Group, Lecture, Lesson, ParticipantComment, StudentAdditionalSubject, Subject, SubjectIcon,
                        SubjectItem, SubjectJournal, SubjectTeacherAssociation, Teacher, TestLesson, User)
from app.schemas.subject_schemas import SubjectCreate, SubjectUpdate


def create_new_subject_db(db: Session, subject: SubjectCreate):
    is_published = subject.is_published if subject.is_published is not None else False
    exam_date = subject.exam_date if subject.exam_date is not None else None

    new_subject = Subject(
        title=subject.title,
        specialization_id=subject.specialization_id,
        course_id=subject.course_id,
        group_id=subject.group_id,
        description=subject.description,
        is_published=is_published,
        quantity_lecture=subject.quantity_lecture,
        quantity_seminar=subject.quantity_seminar,
        quantity_test=subject.quantity_test,
        quantity_module=subject.quantity_module,
        score=subject.score,
        exam_date=exam_date
    )

    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)
    return new_subject


def create_subject_item_db(db: Session, subject_id: int, item: str):
    new_item = SubjectItem(
        text=item,
        subject_id=subject_id
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


def create_subject_icon_db(
        db: Session,
        subject_id: int | None,
        is_default: bool,
        icon_path: str
):
    new_icon = SubjectIcon(
        icon_path=icon_path,
        is_default=is_default,
        subject_id=subject_id
    )

    db.add(new_icon)
    db.commit()
    db.refresh(new_icon)
    return new_icon


def select_all_subjects_db(db: Session):
    return db.query(Subject).all()


def select_subject_by_id_db(db: Session, subject_id: int):
    return db.query(Subject).filter(Subject.id == subject_id).first()


def select_subjects_by_specialization_db(db: Session, specialization_id: int):
    return db.query(Subject).filter(Subject.specialization_id == specialization_id).all()


def select_subjects_by_course_db(db: Session, course_id: int):
    return db.query(Subject).filter(Subject.course_id == course_id).all()


def select_subject_by_group_id_db(db: Session, group_id: int):
    query = db.query(
        Subject.id.label("subject_id"),
        Subject.title.label("subject_title")
    )\
        .join(Group, Group.id == Subject.group_id)\
        .filter(Group.id == group_id)
    return query.all()


def select_subjects_by_group_db(db: Session, group_name: str):
    query = db.query(
        Subject.id,
        Subject.title,
        Subject.image_path
    )\
        .join(Group, Group.specialization_id == Subject.specialization_id)\
        .filter(Group.group_name == group_name)

    return query.all()


def update_subject_image_path_db(db: Session, subject: Subject, new_path: str):
    subject.image_path = new_path
    db.commit()
    db.refresh(subject)


def update_subject_logo_path_db(db: Session, subject: Subject, new_path: str):
    subject.logo_path = new_path
    db.commit()
    db.refresh(subject)


def update_subject_info_db(db: Session, subject: Subject, subject_data: SubjectUpdate):
    if subject_data.is_published is None:
        subject_data.is_published = True

    for field, value in subject_data:
        if value is not None:
            setattr(subject, field, value)

    db.commit()
    db.refresh(subject)
    return subject


def update_subject_item_text_db(db: Session, subject_item: SubjectItem, text: str):
    subject_item.text = text
    db.commit()
    db.refresh(subject_item)
    return subject_item


def delete_subject_db(db: Session, subject: Subject):
    db.delete(subject)
    db.commit()


def set_teacher_for_subject_db(db: Session, teacher_id: int, subject_id: int):
    new_association = SubjectTeacherAssociation(
        teacher_id=teacher_id,
        subject_id=subject_id
    )

    db.add(new_association)
    db.commit()
    db.refresh(new_association)


def select_teachers_for_subject_db(db: Session, subject_id: int):
    teachers = db.query(
        Teacher.id, Teacher.name, Teacher.surname,
        Teacher.email, Teacher.image_path, User.last_active) \
        .join(SubjectTeacherAssociation, SubjectTeacherAssociation.teacher_id == Teacher.id) \
        .join(User, Teacher.user_id == User.id) \
        .filter(SubjectTeacherAssociation.subject_id == subject_id) \
        .all()

    teachers_list = []

    for teacher in teachers:
        teacher_dict = {
            "id": teacher.id,
            "name": teacher.name,
            "surname": teacher.surname,
            "email": teacher.email,
            "image_path": teacher.image_path,
            "last_active": teacher.last_active
        }
        teachers_list.append(teacher_dict)

    return teachers_list


def sign_student_for_addition_subject_db(db: Session, subject_id: int, student_id: int):
    student_addition_subject = StudentAdditionalSubject(
        subject_id=subject_id,
        student_id=student_id
    )

    db.add(student_addition_subject)
    db.commit()
    db.refresh(student_addition_subject)
    return student_addition_subject


def select_dop_subjects(db: Session, student_id: int):
    subjects = db.query(
        Subject.id,
        Subject.title,
        Subject.image_path
    )\
        .join(StudentAdditionalSubject, StudentAdditionalSubject.subject_id == Subject.id)\
        .filter(StudentAdditionalSubject.student_id == student_id)\
        .all()

    return subjects


def select_subject_exam_date(db: Session, subject_id: int):
    exam_date = db.query(Subject.exam_date).filter(Subject.id == subject_id).scalar()
    return exam_date.strftime('%Y-%m-%d')


def select_subject_item_db(db: Session, subject_id: int):
    return db.query(SubjectItem).filter(SubjectItem.subject_id == subject_id).first()


def select_subject_icons_db(db: Session, subject_id: int):
    icons = db.query(SubjectIcon).filter(
        or_(
            SubjectIcon.is_default,
            SubjectIcon.subject_id == subject_id
        )
    ).all()

    return icons


def select_subject_icon_db(db: Session, icon_path: str):
    icon = db.query(SubjectIcon).filter(SubjectIcon.icon_path == icon_path).first()
    return icon


def delete_subject_icon_db(db: Session, subject_icon: SubjectIcon):
    db.delete(subject_icon)
    db.commit()


def create_or_update_participant_comment_db(
        db: Session,
        subject_id: int,
        student_id: int,
        comment: str
):
    part_comment = db.query(ParticipantComment).filter(
        ParticipantComment.subject_id == subject_id,
        ParticipantComment.student_id == student_id).first()

    if part_comment:
        part_comment.comment = comment
        db.commit()
        db.refresh(part_comment)
        return part_comment
    else:
        new_comment = ParticipantComment(
            subject_id=subject_id,
            student_id=student_id,
            comment=comment
        )
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        return new_comment


def select_lesson_id_and_subject_id_by_test_id_db(db: Session, test_id: int):
    result = db.query(
        Lesson.subject_id.label("subject_id"),
        Lesson.id.label("lesson_id")
    )\
        .select_from(TestLesson)\
        .join(Lesson, Lesson.id == TestLesson.lesson_id)\
        .filter(TestLesson.id == test_id)\
        .first()
    return result


def select_lesson_id_and_subject_id_by_lecture_id_db(db: Session, lecture_id: int):
    result = db.query(
        Lesson.subject_id.label("subject_id"),
        Lesson.id.label("lesson_id")
    )\
        .select_from(Lecture)\
        .join(Lesson, Lesson.id == Lecture.lesson_id)\
        .filter(Lecture.id == lecture_id)\
        .first()
    return result


def filling_journal(
        db: Session,
        subject_id: int,
        lesson_id: int,
        student_id: int,
        score: int = None,
        absent: int = None
):
    new_row = SubjectJournal(
        score=score,
        absent=absent,
        subject_id=subject_id,
        lesson_id=lesson_id,
        student_id=student_id
    )
    db.add(new_row)
    db.commit()
    db.refresh(new_row)
    return new_row


def select_journal_row(db: Session, lesson_id: int, student_id: int, subject_id: int):
    result = db.query(
        SubjectJournal
    ).filter(
        SubjectJournal.lesson_id == lesson_id,
        SubjectJournal.subject_id == subject_id,
        SubjectJournal.student_id == student_id
    ).first()
    return result


def update_score_to_journal(db: Session, journal_row: SubjectJournal, score: int):
    journal_row.score = score
    db.commit()
    db.refresh(journal_row)
    return journal_row
