from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from app import db, bcrypt
from app.models import User

bp = Blueprint('auth', __name__)

@bp.route('/register', methods = ['POST'])
def register():
    data = request.json
    
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(username = data['username'], email = data['email'], password = hashed_password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'User registered successfully'
    }), 201

@bp.route('/login', methods = ['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email = data['email']).first()

    if user and bcrypt.check_password_hash(user.password, data['password']):
        token = create_access_token(identity = user.id)

        return jsonify({
            'token': token
        }), 200
    
    return jsonify({
        'error': 'Invalid credentials'
    }), 401