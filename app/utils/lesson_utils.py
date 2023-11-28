from typing import Dict

from sqlalchemy.orm import Session

from app.crud.lesson_crud import get_lesson_info_db
from app.models import Lecture, TestAnswer, TestLesson, TestQuestion


def get_lesson_base_info(db: Session, lesson_id: int) -> Dict:
    lesson_base = get_lesson_info_db(db=db, lesson_id=lesson_id)

    result = {
        "lessonTitle": lesson_base.lessonTitle,
        "lessonDescription": lesson_base.lessonDescription,
        "lessonDate": lesson_base.lessonDate,
        "lessonEnd": lesson_base.lessonEnd,
    }

    return result


def get_lecture_attributes_info(base_info: Dict, lecture: Lecture) -> Dict:
    base_info["lectureId"] = lecture.id
    base_info["lectureInfo"] = []
    lecture_attributes = lecture.attributes

    for attr in lecture_attributes:
        if attr.attr_type == "text":
            text_attr = {
                "attributeId": attr.id,
                "attributeNumber": attr.attr_number,
                "attributeType": attr.attr_type,
                "attributeTitle": attr.attr_title,
                "attributeText": attr.attr_text,
                "hided": attr.hided
            }
            base_info["lectureInfo"].append(text_attr)

        elif attr.attr_type in ["present", "audio", "video"]:
            file_attr = {
                "attributeId": attr.id,
                "attributeNumber": attr.attr_number,
                "attributeType": attr.attr_type,
                "attributeTitle": attr.attr_title,
                "attributeText": attr.attr_text,
                "hided": attr.hided,
                "fileId": attr.lecture_file[0].id,
                "fileName": attr.lecture_file[0].filename,
                "filePath": attr.lecture_file[0].file_path,
                "fileSize": attr.lecture_file[0].file_size,
                "downloadAllowed": attr.lecture_file[0].download_allowed
            }
            base_info["lectureInfo"].append(file_attr)

        elif attr.attr_type == "file":
            files_attr = {
                "attributeId": attr.id,
                "attributeNumber": attr.attr_number,
                "attributeType": attr.attr_type,
                "attributeTitle": attr.attr_title,
                "attributeText": attr.attr_text,
                "hided": attr.hided,
                "attributeFiles": []
            }

            for file in attr.lecture_file:
                file_data = {
                    "fileId": file.id,
                    "fileName": file.filename,
                    "filePath": file.file_path,
                    "fileSize": file.file_size,
                    "downloadAllowed": file.download_allowed
                }
                files_attr["attributeFiles"].append(file_data)

            base_info["lectureInfo"].append(files_attr)

        elif attr.attr_type == "picture":
            images_attr = {
                "attributeId": attr.id,
                "attributeNumber": attr.attr_number,
                "attributeType": attr.attr_type,
                "attributeTitle": attr.attr_title,
                "attributeText": attr.attr_text,
                "hided": attr.hided,
                "attributeImages": []
            }

            for image in attr.lecture_file:
                image_data = {
                    "imageId": image.id,
                    "imageName": image.filename,
                    "imagePath": image.file_path,
                    "imageSize": image.file_size,
                    "imageDescription": image.file_description,
                    "downloadAllowed": image.download_allowed
                }
                images_attr["attributeImages"].append(image_data)

            base_info["lectureInfo"].append(images_attr)

        elif attr.attr_type == "link":
            link_attr = {
                "attributeId": attr.id,
                "attributeNumber": attr.attr_number,
                "attributeType": attr.attr_type,
                "attributeTitle": attr.attr_title,
                "attributeText": attr.attr_text,
                "hided": attr.hided,
                "attributeLinks": []
            }

            for link in attr.lecture_link:
                link_data = {
                    "linkId": link.id,
                    "link": link.link,
                    "anchor": link.anchor
                }
                link_attr["attributeLinks"].append(link_data)
            base_info["lectureInfo"].append(link_attr)

        else:
            homework_attr = {
                "attributeId": attr.id,
                "attributeNumber": attr.attr_number,
                "attributeType": attr.attr_type,
                "attributeTitle": attr.attr_title,
                "attributeText": attr.attr_text,
                "hided": attr.hided,
                "attributeFiles": [],
                "attributeLinks": []
            }

            if len(attr.lecture_file) >= 1:
                for file in attr.lecture_file:
                    file_data = {
                        "fileId": file.id,
                        "fileName": file.filename,
                        "filePath": file.file_path,
                        "fileSize": file.file_size,
                        "downloadAllowed": file.download_allowed
                    }
                    homework_attr["attributeFiles"].append(file_data)

            if len(attr.lecture_link) >= 1:
                for link in attr.lecture_link:
                    link_data = {
                        "linkId": link.id,
                        "link": link.link,
                        "anchor": link.anchor
                    }
                    homework_attr["attributeLinks"].append(link_data)

            base_info["lectureInfo"].append(homework_attr)
    return base_info


def set_test_info(lesson_base: Dict, test_lesson: TestLesson) -> Dict:
    test_info_dict = {
        "testId": test_lesson.id,
        "isPublished": test_lesson.is_published,
        "setTimer": test_lesson.set_timer,
        "timer": test_lesson.timer,
        "attempts": test_lesson.attempts,
        "showAnswer": test_lesson.show_answer,
        "minScore": test_lesson.min_score,
        "shuffleAnswer": test_lesson.shuffle_answer,
        "deadline": str(test_lesson.deadline),
        "testQuestions": []
    }

    lesson_base.update(test_info_dict)
    return lesson_base


def set_test_question_info(question: TestQuestion) -> Dict:
    question_info = {
        "questionId": question.id,
        "questionType": question.question_type.type,
        "questionText": question.question_text,
        "questionScore": question.question_score,
        "questionNumber": question.question_number,
        "hided": question.hided,
        "questionAnswers": []
    }
    return question_info


def set_test_answer_info(answer: TestAnswer) -> Dict:
    if answer.image_path:
        return {"answerId": answer.id, "answerText": answer.answer_text, "imagePath": answer.image_path}
    else:
        return {"answerId": answer.id, "answerText": answer.answer_text}


def set_three_next_lesson(lessons):
    lessons_list = []

    for lesson in lessons:
        lesson_dict = {
            "lesson_date": lesson.lesson_date,
            "lesson_type": lesson.lesson_type
        }
        lessons_list.append(lesson_dict)

    return lessons_list
