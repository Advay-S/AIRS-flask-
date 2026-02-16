# AIRS-flask - AI Resume Shortlisting Application

A Flask-based application for intelligent resume screening and matching using AI embeddings and vector similarity search.

## 🚀 Features

- **Resume Upload & Processing**: Extract text from PDF, DOCX, and TXT files
- **AI-Powered Matching**: Uses sentence transformers for semantic understanding
- **Vector Similarity Search**: Efficient resume matching using PostgreSQL with pgvector
- **RESTful API**: Clean API endpoints for integration
- **Scalable Architecture**: Modular design with services, routes, and models

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL 12+ with pgvector extension
- 2GB+ RAM (for transformer models)

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Advay-S/AIRS-flask-.git
cd AIRS-flask-
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up PostgreSQL with pgvector

#### Install pgvector extension:

```bash
# Ubuntu/Debian
sudo apt-get install postgresql-15-pgvector

# macOS (with Homebrew)
brew install pgvector
```

#### Create database and initialize schema:

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE resume_db;

# Connect to the database
\c resume_db

# Run initialization script
\i database/init.sql
```

### 5. Configure environment (optional)

Create a `.env` file for custom configuration:

```bash
DATABASE_URL=postgresql://postgres:password@localhost:5432/resume_db
FLASK_DEBUG=True  # Set to False in production for security
```

**Security Note:** Debug mode should NEVER be enabled in production as it can expose sensitive information and allow arbitrary code execution.

## 🚀 Running the Application

### Development mode:

```bash
# Enable debug mode for development
export FLASK_DEBUG=True
python app.py
```

The application will start on `http://0.0.0.0:5000`

### Production mode with Gunicorn:

```bash
# Disable debug mode in production (default)
export FLASK_DEBUG=False
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📡 API Endpoints

### 1. Root Endpoint

```bash
GET /
```

Returns API information and available endpoints.

**Response:**
```json
{
  "message": "AI Resume Screener API",
  "version": "1.0.0",
  "endpoints": {
    "upload": "/api/resumecontroller/upload",
    "match": "/api/resumecontroller/match",
    "rankmatch": "/api/resumecontroller/rankmatch"
  }
}
```

### 2. Upload Resume

```bash
POST /api/resumecontroller/upload
Content-Type: multipart/form-data
```

Upload a resume file (PDF, DOCX, or TXT).

**Request:**
```bash
curl -X POST http://localhost:5000/api/resumecontroller/upload \
  -F "file=@resume.pdf"
```

**Response:**
```json
{
  "message": "Resume processed successfully!",
  "filename": "resume.pdf",
  "text_length": 1234,
  "preview": "John Doe\nSoftware Engineer..."
}
```

### 3. Match Resumes

```bash
POST /api/resumecontroller/match
Content-Type: application/json
```

Find resumes matching a job description.

**Request:**
```bash
curl -X POST http://localhost:5000/api/resumecontroller/match \
  -H "Content-Type: application/json" \
  -d '{
    "jobDescription": "Looking for a Python developer with Flask experience"
  }'
```

**Response:**
```json
{
  "matches": [
    "Match Score: 0.85 | John Doe - Python Developer with 5 years...",
    "Match Score: 0.78 | Jane Smith - Full Stack Engineer..."
  ],
  "detailed_results": [
    {
      "id": 1,
      "score": 0.85,
      "text": "Full resume text...",
      "formatted": "Match Score: 0.85 | John Doe..."
    }
  ],
  "count": 2
}
```

### 4. Rank Match

```bash
POST /api/resumecontroller/rankmatch
```

Alias for `/match` endpoint with identical functionality.

## 🏗️ Project Structure

```
AIRS-flask-/
├── app.py                          # Main Flask application
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore patterns
├── README.md                       # Documentation
├── models/
│   └── __init__.py                 # Models package
├── services/
│   ├── __init__.py                 # Services package
│   ├── embedding_service.py        # Text embedding generation
│   ├── document_parser.py          # Document text extraction
│   └── resume_service.py           # Resume processing logic
├── routes/
│   ├── __init__.py                 # Routes package
│   └── resume_routes.py            # API endpoints
└── database/
    └── init.sql                    # Database schema
```

## 🔧 Configuration

Edit `config.py` to customize:

- **Database Connection**: `SQLALCHEMY_DATABASE_URI`
- **File Upload Settings**: `MAX_CONTENT_LENGTH`, `ALLOWED_EXTENSIONS`
- **Embedding Model**: `MODEL_NAME` (default: all-MiniLM-L6-v2)
- **API Settings**: JSON formatting options

## 🧪 Testing the Application

### Test Resume Upload:

```bash
# Create a sample resume
echo "John Doe
Software Engineer
Skills: Python, Flask, PostgreSQL
Experience: 5 years in web development" > sample_resume.txt

# Upload the resume
curl -X POST http://localhost:5000/api/resumecontroller/upload \
  -F "file=@sample_resume.txt"
```

### Test Resume Matching:

```bash
curl -X POST http://localhost:5000/api/resumecontroller/match \
  -H "Content-Type: application/json" \
  -d '{
    "jobDescription": "Python developer with database experience"
  }'
```

## 🔍 How It Works

1. **Upload**: Resume files are parsed to extract text content
2. **Embedding**: Text is converted to 384-dimensional vectors using sentence transformers
3. **Storage**: Vectors are stored in PostgreSQL with pgvector extension
4. **Matching**: Job descriptions are embedded and compared using cosine similarity
5. **Ranking**: Results are sorted by similarity score and returned

## 📦 Dependencies

- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **sentence-transformers**: Text embedding models
- **pgvector**: PostgreSQL vector extension
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX text extraction
- **torch**: PyTorch for transformer models

## 🐛 Troubleshooting

### Database Connection Issues:

- Verify PostgreSQL is running: `sudo systemctl status postgresql`
- Check database credentials in `config.py`
- Ensure pgvector extension is installed

### Model Loading Issues:

- First run downloads ~80MB model (sentence-transformers/all-MiniLM-L6-v2)
- Ensure stable internet connection
- Check available disk space

### File Upload Issues:

- Verify file size is under 16MB
- Check file format is PDF, DOCX, or TXT
- Ensure file is not corrupted

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 👥 Authors

- Advay S - Initial work

## 🙏 Acknowledgments

- Sentence Transformers library for embeddings
- pgvector for efficient vector operations
- Flask community for excellent documentation

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ using Flask, AI, and PostgreSQL**
