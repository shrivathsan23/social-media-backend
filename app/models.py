from . import db
from enum import Enum
from datetime import datetime as dt

class InteractType(Enum):
    LIKE = 0
    COMMENT = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(128), nullable = False)
    posts = db.relationship('Post', backref = 'author', lazy = True)
    interactions = db.relationship('Interaction', backref = 'user', lazy = True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text, nullable = False)
    timestamp = db.Column(db.DateTime, default = dt.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    interactions = db.relationship('Interaction', backref = 'post', lazy = True)

class Interaction(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    interaction_type = db.Column(db.Enum(InteractType), nullable = False)
    content = db.Column(db.Text, nullable = True)
    timestamp = db.Column(db.DateTime, default = dt.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable = False)