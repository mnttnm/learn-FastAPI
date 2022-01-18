"""add users table

Revision ID: 37bc042d7b58
Revises: 157a83659abd
Create Date: 2022-01-11 17:36:33.551676

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37bc042d7b58'
down_revision = '157a83659abd'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users",
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),  # way to add primary key
                    sa.UniqueConstraint('email')
                    ),


def downgrade():
    op.drop_table("users")
