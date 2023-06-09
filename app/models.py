from enum import Enum as EnumType

from sqlalchemy import (Boolean, Column, Date, DateTime, Enum, ForeignKey,
                        Integer, String, Text, Time)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class UserTypeOption(str, EnumType):
    student = 'student'
    moder = 'moder'
    teacher = 'teacher'
    curator = 'curator'


class LessonTypeOption(str, EnumType):
    ordinary = 'ordinary'
    homework = 'homework'
    test = 'test'
    webinar = 'webinar'
    module_test = 'module_test'


class MessageTypeOption(str, EnumType):
    alone = 'alone'
    everyone = 'everyone'
    several = 'several'


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

    user_type_id = Column(Integer, ForeignKey('user_type.id'))

    user_type = relationship('UserType', back_populates='user')
    student = relationship('Student', back_populates='user')
    teacher = relationship('Teacher', back_populates='user')
    curator = relationship('Curator', back_populates='user')
    moder = relationship('Moder', back_populates='user')
    chat_message = relationship('GroupChat', back_populates='user')
    chat_answer = relationship('GroupChatAnswer', back_populates='user')
    recipient = relationship('MessageRecipient', back_populates='user')


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
    student_test_answer = relationship('StudentTestAnswer', back_populates='student')
    student_homework_answer = relationship('StudentHomeworkAnswer', back_populates='student')


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
    student_test_answer_comment = relationship('StudentTestAnswerComment', back_populates='teacher')
    student_homework_answer_comment = relationship('StudentHomeworkAnswerComment', back_populates='teacher')


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


class Session(Base):
    __tablename__ = "session"

    id = Column(Integer, primary_key=True, index=True)
    session_date = Column(Date)
    passed = Column(Boolean)


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
    quantity_webinar = Column(Integer)
    score = Column(Integer)

    specialization_id = Column(Integer, ForeignKey('specialization.id'))
    course_id = Column(Integer, ForeignKey('course.id'))

    teachers = relationship('Teacher', secondary='subject_teacher_association', back_populates='subjects')
    specialization = relationship('Specialization', back_populates='subject')
    course = relationship('Course', back_populates='subject')
    module = relationship('Module', back_populates='subject')
    lesson = relationship('Lesson', back_populates='subject')
    subject_chat = relationship('SubjectChat', back_populates='subject')
    subject_info = relationship('SubjectInfo', back_populates='subject')
    subject_instruction = relationship('SubjectInstruction', back_populates='subject')


class SubjectTeacherAssociation(Base):
    __tablename__ = "subject_teacher_association"

    subject_id = Column(Integer, ForeignKey('subject.id'), primary_key=True)
    teacher_id = Column(Integer, ForeignKey('teacher.id'), primary_key=True)


class SubjectInfo(Base):
    __tablename__ = "subject_info"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey('subject.id'))
    header = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    number = Column(Integer, nullable=False)

    subject = relationship('Subject', back_populates='subject_info')
    subject_info_item = relationship('SubjectInfoItem', back_populates='subject_info')


class SubjectInfoItem(Base):
    __tablename__ = "subject_info_item"

    id = Column(Integer, primary_key=True, index=True)
    subject_info_id = Column(Integer, ForeignKey('subject_info.id'))
    icon = Column(String)
    icon_text = Column(String)

    subject_info = relationship('SubjectInfo', back_populates='subject_info_item')


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

    ordinary_lesson = relationship('OrdinaryLesson', back_populates='lesson')
    test_lesson = relationship('TestLesson', back_populates='lesson')
    homework_lesson = relationship('HomeworkLesson', back_populates='lesson')
    webinar_lesson = relationship('WebinarLesson', back_populates='lesson')


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

    student_id = Column(Integer, ForeignKey('student.id'))
    lesson_id = Column(Integer, ForeignKey('lesson.id'))

    student = relationship('Student', back_populates='lesson_score')
    lesson = relationship('Lesson', back_populates='lesson_score')


class OrdinaryLesson(Base):
    __tablename__ = "ordinary_lesson"

    id = Column(Integer, primary_key=True, index=True)

    lesson_id = Column(Integer, ForeignKey('lesson.id'))

    lesson = relationship('Lesson', uselist=False, back_populates='ordinary_lesson')
    attributes = relationship('OrdinaryLessonAttribute', back_populates='ordinary_lesson')
    values = relationship('OrdinaryLessonValue', back_populates='ordinary_lesson')


class OrdinaryLessonAttribute(Base):
    __tablename__ = "ordinary_lesson_attribute"

    id = Column(Integer, primary_key=True, index=True)
    attribute_name = Column(String)
    attr_number = Column(Integer)
    download_allowed = Column(Boolean)

    ordinary_lesson_id = Column(Integer, ForeignKey('ordinary_lesson.id'))

    ordinary_lesson = relationship('OrdinaryLesson', back_populates='attributes')
    ordinary_lesson_value = relationship('OrdinaryLessonValue', back_populates='ordinary_lesson_attribute')


class OrdinaryLessonValue(Base):
    __tablename__ = "ordinary_lesson_value"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Text)

    ordinary_lesson_id = Column(Integer, ForeignKey('ordinary_lesson.id'))
    ordinary_lesson_attribute_id = Column(Integer, ForeignKey('ordinary_lesson_attribute.id'))

    ordinary_lesson = relationship('OrdinaryLesson', back_populates='values')
    ordinary_lesson_attribute = relationship('OrdinaryLessonAttribute', back_populates='ordinary_lesson_value')


