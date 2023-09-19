from enum import Enum as EnumType

from sqlalchemy import Boolean, Column, Date, DateTime, Enum, ForeignKey, Integer, String, Text, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class UserTypeOption(str, EnumType):
    student = 'student'
    moder = 'moder'
    teacher = 'teacher'
    curator = 'curator'


class LessonTypeOption(str, EnumType):
    lecture = 'lecture'
    seminar = 'seminar'
    test = 'test'
    online_lecture = 'online_lecture'
    online_seminar = 'online_seminar'
    module_control = 'module_control'
    exam = 'exam'


class QuestionTypeOption(str, EnumType):
    test = 'test'
    boolean = 'boolean'
    test_with_photo = 'test_with_photo'
    test_with_input = 'test_with_input'
    matching = 'matching'
    open_question = 'open_question'


class MessageTypeOption(str, EnumType):
    alone = 'alone'
    everyone = 'everyone'
    several = 'several'


class ModuleControlTypeOption(str, EnumType):
    with_video = 'with_video'
    only_test = 'only_test'


class UserType(Base):
    __tablename__ = "user_type"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(UserTypeOption), nullable=False)

    user = relationship('User', back_populates='user_type')


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(25), index=True, unique=True, nullable=False)
    hashed_pass = Column(String, nullable=False)
    is_active = Column(Boolean)
    token = Column(String)
    exp_token = Column(DateTime)
    last_active = Column(Date)

    user_type_id = Column(Integer, ForeignKey('user_type.id'))

    user_type = relationship('UserType', back_populates='user')
    student = relationship('Student', back_populates='user')
    teacher = relationship('Teacher', back_populates='user')
    curator = relationship('Curator', back_populates='user')
    moder = relationship('Moder', back_populates='user')

    chat_message = relationship('GroupChat', back_populates='user')
    chat_answer = relationship('GroupChatAnswer', back_populates='user')
    recipient = relationship('MessageRecipient', back_populates='user')

    subject_message = relationship('SubjectChat', back_populates='user')
    subject_answer = relationship('SubjectChatAnswer', back_populates='user')
    subject_recipient = relationship('SubjectRecipient', back_populates='user')


class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False)
    surname = Column(String(64), nullable=False)
    lastname = Column(String(64), nullable=False)
    phone = Column(String(15), nullable=False)
    email = Column(String(40), nullable=False)
    image_path = Column(String)
    qualification = Column(String)
    educational_program = Column(String)
    subject_area = Column(String)
    field_of_study = Column(String)
    group_leader = Column(Boolean, default=False, nullable=False, autoincrement=True)
    date_added = Column(Date, nullable=False, autoincrement=True)

    user_id = Column(Integer, ForeignKey('user.id'))
    specialization_id = Column(Integer, ForeignKey('specialization.id'))
    course_id = Column(Integer, ForeignKey('course.id'))
    group_id = Column(Integer, ForeignKey('group.id'))

    user = relationship('User', back_populates='student')
    specialization = relationship('Specialization', back_populates='student')
    course = relationship('Course', back_populates='student')
    group = relationship('Group', back_populates='student')

    lesson_missing = relationship('LessonMissing', back_populates='student')
    lesson_score = relationship('LessonScore', back_populates='student')
    lecture_score = relationship('LectureScore', back_populates='student')

    student_test = relationship('StudentTest', back_populates='student')
    student_test_answer = relationship('StudentTestAnswer', back_populates='student')
    student_test_matching = relationship('StudentTestMatching', back_populates='student')
    test_feedback = relationship('TestFeedback', back_populates='student')
    student_seminar = relationship('StudentSeminar', back_populates='student')
    student_seminar_answer = relationship('StudentSeminarAnswer', back_populates='student')
    student_seminar_matching = relationship('StudentSeminarMatching', back_populates='student')
    seminar_feedback = relationship('SeminarFeedback', back_populates='student')
    video_lecture_score = relationship('VideoLectureScore', back_populates='student')
    video_seminar_score = relationship('VideoSeminarScore', back_populates='student')
    student_module = relationship('StudentModule', back_populates='student')
    student_module_answer = relationship('StudentModuleAnswer', back_populates='student')
    student_module_matching = relationship('StudentModuleMatching', back_populates='student')

    additional_subject = relationship('Subject', secondary='student_additional_subject', back_populates='students')
    participant_comment = relationship('ParticipantComment', back_populates='student')


class Teacher(Base):
    __tablename__ = "teacher"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False)
    surname = Column(String(64), nullable=False)
    lastname = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False)
    image_path = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User', back_populates='teacher')
    subjects = relationship('Subject', secondary='subject_teacher_association', back_populates='teachers')
    groups = relationship('Group', secondary='group_teacher_association', back_populates='teachers')
    lesson = relationship('Lesson', back_populates='teacher')

    test_feedback_answer = relationship('TestFeedbackAnswer', back_populates='teacher')
    seminar_feedback_answer = relationship('SeminarFeedbackAnswer', back_populates='teacher')


