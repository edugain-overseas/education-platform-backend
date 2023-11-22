from celery import Celery

from app.crud.subject_crud import (filling_journal, select_journal_row,
                                   select_lesson_id_and_subject_id_by_lecture_id_db,
                                   select_lesson_id_and_subject_id_by_test_id_db, update_score_to_journal)
from app.session import SessionLocal
from app.setting import BROKER_URL

celery_app = Celery("celery", broker=BROKER_URL)


@celery_app.task
def confirm_lecture_in_journal(student_id: int, lecture_id: int):
    db = SessionLocal()
    data = select_lesson_id_and_subject_id_by_lecture_id_db(db=db, lecture_id=lecture_id)
    journal_row = select_journal_row(db=db, lesson_id=data.lesson_id,
                                     student_id=student_id, subject_id=data.subject_id)

    if journal_row is None:
        filling_journal(db=db, absent=True, subject_id=data.subject_id,
                        lesson_id=data.lesson_id, student_id=student_id)

    db.close()


@celery_app.task
def write_test_score_to_journal(student_id: int, score: int, test_id: int):
    db = SessionLocal()
    data = select_lesson_id_and_subject_id_by_test_id_db(db=db, test_id=test_id)
    journal_data = select_journal_row(
        db=db,
        student_id=student_id,
        subject_id=data.subject_id,
        lesson_id=data.lesson_id
    )

    if journal_data is None:
        filling_journal(
            db=db,
            score=score,
            subject_id=data.subject_id,
            lesson_id=data.lesson_id,
            student_id=student_id
        )
    else:
        update_score_to_journal(db=db, journal_row=journal_data, score=score)

    db.close()
