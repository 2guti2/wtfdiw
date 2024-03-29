"""empty message

Revision ID: e3fa50d4ee07
Revises: b95723a62542
Create Date: 2020-04-09 23:01:59.966795

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3fa50d4ee07'
down_revision = 'b95723a62542'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'surname')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('surname', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