class Curator(Base):
    __tablename__ = "curator"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False)
    surname = Column(String(64), nullable=False)
    lastname = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False)
    image_path = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User', back_populates='curator')
    group = relationship('Group', back_populates='curator')


class Moder(Base):
    __tablename__ = "moder"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64))
    surname = Column(String(64))
    lastname = Column(String(64))
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User', back_populates='moder')


class Course(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True, index=True)
    course_number = Column(Integer, default=1, nullable=False)
    semester_number = Column(Integer, default=1, nullable=False)

    specialization = relationship('Specialization', back_populates='course')
    subject = relationship('Subject', back_populates='course')
    student = relationship('Student', back_populates='course')


class Specialization(Base):
    __tablename__ = "specialization"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    course_id = Column(Integer, ForeignKey('course.id'))

    course = relationship('Course', back_populates='specialization')
    subject = relationship('Subject', back_populates='specialization')
    group = relationship('Group', back_populates='specialization')
    student = relationship('Student', back_populates='specialization')


class Subject(Base):
    __tablename__ = "subject"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    image_path = Column(String)
    logo_path = Column(String)
    is_published = Column(Boolean)
    quantity_lecture = Column(Integer)
    quantity_seminar = Column(Integer)
    quantity_test = Column(Integer)
    quantity_module = Column(Integer)
    score = Column(Integer)
    exam_date = Column(Date)

    specialization_id = Column(Integer, ForeignKey('specialization.id'))
    course_id = Column(Integer, ForeignKey('course.id'))
    group_id = Column(Integer, ForeignKey('group.id'))

    teachers = relationship('Teacher', secondary='subject_teacher_association', back_populates='subjects')
    students = relationship('Student', secondary='student_additional_subject', back_populates='additional_subject')
    specialization = relationship('Specialization', back_populates='subject')
    course = relationship('Course', back_populates='subject')
    module = relationship('Module', back_populates='subject')
    lesson = relationship('Lesson', back_populates='subject')
    group = relationship('Group', back_populates='subject')
    subject_chat = relationship('SubjectChat', back_populates='subject')
    subject_item = relationship('SubjectItem', back_populates='subject')
    subject_icon = relationship('SubjectIcon', back_populates='subject')
    subject_instruction = relationship('SubjectInstruction', back_populates='subject')
    participant_comment = relationship('ParticipantComment', back_populates='subject')

    @property
    def get_total(self):
        return self.quantity_seminar + self.quantity_lecture + self.quantity_module + self.quantity_test


class SubjectTeacherAssociation(Base):
    __tablename__ = "subject_teacher_association"

    subject_id = Column(Integer, ForeignKey('subject.id'), primary_key=True)
    teacher_id = Column(Integer, ForeignKey('teacher.id'), primary_key=True)


class StudentAdditionalSubject(Base):
    __tablename__ = "student_additional_subject"

    subject_id = Column(Integer, ForeignKey('subject.id'), primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'), primary_key=True)


class SubjectItem(Base):
    __tablename__ = "subject_item"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    subject_id = Column(Integer, ForeignKey('subject.id'))

    subject = relationship('Subject', uselist=False, back_populates='subject_item')


class SubjectIcon(Base):
    __tablename__ = "subject_icon"

    id = Column(Integer, primary_key=True, index=True)
    icon_path = Column(String, nullable=False)
    is_default = Column(Boolean, nullable=False)
    subject_id = Column(Integer, ForeignKey('subject.id'))

    subject = relationship('Subject', back_populates='subject_icon')


class SubjectInstruction(Base):
    __tablename__ = "subject_instruction"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey('subject.id'))
    number = Column(Integer, nullable=False)
    header = Column(String, nullable=False)
    text = Column(Text)
    date = Column(Date)

    subject = relationship('Subject', back_populates='subject_instruction')
    subject_instruction_files = relationship('SubjectInstructionFiles', back_populates='subject_instruction')


class SubjectInstructionFiles(Base):
    __tablename__ = "subject_instruction_files"

    id = Column(Integer, primary_key=True, index=True)
    subject_instruction_id = Column(Integer, ForeignKey('subject_instruction.id'))
    file = Column(String, nullable=False)

    subject_instruction = relationship('SubjectInstruction', back_populates='subject_instruction_files')


class ParticipantComment(Base):
    __tablename__ = "participant_comment"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey('subject.id'))
    student_id = Column(Integer, ForeignKey('student.id'))
    comment = Column(String, nullable=False)

    subject = relationship('Subject', back_populates='participant_comment')
    student = relationship('Student', back_populates='participant_comment')


