import uuid
from datetime import datetime

from flask import Blueprint, request, jsonify
from sqlalchemy import and_

from apps.auxiliary.model import Move_record, First_second_mapping, Vac_record
from apps.organization.model import Warehouse, Vehicle
from apps.user.model import Move_manager, Hospital_manager, Move_operator, Hospital_operator, Recipient, Person, \
    Supervisor
from apps.vaccine.model import Vaccine
from ext import db

user_bp = Blueprint('user', __name__)


@user_bp.route('/user/existPhone', methods=["POST"])
def existPhone(phone):
    """
    :function:
        判断手机号是否存在
    :return:
    """
    supervisor = Supervisor.query.filter(Supervisor.phone == phone).first()
    move_manager = Move_manager.query.filter(Move_manager.phone == phone).first()
    move_operator = Move_operator.query.filter(Move_operator.phone == phone).first()
    hospital_manager = Hospital_manager.query.filter(Hospital_manager.phone == phone).first()
    doctor = Hospital_operator.query.filter(Hospital_operator.phone == phone).first()
    if supervisor or move_manager or move_operator or hospital_manager or doctor:
        return True
    else:
        return False


@user_bp.route('/user/add_manager', methods=["POST"])
def add_manager():
    """
    :function : 增加一个管理员
    :param:: organization_type: 物流的管理员（2）,医院的管理员(3)
    :param: oid : 机构ID
    :return: 增加是否成功
    """
    realname = request.form.get("realname")
    phone = request.form.get("phone")
    id_number = request.form.get("id_number")
    password = request.form.get("password")
    oid = request.form.get("oid")
    organization_type = request.form.get("organization_type")

    if existPhone(phone):
        return jsonify(msg="error", reason="手机号已经存在")
    else:
        if organization_type == "2":
            move_manager = Move_manager(realname, phone, password, id_number, oid)
            db.session.add(move_manager)
        elif organization_type == "3":
            hospital_manager = Hospital_manager(realname, phone, password, id_number, oid)
            db.session.add(hospital_manager)

        try:
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify(msg="error", reason="录入失败")
        else:
            return jsonify(msg="success")


@user_bp.route('/user/add_moveoperator', methods=["POST"])
def add_moveoperator():
    """
    :function
        增加物流操作员 （注册操作）
    :return
        增加是否成功
    """
    realname = request.form.get("realname")
    phone = request.form.get("phone")
    id_number = request.form.get("id_number")
    password = request.form.get("password")
    warehouse_id = request.form.get("warehouse_id")
    logistics_id = request.form.get("logistics_id")

    if existPhone(phone):
        return jsonify(msg="error", reason="手机号已经存在")
    else:
        move_operator = Move_operator(realname, phone, password, id_number, warehouse_id, logistics_id)
        db.session.add(move_operator)

        try:
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify(msg="error", reason="注册失败")
        else:
            return jsonify(msg="success")


@user_bp.route('/user/add_doctor', methods=["POST"])
def add_doctor():
    """
    :function
        增加医护人员  （注册操作）
    :return
        增加是否成功
    """
    realname = request.form.get("realname")
    phone = request.form.get("phone")
    id_number = request.form.get("id_number")
    password = request.form.get("password")
    hospital_id = request.form.get("hospital_id")

    if existPhone(phone):
        return jsonify(msg="error", reason="手机号已经存在")
    else:
        hospital_operator = Hospital_operator(realname, phone, password, id_number, hospital_id)
        db.session.add(hospital_operator)

        try:
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify(msg="error", reason="注册失败")
        else:
            return jsonify(msg="success")


