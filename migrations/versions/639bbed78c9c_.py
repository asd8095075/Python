"""empty message

Revision ID: 639bbed78c9c
Revises: 784360979bbf
Create Date: 2019-05-18 11:14:26.068661

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '639bbed78c9c'
down_revision = '784360979bbf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('passwd', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
