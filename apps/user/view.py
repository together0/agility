from flask import Blueprint, request, jsonify
from sqlalchemy import and_

from apps.user.model import Move_manager, Hospital_manager, Move_operator, Hospital_operator, Recipient, Person
from ext import db

user_bp = Blueprint('user', __name__)


@user_bp.route('/user/add_manager', methods=["POST"])
def add_manager():
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


@user_bp.route('/user/add_operator_or_recipient', methods=["POST"])
def add_operator_or_recipient():
    realname = request.form.get("realname")
    phone = request.form.get("phone")
    id_number = request.form.get("id_number")
    password = request.form.get("password")
    oid = request.form.get("oid")
    person_type = request.form.get("person_type")

    if person_type == "1":
        recipient = Recipient(realname, phone, password, id_number)
        db.session.add(recipient)
    elif person_type == "2":
        move_operator = Move_operator(realname, phone, password, id_number, oid)
        db.session.add(move_operator)
    elif person_type == "3":
        hospital_operator = Hospital_operator(realname, phone, password, id_number, oid)
        db.session.add(hospital_operator)

    try:
        db.session.commit()
    except Exception as e:
        print(e)
        return "False"
    else:
        return "True"


@user_bp.route('/user/login', methods=["POST"])
def login():
    phone = request.form.get("phone")
    password = request.form.get("password")
    person_type = request.form.get("person_type")
    print("-------------")
    print(phone, password, person_type)
    print("-------------")

    person = Person()
    if person_type == "1":  # "物流管理员--1"
        person = Move_manager.query.filter(and_(Move_manager.phone == phone,
                                                Move_manager.password == password)).first()
    elif person_type == "2":  # "医院管理员--2"
        person = Hospital_manager.query.filter(and_(Hospital_manager.phone == phone,
                                                    Hospital_manager.password == password)).first()
    elif person_type == "3":  # "物流操作员--3"
        person = Move_operator.query.filter(and_(Move_operator.phone == phone,
                                                 Move_operator.password == password)).first()
    elif person_type == "4":  # "医护人员--4"
        person = Hospital_operator.query.filter(and_(Hospital_operator.phone == phone,
                                                     Hospital_operator.password == password)).first()
    else:  # "接种人员--5"
        person = Recipient.query.filter(and_(Recipient.phone == phone,
                                             Recipient.password == password)).first()
    if person is None:
        return "False"
    else:
        print(person.realname, person.phone, person.password, person.id_number)
        return jsonify(person.to_json())