@user_bp.route('/user/add_recipient', methods=["POST"])
def add_recipient():
    """
    :function
        增加一个接种人员  （注册操作）
    :return
        增加是否成功
    """
    realname = request.form.get("name")
    phone = request.form.get("phone")
    id_number = request.form.get("id_number")
    gender = request.form.get("gender")
    hospital_id = request.form.get("hospital_id")

    if gender == "男":
        gender = 1
    else:
        gender = 0

    uid = uuid.uuid4()
    uidStr = str(uid)
    reservation_code = uidStr.replace('-', '')

    recipient = Recipient(realname, phone, id_number, gender, reservation_code, hospital_id)
    db.session.add(recipient)

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify(msg="error")
    else:
        return jsonify(reservation_code=reservation_code, msg="success")


@user_bp.route('/user/login', methods=["POST"])
def login():
    """
        function: 用户登录
    :param:
        person_type: ['物流管理员-1','医院管理员-2','物流操作员-3','医护人员-4','接种人员-5','监管部门-6']
    :return:
    """
    phone = request.form.get("phone")
    password = request.form.get("password")

    person1 = Move_manager.query.filter(and_(Move_manager.phone == phone,
                                             Move_manager.password == password)).first()
    person2 = Hospital_manager.query.filter(and_(Hospital_manager.phone == phone,
                                                 Hospital_manager.password == password)).first()
    person3 = Move_operator.query.filter(and_(Move_operator.phone == phone,
                                              Move_operator.password == password,
                                              Move_operator.status == 1)).first()
    person4 = Hospital_operator.query.filter(and_(Hospital_operator.phone == phone,
                                                  Hospital_operator.password == password,
                                                  Hospital_operator.status == 1)).first()
    person5 = Recipient.query.filter(and_(Recipient.phone == phone,
                                          Recipient.password == password)).first()
    person6 = Supervisor.query.filter(and_(Supervisor.phone == phone,
                                           Supervisor.password == password)).first()

    person = Person()
    person_type = 0
    if person1 is not None:  # 物流管理员
        person = person1
        person_type = 1
    elif person2 is not None:  # 医院管理者
        person = person2
        person_type = 2
    elif person3 is not None:  # 物流操作员
        person = person3
        person_type = 3
    elif person4 is not None:  # 医护人员
        person = person4
        person_type = 4
    elif person5 is not None:  # 接种者
        person = person5
        person_type = 5
    elif person6 is not None:  # 监管部门
        person = person6
        person_type = 6
    else:
        person = Person()
        person_type = 0  # 说明没有查到

    return jsonify(person=person.to_json(), person_type=person_type)


# 查询某个状态的操作员
@user_bp.route('/user/movemanager/findOperatorByStatus', methods=["POST"])
def findOperatorByStatus():
    """
        function：物流管理者查询某个状态（未审批、批准、拒绝）下的所有操作员
    :param
        operator_status : 操作员状态
        logistics_id： 哪个物流公司下的操作员，根据前端登录的物流管理员决定
    :return:
    """
    operator_status = int(request.form.get("operator_status"))
    logistics_id = int(request.form.get("logistics_id"))
    operators = Move_operator.query.filter(and_(Move_operator.status == operator_status,
                                                Move_operator.logistics_id == logistics_id)).all()
    results = []
    for operator in operators:
        # 通过遍历结果集 我们将每一条记录转化为json
        results.append(operator.to_json())
    return jsonify(results=results)


# 批准/拒绝操作员的注册请求
@user_bp.route('/user/movemanager/agree_or_disagree', methods=["POST"])
def agree_or_disagree():
    operator_id = request.form.get("operator_id")
    operator_status = int(request.form.get("operator_status"))
    operator = Move_operator.query.get(operator_id)
    operator.status = operator_status
    try:
        db.session.commit()
    except Exception as e:
        return "False"
    else:
        return "True"


@user_bp.route('/user/movemanager/addWarehouse', methods=["POST"])
def addWarehouse():
    """
        function：物流管理员增加仓库
    :param:
        logistics_id: 哪一家物流公司的仓库
    :return:
    """
    name = request.form.get("name")  # 仓库名称
    logistics_id = request.form.get("logistics_id")
    province = request.form.get("province")
    city = request.form.get("city")
    country = request.form.get("country")
    warehouse = Warehouse(name, logistics_id, province, city, country)
    try:
        db.session.add(warehouse)
        db.session.commit()
    except Exception as e:
        return "False"
    else:
        return "True"


