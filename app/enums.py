from enum import Enum as EnumType


class UserTypeOption(str, EnumType):
    student = "student"
    moder = "moder"
    teacher = "teacher"
    curator = "curator"


class LessonTypeOption(str, EnumType):
    lecture = "lecture"
    seminar = "seminar"
    test = "test"
    online_lecture = "online_lecture"
    online_seminar = "online_seminar"
    module_control = "module_control"
    exam = "exam"


class LectureAttributeType(str, EnumType):
    text = "text"
    present = "present"
    audio = "audio"
    picture = "picture"
    video = "video"
    file = "file"
    link = "link"
    homework = "homework"


class QuestionTypeOption(str, EnumType):
    test = "test"
    boolean = "boolean"
    answer_with_photo = "answer_with_photo"
    question_with_photo = "question_with_photo"
    test_with_input = "test_with_input"
    matching = "matching"
    open_question = "open_question"
    multiple_choice = "multiple_choice"


class MessageTypeOption(str, EnumType):
    alone = "alone"
    everyone = "everyone"
    several = "several"


class ModuleControlTypeOption(str, EnumType):
    with_video = "with_video"
    only_test = "only_test"
