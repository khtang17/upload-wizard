"""drop natural product column

Revision ID: 3cc9f19b5091
Revises: 191b3c6acece
Create Date: 2019-07-24 10:22:51.624462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3cc9f19b5091'
down_revision = '191b3c6acece'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('history', 'natural_products')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('history', sa.Column('natural_products', sa.BOOLEAN(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
