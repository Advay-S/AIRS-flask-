import os

class Config:
    """Application configuration"""
    
    # Debug mode (should be False in production)
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:password@localhost:5432/resume_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # File upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = '/tmp/uploads'
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
    
    # Model settings
    MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'
    EMBEDDING_DIMENSION = 384
    
    # API settings
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
