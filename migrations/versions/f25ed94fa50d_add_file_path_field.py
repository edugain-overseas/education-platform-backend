"""Add file_path field

Revision ID: f25ed94fa50d
Revises: a4cdd988d399
Create Date: 2023-06-30 16:03:11.731709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f25ed94fa50d'
down_revision = 'a4cdd988d399'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('group_chat_attach_file', sa.Column('file_path', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('group_chat_attach_file', 'file_path')
    # ### end Alembic commands ###