"""auto-vote

Revision ID: 654e00c3845b
Revises: b85695b36791
Create Date: 2022-01-11 18:06:49.395041

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '654e00c3845b'
down_revision = 'b85695b36791'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('post_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['post_id'], ['posts.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(
                        ['user_id'], ['users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('user_id', 'post_id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    # ### end Alembic commands ###
