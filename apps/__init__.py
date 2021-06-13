from flask import Flask

from apps.organization.view import organization_bp
from apps.user.view import user_bp
from apps.vaccine.view import vaccine_bp
from ext import db
from settings import DevelopmentConfig


def create_app():
    # 创建核心对象
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    # 加载配置文件
    app.config.from_object(DevelopmentConfig)
    # 初始化迁移对象、映射对象db
    db.init_app(app=app)
    # 注册蓝图
    app.register_blueprint(user_bp)
    app.register_blueprint(organization_bp)
    app.register_blueprint(vaccine_bp)
    return app