class Group(Base):
    __tablename__ = "group"

    id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String, nullable=False)
    curator_id = Column(Integer, ForeignKey('curator.id'))
    specialization_id = Column(Integer, ForeignKey('specialization.id'))

    teachers = relationship('Teacher', secondary='group_teacher_association', back_populates='groups')
    curator = relationship('Curator', back_populates='group')
    specialization = relationship('Specialization', back_populates='group')
    student = relationship('Student', back_populates='group')
    group_chat = relationship('GroupChat', back_populates='group')
    subject = relationship('Subject', back_populates='group')


class GroupTeacherAssociation(Base):
    __tablename__ = "group_teacher_association"

    group_id = Column(Integer, ForeignKey('group.id'), primary_key=True)
    teacher_id = Column(Integer, ForeignKey('teacher.id'), primary_key=True)


class Module(Base):
    __tablename__ = "module"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, default=1, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    subject_id = Column(Integer, ForeignKey('subject.id'))

    subject = relationship('Subject', back_populates='module')
    lesson = relationship('Lesson', back_populates='module')
    module_control = relationship('ModuleControl', back_populates='module')


class LessonType(Base):
    __tablename__ = "lesson_type"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(LessonTypeOption), nullable=False)

    lesson = relationship('Lesson', back_populates='lesson_type')


class Lesson(Base):
    __tablename__ = "lesson"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, default=1, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    is_published = Column(Boolean, default=False)
    lesson_date = Column(DateTime)
    lesson_end = Column(Time)

    lesson_type_id = Column(Integer, ForeignKey('lesson_type.id'))
    module_id = Column(Integer, ForeignKey('module.id'))
    subject_id = Column(Integer, ForeignKey('subject.id'))
    teacher_id = Column(Integer, ForeignKey('teacher.id'))

    lesson_type = relationship('LessonType', back_populates='lesson')
    module = relationship('Module', back_populates='lesson')
    subject = relationship('Subject', back_populates='lesson')
    teacher = relationship('Teacher', back_populates='lesson')
    lesson_missing = relationship('LessonMissing', back_populates='lesson')
    lesson_score = relationship('LessonScore', back_populates='lesson')

    lecture = relationship('Lecture', back_populates='lesson')
    test_lesson = relationship('TestLesson', back_populates='lesson')
    seminar = relationship('Seminar', back_populates='lesson')
    video_lecture = relationship('VideoLecture', back_populates='lesson')
    video_seminar = relationship('VideoSeminar', back_populates='lesson')
    module_control = relationship('ModuleControl', back_populates='lesson')


class LessonMissing(Base):
    __tablename__ = "lesson_missing"

    id = Column(Integer, primary_key=True, index=True)
    missing = Column(Boolean)

    student_id = Column(Integer, ForeignKey('student.id'))
    lesson_id = Column(Integer, ForeignKey('lesson.id'))

    student = relationship('Student', back_populates='lesson_missing')
    lesson = relationship('Lesson', back_populates='lesson_missing')


class LessonScore(Base):
    __tablename__ = "lesson_score"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer)
    lesson_type = Column(Enum(LessonTypeOption))

    student_id = Column(Integer, ForeignKey('student.id'))
    lesson_id = Column(Integer, ForeignKey('lesson.id'))

    student = relationship('Student', back_populates='lesson_score')
    lesson = relationship('Lesson', back_populates='lesson_score')


class Lecture(Base):
    __tablename__ = "lecture"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey('lesson.id'))

    lesson = relationship('Lesson', uselist=False, back_populates='lecture')
    attributes = relationship('LectureAttribute', back_populates='lecture')
    values = relationship('LectureValue', back_populates='lecture')
    lecture_score = relationship('LectureScore', back_populates='lecture')


class LectureAttribute(Base):
    __tablename__ = "lecture_attribute"

    id = Column(Integer, primary_key=True, index=True)
    attr_type = Column(String)
    attr_title = Column(String)
    attr_number = Column(Integer)
    download_allowed = Column(Boolean)
    lecture_id = Column(Integer, ForeignKey('lecture.id'))

    lecture = relationship('Lecture', back_populates='attributes')
    lecture_value = relationship('LectureValue', back_populates='lecture_attribute')


class LectureValue(Base):
    __tablename__ = "lecture_value"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Text)
    lecture_id = Column(Integer, ForeignKey('lecture.id'))
    lecture_attribute_id = Column(Integer, ForeignKey('lecture_attribute.id'))

    lecture = relationship('Lecture', back_populates='values')
    lecture_attribute = relationship('LectureAttribute', back_populates='lecture_value')


