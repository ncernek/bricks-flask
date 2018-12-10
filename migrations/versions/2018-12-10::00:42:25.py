"""empty message

Revision ID: 9f2725a01e4c
Revises: e7a39d0852d5
Create Date: 2018-12-10 00:42:25.439512

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9f2725a01e4c'
down_revision = 'e7a39d0852d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('exchange', sa.Column('next_router', sa.String(length=32), nullable=True))
    op.add_column('exchange', sa.Column('router', sa.String(length=32), nullable=False))
    op.drop_column('exchange', 'pre_actions')
    op.drop_column('exchange', 'inbound_format')
    op.drop_column('exchange', 'actions')
    op.drop_column('exchange', 'router_id')
    op.drop_column('exchange', 'next_router_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('exchange', sa.Column('next_router_id', sa.VARCHAR(length=32), autoincrement=False, nullable=True))
    op.add_column('exchange', sa.Column('router_id', sa.VARCHAR(length=32), autoincrement=False, nullable=False))
    op.add_column('exchange', sa.Column('actions', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True))
    op.add_column('exchange', sa.Column('inbound_format', sa.VARCHAR(length=32), autoincrement=False, nullable=False))
    op.add_column('exchange', sa.Column('pre_actions', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True))
    op.drop_column('exchange', 'router')
    op.drop_column('exchange', 'next_router')
    # ### end Alembic commands ###
