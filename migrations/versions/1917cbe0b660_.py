"""empty message

Revision ID: 1917cbe0b660
Revises: 
Create Date: 2021-06-18 14:26:21.461993

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1917cbe0b660'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hospital',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('organization_name', sa.String(length=80), nullable=False),
    sa.Column('realname', sa.String(length=40), nullable=False),
    sa.Column('phone', sa.String(length=11), nullable=False),
    sa.Column('province', sa.String(length=20), nullable=False),
    sa.Column('city', sa.String(length=20), nullable=False),
    sa.Column('country', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('logistics',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('organization_name', sa.String(length=80), nullable=False),
    sa.Column('realname', sa.String(length=40), nullable=False),
    sa.Column('phone', sa.String(length=11), nullable=False),
    sa.Column('province', sa.String(length=20), nullable=False),
    sa.Column('city', sa.String(length=20), nullable=False),
    sa.Column('country', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('producer',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('organization_name', sa.String(length=80), nullable=False),
    sa.Column('realname', sa.String(length=40), nullable=False),
    sa.Column('phone', sa.String(length=11), nullable=False),
    sa.Column('province', sa.String(length=20), nullable=False),
    sa.Column('city', sa.String(length=20), nullable=False),
    sa.Column('country', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recipient',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('password', sa.String(length=64), nullable=False),
    sa.Column('realname', sa.String(length=20), nullable=False),
    sa.Column('id_number', sa.String(length=18), nullable=False),
    sa.Column('phone', sa.String(length=11), nullable=False),
    sa.Column('register_date', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('supervisor',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('password', sa.String(length=64), nullable=False),
    sa.Column('realname', sa.String(length=20), nullable=False),
    sa.Column('id_number', sa.String(length=18), nullable=False),
    sa.Column('phone', sa.String(length=11), nullable=False),
    sa.Column('register_date', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('hospital_manager',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('password', sa.String(length=64), nullable=False),
    sa.Column('realname', sa.String(length=20), nullable=False),
    sa.Column('id_number', sa.String(length=18), nullable=False),
    sa.Column('phone', sa.String(length=11), nullable=False),
    sa.Column('register_date', sa.DATETIME(), nullable=True),
    sa.Column('hospital_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['hospital_id'], ['hospital.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('hospital_operator',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('password', sa.String(length=64), nullable=False),
    sa.Column('realname', sa.String(length=20), nullable=False),
    sa.Column('id_number', sa.String(length=18), nullable=False),
    sa.Column('phone', sa.String(length=11), nullable=False),
    sa.Column('register_date', sa.DATETIME(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('hospital_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['hospital_id'], ['hospital.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('move_manager',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('password', sa.String(length=64), nullable=False),
    sa.Column('realname', sa.String(length=20), nullable=False),
    sa.Column('id_number', sa.String(length=18), nullable=False),
    sa.Column('phone', sa.String(length=11), nullable=False),
    sa.Column('register_date', sa.DATETIME(), nullable=True),
    sa.Column('logistics_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['logistics_id'], ['logistics.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('vaccine',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_trace_code', sa.String(length=32), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=False),
    sa.Column('kind_name', sa.String(length=40), nullable=True),
    sa.Column('dose', sa.Float(), nullable=True),
    sa.Column('person_num', sa.Integer(), nullable=True),
    sa.Column('produce_date', sa.DATETIME(), nullable=True),
    sa.Column('complete_num', sa.Integer(), nullable=True),
    sa.Column('producer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['producer_id'], ['producer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vehicle',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('licence', sa.String(length=10), nullable=False),
    sa.Column('driver_name', sa.String(length=20), nullable=False),
    sa.Column('driver_phone', sa.String(length=11), nullable=False),
    sa.Column('logistics_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['logistics_id'], ['logistics.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('warehouse',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('province', sa.String(length=20), nullable=False),
    sa.Column('city', sa.String(length=20), nullable=False),
    sa.Column('country', sa.String(length=20), nullable=True),
    sa.Column('logistics_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['logistics_id'], ['logistics.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('first_second_mapping',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('second_trace_code', sa.String(length=33), nullable=True),
    sa.Column('vaccine_id', sa.Integer(), nullable=True),
    sa.Column('operate_date', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['vaccine_id'], ['vaccine.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('move_operator',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('password', sa.String(length=64), nullable=False),
    sa.Column('realname', sa.String(length=20), nullable=False),
    sa.Column('id_number', sa.String(length=18), nullable=False),
    sa.Column('phone', sa.String(length=11), nullable=False),
    sa.Column('register_date', sa.DATETIME(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('warehouse_id', sa.Integer(), nullable=False),
    sa.Column('logistics_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['logistics_id'], ['logistics.id'], ),
    sa.ForeignKeyConstraint(['warehouse_id'], ['warehouse.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('vac_record',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('vaccine_id', sa.Integer(), nullable=True),
    sa.Column('recipient_id', sa.Integer(), nullable=True),
    sa.Column('doctor_id', sa.Integer(), nullable=True),
    sa.Column('operate_date', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['doctor_id'], ['hospital_operator.id'], ),
    sa.ForeignKeyConstraint(['recipient_id'], ['recipient.id'], ),
    sa.ForeignKeyConstraint(['vaccine_id'], ['vaccine.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('move_record',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('vaccine_id', sa.Integer(), nullable=True),
    sa.Column('warehouse_id', sa.Integer(), nullable=True),
    sa.Column('vehicle_id', sa.Integer(), nullable=True),
    sa.Column('operator_id', sa.Integer(), nullable=True),
    sa.Column('in_date', sa.DATETIME(), nullable=True),
    sa.Column('out_date', sa.DATETIME(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['operator_id'], ['move_operator.id'], ),
    sa.ForeignKeyConstraint(['vaccine_id'], ['vaccine.id'], ),
    sa.ForeignKeyConstraint(['vehicle_id'], ['vehicle.id'], ),
    sa.ForeignKeyConstraint(['warehouse_id'], ['warehouse.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('move_record')
    op.drop_table('vac_record')
    op.drop_table('move_operator')
    op.drop_table('first_second_mapping')
    op.drop_table('warehouse')
    op.drop_table('vehicle')
    op.drop_table('vaccine')
    op.drop_table('move_manager')
    op.drop_table('hospital_operator')
    op.drop_table('hospital_manager')
    op.drop_table('supervisor')
    op.drop_table('recipient')
    op.drop_table('producer')
    op.drop_table('logistics')
    op.drop_table('hospital')
    # ### end Alembic commands ###