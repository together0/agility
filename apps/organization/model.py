from datetime import datetime

from ext import db


class ObjectToJson:
    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


class Producer(db.Model, ObjectToJson):     # 生产机构
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organization_name = db.Column(db.String(80), nullable=False)
    realname = db.Column(db.String(40), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    province = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(20), nullable=False)


class Logistics(db.Model, ObjectToJson):   # 物流公司
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organization_name = db.Column(db.String(80), nullable=False, unique=True)
    realname = db.Column(db.String(40), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    province = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(20), nullable=False)
    # 一对多关系：一个物流公司对应多个仓库
    # warehouses 对应的仓库
    warehouses = db.relationship('Warehouse', backref='logistics')
    # 一对多关系：一个物流公司对应多个车辆
    # vehicle 对应的车辆
    vehicles = db.relationship('Vehicle', backref='logistics')
    # 一对多关系：一个物流公司对应多个管理员
    managers = db.relationship('Move_manager', backref='logistics')
    # 一对多关系：一个物流公司对应多个操作员
    operators = db.relationship('Move_operator', backref='logistics')


class Hospital(db.Model, ObjectToJson):    # 医院
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organization_name = db.Column(db.String(80), nullable=False, unique=True)
    realname = db.Column(db.String(40), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    province = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(20), nullable=False)
    # 一对多关系：一个医院对应多个管理员
    managers = db.relationship('Hospital_manager', backref='hospital')
    # 一对多关系：一个医院对应多个医护人员
    operators = db.relationship('Hospital_operator', backref='hospital')


class Warehouse(db.Model, ObjectToJson):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)  # 仓库名称
    province = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(20))
    # 一对多关系：一个仓库对应多个操作员
    operators = db.relationship('Move_operator', backref='warehouse')
    # 一对多关系：一个物流公司对应多个仓库
    # logistics_id 对应物流公司的id
    logistics_id = db.Column(db.Integer, db.ForeignKey('logistics.id'), nullable=False)

    def __init__(self, name="none", logistics_id=0, province="none", city="none", country="none"):
        self.name = name
        self.province = province
        self.city = city
        self.country = country
        self.logistics_id = logistics_id


class Vehicle(db.Model, ObjectToJson):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    licence = db.Column(db.String(10), nullable=False)
    driver_name = db.Column(db.String(20), nullable=False)
    driver_phone = db.Column(db.String(11), nullable=False)
    # 一对多关系：一个物流公司对应多个车辆
    # logistics_id 对应物流公司的id
    logistics_id = db.Column(db.Integer, db.ForeignKey('logistics.id'), nullable=False)

    def __init__(self, licence="none", logistics_id="none", driver_name="none", driver_phone="none"):
        self.licence = licence
        self.logistics_id = logistics_id
        self.driver_name = driver_name
        self.driver_phone = driver_phone

