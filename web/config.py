import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'biden-is-the-president'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super_secret'
    UPLOAD_FOLDER = "static/defect_images/"
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'tif'}
