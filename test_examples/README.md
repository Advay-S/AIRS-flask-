# Test Examples

This directory contains test scripts and examples for AIRS-flask API.

## Available Test Scripts

### 1. quick_test.sh
Quick bash script to test basic functionality.

**Usage:**
```bash
./quick_test.sh
```

**Requirements:**
- bash
- curl
- python3 (for JSON formatting)
- Application running on localhost:5000

**What it tests:**
- API availability
- Resume upload
- Candidate matching

---

### 2. test_api.py
Comprehensive Python test script.

**Usage:**
```bash
python test_api.py
```

**Requirements:**
- Python 3.6+
- requests library: `pip install requests`
- Application running on localhost:5000

**What it tests:**
- API status check
- Resume upload functionality
- Candidate matching with multiple job descriptions
- Error handling (invalid inputs)
- RankMatch endpoint

---

## Before Running Tests

1. **Start the application:**
   ```bash
   cd ..
   python app.py
   ```

2. **Verify it's running:**
   ```bash
   curl http://localhost:5000/
   ```

3. **Run tests:**
   ```bash
   # Bash tests
   ./quick_test.sh
   
   # Python tests
   python test_api.py
   ```

---

## Manual Testing Examples

### Upload a Resume

```bash
# Create sample resume
cat > sample_resume.txt << 'EOFSAMPLE'
Alice Johnson
Software Engineer
Skills: Python, Flask, PostgreSQL
Experience: 5 years in backend development
EOFSAMPLE

# Upload it
curl -X POST http://localhost:5000/api/resumecontroller/upload \
  -F "file=@sample_resume.txt"
```

### Search for Candidates

```bash
curl -X POST http://localhost:5000/api/resumecontroller/match \
  -H "Content-Type: application/json" \
  -d '{"jobDescription": "Python developer with Flask experience"}'
```

---

## Expected Results

### Successful Upload
```json
{
  "message": "Resume processed successfully!",
  "filename": "sample_resume.txt",
  "text_length": 123,
  "preview": "Alice Johnson..."
}
```

### Successful Match
```json
{
  "matches": [
    "Match Score: 0.85 | Alice Johnson - Software Engineer..."
  ],
  "detailed_results": [...],
  "count": 1
}
```

---

## Troubleshooting

**Connection Refused:**
- Make sure the application is running
- Check if port 5000 is accessible

**No Matches Found:**
- Upload at least one resume before searching
- Check that resume was uploaded successfully

**Module Not Found (Python):**
- Install requirements: `pip install requests`

For more detailed testing instructions, see [TESTING.md](../TESTING.md) in the root directory.
