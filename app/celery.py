from celery import Celery

from app.crud.subject_crud import filling_journal, select_lesson_id_and_subject_id_by_lecture_id_db
from app.session import SessionLocal
from app.setting import BROKER_URL

celery_app = Celery("celery", broker=BROKER_URL)


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

    db.close()
