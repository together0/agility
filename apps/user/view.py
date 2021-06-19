from flask import Blueprint, request, jsonify
from sqlalchemy import and_

from apps.auxiliary.model import Move_record, First_second_mapping
from apps.organization.model import Warehouse, Vehicle
from apps.user.model import Move_manager, Hospital_manager, Move_operator, Hospital_operator, Recipient, Person, \
    Supervisor
from apps.vaccine.model import Vaccine
from ext import db

user_bp = Blueprint('user', __name__)


@user_bp.route('/user/add_manager', methods=["POST"])
def add_manager():
    """
        function : 增加一个管理员
        params:
            organization_type: 物流的管理员（2）,医院的管理员(3)
    :return: 增加是否成功
    """
    realname = request.form.get("realname")
    phone = request.form.get("phone")
    id_number = request.form.get("id_number")
    password = request.form.get("password")
    oid = request.form.get("oid")
    organization_type = request.form.get("organization_type")

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
        return "False"
    else:
        return "True"


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

    move_operator = Move_operator(realname, phone, password, id_number, warehouse_id, logistics_id)
    db.session.add(move_operator)

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        return "False"
    else:
        return "True"


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

    hospital_operator = Hospital_operator(realname, phone, password, id_number, hospital_id)
    db.session.add(hospital_operator)

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        return "False"
    else:
        return "True"


@user_bp.route('/user/add_recipient', methods=["POST"])
def add_recipient():
    """
    :function
        增加一个操作员或者接种人员  （注册操作）
    :return
        增加是否成功
    """
    realname = request.form.get("realname")
    phone = request.form.get("phone")
    id_number = request.form.get("id_number")
    password = request.form.get("password")

    recipient = Recipient(realname, phone, password, id_number)
    db.session.add(recipient)

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        return "False"
    else:
        return "True"


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
    person_type = request.form.get("person_type")

    person = Person()
    if person_type == "1":  # "物流管理员--1"
        person = Move_manager.query.filter(and_(Move_manager.phone == phone,
                                                Move_manager.password == password)).first()
    elif person_type == "2":  # "医院管理员--2"
        person = Hospital_manager.query.filter(and_(Hospital_manager.phone == phone,
                                                    Hospital_manager.password == password)).first()
    elif person_type == "3":  # "物流操作员--3"
        person = Move_operator.query.filter(and_(Move_operator.phone == phone,
                                                 Move_operator.password == password,
                                                 Move_operator.status == 1)).first()
    elif person_type == "4":  # "医护人员--4"
        person = Hospital_operator.query.filter(and_(Hospital_operator.phone == phone,
                                                     Hospital_operator.password == password,
                                                     Hospital_operator.status == 1)).first()
    elif person_type == "5":  # "接种人员--5"
        person = Recipient.query.filter(and_(Recipient.phone == phone,
                                             Recipient.password == password)).first()
    elif person_type == "6":  # 监管部门
        person = Supervisor.query.filter(and_(Supervisor.phone == phone,
                                              Supervisor.password == password)).first()

    if person is None:
        return "False"
    else:
        return jsonify(person.to_json())


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
