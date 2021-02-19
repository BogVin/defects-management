from app import app
from flask_restful import fields
import os
import os.path
from werkzeug.utils import secure_filename
from datetime import datetime as dt


class FileHandler:
    def __init__(self, photo, user_id):
        if os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        else:
            os.makedirs(app.config['UPLOAD_FOLDER'])
        self.filename = user_id + "_" + str(dt.utcnow()) + secure_filename(photo.filename)
        self.photo = photo

    def allowed_file(self):
        return '.' in self.filename and \
               self.filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    def save(self):
        if self.photo and self.allowed_file():
            self.photo.save(os.path.join(app.config['UPLOAD_FOLDER'], self.filename))
            return self.filename


class EnumItem(fields.Raw):
    def format(self, value):
        return value.value