class LectureScore(Base):
    __tablename__ = "lecture_score"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer)
    check = Column(Boolean, default=False, nullable=False)

    lecture_id = Column(Integer, ForeignKey('lecture.id'))
    student_id = Column(Integer, ForeignKey('student.id'))

    lecture = relationship('Lecture', back_populates='lecture_score')
    student = relationship('Student', back_populates='lecture_score')


class QuestionType(Base):
    __tablename__ = "question_type"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(QuestionTypeOption), nullable=False)

    test_question = relationship('TestQuestion', back_populates='question_type')
    seminar_question = relationship('SeminarQuestion', back_populates='question_type')
    module_question = relationship('ModuleQuestion', back_populates='question_type')


class TestLesson(Base):
    __tablename__ = "test_lesson"

    id = Column(Integer, primary_key=True, index=True)
    is_published = Column(Boolean, nullable=False)
    set_timer = Column(Boolean)
    timer = Column(Time)
    attempts = Column(Integer, default=1, nullable=False)
    show_answer = Column(Boolean)
    deadline = Column(DateTime)
    lesson_id = Column(Integer, ForeignKey('lesson.id'))

    lesson = relationship('Lesson', uselist=False, back_populates='test_lesson')
    test_question = relationship('TestQuestion', back_populates='test_lesson')
    student_test = relationship('StudentTest', back_populates='test_lesson')


class TestQuestion(Base):
    __tablename__ = "test_question"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    question_number = Column(Integer, default=1, nullable=False)
    question_score = Column(Integer, nullable=False)

    question_type_id = Column(Integer, ForeignKey('question_type.id'))
    test_lesson_id = Column(Integer, ForeignKey('test_lesson.id'))

    question_type = relationship('QuestionType', back_populates='test_question')
    test_lesson = relationship('TestLesson', back_populates='test_question')
    test_answer = relationship('TestAnswer', back_populates='test_question')
    matching_left = relationship('TestMatchingLeft', back_populates='test_question')
    matching_right = relationship('TestMatchingRight', back_populates='test_question')
    student_test_answer = relationship('StudentTestAnswer', back_populates='test_question')
    student_test_matching = relationship('StudentTestMatching', back_populates='test_question')
    test_feedback = relationship('TestFeedback', back_populates='test_question')


class TestAnswer(Base):
    __tablename__ = "test_answer"

    id = Column(Integer, primary_key=True, index=True)
    answer_text = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False)

    question_id = Column(Integer, ForeignKey('test_question.id'), nullable=False)

    test_question = relationship('TestQuestion', back_populates='test_answer')
    student_test_answer = relationship('StudentTestAnswer', back_populates='test_answer')


class TestMatchingLeft(Base):
    __tablename__ = "test_matching_left"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)

    right_id = Column(Integer, ForeignKey('test_matching_right.id'))
    question_id = Column(Integer, ForeignKey('test_question.id'))

    right_option = relationship('TestMatchingRight', back_populates='left_option')
    test_question = relationship('TestQuestion', back_populates='matching_left')
    student_test_matching = relationship('StudentTestMatching', back_populates='left_option')


class TestMatchingRight(Base):
    __tablename__ = "test_matching_right"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    question_id = Column(Integer, ForeignKey('test_question.id'))

    left_option = relationship('TestMatchingLeft', back_populates='right_option')
    test_question = relationship('TestQuestion', back_populates='matching_right')
    student_test_matching = relationship('StudentTestMatching', back_populates='right_option')


class StudentTest(Base):
    __tablename__ = "student_test"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer)
    number_attempt = Column(Integer, default=1, nullable=False)

    test_id = Column(Integer, ForeignKey('test_lesson.id'))
    student_id = Column(Integer, ForeignKey('student.id'))

    test_lesson = relationship('TestLesson', back_populates='student_test')
    student = relationship('Student', back_populates='student_test')
    student_test_answer = relationship('StudentTestAnswer', back_populates='student_test')
    student_test_matching = relationship('StudentTestMatching', back_populates='student_test')


class StudentTestAnswer(Base):
    __tablename__ = "student_test_answer"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer)

    student_id = Column(Integer, ForeignKey('student.id'))
    question_id = Column(Integer, ForeignKey('test_question.id'))
    answer_id = Column(Integer, ForeignKey('test_answer.id'))
    student_test_id = Column(Integer, ForeignKey('student_test.id'))

    student = relationship('Student', back_populates='student_test_answer')
    test_question = relationship('TestQuestion', back_populates='student_test_answer')
    test_answer = relationship('TestAnswer', back_populates='student_test_answer')
    student_test = relationship('StudentTest', back_populates='student_test_answer')


