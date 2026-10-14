import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret_key_accessevent')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://mariaafanaseva@localhost:5432/accessevent'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False