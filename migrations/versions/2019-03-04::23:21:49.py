"""empty message

Revision ID: 6a094410c180
Revises: 416d16ed6116
Create Date: 2019-03-04 23:21:49.898251

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a094410c180'
down_revision = '416d16ed6116'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('app_user', sa.Column('firebase_token', sa.String(length=256), nullable=True))
    op.create_unique_constraint(None, 'app_user', ['firebase_token'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'app_user', type_='unique')
    op.drop_column('app_user', 'firebase_token')
    # ### end Alembic commands ###
