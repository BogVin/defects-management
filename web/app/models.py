from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from enum import Enum


class Role(Enum):
    not_specified = "Не визначено"
    technical_worker = "Технічний працівник"
    sanitary_worker = "Санітарний працівник"


class Status(Enum):
    open = "Відкрито"
    in_process = "В процесі"
    closed = "Закрито"


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
    telegram_id = db.Column(db.String(20), nullable=False, unique=True)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60))
    username = db.Column(db.String(60))
    role = db.Column(db.Enum(Role), default=Role.not_specified, nullable=False)
    defects_created = db.relationship('DefectInfo', backref='created_by_user', lazy='dynamic', foreign_keys="DefectInfo.created_by")
    defects_working = db.relationship('DefectInfo', backref='work_by_user', lazy='dynamic', foreign_keys="DefectInfo.worker")
    is_active = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'User[{self.first_name}, {self.last_name}]'


class Defect(db.Model):
    __table_name__ = "defects"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String)
    room = db.Column(db.Integer)
    attachment = db.Column(db.String)
    info = db.relationship("DefectInfo", back_populates="defect", uselist=False, cascade="all,delete")

    def __repr__(self):
        return f'Defect[{self.title}]'


class DefectInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer, db.ForeignKey('telegram_user.id'))
    worker = db.Column(db.Integer, db.ForeignKey('telegram_user.id'), nullable=True)
    status = db.Column(db.Enum(Status), default=Status.open, nullable=False)
    open_date = db.Column(db.DateTime, index=True, default=dt.utcnow())
    close_date = db.Column(db.DateTime)
    defect_id = db.Column(db.Integer, db.ForeignKey('defect.id'))
    defect = db.relationship("Defect", back_populates="info")

    def __repr__(self):
        return f'Defect[{self.status, self.defect}]'
