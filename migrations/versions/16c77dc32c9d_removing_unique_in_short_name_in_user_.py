"""removing unique in short_name in user table

Revision ID: 16c77dc32c9d
Revises: d2c4dfe71fb8
Create Date: 2019-08-13 11:21:52.921803

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16c77dc32c9d'
down_revision = 'd2c4dfe71fb8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_short_name', table_name='user')
    op.create_index(op.f('ix_user_short_name'), 'user', ['short_name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_short_name'), table_name='user')
    op.create_index('ix_user_short_name', 'user', ['short_name'], unique=True)
    # ### end Alembic commands ###
