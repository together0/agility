import uuid

from flask import Blueprint, request

from apps.vaccine.model import Vaccine
from ext import db

vaccine_bp = Blueprint('vaccine', __name__)


@vaccine_bp.route('/vaccine/add', methods=["POST"])
def add_vaccine():
    """
    :function: 模拟机器添加疫苗信息
    :return:
    """
    producer_id = request.form.get("producer_id")
    kind_name = request.form.get("kind_name")  # 疫苗名称
    # first_trace_code = request.form.get("first_trace_code")  # 一级追溯码
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
