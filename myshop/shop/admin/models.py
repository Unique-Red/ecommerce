from shop import db
#from flask_login import UserMixin

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(120), unique=False, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), unique=False, nullable=False)
    profile = db.Column(db.String(180), unique=False, nullable=False, default="profile.jpg")

    def __repr__(self):
        return '<User %r>' % self.username

db.create_all()