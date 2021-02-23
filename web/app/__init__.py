from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)
cors = CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)


from app import telegram_users_view, defects_view, admin_view


api.add_resource(defects_view.DefectList, "/defects")
api.add_resource(defects_view.DefectPost, "/defects")
api.add_resource(defects_view.DefectInfo, "/defects/<int:defect_id>/info")
api.add_resource(defects_view.DefectImage, "/defects/image/<string:image_name>")
api.add_resource(defects_view.DefectsByStatus, "/defects/<string:status>")
api.add_resource(defects_view.Defect, "/defects/<int:defect_id>")
api.add_resource(defects_view.DefectsByDateAndStatus, "/defects/date")
api.add_resource(defects_view.DefectsByWorkerId, "/defects/worker/<string:worker_id>")

api.add_resource(admin_view.AdminLogin, "/admin/login")

api.add_resource(telegram_users_view.TUserList, "/users/")
api.add_resource(telegram_users_view.TUser, "/users/<int:user_id>")
api.add_resource(telegram_users_view.TBotLogin, "/users/login/<string:telegram_id>")
api.add_resource(telegram_users_view.TBot, "/users/me/<string:telegram_id>")
