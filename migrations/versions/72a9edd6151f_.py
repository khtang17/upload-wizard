"""empty message

Revision ID: 72a9edd6151f
Revises: 0582129ead26
Create Date: 2018-05-30 11:31:06.113925

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '72a9edd6151f'
down_revision = '0582129ead26'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('field_allowed_value', 'allowed_values',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('field_decimal', 'decimal_places',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('field_decimal', 'max_val',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.alter_column('field_decimal', 'min_val',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('field_decimal', 'min_val',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('field_decimal', 'max_val',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.alter_column('field_decimal', 'decimal_places',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('field_allowed_value', 'allowed_values',
               existing_type=sa.TEXT(),
               nullable=True)
    # ### end Alembic commands ###