"""Added tables

Revision ID: 064140955be6
Revises: 
Create Date: 2023-06-09 16:32:17.988600

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '064140955be6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('course',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course_number', sa.Integer(), nullable=False),
    sa.Column('semester_number', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_course_id'), 'course', ['id'], unique=False)
    op.create_table('lesson_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Enum('ordinary', 'homework', 'test', 'webinar', 'module_test', name='lessontypeoption'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lesson_type_id'), 'lesson_type', ['id'], unique=False)
    op.create_table('session',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('session_date', sa.Date(), nullable=True),
    sa.Column('passed', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_session_id'), 'session', ['id'], unique=False)
    op.create_table('user_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Enum('student', 'moder', 'teacher', 'curator', name='usertypeoption'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_type_id'), 'user_type', ['id'], unique=False)
    op.create_table('specialization',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_specialization_id'), 'specialization', ['id'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=25), nullable=False),
    sa.Column('hashed_pass', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('token', sa.String(), nullable=True),
    sa.Column('exp_token', sa.DateTime(), nullable=True),
    sa.Column('user_type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_type_id'], ['user_type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('curator',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('surname', sa.String(length=64), nullable=False),
    sa.Column('lastname', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_curator_id'), 'curator', ['id'], unique=False)
    op.create_table('moder',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('surname', sa.String(length=64), nullable=True),
    sa.Column('lastname', sa.String(length=64), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_moder_id'), 'moder', ['id'], unique=False)
    op.create_table('subject',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('image_path', sa.String(), nullable=True),
    sa.Column('logo_path', sa.String(), nullable=True),
    sa.Column('is_published', sa.Boolean(), nullable=True),
    sa.Column('quantity_lecture', sa.Integer(), nullable=True),
    sa.Column('quantity_seminar', sa.Integer(), nullable=True),
    sa.Column('quantity_test', sa.Integer(), nullable=True),
    sa.Column('quantity_webinar', sa.Integer(), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('specialization_id', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['specialization_id'], ['specialization.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subject_id'), 'subject', ['id'], unique=False)
    op.create_table('teacher',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('surname', sa.String(length=64), nullable=False),
    sa.Column('lastname', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_teacher_id'), 'teacher', ['id'], unique=False)
    op.create_table('group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group_name', sa.String(), nullable=False),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.Column('curator_id', sa.Integer(), nullable=True),
    sa.Column('specialization_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['curator_id'], ['curator.id'], ),
    sa.ForeignKeyConstraint(['specialization_id'], ['specialization.id'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_group_id'), 'group', ['id'], unique=False)
    op.create_table('module',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('subject_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['subject_id'], ['subject.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_module_id'), 'module', ['id'], unique=False)
    op.create_table('subject_chat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject_id', sa.Integer(), nullable=True),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('datetime_message', sa.DateTime(), autoincrement=True, nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('sender_type', sa.Enum('student', 'moder', 'teacher', 'curator', name='usertypeoption'), nullable=False),
    sa.ForeignKeyConstraint(['subject_id'], ['subject.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subject_chat_id'), 'subject_chat', ['id'], unique=False)
    op.create_table('subject_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject_id', sa.Integer(), nullable=True),
    sa.Column('header', sa.String(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['subject_id'], ['subject.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subject_info_id'), 'subject_info', ['id'], unique=False)
    op.create_table('subject_instruction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject_id', sa.Integer(), nullable=True),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('header', sa.String(), nullable=False),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['subject_id'], ['subject.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subject_instruction_id'), 'subject_instruction', ['id'], unique=False)
    op.create_table('subject_teacher_association',
    sa.Column('subject_id', sa.Integer(), nullable=False),
    sa.Column('teacher_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['subject_id'], ['subject.id'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], ),
    sa.PrimaryKeyConstraint('subject_id', 'teacher_id')
    )
    op.create_table('group_chat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('datetime_message', sa.DateTime(), autoincrement=True, nullable=True),
    sa.Column('fixed', sa.Boolean(), nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('sender_type', sa.Enum('student', 'moder', 'teacher', 'curator', name='usertypeoption'), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_group_chat_id'), 'group_chat', ['id'], unique=False)
    op.create_table('lesson',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('is_published', sa.Boolean(), nullable=True),
    sa.Column('lesson_date', sa.DateTime(), nullable=True),
    sa.Column('lesson_type_id', sa.Integer(), nullable=True),
    sa.Column('module_id', sa.Integer(), nullable=True),
    sa.Column('subject_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['lesson_type_id'], ['lesson_type.id'], ),
    sa.ForeignKeyConstraint(['module_id'], ['module.id'], ),
    sa.ForeignKeyConstraint(['subject_id'], ['subject.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lesson_id'), 'lesson', ['id'], unique=False)
    op.create_table('student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('surname', sa.String(length=64), nullable=False),
    sa.Column('lastname', sa.String(length=64), nullable=False),
    sa.Column('phone', sa.String(length=15), nullable=False),
    sa.Column('email', sa.String(length=40), nullable=False),
    sa.Column('image_path', sa.String(), nullable=True),
    sa.Column('qualification', sa.String(), nullable=True),
    sa.Column('educational_program', sa.String(), nullable=True),
    sa.Column('subject_area', sa.String(), nullable=True),
    sa.Column('group_leader', sa.Boolean(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('specialization_id', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.ForeignKeyConstraint(['specialization_id'], ['specialization.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_student_id'), 'student', ['id'], unique=False)
    op.create_table('subject_chat_answer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('datetime_message', sa.DateTime(), autoincrement=True, nullable=True),
    sa.Column('subject_chat_id', sa.Integer(), nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('sender_type', sa.Enum('student', 'moder', 'teacher', 'curator', name='usertypeoption'), nullable=False),
    sa.ForeignKeyConstraint(['subject_chat_id'], ['subject_chat.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subject_chat_answer_id'), 'subject_chat_answer', ['id'], unique=False)
    op.create_table('subject_info_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject_info_id', sa.Integer(), nullable=True),
    sa.Column('icon', sa.String(), nullable=True),
    sa.Column('icon_text', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['subject_info_id'], ['subject_info.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subject_info_item_id'), 'subject_info_item', ['id'], unique=False)
    op.create_table('subject_instruction_files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subject_instruction_id', sa.Integer(), nullable=True),
    sa.Column('file', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['subject_instruction_id'], ['subject_instruction.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subject_instruction_files_id'), 'subject_instruction_files', ['id'], unique=False)
    op.create_table('group_chat_answer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('datetime_message', sa.DateTime(), autoincrement=True, nullable=True),
    sa.Column('group_chat_id', sa.Integer(), nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('sender_type', sa.Enum('student', 'moder', 'teacher', 'curator', name='usertypeoption'), nullable=False),
    sa.ForeignKeyConstraint(['group_chat_id'], ['group_chat.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_group_chat_answer_id'), 'group_chat_answer', ['id'], unique=False)
    op.create_table('homework_lesson',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('deadline', sa.DateTime(), nullable=True),
    sa.Column('attachment_file', sa.String(), nullable=True),
    sa.Column('attachment_filename', sa.String(), nullable=True),
    sa.Column('lesson_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['lesson_id'], ['lesson.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_homework_lesson_id'), 'homework_lesson', ['id'], unique=False)
    op.create_table('lesson_missing',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('missing', sa.Boolean(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('lesson_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['lesson_id'], ['lesson.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lesson_missing_id'), 'lesson_missing', ['id'], unique=False)
    op.create_table('lesson_score',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('lesson_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['lesson_id'], ['lesson.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lesson_score_id'), 'lesson_score', ['id'], unique=False)
    op.create_table('ordinary_lesson',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('lesson_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['lesson_id'], ['lesson.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ordinary_lesson_id'), 'ordinary_lesson', ['id'], unique=False)
    op.create_table('test_lesson',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timer', sa.Time(), nullable=True),
    sa.Column('attempts', sa.Integer(), nullable=False),
    sa.Column('lesson_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['lesson_id'], ['lesson.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_test_lesson_id'), 'test_lesson', ['id'], unique=False)
    op.create_table('webinar_lesson',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('link', sa.String(), nullable=False),
    sa.Column('lesson_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['lesson_id'], ['lesson.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_webinar_lesson_id'), 'webinar_lesson', ['id'], unique=False)
    op.create_table('ordinary_lesson_attribute',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('attribute_name', sa.String(), nullable=True),
    sa.Column('ordinary_lesson_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ordinary_lesson_id'], ['ordinary_lesson.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ordinary_lesson_attribute_id'), 'ordinary_lesson_attribute', ['id'], unique=False)
    op.create_table('student_homework_answer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('answer_text', sa.Text(), nullable=True),
    sa.Column('answer_attachment_file', sa.String(), nullable=True),
    sa.Column('answer_attachment_filename', sa.String(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('homework_lesson_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['homework_lesson_id'], ['homework_lesson.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_student_homework_answer_id'), 'student_homework_answer', ['id'], unique=False)
    op.create_table('student_test_answer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number_attempt', sa.Integer(), nullable=False),
    sa.Column('answer_text', sa.String(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('test_lesson_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.ForeignKeyConstraint(['test_lesson_id'], ['test_lesson.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_student_test_answer_id'), 'student_test_answer', ['id'], unique=False)
    op.create_table('test_lesson_question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_text', sa.Text(), nullable=False),
    sa.Column('question_number', sa.Integer(), nullable=False),
    sa.Column('test_lesson_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['test_lesson_id'], ['test_lesson.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_test_lesson_question_id'), 'test_lesson_question', ['id'], unique=False)
    op.create_table('ordinary_lesson_value',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.Text(), nullable=True),
    sa.Column('ordinary_lesson_id', sa.Integer(), nullable=True),
    sa.Column('ordinary_lesson_attribute_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ordinary_lesson_attribute_id'], ['ordinary_lesson_attribute.id'], ),
    sa.ForeignKeyConstraint(['ordinary_lesson_id'], ['ordinary_lesson.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ordinary_lesson_value_id'), 'ordinary_lesson_value', ['id'], unique=False)
    op.create_table('student_homework_answer_comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comment_text', sa.Text(), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.Column('student_homework_answer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['student_homework_answer_id'], ['student_homework_answer.id'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_student_homework_answer_comment_id'), 'student_homework_answer_comment', ['id'], unique=False)
    op.create_table('student_test_answer_comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comment_text', sa.Text(), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.Column('student_test_answer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['student_test_answer_id'], ['student_test_answer.id'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_student_test_answer_comment_id'), 'student_test_answer_comment', ['id'], unique=False)
    op.create_table('test_lesson_answer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('answer_text', sa.Text(), nullable=True),
    sa.Column('is_correct', sa.Boolean(), nullable=True),
    sa.Column('test_lesson_question_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['test_lesson_question_id'], ['test_lesson_question.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_test_lesson_answer_id'), 'test_lesson_answer', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_test_lesson_answer_id'), table_name='test_lesson_answer')
    op.drop_table('test_lesson_answer')
    op.drop_index(op.f('ix_student_test_answer_comment_id'), table_name='student_test_answer_comment')
    op.drop_table('student_test_answer_comment')
    op.drop_index(op.f('ix_student_homework_answer_comment_id'), table_name='student_homework_answer_comment')
    op.drop_table('student_homework_answer_comment')
    op.drop_index(op.f('ix_ordinary_lesson_value_id'), table_name='ordinary_lesson_value')
    op.drop_table('ordinary_lesson_value')
    op.drop_index(op.f('ix_test_lesson_question_id'), table_name='test_lesson_question')
    op.drop_table('test_lesson_question')
    op.drop_index(op.f('ix_student_test_answer_id'), table_name='student_test_answer')
    op.drop_table('student_test_answer')
    op.drop_index(op.f('ix_student_homework_answer_id'), table_name='student_homework_answer')
    op.drop_table('student_homework_answer')
    op.drop_index(op.f('ix_ordinary_lesson_attribute_id'), table_name='ordinary_lesson_attribute')
    op.drop_table('ordinary_lesson_attribute')
    op.drop_index(op.f('ix_webinar_lesson_id'), table_name='webinar_lesson')
    op.drop_table('webinar_lesson')
    op.drop_index(op.f('ix_test_lesson_id'), table_name='test_lesson')
    op.drop_table('test_lesson')
    op.drop_index(op.f('ix_ordinary_lesson_id'), table_name='ordinary_lesson')
    op.drop_table('ordinary_lesson')
    op.drop_index(op.f('ix_lesson_score_id'), table_name='lesson_score')
    op.drop_table('lesson_score')
    op.drop_index(op.f('ix_lesson_missing_id'), table_name='lesson_missing')
    op.drop_table('lesson_missing')
    op.drop_index(op.f('ix_homework_lesson_id'), table_name='homework_lesson')
    op.drop_table('homework_lesson')
    op.drop_index(op.f('ix_group_chat_answer_id'), table_name='group_chat_answer')
    op.drop_table('group_chat_answer')
    op.drop_index(op.f('ix_subject_instruction_files_id'), table_name='subject_instruction_files')
    op.drop_table('subject_instruction_files')
    op.drop_index(op.f('ix_subject_info_item_id'), table_name='subject_info_item')
    op.drop_table('subject_info_item')
    op.drop_index(op.f('ix_subject_chat_answer_id'), table_name='subject_chat_answer')
    op.drop_table('subject_chat_answer')
    op.drop_index(op.f('ix_student_id'), table_name='student')
    op.drop_table('student')
    op.drop_index(op.f('ix_lesson_id'), table_name='lesson')
    op.drop_table('lesson')
    op.drop_index(op.f('ix_group_chat_id'), table_name='group_chat')
    op.drop_table('group_chat')
    op.drop_table('subject_teacher_association')
    op.drop_index(op.f('ix_subject_instruction_id'), table_name='subject_instruction')
    op.drop_table('subject_instruction')
    op.drop_index(op.f('ix_subject_info_id'), table_name='subject_info')
    op.drop_table('subject_info')
    op.drop_index(op.f('ix_subject_chat_id'), table_name='subject_chat')
    op.drop_table('subject_chat')
    op.drop_index(op.f('ix_module_id'), table_name='module')
    op.drop_table('module')
    op.drop_index(op.f('ix_group_id'), table_name='group')
    op.drop_table('group')
    op.drop_index(op.f('ix_teacher_id'), table_name='teacher')
    op.drop_table('teacher')
    op.drop_index(op.f('ix_subject_id'), table_name='subject')
    op.drop_table('subject')
    op.drop_index(op.f('ix_moder_id'), table_name='moder')
    op.drop_table('moder')
    op.drop_index(op.f('ix_curator_id'), table_name='curator')
    op.drop_table('curator')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_specialization_id'), table_name='specialization')
    op.drop_table('specialization')
    op.drop_index(op.f('ix_user_type_id'), table_name='user_type')
    op.drop_table('user_type')
    op.drop_index(op.f('ix_session_id'), table_name='session')
    op.drop_table('session')
    op.drop_index(op.f('ix_lesson_type_id'), table_name='lesson_type')
    op.drop_table('lesson_type')
    op.drop_index(op.f('ix_course_id'), table_name='course')
    op.drop_table('course')
    # ### end Alembic commands ###