@user_bp.route('/user/movemanager/addVehicle', methods=["POST"])
def addVehicle():
    """
        function：物流管理员增加运输车辆
    :param:
        logistics_id: 哪一家物流公司的车辆
    :return:
    """
    licence = request.form.get("licence")  # 车牌号
    logistics_id = request.form.get("logistics_id")
    driver_name = request.form.get("driver_name")
    driver_phone = request.form.get("driver_phone")

    vehicle = Vehicle(licence, logistics_id, driver_name, driver_phone)
    try:
        db.session.add(vehicle)
        db.session.commit()
    except Exception as e:
        return "False"
    else:
        return "True"


@user_bp.route('/user/moveoperator/in_warehouse', methods=["POST"])
def in_warehouse():
    """
        function：入库操作
    :param:
        warehouse_id: 进入的哪一个仓库
        vehicle_id: 使用的哪一个车辆
        operator_id: 操作者的ID
        trace_code_list: 追溯码(一级、二级都可以有)
    :return:
        成功/失败
    """
    warehouse_id = request.form.get("warehouse_id")
    vehicle_id = request.form.get("vehicle_id")
    operator_id = request.form.get("operator_id")
    trace_code_list = request.form.get("trace_code_list").split(",")

    # 所有疫苗的ID
    vaccine_ids = []
    for trace_code in trace_code_list:
        if len(trace_code) == 32:  # 一级追溯码
            vaccine = Vaccine.query.filter(Vaccine.first_trace_code == trace_code).first()
            vaccine_ids.append(vaccine.id)
        elif len(trace_code) == 33:  # 二级追溯码
            mappings = First_second_mapping.query.filter(First_second_mapping.second_trace_code == trace_code).all()
            for mapping in mappings:
                vaccine_ids.append(mapping.vaccine_id)
        else:
            raise Exception("追溯码出错")

    records = []
    for vaccine_id in vaccine_ids:
        record = Move_record(vaccine_id=vaccine_id, warehouse_id=warehouse_id,
                             vehicle_id=vehicle_id, operator_id=operator_id,
                             status=False)
        records.append(record)

    try:
        db.session.bulk_save_objects(records)
        db.session.commit()
    except Exception as e:
        return "False"
    else:
        return "True"


@user_bp.route('/user/moveoperator/out_warehouse', methods=["POST"])
def out_warehouse():
    """
        function：出库操作
    :param:
        warehouse_id: 哪一个仓库
        vehicle_id: 使用哪一个车辆
        operator_id: 操作者的ID
        trace_code_list: 追溯码（一级、二级都可能出现）
    :return:
        成功/失败
    """
    warehouse_id = request.form.get("warehouse_id")
    vehicle_id = request.form.get("vehicle_id")
    operator_id = request.form.get("operator_id")
    trace_code_list = request.form.get("trace_code_list").split(",")
    # 判断所有输入的疫苗是否存在于该仓库中，如果都存在可以出库，否则跳过出库操作，返回错误信息
    is_exist = True

    vaccine_ids = []
    for trace_code in trace_code_list:
        if len(trace_code) == 32:  # 一级追溯码
            vaccine = Vaccine.query.filter(Vaccine.first_trace_code == trace_code).first()
            if vaccine is None:
                is_exist = False
                break
            vaccine_ids.append(vaccine.id)
        elif len(trace_code) == 33:  # 二级追溯码
            mappings = First_second_mapping.query.filter(First_second_mapping.second_trace_code == trace_code).all()
            if len(mappings) == 0:
                is_exist = False
                break
            for mapping in mappings:
                vaccine_ids.append(mapping.vaccine_id)
        else:
            raise Exception("追溯码出错")

    if is_exist:
        records = []
        for vaccine_id in vaccine_ids:
            record = Move_record(vaccine_id=vaccine_id, warehouse_id=warehouse_id,
                                 vehicle_id=vehicle_id, operator_id=operator_id,
                                 status=1)
            records.append(record)

        try:
            db.session.bulk_save_objects(records)
            db.session.commit()
        except Exception as e:
            return "False"
        else:
            return "True"
    else:
        return "not_exist"


