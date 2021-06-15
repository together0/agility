"""empty message

Revision ID: 04faaa76bba0
Revises: 
Create Date: 2021-06-15 15:19:28.936436

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04faaa76bba0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('first_second_mapping',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('second_trace_code', sa.String(length=33), nullable=True),
    sa.Column('vaccine_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['vaccine_id'], ['vaccine.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('first_second_mapping')
    # ### end Alembic commands ###