class TestLesson(Base):
    __tablename__ = "test_lesson"

    id = Column(Integer, primary_key=True, index=True)
    timer = Column(Time)
    attempts = Column(Integer, default=1, nullable=False)

    lesson_id = Column(Integer, ForeignKey('lesson.id'))

    lesson = relationship('Lesson', uselist=False, back_populates='test_lesson')
    test_lesson_question = relationship('TestLessonQuestion', back_populates='test_lesson')
    student_test_answer = relationship('StudentTestAnswer', back_populates='test_lesson')


class TestLessonQuestion(Base):
    __tablename__ = "test_lesson_question"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    question_number = Column(Integer, default=1, nullable=False)

    test_lesson_id = Column(Integer, ForeignKey('test_lesson.id'))

    test_lesson = relationship('TestLesson', back_populates='test_lesson_question')
    test_lesson_answer = relationship('TestLessonAnswer', back_populates='test_lesson_question')


class TestLessonAnswer(Base):
    __tablename__ = "test_lesson_answer"

    id = Column(Integer, primary_key=True, index=True)
    answer_text = Column(Text)
    is_correct = Column(Boolean)

    test_lesson_question_id = Column(Integer, ForeignKey('test_lesson_question.id'))

    test_lesson_question = relationship('TestLessonQuestion', back_populates='test_lesson_answer')


class StudentTestAnswer(Base):
    __tablename__ = "student_test_answer"

    id = Column(Integer, primary_key=True, index=True)
    number_attempt = Column(Integer, default=1, nullable=False)
    answer_text = Column(String)

    student_id = Column(Integer, ForeignKey('student.id'))
    test_lesson_id = Column(Integer, ForeignKey('test_lesson.id'))

    student = relationship('Student', back_populates='student_test_answer')
    test_lesson = relationship('TestLesson', back_populates='student_test_answer')
    student_test_answer_comment = relationship('StudentTestAnswerComment', back_populates='student_test_answer')


class StudentTestAnswerComment(Base):
    __tablename__ = "student_test_answer_comment"

    id = Column(Integer, primary_key=True, index=True)
    comment_text = Column(Text)

    teacher_id = Column(Integer, ForeignKey('teacher.id'))
    student_test_answer_id = Column(Integer, ForeignKey('student_test_answer.id'))

    teacher = relationship('Teacher', back_populates='student_test_answer_comment')
    student_test_answer = relationship('StudentTestAnswer', back_populates='student_test_answer_comment')


class HomeworkLesson(Base):
    __tablename__ = "homework_lesson"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    deadline = Column(DateTime)
    attachment_file = Column(String)
    attachment_filename = Column(String)

    lesson_id = Column(Integer, ForeignKey('lesson.id'))

    lesson = relationship('Lesson', uselist=False, back_populates='homework_lesson')
    student_homework_answer = relationship('StudentHomeworkAnswer', back_populates='homework_lesson')


class StudentHomeworkAnswer(Base):
    __tablename__ = "student_homework_answer"

    id = Column(Integer, primary_key=True, index=True)
    answer_text = Column(Text)
    answer_attachment_file = Column(String)
    answer_attachment_filename = Column(String)

    student_id = Column(Integer, ForeignKey('student.id'))
    homework_lesson_id = Column(Integer, ForeignKey('homework_lesson.id'))

    student = relationship('Student', back_populates='student_homework_answer')
    homework_lesson = relationship('HomeworkLesson', back_populates='student_homework_answer')
    student_homework_answer_comment = relationship(
        'StudentHomeworkAnswerComment',
        back_populates='student_homework_answer')


class StudentHomeworkAnswerComment(Base):
    __tablename__ = "student_homework_answer_comment"

    id = Column(Integer, primary_key=True, index=True)
    comment_text = Column(Text)

    teacher_id = Column(Integer, ForeignKey('teacher.id'))
    student_homework_answer_id = Column(Integer, ForeignKey('student_homework_answer.id'))

    teacher = relationship('Teacher', back_populates='student_homework_answer_comment')
    student_homework_answer = relationship(
        'StudentHomeworkAnswer',
        back_populates='student_homework_answer_comment')


class WebinarLesson(Base):
    __tablename__ = "webinar_lesson"

    id = Column(Integer, primary_key=True, index=True)
    link = Column(String, nullable=False)

    lesson_id = Column(Integer, ForeignKey('lesson.id'))

    lesson = relationship('Lesson', uselist=False, back_populates='webinar_lesson')


class GroupChatAttachFile(Base):
    __tablename__ = "group_chat_attach_file"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String)
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


class SubjectChat(Base):
    __tablename__ = "subject_chat"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)
    datetime_message = Column(DateTime, autoincrement=True)
    sender_id = Column(Integer)
    sender_type = Column(Enum(UserTypeOption), nullable=False)
    subject_id = Column(Integer, ForeignKey('subject.id'))

    subject = relationship('Subject', back_populates='subject_chat')
    subject_chat_answer = relationship('SubjectChatAnswer', back_populates='subject_chat')


class SubjectChatAnswer(Base):
    __tablename__ = "subject_chat_answer"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)
    datetime_message = Column(DateTime, autoincrement=True)
    subject_chat_id = Column(Integer, ForeignKey('subject_chat.id'))
    sender_id = Column(Integer)
    sender_type = Column(Enum(UserTypeOption), nullable=False)

    subject_chat = relationship('SubjectChat', back_populates='subject_chat_answer')
