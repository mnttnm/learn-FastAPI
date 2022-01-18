"""add foreign key to posts

Revision ID: b85695b36791
Revises: 6880b5821432
Create Date: 2022-01-11 18:04:24.620310

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b85695b36791'
down_revision = '6880b5821432'
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key("post_users_fk", source_table="posts", referent_table="users", local_cols=[
                          "owner_id"], remote_cols=["id"], ondelete="CASCADE")


def downgrade():
    op.drop_constraint("post_users_fk", table_name="posts")
