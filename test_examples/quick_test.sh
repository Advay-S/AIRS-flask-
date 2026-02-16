#!/bin/bash
# quick_test.sh - Quick test script for AIRS-flask API
# Usage: ./quick_test.sh

set -e

BASE_URL="http://localhost:5000"
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  AIRS-flask Quick Test Script${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Test 1: Check if API is running
echo -e "${BLUE}[TEST 1] Checking if API is running...${NC}"
if curl -s "${BASE_URL}/" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ API is running${NC}"
    curl -s "${BASE_URL}/" | python3 -m json.tool
else
    echo -e "${RED}✗ API is not running. Please start the application first.${NC}"
    echo "Run: python app.py"
    exit 1
fi
echo ""

# Test 2: Create sample resume
echo -e "${BLUE}[TEST 2] Creating sample resume...${NC}"
cat > /tmp/sample_resume.txt << 'EOF'
John Doe
Senior Software Engineer

CONTACT:
Email: john.doe@example.com
Phone: (555) 123-4567

SKILLS:
- Python, Flask, Django
- PostgreSQL, MongoDB
- Docker, Kubernetes
- REST API Development

EXPERIENCE:
Senior Engineer | Tech Corp | 2020-Present
- Built scalable microservices with Flask
- Designed REST APIs handling 10K+ requests/sec
- Managed PostgreSQL databases

Software Engineer | StartupXYZ | 2016-2020
- Developed web applications with Django
- Implemented CI/CD pipelines

EDUCATION:
BS Computer Science | UC Berkeley | 2016
EOF
echo -e "${GREEN}✓ Sample resume created${NC}"
echo ""

# Test 3: Upload resume
echo -e "${BLUE}[TEST 3] Uploading resume...${NC}"
UPLOAD_RESPONSE=$(curl -s -X POST "${BASE_URL}/api/resumecontroller/upload" \
    -F "file=@/tmp/sample_resume.txt")

if echo "$UPLOAD_RESPONSE" | grep -q "Resume processed successfully"; then
    echo -e "${GREEN}✓ Resume uploaded successfully${NC}"
    echo "$UPLOAD_RESPONSE" | python3 -m json.tool
else
    echo -e "${RED}✗ Resume upload failed${NC}"
    echo "$UPLOAD_RESPONSE"
    exit 1
fi
echo ""

# Test 4: Search for matching candidates
echo -e "${BLUE}[TEST 4] Searching for matching candidates...${NC}"
MATCH_RESPONSE=$(curl -s -X POST "${BASE_URL}/api/resumecontroller/match" \
    -H "Content-Type: application/json" \
    -d '{"jobDescription": "Looking for a Python developer with Flask and PostgreSQL experience for building REST APIs"}')

if echo "$MATCH_RESPONSE" | grep -q "matches"; then
    echo -e "${GREEN}✓ Match search successful${NC}"
    echo "$MATCH_RESPONSE" | python3 -m json.tool
else
    echo -e "${RED}✗ Match search failed${NC}"
    echo "$MATCH_RESPONSE"
    exit 1
fi
echo ""

# Clean up
rm -f /tmp/sample_resume.txt

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✓ All tests passed!${NC}"
echo -e "${BLUE}========================================${NC}"
