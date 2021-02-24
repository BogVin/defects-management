from flask_restful import Resource, fields, marshal_with, abort,  reqparse
from app import app, models, db, utils
import werkzeug
from flask_jwt_extended import jwt_required
from datetime import datetime as dt
import base64


class IdItem(fields.Raw):
    def format(self, value):
        return value.id


resource_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'room': fields.Integer,
    'attachment': fields.String,
    'info': IdItem
}

resource_info_fields = {
    'id': fields.Integer,
    'created_by': fields.Integer,
    'worker': fields.Integer,
    'status': utils.EnumItem,
    'open_date': fields.DateTime,
    'close_date': fields.DateTime,
    'defect_id': fields.Integer,
    'defect': IdItem
}


defect_puts_args = reqparse.RequestParser()
defect_puts_args.add_argument("created_by", type=str, help="Created by", required=True)
defect_puts_args.add_argument("title", type=str, help="Title", required=True)
defect_puts_args.add_argument("description", type=str, help="Description")
defect_puts_args.add_argument("room", type=int, help="Room number")
defect_puts_args.add_argument("attachment", type=werkzeug.datastructures.FileStorage, location='files')


defect_update_args = reqparse.RequestParser()
defect_update_args.add_argument("title", type=str, help="Title", required=True)
defect_update_args.add_argument("description", type=str, help="Description", required=True)
defect_update_args.add_argument("room", type=int, help="Room number", required=True)


defect_info_args = reqparse.RequestParser()
defect_info_args.add_argument("worker", type=str, help="Worker", required=True)
defect_info_args.add_argument("status", type=str, help="Status", required=True)


class DefectList(Resource):
    @jwt_required
    @marshal_with(resource_fields)
    def get(self):
        defects = models.Defect.query.all()
        if not defects:
            abort(404, message="Users not found")
        return defects


class DefectPost(Resource):
    @jwt_required
    @marshal_with(resource_fields)
    def post(self):
        args = defect_puts_args.parse_args()
        photo = args['attachment']
        fh = utils.FileHandler(photo, args['created_by'])
        fh.save()
        defect = models.Defect(title=args['title'], description=args['description'],
                               room=args['room'], attachment=fh.filename)
        user = models.TelegramUser.query.filter_by(telegram_id=args['created_by']).first()
        defect_info = models.DefectInfo(created_by_user=user, defect=defect)
        db.session.add(defect)
        db.session.add(defect_info)
        db.session.commit()
        return defect, 201


class Defect(Resource):
    @jwt_required
    @marshal_with(resource_fields)
    def get(self, defect_id):
        defect = models.Defect.query.get(defect_id)
        if not defect:
            abort(404, message="User not found")
        return defect

    @jwt_required
    @marshal_with(resource_fields)
    def put(self, defect_id):
        args = defect_puts_args.parse_args()
        defect = models.Defect.query.get(defect_id)
        if not defect:
            abort(404, message="Defect doesn't exist, cannot update")

        defect.title = args['title']
        defect.description = args['description']
        defect.room = args['room']

        db.session.commit()

        return defect

    @jwt_required
    def delete(self, defect_id):
        defect = models.Defect.query.get(defect_id)
        if not defect:
            abort(404, message="Defect doesn't exist, cannot delete")
        db.session.delete(defect)
        db.session.commit()
        return {"message": "Defect deleted successfully"}


class DefectInfo(Resource):
    @jwt_required
    @marshal_with(resource_info_fields)
    def get(self, defect_id):
        defect_info = models.DefectInfo.query.filter_by(defect_id=defect_id).first()
        if not defect_info:
            abort(404, message="Doesn't exist")
        return defect_info

    @jwt_required
    @marshal_with(resource_info_fields)
    def put(self, defect_id):
        args = defect_info_args.parse_args()
        defect_info = models.DefectInfo.query.filter_by(defect_id=defect_id).first()
        if not defect_info:
            abort(404, message="Doesn't exist")
        user = models.TelegramUser.query.filter_by(telegram_id=args['worker']).first()
        defect_info.worker = user
        defect_info.status = args['status']
        if defect_info.status == models.Status.closed.name:
            defect_info.close_date = dt.utcnow()
        db.session.commit()
        return defect_info


class DefectImage(Resource):
    @jwt_required
    def get(self, image_name):
        try:
            with open(app.config['UPLOAD_FOLDER']+image_name, 'rb') as image:
                encoded_image = base64.b64encode(image.read())
        except FileNotFoundError:
            abort(404, message="Image not found")
        return {"image_encode": str(encoded_image)}
