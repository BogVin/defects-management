from flask_restful import Resource, fields, marshal_with, abort,  reqparse
from app import models
from app import db


class RoleItem(fields.Raw):
    def format(self, value):
        return value.value

resource_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'username': fields.String,
    "phone": fields.String,
    "role": RoleItem,
}

user_puts_args = reqparse.RequestParser()
user_puts_args.add_argument("id", type=int, help="Enter user id", required=True)
user_puts_args.add_argument("first_name", type=str, help="User name", required=True)
user_puts_args.add_argument("last_name", type=str, help="Last name", required=True)
user_puts_args.add_argument("username", type=str, help="Username", required=True)
user_puts_args.add_argument("phone", type=str, help="phone number", required=True)


user_update_args = reqparse.RequestParser()
user_update_args.add_argument("first_name", type=str, help="Name")
user_update_args.add_argument("last_name", type=str, help="Last name")
user_update_args.add_argument("username", type=str, help="Username ")
user_update_args.add_argument("role", type=str, help="role")

class TUserList(Resource):
    @marshal_with(resource_fields)
    def get(self):
        users = models.TelegramUser.query.all()
        if not users:
            abort(404, message="Users not found")
        return users


class TUser(Resource):
    @marshal_with(resource_fields)
    def get(self,user_id):
        user = models.TelegramUser.query.get(user_id)
        if not user:
            abort(404, message="User not found")
        return user

    @marshal_with(resource_fields)
    def post(self, user_id):
        args = user_puts_args.parse_args()
        result = models.TelegramUser.query.filter_by(id=user_id).first()
        if result:
            abort(409, message="User already exist")

        user = models.TelegramUser(id=args['id'], first_name=args['first_name'], last_name=args['last_name'], username=args['username'],
                                   phone=args['phone'])
        db.session.add(user)
        db.session.commit()
        return user, 201

    @marshal_with(resource_fields)
    def put(self, user_id):
        args = user_update_args.parse_args()
        user = models.TelegramUser.query.get(user_id)
        if not user:
            abort(404, message="User doesn't exist, cannot update")

        if args['first_name']:
            user.first_name = args['first_name']
        if args['last_name']:
            user.last_name = args['last_name']
        if args['username']:
            user.username = args['username']
        if args['role']:
            user.role = args['role']

        db.session.commit()

        return user

    def delete(self, user_id):
        user = models.TelegramUser.query.get(user_id)
        if not user:
            abort(404, message="User doesn't exist, cannot delete")
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}
