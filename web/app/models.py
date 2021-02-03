from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from enum import Enum


class Role(Enum):
    not_specified = 'Not Specified'
    technical_worker = 'Technical Worker'
    sanitary_worker = "Sanitary Worker"


class Status(Enum):
    open = "Open"
    in_process = "In Process"
    closed = "Closed"


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f'Admin[{self.email}]'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class TelegramUser(db.Model):
    __table_name__ = "telegram_users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    username = db.Column(db.String(60))
    phone = db.Column(db.String, nullable=False)
    role = db.Column(db.Enum(Role), default=Role.not_specified, nullable=False)
    defects_created = db.relationship('Defect', backref='created_by_user', lazy='dynamic', foreign_keys="Defect.created_by")
    defects_working = db.relationship('Defect', backref='work_by_user', lazy='dynamic', foreign_keys="Defect.worker")


    def __repr__(self):
        return f'User[{self.first_name}, {self.last_name}]'


class Defect(db.Model):
    __table_name__ = "defects"
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer, db.ForeignKey('telegram_user.id'))
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String)
    open_date = db.Column(db.DateTime, index=True, default=dt.utcnow())
    close_date = db.Column(db.DateTime)
    room = db.Column(db.Integer)
    attachment = db.Column(db.LargeBinary)
    status = db.Column(db.Enum(Status), default=Status.open, nullable=False)
    worker = db.Column(db.Integer, db.ForeignKey('telegram_user.id'))

    def __repr__(self):
        return f'Defect[{self.title}]'
