from app import models, db
from flask import jsonify
from flask_restful import Resource, fields, marshal_with, abort,  reqparse
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required


admin_puts_args = reqparse.RequestParser()
admin_puts_args.add_argument("email", type=str, help="Вкажіть email", required=True)
admin_puts_args.add_argument("password", type=str, help="Введіть пароль", required=True)


resource_fields = {
    'email': fields.String,
}


class AdminLogin(Resource):
    def post(self):
        args = admin_puts_args.parse_args()
        email = args["email"]
        password = args["password"]
        admin = models.Admin.query.filter_by(email=email).first()
        if not admin:
            return abort(401, message="Невірний email")
        if not password or not admin.check_password(password):
            return abort(401, message="Невірний пароль")

        access_token = create_access_token(identity=email, expires_delta=False)
        return jsonify(access_token=access_token)


class Admin(Resource):
    @jwt_required
    @marshal_with(resource_fields)
    def post(self):
        args = admin_puts_args.parse_args()
        password = generate_password_hash(args['password'])
        admin = models.Admin(email=args['email'], password=password)
        db.session.add(admin)
        db.session.commit()
        return admin

    @jwt_required
    @marshal_with(resource_fields)
    def get(self):
        admins = models.Admin.query.all()
        return admins
