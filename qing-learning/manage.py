# encoding: utf-8

from flask_migrate import Migrate,MigrateCommand
from app import app
from flask_script import Manager
from exts import db
import config
from models import UserModel, QuestionModel, AnswerModel

app.config.from_object(config)
db.init_app(app)


manager = Manager(app)

migrate = Migrate(app,db)

manager.add_command('db',MigrateCommand)

if __name__ == "__main__":
    manager.run(host='0.0.0.0', port=80)
