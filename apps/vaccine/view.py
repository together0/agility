from flask import Blueprint

vaccine_bp = Blueprint('vaccine', __name__)


@vaccine_bp.route('/vaccine/add')
def add_vaccine():
    pass
