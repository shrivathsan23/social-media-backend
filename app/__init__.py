from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app)

    with app.app_context():
        from .routes import auth, posts, interactions

        app.register_blueprint(auth.bp, url_prefix = '/auth')
        app.register_blueprint(posts.bp, url_prefix = '/posts')
        app.register_blueprint(interactions.bp, url_prefix = '/interactions')

        db.create_all()
    
    return app