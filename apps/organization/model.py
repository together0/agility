from datetime import datetime

from ext import db


class Producer(db.Model):     # 生产机构
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organization_name = db.Column(db.String(80), nullable=False)
    realname = db.Column(db.String(40), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    province = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(20), nullable=False)

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


class Logistics(db.Model):   # 物流公司
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organization_name = db.Column(db.String(80), nullable=False)
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

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


class Hospital(db.Model):    # 医院
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organization_name = db.Column(db.String(80), nullable=False)
    realname = db.Column(db.String(40), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    province = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(20), nullable=False)
    # 一对多关系：一个医院对应多个管理员
    managers = db.relationship('Hospital_manager', backref='hospital')
    # 一对多关系：一个医院对应多个医护人员
    operators = db.relationship('Hospital_operator', backref='hospital')

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    realname = db.Column(db.String(20), nullable=False)
    # 一对多关系：一个物流公司对应多个仓库
    # logistics_id 对应物流公司的id
    logistics_id = db.Column(db.Integer, db.ForeignKey('logistics.id'), nullable=False)


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    licence = db.Column(db.String(10), nullable=False)
    driver_name = db.Column(db.String(20), nullable=False)
    driver_id_number = db.Column(db.String(18), nullable=False)
    # 一对多关系：一个物流公司对应多个车辆
    # logistics_id 对应物流公司的id
    logistics_id = db.Column(db.Integer, db.ForeignKey('logistics.id'), nullable=False)