class StudentTestMatching(Base):
    __tablename__ = "student_test_matching"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer)

    student_id = Column(Integer, ForeignKey('student.id'))
    question_id = Column(Integer, ForeignKey('test_question.id'))
    left_option_id = Column(Integer, ForeignKey('test_matching_left.id'))
    right_option_id = Column(Integer, ForeignKey('test_matching_right.id'))
    student_test_id = Column(Integer, ForeignKey('student_test.id'))

    student = relationship('Student', back_populates='student_test_matching')
    test_question = relationship('TestQuestion', back_populates='student_test_matching')
    left_option = relationship('TestMatchingLeft', back_populates='student_test_matching')
    right_option = relationship('TestMatchingRight', back_populates='student_test_matching')
    student_test = relationship('StudentTest', back_populates='student_test_matching')


class TestFeedback(Base):
    __tablename__ = "test_feedback"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)

    student_id = Column(Integer, ForeignKey('student.id'))
    question_id = Column(Integer, ForeignKey('test_question.id'))

    student = relationship('Student', back_populates='test_feedback')
    test_question = relationship('TestQuestion', back_populates='test_feedback')
    feedback_answer = relationship('TestFeedbackAnswer', back_populates='test_feedback')


class TestFeedbackAnswer(Base):
    __tablename__ = "test_feedback_answer"

    id = Column(Integer, primary_key=True, index=True)
    answer = Column(String)

    teacher_id = Column(Integer, ForeignKey('teacher.id'))
    test_feedback_id = Column(Integer, ForeignKey('test_feedback.id'))

    teacher = relationship('Teacher', back_populates='test_feedback_answer')
    test_feedback = relationship('TestFeedback', back_populates='feedback_answer')


class Seminar(Base):
    __tablename__ = "seminar"

    id = Column(Integer, primary_key=True, index=True)
    is_published = Column(Boolean, nullable=False)
    set_timer = Column(Boolean)
    timer = Column(Time)
    attempts = Column(Integer, default=1, nullable=False)
    lesson_id = Column(Integer, ForeignKey('lesson.id'))

    lesson = relationship('Lesson', uselist=False, back_populates='seminar')
    seminar_question = relationship('SeminarQuestion', back_populates='seminar')
    student_seminar = relationship('StudentSeminar', back_populates='seminar')


class SeminarQuestion(Base):
    __tablename__ = "seminar_question"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    question_number = Column(Integer, default=1, nullable=False)
    question_score = Column(Integer, nullable=False)

    question_type_id = Column(Integer, ForeignKey('question_type.id'))
    seminar_id = Column(Integer, ForeignKey('seminar.id'))

    question_type = relationship('QuestionType', back_populates='seminar_question')
    seminar = relationship('Seminar', back_populates='seminar_question')
    seminar_answer = relationship('SeminarAnswer', back_populates='seminar_question')
    matching_left = relationship('SeminarMatchingLeft', back_populates='seminar_question')
    matching_right = relationship('SeminarMatchingRight', back_populates='seminar_question')
    student_seminar_answer = relationship('StudentSeminarAnswer', back_populates='seminar_question')
    student_seminar_matching = relationship('StudentSeminarMatching', back_populates='seminar_question')
    seminar_feedback = relationship('SeminarFeedback', back_populates='seminar_question')


class SeminarAnswer(Base):
    __tablename__ = "seminar_answer"

    id = Column(Integer, primary_key=True, index=True)
    answer_text = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False)

    question_id = Column(Integer, ForeignKey('seminar_question.id'), nullable=False)

    seminar_question = relationship('SeminarQuestion', back_populates='seminar_answer')
    student_seminar_answer = relationship('StudentSeminarAnswer', back_populates='seminar_answer')


class SeminarMatchingLeft(Base):
    __tablename__ = "seminar_matching_left"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)

    right_id = Column(Integer, ForeignKey('seminar_matching_right.id'))
    question_id = Column(Integer, ForeignKey('seminar_question.id'))

    right_option = relationship('SeminarMatchingRight', back_populates='left_option')
    seminar_question = relationship('SeminarQuestion', back_populates='matching_left')
    student_seminar_matching = relationship('StudentSeminarMatching', back_populates='left_option')


class SeminarMatchingRight(Base):
    __tablename__ = "seminar_matching_right"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    question_id = Column(Integer, ForeignKey('seminar_question.id'))

    left_option = relationship('SeminarMatchingLeft', back_populates='right_option')
    seminar_question = relationship('SeminarQuestion', back_populates='matching_right')
    student_seminar_matching = relationship('StudentSeminarMatching', back_populates='right_option')


class StudentSeminar(Base):
    __tablename__ = "student_seminar"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer)
    number_attempt = Column(Integer, default=1)

    seminar_id = Column(Integer, ForeignKey('seminar.id'))
    student_id = Column(Integer, ForeignKey('student.id'))

    seminar = relationship('Seminar', back_populates='student_seminar')
    student = relationship('Student', back_populates='student_seminar')
    student_seminar_answer = relationship('StudentSeminarAnswer', back_populates='student_seminar')
    student_seminar_matching = relationship('StudentSeminarMatching', back_populates='student_seminar')


