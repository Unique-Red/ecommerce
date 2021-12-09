from enum import unique
from shop import db
from datetime import datetime
from flask_login import UserMixin
import json

class Register(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(120), unique=False, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), unique=False, nullable=False)
    country = db.Column(db.String(120), unique=False, nullable=False)
    state = db.Column(db.String(120), unique=False, nullable=False)
    city = db.Column(db.String(120), unique=False, nullable=False)
    contact = db.Column(db.String(120), unique=False, nullable=False)
    address = db.Column(db.String(120), unique=False, nullable=False)

    profile = db.Column(db.String(180), unique=False, nullable=False, default="profile.jpg")
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Register %r>' % self.name

class JsonEncodedDict(db.TypeDecorator):
    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)
    def process_result_value(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.loads(value)
        

class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    orders = db.Column(JsonEncodedDict)

    def __repr__(self):
        return '<CustomerOrder %r>' % self.invoice
    

    

db.create_all()