"""add content column to posts table

Revision ID: df6d1f3de14e
Revises: daf74722f5ef
Create Date: 2022-10-08 21:15:00.831481

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df6d1f3de14e'
down_revision = 'daf74722f5ef'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
