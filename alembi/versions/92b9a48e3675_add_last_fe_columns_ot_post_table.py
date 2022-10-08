"""add last fe columns ot post table

Revision ID: 92b9a48e3675
Revises: f0cf6f9e70c0
Create Date: 2022-10-08 21:31:07.614060

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92b9a48e3675'
down_revision = 'f0cf6f9e70c0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', 
                sa.Column('published', sa.Boolean(), nullable=False , server_default= 'TRUE'),
                )
    op.add_column('posts',
                sa.Column('created_at' , sa.TIMESTAMP(timezone=True) , nullable=False,server_default=sa.text('now()'))
                )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')

    pass
