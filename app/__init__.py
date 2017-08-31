import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


CONFIG = 'config.' + os.getenv('ENV', 'Development')
app = Flask(__name__)
app.config.from_object(CONFIG)
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from app import views, models
