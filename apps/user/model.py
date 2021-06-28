from datetime import datetime

from ext import db


class Person(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password = db.Column(db.String(64), nullable=False)
    realname = db.Column(db.String(20), nullable=False)
    id_number = db.Column(db.String(18), nullable=False)
    phone = db.Column(db.String(11), nullable=False, unique=True)
    register_date = db.Column(db.DATETIME, default=datetime.now)

    def __init__(self, realname="none", phone="none", password="none", id_number="none"):
        self.realname = realname
        self.phone = phone
        self.password = password
        self.id_number = id_number

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


class Supervisor(Person):  # 监督部门
    def __init__(self, realname, phone, password, id_number):
        super().__init__(realname, phone, password, id_number)


class Recipient(Person):  # 接种者
    gender = db.Column(db.Integer, default=0)  # 1-男，0-女
    reservation_code = db.Column(db.String(32), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    status = db.Column(db.Integer, default=0)  # 1-接种完成，0-未接种

    def __init__(self, realname=None, phone=None, id_number=None, gender=None, reservation_code=None, hospital_id=None):
        super().__init__(realname, phone, password="1", id_number=id_number)
        self.gender = gender
        self.reservation_code = reservation_code
        self.hospital_id = hospital_id


class Move_manager(Person):  # 物流管理者
    # 一对多关系：一个物流公司对应多个管理员
    logistics_id = db.Column(db.Integer, db.ForeignKey('logistics.id'), nullable=False)

    def __init__(self, realname, phone, password, id_number, logistics_id):
        super().__init__(realname, phone, password, id_number)
        self.logistics_id = logistics_id


class Hospital_manager(Person):  # 医院管理者
    # 一对多关系：一个医院对应多个管理员
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)

    def __init__(self, realname, phone, password, id_number, hospital_id):
        super().__init__(realname, phone, password, id_number)
        self.hospital_id = hospital_id


class Move_operator(Person):
    status = db.Column(db.Integer, default=0)  # 注册申请是否通过 0:未处理，1:通过，2:拒绝
    # 一对多关系：一个物流公司对应多个操作员
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)
    # 物流公司的ID
    logistics_id = db.Column(db.Integer, db.ForeignKey('logistics.id'), nullable=False)

    def __init__(self, realname=None, phone=None, password=None, id_number=None, warehouse_id=None, logistics_id=None):
        super().__init__(realname, phone, password, id_number)
        self.warehouse_id = warehouse_id
        self.logistics_id = logistics_id


class Hospital_operator(Person):  # 医护人员
    status = db.Column(db.Integer, default=0)  # 注册申请是否通过
    # 一对多关系：一个医院对应多个医护人员
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)

    def __init__(self, realname=None, phone=None, password=None, id_number=None, hospital_id=None):
        super().__init__(realname, phone, password, id_number)
        self.hospital_id = hospital_id

# class Person(db.Model):
#     __abstract__ = True
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     username = db.Column(db.String(10), nullable=False)
#     password = db.Column(db.String(64), nullable=False)
#     realname = db.Column(db.String(20), nullable=False)
#     id_number = db.Column(db.String(18), nullable=False)
#     phone = db.Column(db.String(11), nullable=False, unique=True)
#     gender = db.Column(db.Boolean, default=False)
#     register_date = db.Column(db.DATETIME, default=datetime.now)
#
#
# class Supervisor(Person):
#     pass
#
#
# class Recipient(Person):   # 接种者
#     pass
#
#
# class Manager(Person):    # 管理人员父类
#     __abstract__ = True
#
#
# class Move_manager(Manager):
#     # 一对多关系：一个物流公司对应多个管理员
#     logistics_id = db.Column(db.Integer, db.ForeignKey('logistics.id'), nullable=False)
#
#
# class Hospital_manager(Manager):
#     # 一对多关系：一个医院对应多个管理员
#     hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
#
#
# class Operator(Person):   # 操作人员父类
#     __abstract__ = True
#
#
# class Move_operator(Operator):
#     # 一对多关系：一个物流公司对应多个操作员
#     logistics_id = db.Column(db.Integer, db.ForeignKey('logistics.id'), nullable=False)
#
#
# class Hospital_operator(Operator):  # 医护人员
#     # 一对多关系：一个医院对应多个医护人员
#     hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
