"""Set up users table

Revision ID: cfdd7b9f348d
Revises: df6d1f3de14e
Create Date: 2022-10-08 21:20:36.408104

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfdd7b9f348d'
down_revision = 'df6d1f3de14e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', 
                sa.Column('id', sa.Integer() , nullable = False),
                sa.Column('email',sa.String , nullable = False),
                sa.Column('password', sa.String, nullable=False ),
                sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
                sa.PrimaryKeyConstraint('id'),
                sa.UniqueConstraint('email')                     
                )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
