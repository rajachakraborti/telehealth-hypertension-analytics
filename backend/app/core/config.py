# Configuration settings for the backend application

import os


class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_default_secret_key'
    DEBUG = os.environ.get('DEBUG', 'False').lower() in ['true', '1']
    DATABASE_URI = os.environ.get('DATABASE_URI') or 'postgresql://user:password@localhost/dbname'
    LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'INFO')
    ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx', 'json', 'parquet'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit for uploads
    APP_HOST = os.environ.get('APP_HOST', '0.0.0.0')
    APP_PORT = int(os.environ.get('APP_PORT', '8000'))


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or 'sqlite:///:memory:'


# Default settings instance
settings = DevelopmentConfig()