from celery import Celery

from app.crud.subject_crud import select_lesson_id_and_subject_id_by_lecture_id_db, filling_journal
from app.session import SessionLocal

celery_app = Celery("celery", broker="redis://localhost:6379")


@celery_app.task
def confirm_lecture_in_journal(student_id: int, lecture_id: int):
    db = SessionLocal()
    data = select_lesson_id_and_subject_id_by_lecture_id_db(db=db, lecture_id=lecture_id)

    filling_journal(
        db=db,
        absent=True,
        subject_id=data.subject_id,
        lesson_id=data.lesson_id,
        student_id=student_id
    )