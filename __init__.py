from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
#from flask.ext.uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
import os


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = "helloworld"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myshop.db'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


from .admin import routes
from .products import routes
