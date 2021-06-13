from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from apps import create_app
from ext import db

from apps.user.model import *
from apps.vaccine.model import *
from apps.auxiliary.model import *
from apps.organization.model import *

app = create_app()
manager = Manager(app=app)

# 数据库命令
migrate = Migrate(app=app, db=db)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

