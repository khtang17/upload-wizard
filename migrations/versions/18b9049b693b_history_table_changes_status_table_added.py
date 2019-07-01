"""history table changes, status table added

Revision ID: 18b9049b693b
Revises: 1bc5ad2fb7b0
Create Date: 2019-07-01 13:41:24.420652

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18b9049b693b'
down_revision = '1bc5ad2fb7b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('status',
    sa.Column('status_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('status', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('status_id')
    )
    op.add_column('history', sa.Column('availability', sa.String(length=50), nullable=True))
    op.add_column('history', sa.Column('catalog_type', sa.String(length=50), nullable=True))
    op.add_column('history', sa.Column('last_updated', sa.DateTime(), nullable=True))
    op.add_column('history', sa.Column('status_id', sa.Integer(), nullable=True))
    op.add_column('history', sa.Column('upload_type', sa.String(length=50), nullable=True))
    op.create_index(op.f('ix_history_last_updated'), 'history', ['last_updated'], unique=False)
    op.drop_index('ix_history_status', table_name='history')
    op.create_foreign_key(None, 'history', 'status', ['status_id'], ['status_id'])
    op.drop_column('history', 'type')
    op.drop_column('history', 'purchasability')
    op.drop_column('history', 'status')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('history', sa.Column('status', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('history', sa.Column('purchasability', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.add_column('history', sa.Column('type', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'history', type_='foreignkey')
    op.create_index('ix_history_status', 'history', ['status'], unique=False)
    op.drop_index(op.f('ix_history_last_updated'), table_name='history')
    op.drop_column('history', 'upload_type')
    op.drop_column('history', 'status_id')
    op.drop_column('history', 'last_updated')
    op.drop_column('history', 'catalog_type')
    op.drop_column('history', 'availability')
    op.drop_table('status')
    # ### end Alembic commands ###
