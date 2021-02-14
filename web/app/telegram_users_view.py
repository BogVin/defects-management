from flask_restful import Resource, fields, marshal_with, abort,  reqparse
from app import models
from app import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import jsonify
from app import utils


resource_fields = {
    'telegram_id': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'username': fields.String,
    'role': utils.EnumItem,
    'is_active': fields.Boolean
}

user_puts_args = reqparse.RequestParser()
user_puts_args.add_argument("telegram_id", type=str, help="Enter user id", required=True)
user_puts_args.add_argument("first_name", type=str, help="User name", required=True)
user_puts_args.add_argument("last_name", type=str, help="Last name", required=True)
user_puts_args.add_argument("username", type=str, help="Username", required=True)


user_update_args = reqparse.RequestParser()
user_update_args.add_argument("first_name", type=str, help="Name", required=True)
user_update_args.add_argument("last_name", type=str, help="Last name", required=True)
user_update_args.add_argument("username", type=str, help="Username ", required=True)
user_update_args.add_argument("role", type=str, help="Role", required=True)
user_update_args.add_argument("is_active", type=bool, help="Is active", required=True)


class TUserList(Resource):
    @jwt_required
    @marshal_with(resource_fields)
    def get(self):
        current_user = get_jwt_identity()
        if isinstance(current_user, str) and models.Admin.query.filter_by(email=current_user).first():
            users = models.TelegramUser.query.all()
            if not users:
                abort(404, message="Users not found")
            return users
        else:
            abort(401)

    @marshal_with(resource_fields)
    def post(self):
        args = user_puts_args.parse_args()
        result = models.TelegramUser.query.filter_by(telegram_id=args["telegram_id"]).first()
        if result:
            abort(409, message="User already exist")

        user = models.TelegramUser(telegram_id=args['telegram_id'], first_name=args['first_name'], last_name=args['last_name'], username=args['username'],)
        db.session.add(user)
        db.session.commit()
        return user, 201


class TUser(Resource):
    @jwt_required
    @marshal_with(resource_fields)
    def get(self, user_id):
        user = models.TelegramUser.query.get(user_id)
        if not user:
            abort(404, message="User not found")
        return user

    @jwt_required
    @marshal_with(resource_fields)
    def put(self, user_id):
        args = user_update_args.parse_args()
        user = models.TelegramUser.query.get(user_id)
        if not user:
            abort(404, message="User doesn't exist, cannot update")

        user.first_name = args['first_name']
        user.last_name = args['last_name']
        user.username = args['username']
        user.role = args['role']
        user.is_active = args['is_active']

        db.session.commit()

        return user

    @jwt_required
    def delete(self, user_id):
        user = models.TelegramUser.query.get(user_id)
        if not user:
            abort(404, message="User doesn't exist, cannot delete")
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}


class TUserLogin(Resource):
    def post(self, telegram_id):
        user = models.TelegramUser.query.filter_by(telegram_id=telegram_id).first()
        if not user:
            abort(401, message="Wrong user id")
        if user.is_active:
            access_token = create_access_token(identity=telegram_id)
            return jsonify(access_token=access_token)
        else:
            return {"message": "You not active, wait for you activation"}
