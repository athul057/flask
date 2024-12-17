"""Make store_id nullable

Revision ID: b3a9950b46d0
Revises: 
Create Date: 2024-12-14 08:41:38.527085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3a9950b46d0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tags', schema=None) as batch_op:
        batch_op.alter_column('store_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tags', schema=None) as batch_op:
        batch_op.alter_column('store_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
