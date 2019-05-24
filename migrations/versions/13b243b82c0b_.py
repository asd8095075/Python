"""empty message

Revision ID: 13b243b82c0b
Revises: 6a54be5d8a29
Create Date: 2019-05-21 13:39:20.854311

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13b243b82c0b'
down_revision = '6a54be5d8a29'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('phone', sa.String(length=30), nullable=True))
    op.add_column('user', sa.Column('username', sa.String(length=20), nullable=True))
    op.create_unique_constraint(None, 'user', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'username')
    op.drop_column('user', 'phone')
    # ### end Alembic commands ###