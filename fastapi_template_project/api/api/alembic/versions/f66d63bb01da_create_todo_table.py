"""Create 'todo' table

Revision ID: f66d63bb01da
Revises: 
Create Date: 2022-06-09 22:21:17.096266

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f66d63bb01da'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('todo',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('todo')