@user_bp.route('/user/findDoctorByPhone', methods=["POST"])
def findDoctorByPhone():
    """
        function：根据手机号查询医生
    :param:
        phone: 医生手机号
        hospital_id: 医院ID
    :return:
        成功/失败
    """
    phone = request.form.get("phone")
    hospital_id = request.form.get("hospital_id")

    doctor = Hospital_operator.query.filter(and_(Hospital_operator.phone == phone,
                                                 Hospital_operator.hospital_id == hospital_id)).first()

    if doctor is not None:
        return jsonify(doctor=doctor.to_json(), msg="success")
    else:
        return jsonify(msg="error")


@user_bp.route('/user/findRecipientByCode', methods=["POST"])
def findRecipientByCode():
    """
        function：根据预约码查询接种者
    :param:
        reservation_code: 预约码
        hospital_id: 医院ID
    :return:
        成功/失败
    """
    reservation_code = request.form.get("reservation_code")
    hospital_id = request.form.get("hospital_id")
    recipient = Recipient.query.filter(and_(Recipient.reservation_code == reservation_code,
                                            Recipient.hospital_id == hospital_id)).first()
    recipient.register_date = recipient.register_date.strftime("%Y-%m-%d %H:%M:%S")

    if recipient is not None:
        return jsonify(recipient=recipient.to_json(), msg="success")
    else:
        return jsonify(msg="error")


@user_bp.route('/user/doctor/assign', methods=["POST"])
def assign():
    """
        function：分配医护人员给接种者
    :param:
        reservation_code: 预约码
        hospital_id: 医院ID
    :return:
        成功/失败
    """

    recipient_id = request.form.get("recipient_id")
    doctor_id = request.form.get("doctor_id")

    record = Vac_record(recipient_id, doctor_id)
    db.session.add(record)

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify(msg="error")
    else:
        return jsonify(msg="success")


@user_bp.route('/user/doctor/findRecipientList', methods=["POST"])
def findRecipientList():
    """
        function：查询分配给某个医护人员的接种者，（只查询还未接种的）
    :param:
        doctor_id: 医护人员ID
    :return:
        接种者列表、接种记录ids
    """

    doctor_id = request.form.get("doctor_id")

    records = Vac_record.query.filter(and_(Vac_record.doctor_id == doctor_id,
                                           Vac_record.status == 0)).all()
    recipient_list = []
    record_ids = []
    for record in records:
        recipient = Recipient.query.get(record.recipient_id)
        recipient_list.append(recipient.to_json())
        record_ids.append(record.id)

    return jsonify(recipient_list=recipient_list, record_ids=record_ids)


@user_bp.route('/user/doctor/inject', methods=["POST"])
def inject():
    """
        function：医护人员注射疫苗
    :param:
        vaccine_id: 注射疫苗的追溯码
        record_id: 接种记录的ID
    :return:
        成功/失败
    """

    trace_code = request.form.get("trace_code")
    record_id = request.form.get("record_id")
    vaccine = Vaccine.query.filter(Vaccine.first_trace_code == trace_code).first()

    record = Vac_record.query.get(record_id)
    record.status = 1
    record.vaccine_id = vaccine.id
    record.operate_date = datetime.now()

    try:
        db.session.commit()
    except Exception as e:
        return jsonify(msg="error")
    else:
        return jsonify(msg="success")