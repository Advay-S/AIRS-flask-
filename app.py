from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes.resume_routes import resume_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db = SQLAlchemy(app)

# Register blueprints
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
    app.run(debug=True, host='0.0.0.0', port=5000)
