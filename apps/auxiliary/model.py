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


class Transportation(ObjectToJson):
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


class Vaccination (ObjectToJson):
    """
        一条接种记录，包括医院、医生、时间。
    """
    def __init__(self, record_id, operate_date, doctor=None, recipient=None, vaccine=None):
        """
        :param doctor: 接种医生
        :param operate_date: 接种时间
        """
        self.record_id = record_id
        self.operate_date = operate_date.strftime("%Y-%m-%d %H:%M:%S")
        if doctor is not None:
            self.doctor_name = doctor.realname
            self.doctor_phone = doctor.phone
            self.hospital_name = doctor.hospital.organization_name
        if recipient is not None:
            self.recipient_name = recipient.realname
            self.recipient_idcard = recipient.id_number
            self.recipient_phone = recipient.phone
        if vaccine is not None:
            self.vaccine_name = vaccine.name


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


# 疫苗的接种记录
class Vac_record(db.Model, ObjectToJson):   # 疫苗的接种记录
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vaccine_id = db.Column(db.Integer, db.ForeignKey('vaccine.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('recipient.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('hospital_operator.id'))
    status = db.Column(db.Integer, default=0)  # 1-已经接种  0-未接种
    operate_date = db.Column(db.DATETIME)  # 接种时间

    def __init__(self, recipient_id, doctor_id):
        self.recipient_id = recipient_id
        self.doctor_id = doctor_id


# 一级追溯码和二级追溯码的对应表
class First_second_mapping(db.Model, ObjectToJson):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    second_trace_code = db.Column(db.String(33))
    # 对应的疫苗的编号
    vaccine_id = db.Column(db.Integer, db.ForeignKey('vaccine.id'))
    # 打包时间
    operate_date = db.Column(db.DATETIME, default=datetime.now)  # 接种时间


