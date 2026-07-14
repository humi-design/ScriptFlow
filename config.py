import os
from datetime import timedelta


class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'scriptflow-secret-key-change-this')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024


class ProductionConfig(Config):
    """Production - MySQL"""
    DEBUG = False
    
    # MySQL Database Configuration
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = os.environ.get('MYSQL_PORT', '3306')
    MYSQL_USER = os.environ.get('MYSQL_USER', '')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'scriptflow_db')
    
    # Construct MySQL connection string
    if MYSQL_USER and MYSQL_PASSWORD and MYSQL_DATABASE:
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@"
            f"{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"
        )
    else:
        raise ValueError("MySQL credentials not configured. Set MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE environment variables.")


class TestingConfig(Config):
    """Testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': ProductionConfig
}
