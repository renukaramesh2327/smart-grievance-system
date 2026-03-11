import os
from datetime import timedelta

class Config:
    # Secret key for JWT
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database (Render/Heroku use DATABASE_URL; fix postgres:// -> postgresql:// for SQLAlchemy)
    _db_url = os.environ.get('DATABASE_URL', 'sqlite:///grievance.db')
    if _db_url.startswith('postgres://'):
        _db_url = _db_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = _db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    JWT_SECRET_KEY = SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    
    # OTP Settings
    OTP_EXPIRY_MINUTES = 5
    OTP_MAX_ATTEMPTS = 5
    OTP_RATE_LIMIT_PER_HOUR = 3
    
    # Demo Mode (Free tier)
    DEMO_EMAIL_MODE = os.environ.get('DEMO_EMAIL_MODE', 'true').lower() == 'true'
    DEMO_SMS_MODE = os.environ.get('DEMO_SMS_MODE', 'true').lower() == 'true'
    
    # Email Configuration (Gmail SMTP - Free)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')  # Your Gmail address
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')  # Your Gmail App Password
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'Smart Grievance System <noreply@grievance.gov>')
    
    # ML Model paths
    MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ml', 'artifacts', 'model.joblib')
    VECTORIZER_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ml', 'artifacts', 'vectorizer.joblib')
    
    # App settings (8000 for local dev, use PORT env for production)
    PORT = int(os.environ.get('PORT', 8000))