class StudentSeminarAnswer(Base):
    __tablename__ = "student_seminar_answer"

    id = Column(Integer, primary_key=True, index=True)
    answer_text = Column(String)
    score = Column(Integer)

    student_id = Column(Integer, ForeignKey('student.id'))
    question_id = Column(Integer, ForeignKey('seminar_question.id'))
    answer_id = Column(Integer, ForeignKey('seminar_answer.id'))
    student_seminar_id = Column(Integer, ForeignKey('student_seminar.id'))

    student = relationship('Student', back_populates='student_seminar_answer')
    seminar_question = relationship('SeminarQuestion', back_populates='student_seminar_answer')
    seminar_answer = relationship('SeminarAnswer', back_populates='student_seminar_answer')
    student_seminar = relationship('StudentSeminar', back_populates='student_seminar_answer')


class StudentSeminarMatching(Base):
    __tablename__ = "student_seminar_matching"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer)

    student_id = Column(Integer, ForeignKey('student.id'))
    question_id = Column(Integer, ForeignKey('seminar_question.id'))
    left_option_id = Column(Integer, ForeignKey('seminar_matching_left.id'))
    right_option_id = Column(Integer, ForeignKey('seminar_matching_right.id'))
    student_seminar_id = Column(Integer, ForeignKey('student_seminar.id'))

    student = relationship('Student', back_populates='student_seminar_matching')
    seminar_question = relationship('SeminarQuestion', back_populates='student_seminar_matching')
    left_option = relationship('SeminarMatchingLeft', back_populates='student_seminar_matching')
    right_option = relationship('SeminarMatchingRight', back_populates='student_seminar_matching')
    student_seminar = relationship('StudentSeminar', back_populates='student_seminar_matching')


class SeminarFeedback(Base):
    __tablename__ = "seminar_feedback"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)

    student_id = Column(Integer, ForeignKey('student.id'))
    question_id = Column(Integer, ForeignKey('seminar_question.id'))

    student = relationship('Student', back_populates='seminar_feedback')
    seminar_question = relationship('SeminarQuestion', back_populates='seminar_feedback')
    feedback_answer = relationship('SeminarFeedbackAnswer', back_populates='seminar_feedback')


class SeminarFeedbackAnswer(Base):
    __tablename__ = "seminar_feedback_answer"

    id = Column(Integer, primary_key=True, index=True)
    answer = Column(String)

    teacher_id = Column(Integer, ForeignKey('teacher.id'))
    seminar_feedback_id = Column(Integer, ForeignKey('seminar_feedback.id'))

    teacher = relationship('Teacher', back_populates='seminar_feedback_answer')
    seminar_feedback = relationship('SeminarFeedback', back_populates='feedback_answer')


class VideoLecture(Base):
    __tablename__ = "video_lecture"

    id = Column(Integer, primary_key=True, index=True)
    link = Column(String, nullable=False)

    lesson_id = Column(Integer, ForeignKey('lesson.id'))

    lesson = relationship('Lesson', uselist=False, back_populates='video_lecture')
    video_lecture_score = relationship('VideoLectureScore', back_populates='video_lecture')


class VideoLectureScore(Base):
    __tablename__ = "video_lecture_score"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer)

    video_lecture_id = Column(Integer, ForeignKey('video_lecture.id'))
    student_id = Column(Integer, ForeignKey('student.id'))

    video_lecture = relationship('VideoLecture', back_populates='video_lecture_score')
    student = relationship('Student', back_populates='video_lecture_score')


class VideoSeminar(Base):
    __tablename__ = "video_seminar"

    id = Column(Integer, primary_key=True, index=True)
    link = Column(String, nullable=False)

    lesson_id = Column(Integer, ForeignKey('lesson.id'))

    lesson = relationship('Lesson', uselist=False, back_populates='video_seminar')
    video_seminar_score = relationship('VideoSeminarScore', back_populates='video_seminar')


class VideoSeminarScore(Base):
    __tablename__ = "video_seminar_score"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer)

    video_seminar_id = Column(Integer, ForeignKey('video_seminar.id'))
    student_id = Column(Integer, ForeignKey('student.id'))

    video_seminar = relationship('VideoSeminar', back_populates='video_seminar_score')
    student = relationship('Student', back_populates='video_seminar_score')


class ModuleControlType(Base):
    __tablename__ = "module_control_type"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(ModuleControlTypeOption), nullable=False)

    module_control = relationship('ModuleControl', back_populates='module_type')


