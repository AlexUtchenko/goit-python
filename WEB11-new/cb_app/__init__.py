from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Abra_Cadabra'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///CB_app.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


from cb_app import routes
