# Testing Guide for AIRS-flask Application

This guide explains how to test the AI Resume Shortlisting application from different user perspectives.

## Table of Contents
1. [Quick Start](#quick-start)
2. [Testing as a User (Candidate)](#testing-as-a-user-candidate)
3. [Testing as HR/Recruiter](#testing-as-hrrecruiter)
4. [Complete Testing Workflow](#complete-testing-workflow)
5. [Testing Tools](#testing-tools)
6. [Sample Test Data](#sample-test-data)

---

## Quick Start

### Prerequisites
1. Application is running (see README.md for setup)
2. Database is initialized with pgvector extension
3. Port 5000 is accessible

### Verify Application is Running

```bash
# Test the root endpoint
curl http://localhost:5000/

# Expected response:
# {
#   "message": "AI Resume Screener API",
#   "version": "1.0.0",
#   "endpoints": {
#     "upload": "/api/resumecontroller/upload",
#     "match": "/api/resumecontroller/match",
#     "rankmatch": "/api/resumecontroller/rankmatch"
#   }
# }
```

---

## Testing as a User (Candidate)

As a candidate/user, your primary action is **uploading your resume** to the system.

### Test Scenario 1: Upload Resume (Text File)

**Step 1:** Create a sample resume file

```bash
cat > sample_resume.txt << 'EOF'
John Doe
Senior Software Engineer

CONTACT:
Email: john.doe@example.com
Phone: (555) 123-4567
Location: San Francisco, CA

SUMMARY:
Experienced software engineer with 8 years in full-stack development. 
Expert in Python, Flask, Django, and PostgreSQL. Strong background in 
building scalable web applications and RESTful APIs.

SKILLS:
- Programming: Python, JavaScript, Java, SQL
- Frameworks: Flask, Django, React, Node.js
- Databases: PostgreSQL, MongoDB, Redis
- Tools: Git, Docker, Kubernetes, AWS
- AI/ML: TensorFlow, scikit-learn, pandas

EXPERIENCE:
Senior Software Engineer | Tech Corp | 2020-Present
- Built microservices architecture serving 1M+ users
- Developed RESTful APIs using Flask and PostgreSQL
- Implemented CI/CD pipelines with GitHub Actions

Software Engineer | StartupXYZ | 2016-2020
- Created web applications using Django and React
- Managed PostgreSQL databases with 100TB+ data
- Mentored junior developers

EDUCATION:
Bachelor of Science in Computer Science
University of California, Berkeley | 2012-2016
EOF
```

**Step 2:** Upload the resume

```bash
curl -X POST http://localhost:5000/api/resumecontroller/upload \
  -F "file=@sample_resume.txt"
```

**Expected Response:**
```json
{
  "message": "Resume processed successfully!",
  "filename": "sample_resume.txt",
  "text_length": 1234,
  "preview": "John Doe\nSenior Software Engineer\n\nCONTACT:..."
}
```

### Test Scenario 2: Upload Resume (PDF)

If you have a PDF resume:

```bash
curl -X POST http://localhost:5000/api/resumecontroller/upload \
  -F "file=@my_resume.pdf"
```

### Test Scenario 3: Upload Resume (DOCX)

If you have a Word document:

```bash
curl -X POST http://localhost:5000/api/resumecontroller/upload \
  -F "file=@my_resume.docx"
```

### Test Scenario 4: Error Handling (Invalid File Type)

```bash
# Try uploading an unsupported file type
echo "test" > test.jpg
curl -X POST http://localhost:5000/api/resumecontroller/upload \
  -F "file=@test.jpg"

# Expected error:
# {
#   "error": "Invalid file type. Allowed types: pdf, doc, docx, txt"
# }
```

### Test Scenario 5: Error Handling (No File)

```bash
curl -X POST http://localhost:5000/api/resumecontroller/upload

# Expected error:
# {
#   "error": "No file provided"
# }
```

---

## Testing as HR/Recruiter

As an HR professional, you will:
1. **Upload multiple candidate resumes** (same as User testing above)
2. **Search for candidates** matching job requirements

### Test Scenario 1: Match Candidates to Job Description

**Step 1:** First, upload several candidate resumes (repeat upload tests above with different resumes)

**Step 2:** Create a job description

```bash
cat > job_description.txt << 'EOF'
We are looking for a Senior Python Developer with the following qualifications:

REQUIRED SKILLS:
- 5+ years experience with Python
- Expert knowledge of Flask or Django frameworks
- Strong PostgreSQL database experience
- REST API development
- Docker and Kubernetes

PREFERRED SKILLS:
- AI/ML experience with TensorFlow or PyTorch
- AWS or cloud platform experience
- Microservices architecture
- CI/CD pipeline experience

RESPONSIBILITIES:
- Design and develop scalable backend services
- Build RESTful APIs for mobile and web applications
- Optimize database queries and performance
- Collaborate with cross-functional teams
- Mentor junior developers
EOF
```

**Step 3:** Find matching candidates

```bash
curl -X POST http://localhost:5000/api/resumecontroller/match \
  -H "Content-Type: application/json" \
  -d @- << 'EOF'
{
  "jobDescription": "We are looking for a Senior Python Developer with 5+ years experience. Must have Flask, Django, PostgreSQL, REST API, Docker, and Kubernetes skills. AI/ML experience with TensorFlow is a plus. Responsibilities include building scalable backend services and RESTful APIs."
}
EOF
```

**Expected Response:**
```json
{
  "matches": [
    "Match Score: 0.87 | John Doe\nSenior Software Engineer...",
    "Match Score: 0.79 | Jane Smith\nFull Stack Developer...",
    "Match Score: 0.72 | Bob Johnson\nBackend Engineer..."
  ],
  "detailed_results": [
    {
      "id": 1,
      "score": 0.87,
      "text": "John Doe\nSenior Software Engineer\n...",
      "formatted": "Match Score: 0.87 | John Doe..."
    }
  ],
  "count": 3
}
```

### Test Scenario 2: Short Job Description

```bash
curl -X POST http://localhost:5000/api/resumecontroller/match \
  -H "Content-Type: application/json" \
  -d '{"jobDescription": "Python developer with Flask experience"}'
```

### Test Scenario 3: Using /rankmatch Endpoint

The `/rankmatch` endpoint is an alias for `/match`:

```bash
curl -X POST http://localhost:5000/api/resumecontroller/rankmatch \
  -H "Content-Type: application/json" \
  -d '{"jobDescription": "Looking for Java Spring Boot developer"}'
```

### Test Scenario 4: Plain Text Job Description

You can also send job description as plain text:

```bash
curl -X POST http://localhost:5000/api/resumecontroller/match \
  -H "Content-Type: text/plain" \
  -d "Looking for a data scientist with Python, machine learning, and statistical analysis experience"
```

### Test Scenario 5: Error Handling (Empty Job Description)

```bash
curl -X POST http://localhost:5000/api/resumecontroller/match \
  -H "Content-Type: application/json" \
  -d '{"jobDescription": ""}'

# Expected error:
# {
#   "error": "No job description provided"
# }
```

---

## Complete Testing Workflow

Here's a complete end-to-end testing workflow:

### Step 1: Start the Application

```bash
# In terminal 1
cd /path/to/AIRS-flask-
source venv/bin/activate
export FLASK_DEBUG=True
python app.py
```

### Step 2: Verify Application Started

```bash
# In terminal 2
curl http://localhost:5000/
```

### Step 3: Upload Multiple Resumes

Create 3 sample resumes with different profiles:

**Resume 1: Python Backend Developer**
```bash
cat > resume1.txt << 'EOF'
Alice Johnson
Python Backend Developer

Skills: Python, Flask, Django, PostgreSQL, Redis, Docker
Experience: 6 years building REST APIs and microservices
Education: MS Computer Science

Projects:
- Built scalable e-commerce backend handling 10K requests/sec
- Developed real-time analytics platform with Flask and PostgreSQL
- Implemented caching layer with Redis
EOF

curl -X POST http://localhost:5000/api/resumecontroller/upload \
  -F "file=@resume1.txt"
```

**Resume 2: Full Stack Developer**
```bash
cat > resume2.txt << 'EOF'
Bob Smith
Full Stack Developer

Skills: JavaScript, React, Node.js, MongoDB, AWS, Python
Experience: 4 years in web development
Education: BS Software Engineering

Projects:
- Created responsive web applications with React
- Built RESTful APIs with Node.js and Express
- Deployed applications on AWS with Docker
EOF

curl -X POST http://localhost:5000/api/resumecontroller/upload \
  -F "file=@resume2.txt"
```

**Resume 3: Data Scientist**
```bash
cat > resume3.txt << 'EOF'
Carol Davis
Data Scientist

Skills: Python, TensorFlow, scikit-learn, pandas, SQL, Jupyter
Experience: 5 years in machine learning and data analysis
Education: PhD in Statistics

Projects:
- Built predictive models with 95% accuracy
- Developed NLP systems for sentiment analysis
- Created data pipelines with Python and SQL
EOF

curl -X POST http://localhost:5000/api/resumecontroller/upload \
  -F "file=@resume3.txt"
```

### Step 4: Search for Backend Developer

```bash
curl -X POST http://localhost:5000/api/resumecontroller/match \
  -H "Content-Type: application/json" \
  -d '{
    "jobDescription": "Looking for a Python backend developer with Flask and PostgreSQL experience for building REST APIs and microservices."
  }'
```

**Expected:** Alice Johnson should be the top match (highest score)

### Step 5: Search for Data Scientist

```bash
curl -X POST http://localhost:5000/api/resumecontroller/match \
  -H "Content-Type: application/json" \
  -d '{
    "jobDescription": "Seeking a data scientist with machine learning, TensorFlow, and Python expertise for predictive modeling projects."
  }'
```

**Expected:** Carol Davis should be the top match

### Step 6: Search for Full Stack Developer

```bash
curl -X POST http://localhost:5000/api/resumecontroller/match \
  -H "Content-Type: application/json" \
  -d '{
    "jobDescription": "Need a full stack developer with React, Node.js, and cloud deployment experience."
  }'
```

**Expected:** Bob Smith should be the top match

---

## Testing Tools

### 1. Using cURL (Command Line)

Most examples above use `curl`. This is the simplest way to test the API.

### 2. Using Python Script

Create a Python test script:

```python
# test_api.py
import requests
import json

BASE_URL = "http://localhost:5000"

def test_upload_resume(filename):
    """Upload a resume file"""
    url = f"{BASE_URL}/api/resumecontroller/upload"
    
    with open(filename, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files)
    
    print(f"Upload {filename}:")
    print(json.dumps(response.json(), indent=2))
    print()
    return response.json()

def test_match_candidates(job_description):
    """Find matching candidates"""
    url = f"{BASE_URL}/api/resumecontroller/match"
    
    data = {"jobDescription": job_description}
    response = requests.post(url, json=data)
    
    print(f"Match results:")
    result = response.json()
    print(f"Found {result.get('count', 0)} matches")
    
    for match in result.get('matches', []):
        print(f"  - {match}")
    print()
    return result

if __name__ == "__main__":
    # Test uploads
    test_upload_resume("resume1.txt")
    test_upload_resume("resume2.txt")
    test_upload_resume("resume3.txt")
    
    # Test matching
    test_match_candidates(
        "Looking for a Python developer with Flask and PostgreSQL experience"
    )
```

Run it:
```bash
python test_api.py
```

### 3. Using Postman

1. **Import Collection:**
   - Create new collection: "AIRS Resume API"
   
2. **Add Upload Request:**
   - Method: POST
   - URL: `http://localhost:5000/api/resumecontroller/upload`
   - Body: form-data
   - Key: `file` (type: File)
   - Select your resume file

3. **Add Match Request:**
   - Method: POST
   - URL: `http://localhost:5000/api/resumecontroller/match`
   - Headers: `Content-Type: application/json`
   - Body: raw (JSON)
   ```json
   {
     "jobDescription": "Your job description here"
   }
   ```

### 4. Using HTTPie (Alternative to cURL)

```bash
# Install HTTPie
pip install httpie

# Upload resume
http -f POST localhost:5000/api/resumecontroller/upload file@resume.txt

# Match candidates
http POST localhost:5000/api/resumecontroller/match jobDescription="Python developer with Flask"
```

---

## Sample Test Data

### Sample Resume Templates

**Software Engineer Resume:**
```text
[Name]
Software Engineer

SKILLS:
- Languages: Python, Java, JavaScript
- Frameworks: Flask, Django, Spring Boot
- Databases: PostgreSQL, MySQL, MongoDB
- Tools: Git, Docker, Jenkins

EXPERIENCE:
[Years] years of experience in software development
Developed web applications and REST APIs
Worked with agile teams

EDUCATION:
Bachelor's degree in Computer Science
```

**Data Analyst Resume:**
```text
[Name]
Data Analyst

SKILLS:
- Analysis: SQL, Python, R, Excel
- Visualization: Tableau, PowerBI
- Statistics: Hypothesis testing, regression
- Tools: Jupyter, pandas, numpy

EXPERIENCE:
[Years] years analyzing business data
Created dashboards and reports
Provided data-driven insights

EDUCATION:
Bachelor's degree in Statistics or related field
```

**DevOps Engineer Resume:**
```text
[Name]
DevOps Engineer

SKILLS:
- Cloud: AWS, Azure, GCP
- Containers: Docker, Kubernetes
- CI/CD: Jenkins, GitLab CI, GitHub Actions
- Infrastructure: Terraform, Ansible
- Monitoring: Prometheus, Grafana

EXPERIENCE:
[Years] years in DevOps and infrastructure
Managed cloud deployments
Automated CI/CD pipelines

EDUCATION:
Bachelor's degree in Computer Science
```

### Sample Job Descriptions

**Backend Developer Position:**
```text
We're seeking a Backend Developer with:
- 3+ years Python experience
- Flask or Django framework knowledge
- PostgreSQL database skills
- REST API development
- Microservices architecture understanding
- Docker experience preferred
```

**Data Scientist Position:**
```text
Looking for a Data Scientist with:
- Strong Python programming skills
- Machine learning expertise (TensorFlow, scikit-learn)
- Statistical analysis experience
- SQL and database knowledge
- Experience with pandas, numpy
- PhD or MS in related field preferred
```

**DevOps Position:**
```text
Hiring a DevOps Engineer with:
- AWS or cloud platform expertise
- Kubernetes and Docker experience
- CI/CD pipeline development
- Infrastructure as code (Terraform)
- Linux administration
- Monitoring and logging tools
```

---

## Interpreting Results

### Understanding Match Scores

The application returns **similarity scores** between 0 and 1:

- **0.9 - 1.0**: Excellent match - Resume closely matches job requirements
- **0.8 - 0.9**: Very good match - Strong alignment with requirements
- **0.7 - 0.8**: Good match - Candidate has many relevant skills
- **0.6 - 0.7**: Moderate match - Some relevant experience
- **< 0.6**: Lower match - Limited relevant experience

### Example Result Analysis

```json
{
  "matches": [
    "Match Score: 0.87 | Alice - Python, Flask, PostgreSQL, 6 years...",
    "Match Score: 0.72 | Bob - Python, Django, MySQL, 3 years...",
    "Match Score: 0.58 | Carol - Java, Spring Boot, Oracle, 5 years..."
  ]
}
```

**Analysis:**
- **Alice (0.87)**: Best candidate - Has most of the required skills
- **Bob (0.72)**: Good candidate - Has Python but different database
- **Carol (0.58)**: Weaker match - Different tech stack

---

## Troubleshooting

### Issue: "Connection refused"
**Solution:** Make sure the application is running on port 5000

```bash
# Check if app is running
curl http://localhost:5000/
```

### Issue: "Database error"
**Solution:** Ensure PostgreSQL is running and database is initialized

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Initialize database
psql -U postgres -d resume_db -f database/init.sql
```

### Issue: "No matches found"
**Solution:** Upload more resumes first

```bash
# Upload at least 1 resume before searching
curl -X POST http://localhost:5000/api/resumecontroller/upload \
  -F "file=@sample_resume.txt"
```

### Issue: "Model loading error"
**Solution:** First run downloads the AI model (~80MB), ensure internet connection

---

## Best Practices

### For Users (Candidates):
1. ✅ Use detailed resumes with skills, experience, and education
2. ✅ Include keywords relevant to your target roles
3. ✅ Use standard resume formats (PDF, DOCX, TXT)
4. ✅ Keep file size under 16MB
5. ❌ Don't use images or scanned resumes (text must be extractable)

### For HR/Recruiters:
1. ✅ Write detailed job descriptions with specific skills
2. ✅ Include both required and preferred qualifications
3. ✅ Mention technology stack and tools
4. ✅ Review top 5-10 matches for best results
5. ✅ Use scores as guidance, not absolute decision criteria

---

## Advanced Testing

### Load Testing

Test with multiple concurrent uploads:

```bash
# Upload 10 resumes simultaneously
for i in {1..10}; do
  curl -X POST http://localhost:5000/api/resumecontroller/upload \
    -F "file=@resume${i}.txt" &
done
wait
```

### Performance Testing

Measure response times:

```bash
# Test upload performance
time curl -X POST http://localhost:5000/api/resumecontroller/upload \
  -F "file=@large_resume.pdf"

# Test matching performance
time curl -X POST http://localhost:5000/api/resumecontroller/match \
  -H "Content-Type: application/json" \
  -d '{"jobDescription": "Python developer"}'
```

---

## Summary

**As a User:** Upload your resume using the `/upload` endpoint
**As HR:** Upload candidate resumes, then use `/match` to find the best candidates

For questions or issues, refer to the main README.md or check the application logs.
