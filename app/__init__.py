import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel


CONFIG = 'config.' + os.getenv('ENV', 'Development')
app = Flask(__name__)
app.config.from_object(CONFIG)
db = SQLAlchemy(app)
babel = Babel(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from app import views, models
