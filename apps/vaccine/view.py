import uuid

from flask import Blueprint, request, jsonify
from sqlalchemy import and_

from apps.auxiliary.model import First_second_mapping, Move_record, Vac_record, Transportation, Vaccination
from apps.organization.model import Producer, Warehouse, Vehicle, Hospital
from apps.user.model import Move_operator, Hospital_operator, Recipient
from apps.vaccine.model import Vaccine
from ext import db

vaccine_bp = Blueprint('vaccine', __name__)


@vaccine_bp.route('/index')
def index():
    return "index"


@vaccine_bp.route('/vaccine/add', methods=["POST"])
def add_vaccine():
    """
    :function: 模拟机器添加疫苗信息
    :return:
    """
    producer_id = request.form.get("producer_id")
    kind_name = request.form.get("kind_name")  # 疫苗名称
    vaccine_name = request.form.get("vaccine_name")
    dose = float(request.form.get("dose"))  # 总剂量
    person_num = int(request.form.get("person_num"))  # 几人份

    uid = uuid.uuid4()
    uidStr = str(uid)
    first_trace_code = uidStr.replace('-', '')

    vaccine = Vaccine(first_trace_code, producer_id, vaccine_name, kind_name, dose, person_num)
    try:
        db.session.add(vaccine)
        db.session.commit()
    except Exception as e:
        print(e)
        return "False"
    else:
        return "True"


@vaccine_bp.route('/vaccine/pack', methods=["POST"])
def pack_vaccine():
    """
    :function: 模拟机器打包疫苗
    :params
        trace_code_list： 二级包装中包含的一级包装的追溯码列表
    :return:
    """
    uid = uuid.uuid4()
    uidStr = str(uid)
    second_trace_code = "_" + uidStr.replace('-', '')

    trace_code_list = request.form.get("trace_code_list").split(",")
    mapping_list = []  # 映射记录
    vaccine_ids = []
    for first_trace_code in trace_code_list:
        vaccine = Vaccine.query.filter(Vaccine.first_trace_code == first_trace_code).first()
        mapping = First_second_mapping()
        mapping.second_trace_code = second_trace_code
        mapping.vaccine_id = vaccine.id
        mapping_list.append(mapping)
        vaccine_ids.append(vaccine.id)

    try:
        db.session.bulk_save_objects(mapping_list)
        db.session.commit()

        # 把之间的打包删除掉
        for vaccine_id in vaccine_ids:
            mappings = First_second_mapping.query.filter(First_second_mapping.vaccine_id == vaccine_id)\
                .order_by(-First_second_mapping.operate_date).all()

            if len(mappings) > 1:
                for mapping in mappings[1:]:
                    db.session.delete(mapping)
                    db.session.commit()

    except Exception as e:
        print(e)
        return "False"
    else:
        return "True"


@vaccine_bp.route('/vaccine/trace_by_supervisor', methods=["POST", "GET"])
def trace_by_supervisor():
    """
    :function:
        追踪疫苗（记录生产机构、运输记录、接种记录）, 监督部门使用
    :params
        first_trace_code： 一级别追溯码
    :return:
    """

    first_trace_code = request.form.get("first_trace_code")
    # first_trace_code = "b4297d95a67440eabda2bad17b862656"

    # 查询生产机构
    vaccine = Vaccine.query.filter(Vaccine.first_trace_code == first_trace_code).first()
    producer = Producer.query.get(vaccine.producer_id).to_json()

    # 查询运输记录
    temp_move_records = Move_record.query.filter(Move_record.vaccine_id == vaccine.id)\
        .order_by(Move_record.in_out_date).all()
    move_records = []
    for move_record in temp_move_records:
        warehouse = Warehouse()
        vehicle = Vehicle()
        operator = Move_operator()
        warehouse = Warehouse.query.get(move_record.warehouse_id)
        vehicle = Vehicle.query.get(move_record.vehicle_id)
        operator = Move_operator.query.get(move_record.operator_id)
        transportation = Transportation(warehouse, vehicle, operator,
                                 move_record.in_out_date, move_record.status, move_record.id)
        move_records.append(transportation.to_json())

    # 查询接种记录
    temp_vac_records = Vac_record.query.filter(Vac_record.vaccine_id == vaccine.id)\
        .order_by(Vac_record.operate_date).all()
    vac_records = []
    for vac_record in temp_vac_records:
        doctor = Hospital_operator()
        recipient = Recipient()
        vaccine = Vaccine()
        doctor = Hospital_operator.query.get(vac_record.doctor_id)
        recipient = Recipient.query.get(vac_record.recipient_id)
        vaccine = Vaccine.query.get(vac_record.vaccine_id)
        vaccination = Vaccination(vac_record.id, vac_record.operate_date, doctor, recipient, vaccine)
        vac_records.append(vaccination.to_json())

    vaccine.produce_date = vaccine.produce_date.strftime("%Y-%m-%d %H:%M:%S")
    vaccine = vaccine.to_json()

    return jsonify(vaccine=vaccine, producer=producer,
                   move_records=move_records, vac_records=vac_records)


@vaccine_bp.route('/vaccine/trace_by_recipient', methods=["POST", "GET"])
def trace_by_recipient():
    """
    :function:
        追踪疫苗（记录疫苗名称、生产机构、接种日期、接种医院）, 接种者使用
    :params
        idcard： 身份证
    :return:
    """

    idcard = request.form.get("idcard")

    recipient = Recipient.query.filter(Recipient.id_number == idcard).first()  # 接种者
    temp_vac_records = Vac_record.query.filter(and_(Vac_record.recipient_id == recipient.id,
                                 Vac_record.status == 1)).all()     # 接种记录
    vac_records = []
    for vac_record in temp_vac_records:
        doctor = Hospital_operator()
        vaccine = Vaccine()
        doctor = Hospital_operator.query.get(vac_record.doctor_id)
        vaccine = Vaccine.query.get(vac_record.vaccine_id)
        vaccination = Vaccination(vac_record.id, vac_record.operate_date, doctor=doctor, vaccine=vaccine)
        vac_records.append(vaccination.to_json())

    return jsonify(recipient=recipient.to_json(), vac_records=vac_records)