class ModuleControl(Base):
    __tablename__ = "module_control"

    id = Column(Integer, primary_key=True, index=True)
    is_published = Column(Boolean, nullable=False)
    set_timer = Column(Boolean, default=False, nullable=False)
    timer = Column(Time)
    timer_test = Column(Time)
    attempts = Column(Integer, default=1, nullable=False)
    link = Column(String)

    module_type_id = Column(Integer, ForeignKey('module_control_type.id'))
    module_id = Column(Integer, ForeignKey('module.id'))
    lesson_id = Column(Integer, ForeignKey('lesson.id'))

    module = relationship('Module', uselist=False, back_populates='module_control')
    lesson = relationship('Lesson', uselist=False, back_populates='module_control')
    module_type = relationship('ModuleControlType', back_populates='module_control')
    module_question = relationship('ModuleQuestion', back_populates='module_control')
    student_module = relationship('StudentModule', back_populates='module_control')


class ModuleQuestion(Base):
    __tablename__ = "module_question"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    question_number = Column(Integer, nullable=False)
    question_score = Column(Integer, nullable=False)

    question_type_id = Column(ForeignKey('question_type.id'))
    module_control_id = Column(ForeignKey('module_control.id'))

    question_type = relationship('QuestionType', back_populates='module_question')
    module_control = relationship('ModuleControl', back_populates='module_question')
    module_answer = relationship('ModuleAnswer', back_populates='module_question')
    matching_left = relationship('ModuleMatchingLeft', back_populates='module_question')
    matching_right = relationship('ModuleMatchingRight', back_populates='module_question')
    student_module_answer = relationship('StudentModuleAnswer', back_populates='module_question')
    student_module_matching = relationship('StudentModuleMatching', back_populates='module_question')


class ModuleAnswer(Base):
    __tablename__ = "module_answer"

    id = Column(Integer, primary_key=True, index=True)
    answer_text = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False)

    question_id = Column(Integer, ForeignKey('module_question.id'), nullable=False)

    module_question = relationship('ModuleQuestion', back_populates='module_answer')
    student_module_answer = relationship('StudentModuleAnswer', back_populates='module_answer')


class ModuleMatchingLeft(Base):
    __tablename__ = "module_matching_left"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)

    right_id = Column(Integer, ForeignKey('module_matching_right.id'))
    question_id = Column(Integer, ForeignKey('module_question.id'))

    right_option = relationship('ModuleMatchingRight', back_populates='left_option')
    module_question = relationship('ModuleQuestion', back_populates='matching_left')
    student_module_matching = relationship('StudentModuleMatching', back_populates='left_option')


class ModuleMatchingRight(Base):
    __tablename__ = "module_matching_right"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    question_id = Column(Integer, ForeignKey('module_question.id'))

    left_option = relationship('ModuleMatchingLeft', back_populates='right_option')
    module_question = relationship('ModuleQuestion', back_populates='matching_right')
    student_module_matching = relationship('StudentModuleMatching', back_populates='right_option')


