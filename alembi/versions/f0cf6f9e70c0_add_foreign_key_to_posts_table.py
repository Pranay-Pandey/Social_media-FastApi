"""add foreign key to posts table

Revision ID: f0cf6f9e70c0
Revises: cfdd7b9f348d
Create Date: 2022-10-08 21:27:09.338046

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0cf6f9e70c0'
down_revision = 'cfdd7b9f348d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer() , nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table="users", 
    local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
