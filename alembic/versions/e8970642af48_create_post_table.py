"""create post table

Revision ID: e8970642af48
Revises:
Create Date: 2022-01-11 17:11:10.628712

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import null


# revision identifiers, used by Alembic.
revision = 'e8970642af48'
down_revision = None
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
    op.create_table("posts",
                    sa.Column("id", sa.Integer, primary_key=True,
                              nullable=False),
                    sa.Column("title", sa.String, nullable=False),
                    sa.Column("content", sa.String, nullable=False))


def downgrade():
    op.drop_table("posts")
