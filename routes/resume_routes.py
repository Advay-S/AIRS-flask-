from flask import Blueprint, request, jsonify
from services.resume_service import ResumeService
from app import db

resume_bp = Blueprint('resume', __name__)

def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@resume_bp.route('/upload', methods=['POST'])
def upload_resume():
    """Upload and process resume file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'error': 'Invalid file type. Allowed types: pdf, doc, docx, txt'
            }), 400
        
        service = ResumeService(db.session)
        result = service.process_resume(file)
        
        return jsonify(result), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@resume_bp.route('/match', methods=['POST'])
def match_job():
    """Find resumes matching job description"""
    try:
        if request.is_json:
            data = request.get_json()
            job_description = data.get('jobDescription', '')
        else:
            job_description = request.get_data(as_text=True)
        
        if not job_description or len(job_description.strip()) == 0:
            return jsonify({'error': 'No job description provided'}), 400
        
        service = ResumeService(db.session)
        results = service.find_matching_resumes(job_description)
        
        return jsonify({
            'matches': [r['formatted'] for r in results],
            'detailed_results': results,
            'count': len(results)
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@resume_bp.route('/rankmatch', methods=['POST'])
def rank_match():
    """Rank and match resumes"""
    return match_job()
