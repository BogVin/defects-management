from app import models
from flask import jsonify
from flask_restful import Resource, fields, marshal_with, abort,  reqparse
from flask_jwt_extended import create_access_token

admin_puts_args = reqparse.RequestParser()
admin_puts_args.add_argument("email", type=str, help="Enter email", required=True)
admin_puts_args.add_argument("password", type=str, help="Enter password", required=True)


class AdminLogin(Resource):
    def post(self):
        args = admin_puts_args.parse_args()
        email = args["email"]
        password = args["password"]
        admin = models.Admin.query.filter_by(email=email).first()
        if not admin:
            return abort(401, message="Wrong email")
        if not password or not admin.check_password(password):
            return abort(401, message="Wrong password")

        access_token = create_access_token(identity=email, expires_delta=False)
        return jsonify(access_token=access_token)
