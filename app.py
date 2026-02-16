from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db = SQLAlchemy(app)

# Import and register blueprints after db initialization to avoid circular imports
from routes.resume_routes import resume_bp
app.register_blueprint(resume_bp, url_prefix='/api/resumecontroller')

@app.route('/')
def index():
    return {
        'message': 'AI Resume Screener API',
        'version': '1.0.0',
        'endpoints': {
            'upload': '/api/resumecontroller/upload',
            'match': '/api/resumecontroller/match',
            'rankmatch': '/api/resumecontroller/rankmatch'
        }
    }

if __name__ == '__main__':
    # Debug mode controlled by FLASK_DEBUG environment variable
    # In production, set FLASK_DEBUG=False or use gunicorn
    debug_mode = app.config.get('DEBUG', False)
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
