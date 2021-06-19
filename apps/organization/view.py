import json

from flask import Blueprint, request, jsonify
from sqlalchemy import and_

from apps.organization.model import Producer, Logistics, Hospital, Warehouse, Vehicle
from ext import db

organization_bp = Blueprint('organization', __name__)


@organization_bp.route('/organization/add_organization', methods=["POST"])
def add_organization():
    """
    :function
        增加一个机构（生产机构 / 物流公司 / 医院）
    :param:
        organization_type: 表明是哪一类机构
        organization_name： 机构名称
        realname : 负责人姓名
        phone: 负责人电话
        province、city、country：机构所在的省、市、区（县）
    :return:
        Ture/False : 新增是否成功
    """
    organization_type = request.form.get("organization_type")
    producer = Producer()
    logistics = Logistics()
    hospital = Hospital()
    if organization_type == "1":  # 生产机构
        producer.organization_name = request.form.get("organization_name")
        producer.realname = request.form.get("realname")
        producer.phone = request.form.get("phone")
        producer.province = request.form.get("province")
        producer.city = request.form.get("city")
        producer.country = request.form.get("country")
    elif organization_type == "2":  # 物流公司
        logistics.organization_name = request.form.get("organization_name")
        logistics.realname = request.form.get("realname")
        logistics.phone = request.form.get("phone")
        logistics.province = request.form.get("province")
        logistics.city = request.form.get("city")
        logistics.country = request.form.get("country")
    elif organization_type == "3":  # 医院
        hospital.organization_name = request.form.get("organization_name")
        hospital.realname = request.form.get("realname")
        hospital.phone = request.form.get("phone")
        hospital.province = request.form.get("province")
        hospital.city = request.form.get("city")
        hospital.country = request.form.get("country")
    try:
        if organization_type == "1":
            db.session.add(producer)
        elif organization_type == "2":
            db.session.add(logistics)
        elif organization_type == "3":
            db.session.add(hospital)
        db.session.commit()
    except Exception as e:
        print(e)
        return "False"
    else:
        return "True"


@organization_bp.route('/organization/show_organization', methods=["GET", "POST"])
def show_organization():
    """
    :function
        返回某个类型的所有机构（如：所有的物流公司）
    :param:
        organization_type: 表明是哪一类机构
    :return:
        results: 所有的机构对象
    """
    organization_type = request.args.get("organization_type")
    organization_list = []
    if organization_type == "1":
        organization_list = Producer.query.all()
    elif organization_type == "2":
        organization_list = Logistics.query.all()
    elif organization_type == "3":
        organization_list = Hospital.query.all()
    results = []
    for logistics in organization_list:
        # 通过遍历结果集 我们将每一条记录转化为json
        results.append(logistics.to_json())
    return jsonify(results=results)


@organization_bp.route('/organization/show_organization_by_region', methods=["POST"])
def show_organization_by_region():
    """
    :function
        返回某个地区下的所有机构（生产机构 / 物流公司 / 医院）
    :param:
        organization_type: 表明是哪一类机构
        province、city、country：机构所在的省、市、区（县）
    :return:
    """
    organization_type = request.form.get("organization_type")
    province = request.form.get("province")
    city = request.form.get("city")
    country = request.form.get("country")

    organization_list = []
    if organization_type == "1":
        organization_list = Producer.query.filter(and_(Producer.province == province,
                                                       Producer.city == city, Producer.country == country)).all()
    elif organization_type == "2":
        organization_list = Logistics.query.filter(and_(Logistics.province == province,
                                                        Logistics.city == city, Logistics.country == country)).all()
    elif organization_type == "3":
        organization_list = Hospital.query.filter(and_(Hospital.province == province,
                                                       Hospital.city == city, Hospital.country == country)).all()
    results = []
    for logistics in organization_list:
        # 通过遍历结果集 我们将每一条记录转化为json
        results.append(logistics.to_json())
    return jsonify(results=results)


@organization_bp.route('/organization/show_hospital_by_region', methods=["POST"])
def show_hospital_by_region():
    """
    :function
        返回某个地区下的所有医院
    :param:
        province、city、country：医院所在的省、市、区（县）
    :return:
    """
    province = request.form.get("province")
    city = request.form.get("city")
    country = request.form.get("country")

    hospital_list = Hospital.query.filter(and_(Hospital.province == province,
                                               Hospital.city == city,
                                               Hospital.country == country)).all()
    results = []
    for hospital in hospital_list:
        # 通过遍历结果集 我们将每一条记录转化为json
        results.append(hospital.to_json())

    has_value = 1
    if not results:
        has_value = 0

    return jsonify(results=results, has_value=has_value)


@organization_bp.route('/organization/show_warehouse_by_region', methods=["POST"])
def show_warehouse_by_region():
    """
    :function
        返回某个地区下的所有仓库，包括仓库对应的物流公司信息也一并返回
    :param:
        province、city、country：仓库所在的省、市、区（县）
    :return:
        warehouse_dict:
            key: 物流公司名称， value: 仓库列表
        has_value:
            该地区下是否有仓库
    """
    province = request.form.get("province")
    city = request.form.get("city")
    country = request.form.get("country")

    warehouse_list = Warehouse.query.filter(and_(Warehouse.province == province,
                                                 Warehouse.city == city,
                                                 Warehouse.country == country)).all()

    warehouse_dict = {}
    for warehouse in warehouse_list:
        logistics_name = warehouse.logistics.organization_name
        if logistics_name in warehouse_dict:
            warehouse_dict[logistics_name].append([warehouse.name, warehouse.id, warehouse.logistics_id])
        else:
            warehouse_dict[logistics_name] = [[warehouse.name, warehouse.id, warehouse.logistics_id]]

    has_value = 1
    if not warehouse_dict:
        has_value = 0

    return jsonify(warehouse_dict=warehouse_dict, has_value=has_value)


@organization_bp.route('/organization/show_vehicle_by_logistics', methods=["POST"])
def show_vehicle_by_logistics():
    """
    :function
        返回某个公司的所有运输车辆
    :param:
        logistics_id: 物流公司ID
        licence: 模糊查询的依据
    :return:
        vehicles: 查询到的车辆信息
    """
    logistics_id = request.form.get("logistics_id")
    licence = request.form.get("licence")
    vehicles = Vehicle.query.filter(and_(Vehicle.logistics_id == logistics_id,
                              Vehicle.licence.contains(licence))).all()

    results = []
    for vehicle in vehicles:
        # 通过遍历结果集 我们将每一条记录转化为json
        results.append(vehicle.to_json())

    return jsonify(vehicles=results)


