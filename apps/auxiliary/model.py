# 中间表
from datetime import datetime

from ext import db


# 疫苗的入库和出库操作
class Move_record(db.Model):   # 疫苗的入库和出库记录
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vaccine_id = db.Column(db.Integer, db.ForeignKey('vaccine.id'))
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    operator_id = db.Column(db.Integer, db.ForeignKey('move_operator.id'))
    in_out_date = db.Column(db.DATETIME, default=datetime.now)  # 入库或者出库时间
    status = db.Column(db.Integer, default=0)  # 0:入库  1:出库。

    def __init__(self, vaccine_id, warehouse_id, vehicle_id, operator_id, status=0):
        self.vaccine_id = vaccine_id
        self.warehouse_id = warehouse_id
        self.vehicle_id = vehicle_id
        self.operator_id = operator_id
        self.status = status

    def __str__(self):
        return "vaccine_id:{},warehouse_id:{},vehicle_id:{},operator_id:{},status:{}".format(
            self.vaccine_id,
            self.warehouse_id,
            self.vehicle_id,
            self.operator_id,
            self.status
        )


# 疫苗的接种记录
class Vac_record(db.Model):   # 疫苗的接种记录
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vaccine_id = db.Column(db.Integer, db.ForeignKey('vaccine.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('recipient.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('hospital_operator.id'))
    operate_date = db.Column(db.DATETIME, default=datetime.now)  # 接种时间


# 一级追溯码和二级追溯码的对应表
class First_second_mapping(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    second_trace_code = db.Column(db.String(33))
    # 对应的疫苗的编号
    vaccine_id = db.Column(db.Integer, db.ForeignKey('vaccine.id'))
    # 打包时间
    operate_date = db.Column(db.DATETIME, default=datetime.now)  # 接种时间


