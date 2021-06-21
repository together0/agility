# 中间表
from datetime import datetime

from ext import db


class ObjectToJson:
    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


class Record(ObjectToJson):
    """
        一条运输记录，包括仓库、运输工具、操作者，使用类对象初始化，然后转换为JSON格式。
    """
    def __init__(self, warehouse, vehicle, operator, in_out_date, status, record_id):
        """
        :param warehouse:
        :param vehicle:
        :param operator:
        :param in_out_date: 入库 / 出库的时间
        :param status: 该记录是出库记录还是入库记录，默认是入库
        """
        self.record_id = record_id
        self.warehouse = warehouse.to_json()
        self.warehouse_name = warehouse.name
        self.warehouse_id = warehouse.id
        self.vehicle_licence = vehicle.licence
        self.vehicle_id = vehicle.id
        self.operator_name = operator.realname
        self.operator_id = operator.id
        self.in_out_date = in_out_date.strftime("%Y-%m-%d %H:%M:%S")
        self.status = status


# 疫苗的入库和出库操作记录
class Move_record(db.Model, ObjectToJson):   # 疫苗的入库和出库记录
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


# 疫苗到达医院的记录表（疫苗到达医院的记录表）
class Hospital_record(db.Model, ObjectToJson):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vaccine_id = db.Column(db.Integer, db.ForeignKey('vaccine.id'))   # 疫苗的ID
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'))  # 医院的ID
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))   # 运输车辆ID
    operator_id = db.Column(db.Integer, db.ForeignKey('hospital_manager.id'))  # 操作者ID (医院的管理者)
    in_date = db.Column(db.DATETIME, default=datetime.now)  # 到达医院的时间

    def __init__(self, vaccine_id, hospital_id, vehicle_id, operator_id):
        self.vaccine_id = vaccine_id
        self.hospital_id = hospital_id
        self.vehicle_id = vehicle_id
        self.operator_id = operator_id


# 疫苗的接种记录
class Vac_record(db.Model, ObjectToJson):   # 疫苗的接种记录
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vaccine_id = db.Column(db.Integer, db.ForeignKey('vaccine.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('recipient.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('hospital_operator.id'))
    operate_date = db.Column(db.DATETIME, default=datetime.now)  # 接种时间


# 一级追溯码和二级追溯码的对应表
class First_second_mapping(db.Model, ObjectToJson):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    second_trace_code = db.Column(db.String(33))
    # 对应的疫苗的编号
    vaccine_id = db.Column(db.Integer, db.ForeignKey('vaccine.id'))
    # 打包时间
    operate_date = db.Column(db.DATETIME, default=datetime.now)  # 接种时间


