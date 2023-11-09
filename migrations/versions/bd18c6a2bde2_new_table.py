"""new table

Revision ID: bd18c6a2bde2
Revises: 8715dd6de798
Create Date: 2023-11-03 15:43:41.088020

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'bd18c6a2bde2'
down_revision = '8715dd6de798'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('labels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_default', sa.Boolean(), nullable=True),
    sa.Column('label_name', sa.String(), nullable=True),
    sa.Column('label_svg_path', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_labels_id'), 'labels', ['id'], unique=False)
    op.create_table('student_teacher_letter',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('date', sa.DateTime(), autoincrement=True, nullable=False),
    sa.Column('lesson_id', sa.Integer(), nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('recipient_id', sa.Integer(), nullable=True),
    sa.Column('parent_letter_id', sa.Integer(), nullable=True),
    sa.Column('viewed', sa.Boolean(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['lesson_id'], ['lesson.id'], ),
    sa.ForeignKeyConstraint(['parent_letter_id'], ['student_teacher_letter.id'], ),
    sa.ForeignKeyConstraint(['recipient_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_student_teacher_letter_id'), 'student_teacher_letter', ['id'], unique=False)
    op.create_table('subject_journal',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('absent', sa.Boolean(), nullable=True),
    sa.Column('subject_id', sa.Integer(), nullable=True),
    sa.Column('lesson_id', sa.Integer(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['lesson_id'], ['lesson.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.ForeignKeyConstraint(['subject_id'], ['subject.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subject_journal_id'), 'subject_journal', ['id'], unique=False)
    op.create_table('deleted_letter',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('letter_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['letter_id'], ['student_teacher_letter.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_deleted_letter_id'), 'deleted_letter', ['id'], unique=False)
    op.create_table('letter_labels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('letter_id', sa.Integer(), nullable=True),
    sa.Column('label_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['label_id'], ['labels.id'], ),
    sa.ForeignKeyConstraint(['letter_id'], ['student_teacher_letter.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_letter_labels_id'), 'letter_labels', ['id'], unique=False)
    op.create_table('student_lecture',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('check', sa.Boolean(), nullable=False),
    sa.Column('lecture_id', sa.Integer(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['lecture_id'], ['lecture.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_student_lecture_id'), 'student_lecture', ['id'], unique=False)
    op.drop_index('ix_lesson_score_id', table_name='lesson_score')
    op.drop_table('lesson_score')
    op.drop_index('ix_lesson_missing_id', table_name='lesson_missing')
    op.drop_table('lesson_missing')
    op.drop_index('ix_lecture_score_id', table_name='lecture_score')
    op.drop_table('lecture_score')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lecture_score',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('score', sa.INTEGER(), nullable=True),
    sa.Column('check', sa.BOOLEAN(), nullable=False),
    sa.Column('lecture_id', sa.INTEGER(), nullable=True),
    sa.Column('student_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['lecture_id'], ['lecture.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_lecture_score_id', 'lecture_score', ['id'], unique=False)
    op.create_table('lesson_missing',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('missing', sa.BOOLEAN(), nullable=True),
    sa.Column('student_id', sa.INTEGER(), nullable=True),
    sa.Column('lesson_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['lesson_id'], ['lesson.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_lesson_missing_id', 'lesson_missing', ['id'], unique=False)
    op.create_table('lesson_score',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('score', sa.INTEGER(), nullable=True),
    sa.Column('lesson_type', sa.VARCHAR(length=14), nullable=True),
    sa.Column('student_id', sa.INTEGER(), nullable=True),
    sa.Column('lesson_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['lesson_id'], ['lesson.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_lesson_score_id', 'lesson_score', ['id'], unique=False)
    op.drop_index(op.f('ix_student_lecture_id'), table_name='student_lecture')
    op.drop_table('student_lecture')
    op.drop_index(op.f('ix_letter_labels_id'), table_name='letter_labels')
    op.drop_table('letter_labels')
    op.drop_index(op.f('ix_deleted_letter_id'), table_name='deleted_letter')
    op.drop_table('deleted_letter')
    op.drop_index(op.f('ix_subject_journal_id'), table_name='subject_journal')
    op.drop_table('subject_journal')
    op.drop_index(op.f('ix_student_teacher_letter_id'), table_name='student_teacher_letter')
    op.drop_table('student_teacher_letter')
    op.drop_index(op.f('ix_labels_id'), table_name='labels')
    op.drop_table('labels')
    # ### end Alembic commands ###
