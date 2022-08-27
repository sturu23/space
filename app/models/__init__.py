from app import db
from werkzeug.security import  generate_password_hash,check_password_hash
from flask_login import UserMixin, login_manager

from datetime import datetime

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    secret = db.Column(db.String(128))
    profile_pic = db.Column(db.String(20), nullable=True)
    account_created_time = db.Column(db.DateTime,default=datetime.utcnow)

    def __init__(self, username, email, password,secret,profile_pic):
        self.profile_pic = profile_pic
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.secret = secret


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()


    @classmethod
    def find_by_email(cls, email):
        email = cls.query.filter_by(email=email).first()
        if email:
            return email


class Statia(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('statia', lazy=True))
    post_pic = db.Column(db.String(20),nullable=True)
    created_post_date = db.Column(db.DateTime,default=datetime.utcnow)

    def __init__(self, title, content,user_id):
        self.title = title
        self.content = content
        self.user_id = user_id


    @classmethod
    def find_statia_by_id(cls,id):
        return cls.query.filter_by(id=id).first()


class EditProfile(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key= True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    username = db.Column(db.String(50))
    proffesion = db.Column(db.String(50))
    skills = db.Column(db.String(20))


    def __init__(self,user_id,username,proffesion,skills):
        self.user_id = user_id
        self.username = username
        self.proffesion = proffesion
        self.skills = skills


