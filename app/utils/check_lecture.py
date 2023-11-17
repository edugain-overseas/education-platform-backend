from typing import Dict, List

from sqlalchemy.orm import Session

from app.crud.lecture_crud import get_lecture_db, select_student_lecture


def checking_lecture(db: Session, student_id: int, subject_lessons: List[Dict]) -> List[Dict]:
    for item in subject_lessons:
        if len(item["module_lessons"]) >= 1:
            for lesson_item in item["module_lessons"]:
                if lesson_item["lesson_type"] == "lecture":
                    lecture = get_lecture_db(db=db, lesson_id=lesson_item["lesson_id"])
                    if lecture:
                        student_lecture = select_student_lecture(db=db, lecture_id=lecture.id, student_id=student_id)

                        if student_lecture is not None and student_lecture.check is True:
                            lesson_item["viewed"] = True
                        else:
                            lesson_item["viewed"] = False
                    else:
                        lesson_item["viewed"] = False

    return subject_lessons
