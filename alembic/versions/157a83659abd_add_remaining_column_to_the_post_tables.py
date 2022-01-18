"""add remaining column to the post tables

Revision ID: 157a83659abd
Revises: e8970642af48
Create Date: 2022-01-11 17:30:38.843451

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.schema import ForeignKey


# revision identifiers, used by Alembic.
revision = '157a83659abd'
down_revision = 'e8970642af48'
branch_labels = None
depends_on = None

# class Post(Base):
# __tablename__ = "posts"

# id = Column(Integer, primary_key=True, nullable=False)
# title = Column(String, nullable=False)
# content = Column(String, nullable=False)
# published = Column(Boolean, server_default='True', nullable=False)
# created_at = Column(TIMESTAMP(timezone=True),
#                     nullable=False, server_default=text('now()'))
# owner_id = Column(Integer, ForeignKey(
#     "users.id", ondelete="CASCADE"), nullable=False)

# # sqlalchemy will return the User from the related table based on the
# # relationship that we have defined already.
# owner = relationship("User")


def upgrade():
    op.add_column("posts", sa.Column("published", sa.Boolean(),
                  server_default='True', nullable=False))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                  server_default=text('now()'), nullable=False))
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))


def downgrade():
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    op.drop_column("posts", "created_at")
    op.drop_column("posts", "published")
