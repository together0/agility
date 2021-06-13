from datetime import datetime

from ext import db


class Vaccine(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_trace_code = db.Column(db.String(34), nullable=False, unique=False)
    name = db.Column(db.String(40), nullable=False)
    kind_name = db.Column(db.String(40), nullable=False)  # 种类名称
    kind_id = db.Column(db.Integer, default=0)  # 种类编号
    dose = db.Column(db.Float, default=0)  # 剂量
    person_num = db.Column(db.Integer, default=0)  # 几人份
    produce_date = db.Column(db.DATETIME, default=datetime.now)
    complete_num = db.Column(db.Integer, default=0)  # 接种人数
    # 生产疫苗的机构id
    producer_id = db.Column(db.Integer, db.ForeignKey('producer.id'), nullable=False)
    # 一对多关系：一剂疫苗对应多个入库出库记录
    move_records = db.relationship('Move_record', backref='vaccine')
    # 一对多关系：一剂疫苗对应多个接种记录
    vac_records = db.relationship('Vac_record', backref='vaccine')



