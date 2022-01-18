from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager
import os
from flask_msearch import Search


app = Flask(__name__)
app.config['SECRET_KEY'] = "helloworld"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myshop.db'

db = SQLAlchemy(app)
search = Search()
search.init_app(app)

from shop.admin.models import User

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

from .admin import routes
from .products import routes
from .carts import carts
from .customers import routes
