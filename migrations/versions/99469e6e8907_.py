"""empty message

Revision ID: 99469e6e8907
Revises: 64ad39775433
Create Date: 2018-05-22 14:47:26.676138

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99469e6e8907'
down_revision = '64ad39775433'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('company', sa.Column('job_notify_email', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('company', 'job_notify_email')
    # ### end Alembic commands ###