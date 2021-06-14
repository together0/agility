from datetime import datetime

from ext import db


class Vaccine(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_trace_code = db.Column(db.String(32), nullable=False, unique=False)
    name = db.Column(db.String(40), nullable=False)
    # 灭活疫苗 腺病毒载体疫苗 重组蛋白疫苗 DNA疫苗 RNA疫苗
    kind_name = db.Column(db.String(40), default="灭活疫苗")  # 种类名称
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

    def __init__(self, first_trace_code="none", producer_id=1, name="none", kind_name="none", dose=0.0, person_num=0):
        self.first_trace_code = first_trace_code
        self.name = name
        self.kind_name = kind_name
        self.dose = dose
        self.person_num = person_num
        self.producer_id = producer_id




