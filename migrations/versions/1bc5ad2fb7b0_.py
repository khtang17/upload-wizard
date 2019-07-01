"""empty message

Revision ID: 1bc5ad2fb7b0
Revises: 0f8b50870ab3
Create Date: 2018-07-19 14:37:47.385559

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1bc5ad2fb7b0'
down_revision = '0f8b50870ab3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('field', sa.Column('order', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'field', ['order'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'field', type_='unique')
    op.drop_column('field', 'order')
    # ### end Alembic commands ###
