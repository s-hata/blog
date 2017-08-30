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
    FIREBASE_CONFIG = {
        'apiKey': 'AIzaSyBViY7_HZHRZuKn_uufiKOFuzzMMCGtV54',
        'authDomain': 'blog-40ad8.firebaseapp.com',
        'databaseURL': 'https://blog-40ad8.firebaseio.com',
        'storageBucket': '' 
    }


class Development(Default):
    LOG_LEVEL = logging.DEBUG
    SQLALCHEMY_DATABASE_URI = \
        'mysql://blog:blog@192.168.99.101:3306/blog'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
