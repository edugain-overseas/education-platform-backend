"""fixed shuffle_answer field

Revision ID: e4d005c46dcf
Revises: 8bd948f46c16
Create Date: 2023-10-12 12:07:28.495963

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'e4d005c46dcf'
down_revision = '8bd948f46c16'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test_lesson', sa.Column('shuffle_answer', sa.Boolean(), nullable=True))
    op.drop_column('test_lesson', 'shufle_answer')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test_lesson', sa.Column('shufle_answer', sa.BOOLEAN(), nullable=True))
    op.drop_column('test_lesson', 'shuffle_answer')
    # ### end Alembic commands ###