class StudentModule(Base):
    __tablename__ = "student_module"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer, nullable=False)
    number_attempt = Column(Integer, default=1)

    module_control_id = Column(Integer, ForeignKey('module_control.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('student.id'), nullable=False)

    student = relationship('Student', back_populates='student_module')
    module_control = relationship('ModuleControl', back_populates='student_module')
    student_module_answer = relationship('StudentModuleAnswer', back_populates='student_module')
    student_module_matching = relationship('StudentModuleMatching', back_populates='student_module')


class StudentModuleAnswer(Base):
    __tablename__ = "student_module_answer"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer)
    answer_text = Column(Text)

    student_id = Column(Integer, ForeignKey('student.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('module_question.id'), nullable=False)
    answer_id = Column(Integer, ForeignKey('module_answer.id'), nullable=False)
    student_module_id = Column(Integer, ForeignKey('student_module.id'), nullable=False)

    student = relationship('Student', back_populates='student_module_answer')
    module_question = relationship('ModuleQuestion', back_populates='student_module_answer')
    module_answer = relationship('ModuleAnswer', back_populates='student_module_answer')
    student_module = relationship('StudentModule', back_populates='student_module_answer')


class StudentModuleMatching(Base):
    __tablename__ = "student_module_matching"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer, nullable=False)

    student_id = Column(Integer, ForeignKey('student.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('module_question.id'), nullable=False)
    left_option_id = Column(Integer, ForeignKey('module_matching_left.id'), nullable=False)
    right_option_id = Column(Integer, ForeignKey('module_matching_right.id'), nullable=False)
    student_module_id = Column(Integer, ForeignKey('student_module.id'), nullable=False)

    student = relationship('Student', back_populates='student_module_matching')
    module_question = relationship('ModuleQuestion', back_populates='student_module_matching')
    left_option = relationship('ModuleMatchingLeft', back_populates='student_module_matching')
    right_option = relationship('ModuleMatchingRight', back_populates='student_module_matching')
    student_module = relationship('StudentModule', back_populates='student_module_matching')


class GroupChatAttachFile(Base):
    __tablename__ = "group_chat_attach_file"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String)
    mime_type = Column(String)

    chat_message = Column(Integer, ForeignKey('group_chat.id'))
    chat_answer = Column(Integer, ForeignKey('group_chat_answer.id'))

    group_chat_message = relationship('GroupChat', back_populates='attach_file')
    group_chat_answer = relationship('GroupChatAnswer', back_populates='attach_file')


class GroupChat(Base):
    __tablename__ = "group_chat"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)
    datetime_message = Column(DateTime, autoincrement=True)
    fixed = Column(Boolean, default=False)
    sender_type = Column(Enum(UserTypeOption), nullable=False)
    sender_id = Column(Integer, ForeignKey('user.id'))
    group_id = Column(Integer, ForeignKey('group.id'))
    message_type = Column(Enum(MessageTypeOption), nullable=False)
    read_by = Column(String)

    user = relationship('User', back_populates='chat_message')
    group = relationship('Group', back_populates='group_chat')
    group_chat_answer = relationship('GroupChatAnswer', back_populates='group_chat')
    attach_file = relationship('GroupChatAttachFile', back_populates='group_chat_message')
    recipient = relationship('MessageRecipient', back_populates='group_chat_message')


class GroupChatAnswer(Base):
    __tablename__ = "group_chat_answer"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)
    datetime_message = Column(DateTime, autoincrement=True)
    sender_type = Column(Enum(UserTypeOption), nullable=False)
    sender_id = Column(Integer, ForeignKey('user.id'))
    group_chat_id = Column(Integer, ForeignKey('group_chat.id'))
    read_by = Column(String)

    user = relationship('User', back_populates='chat_answer')
    group_chat = relationship('GroupChat', back_populates='group_chat_answer')
    attach_file = relationship('GroupChatAttachFile', back_populates='group_chat_answer')


class MessageRecipient(Base):
    __tablename__ = "message_recipient"

    id = Column(Integer, primary_key=True, index=True)
    group_chat_id = Column(Integer, ForeignKey('group_chat.id'))
    recipient_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User', back_populates='recipient')
    group_chat_message = relationship('GroupChat', back_populates='recipient')


class SubjectChatAttachFile(Base):
    __tablename__ = "subject_chat_attach_file"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String)
    mime_type = Column(String)

    chat_message = Column(Integer, ForeignKey('subject_chat.id'))
    chat_answer = Column(Integer, ForeignKey('subject_chat_answer.id'))

    subject_chat_message = relationship('SubjectChat', back_populates='attach_file')
    subject_chat_answer = relationship('SubjectChatAnswer', back_populates='attach_file')


class SubjectChat(Base):
    __tablename__ = "subject_chat"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)
    datetime_message = Column(DateTime, autoincrement=True)
    fixed = Column(Boolean, default=False)
    sender_type = Column(Enum(UserTypeOption), nullable=False)
    sender_id = Column(Integer, ForeignKey('user.id'))
    subject_id = Column(Integer, ForeignKey('subject.id'))
    message_type = Column(Enum(MessageTypeOption), nullable=False)
    read_by = Column(String)

    user = relationship('User', back_populates='subject_message')
    subject = relationship('Subject', back_populates='subject_chat')
    subject_chat_answer = relationship('SubjectChatAnswer', back_populates='subject_chat')
    attach_file = relationship('SubjectChatAttachFile', back_populates='subject_chat_message')
    subject_recipient = relationship('SubjectRecipient', back_populates='subject_chat_message')


class SubjectChatAnswer(Base):
    __tablename__ = "subject_chat_answer"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)
    datetime_message = Column(DateTime, autoincrement=True)
    sender_type = Column(Enum(UserTypeOption), nullable=False)
    sender_id = Column(Integer, ForeignKey('user.id'))
    subject_chat_id = Column(Integer, ForeignKey('subject_chat.id'))
    read_by = Column(String)

    user = relationship('User', back_populates='subject_answer')
    subject_chat = relationship('SubjectChat', back_populates='subject_chat_answer')
    attach_file = relationship('SubjectChatAttachFile', back_populates='subject_chat_answer')


class SubjectRecipient(Base):
    __tablename__ = "subject_recipient"

    id = Column(Integer, primary_key=True, index=True)
    subject_chat_id = Column(Integer, ForeignKey('subject_chat.id'))
    recipient_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User', back_populates='subject_recipient')
    subject_chat_message = relationship('SubjectChat', back_populates='subject_recipient')
