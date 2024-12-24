class Config:
    SECRET_KEY = 'secret-key'
    JWT_SECRET_KEY = 'jwt-secret-key'
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///social_media.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False