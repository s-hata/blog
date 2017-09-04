import logging


class Default(object):
    LOG_LEVEL = logging.INFO
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'
    PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_POOL_SIZE = 5
    SQLALCHEMY_POOL_TIMEOUT = 10
    SQLALCHEMY_POOL_RECYCLE = 3600
    SQLALCHEMY_MAX_OVERFLOW = 5
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_MIGRATION_REPO = './db_migration_repo/'
    FIREBASE_CONFIG = {
        'apiKey': 'AIzaSyBViY7_HZHRZuKn_uufiKOFuzzMMCGtV54',
        'authDomain': 'blog-40ad8.firebaseapp.com',
        'databaseURL': 'https://blog-40ad8.firebaseio.com',
        'storageBucket': '' 
    }
    LANGUAGES = {
        'en': 'English',
        'ja': 'Japanease'
    }


class Development(Default):
    LOG_LEVEL = logging.DEBUG
    SQLALCHEMY_DATABASE_URI = \
        'mysql://blog:blog@192.168.99.101:3306/blog'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_RECORD_QUERIES = True
    DATABASE_QUERY_TIMEOUT = 0.1
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class UnitTest(Default):
    LOG_LEVEL = logging.DEBUG
    SQLALCHEMY_DATABASE_URI = \
        'mysql://root@127.0.0.1:3306/circle_test'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class Production(Default):
    LOG_LEVEL = logging.INFO
    SQLALCHEMY_DATABASE_URI = \
        'mysql://b3aa79899f277b:4f669df7@us-cdbr-iron-east-05.cleardb.net/heroku_aeb18f2294cf025'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
