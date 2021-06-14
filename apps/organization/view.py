import json

from flask import Blueprint, request, jsonify
from sqlalchemy import and_

from apps.organization.model import Producer, Logistics, Hospital
from ext import db

organization_bp = Blueprint('organization', __name__)


@organization_bp.route('/organization/add_organization', methods=["POST"])
def add_organization():
    organization_type = request.form.get("organization_type")
    producer = Producer()
    logistics = Logistics()
    hospital = Hospital()
    if organization_type == "1":
        producer.organization_name = request.form.get("organization_name")
        producer.realname = request.form.get("realname")
        producer.phone = request.form.get("phone")
        producer.province = request.form.get("province")
        producer.city = request.form.get("city")
        producer.country = request.form.get("country")
    elif organization_type == "2":
        logistics.organization_name = request.form.get("organization_name")
        logistics.realname = request.form.get("realname")
        logistics.phone = request.form.get("phone")
        logistics.province = request.form.get("province")
        logistics.city = request.form.get("city")
        logistics.country = request.form.get("country")
    elif organization_type == "3":
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
    organization_type = request.form.get("organization_type")
    province = request.form.get("province")
    city = request.form.get("city")
    country = request.form.get("country")

    organization_list = []
    if organization_type == "1":
        organization_list = Producer.query.filter(and_(Producer.province==province,
                                                        Producer.city==city,Producer.country==country)).all()
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

