from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from  app import telegram_users_view

api.add_resource(telegram_users_view.TUserList, "/users/")
api.add_resource(telegram_users_view.TUser, "/users/<int:user_id>")