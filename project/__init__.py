#/crypto/project
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
from flask_mail import Mail,Message

from flask_admin import Admin
from flask_babel import Babel

app = Flask(__name__)

admin = Admin(app)
babel = Babel(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///'+os.path.join(basedir,'data,sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
app.config['SECRET_KEY']='mysecretkey'
db = SQLAlchemy(app)
Migrate(app,db)
mail= Mail(app)
#######################################
#############Login config##############
#######################################
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'
#######################################
#########FOR EMAIL CONFIRMATION########
#######################################
app.config.from_pyfile('config.cfg')
app.secret_key = 'mysecretkey'
s = URLSafeTimedSerializer('mysecretkey')
mail = Mail(app)
#######################################
#######################################
###########REGISTER BLUEPRINTS#########
from project.error_pages.handlers import error_pages
from project.users.views import users
from project.core.views import core
app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(users)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
