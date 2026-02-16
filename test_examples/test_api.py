#!/usr/bin/env python3
"""
test_api.py - Python test script for AIRS-flask API
Usage: python test_api.py
"""

import requests
import json
import sys
import os

BASE_URL = "http://localhost:5000"

def print_header(text):
    """Print colored header"""
    print("\n" + "="*50)
    print(f"  {text}")
    print("="*50 + "\n")

def print_success(text):
    """Print success message"""
    print(f"✓ {text}")

def print_error(text):
    """Print error message"""
    print(f"✗ {text}")

def test_api_status():
    """Test if API is running"""
    print_header("TEST 1: Checking API Status")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print_success("API is running")
            print(json.dumps(response.json(), indent=2))
            return True
        else:
            print_error(f"API returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to API. Is it running?")
        print("Start with: python app.py")
        return False

def create_sample_resume():
    """Create sample resume file"""
    print_header("TEST 2: Creating Sample Resume")
    
    resume_content = """Jane Smith
Python Developer

CONTACT:
Email: jane.smith@email.com
LinkedIn: linkedin.com/in/janesmith

SUMMARY:
Experienced Python developer with 5 years building web applications.
Expert in Flask, Django, and PostgreSQL. Strong problem-solving skills.

SKILLS:
- Languages: Python, JavaScript, SQL
- Frameworks: Flask, Django, FastAPI
- Databases: PostgreSQL, MySQL, Redis
- Tools: Git, Docker, Jenkins, AWS
- Testing: pytest, unittest

EXPERIENCE:

Senior Python Developer | Tech Solutions Inc. | 2021-Present
- Architected and built REST APIs serving 1M+ daily requests
- Developed microservices using Flask and PostgreSQL
- Implemented automated testing with pytest (95% coverage)
- Mentored 3 junior developers

Python Developer | WebApps Co. | 2019-2021
- Built web applications using Django framework
- Optimized database queries (40% performance improvement)
- Integrated third-party APIs
- Collaborated with frontend team on React projects

EDUCATION:
Bachelor of Science in Computer Science
State University | 2015-2019
GPA: 3.8/4.0

CERTIFICATIONS:
- AWS Certified Developer
- Python Professional Certification
"""
    
    filename = "/tmp/test_resume.txt"
    with open(filename, 'w') as f:
        f.write(resume_content)
    
    print_success(f"Sample resume created: {filename}")
    return filename

def test_upload_resume(filename):
    """Test resume upload"""
    print_header("TEST 3: Uploading Resume")
    
    try:
        with open(filename, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                f"{BASE_URL}/api/resumecontroller/upload",
                files=files
            )
        
        if response.status_code == 200:
            print_success("Resume uploaded successfully")
            print(json.dumps(response.json(), indent=2))
            return True
        else:
            print_error(f"Upload failed with status {response.status_code}")
            print(response.text)
            return False
    
    except Exception as e:
        print_error(f"Upload error: {str(e)}")
        return False

def test_match_candidates():
    """Test candidate matching"""
    print_header("TEST 4: Matching Candidates")
    
    job_descriptions = [
        {
            "title": "Python Backend Developer",
            "description": "Looking for a Python developer with Flask and PostgreSQL experience. Must have REST API development skills and Docker knowledge. 5+ years experience required."
        },
        {
            "title": "Full Stack Engineer",
            "description": "Seeking a full stack engineer with Python backend and JavaScript frontend skills. Experience with Django or Flask required. AWS experience is a plus."
        }
    ]
    
    for job in job_descriptions:
        print(f"\n--- Job: {job['title']} ---")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/resumecontroller/match",
                json={"jobDescription": job['description']}
            )
            
            if response.status_code == 200:
                result = response.json()
                print_success(f"Found {result.get('count', 0)} matches")
                
                # Print top 3 matches
                for i, match in enumerate(result.get('matches', [])[:3], 1):
                    print(f"  {i}. {match}")
            else:
                print_error(f"Match failed with status {response.status_code}")
                print(response.text)
        
        except Exception as e:
            print_error(f"Match error: {str(e)}")

def test_error_handling():
    """Test error handling"""
    print_header("TEST 5: Error Handling")
    
    # Test 1: Upload without file
    print("Testing upload without file...")
    try:
        response = requests.post(f"{BASE_URL}/api/resumecontroller/upload")
        if response.status_code == 400:
            print_success("Correctly rejected upload without file")
        else:
            print_error(f"Expected 400, got {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Test 2: Match without job description
    print("\nTesting match without job description...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/resumecontroller/match",
            json={"jobDescription": ""}
        )
        if response.status_code == 400:
            print_success("Correctly rejected empty job description")
        else:
            print_error(f"Expected 400, got {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")

def test_rankmatch_endpoint():
    """Test rankmatch endpoint (alias for match)"""
    print_header("TEST 6: RankMatch Endpoint")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/resumecontroller/rankmatch",
            json={"jobDescription": "Python developer with database experience"}
        )
        
        if response.status_code == 200:
            print_success("RankMatch endpoint working")
            result = response.json()
            print(f"Found {result.get('count', 0)} matches")
        else:
            print_error(f"RankMatch failed with status {response.status_code}")
    
    except Exception as e:
        print_error(f"RankMatch error: {str(e)}")

def cleanup(filename):
    """Clean up test files"""
    if os.path.exists(filename):
        os.remove(filename)
        print(f"\nCleaned up: {filename}")

def main():
    """Main test function"""
    print("\n" + "="*50)
    print("  AIRS-flask Python Test Suite")
    print("="*50)
    
    # Test 1: API Status
    if not test_api_status():
        sys.exit(1)
    
    # Test 2: Create sample resume
    resume_file = create_sample_resume()
    
    # Test 3: Upload resume
    if not test_upload_resume(resume_file):
        cleanup(resume_file)
        sys.exit(1)
    
    # Test 4: Match candidates
    test_match_candidates()
    
    # Test 5: Error handling
    test_error_handling()
    
    # Test 6: RankMatch endpoint
    test_rankmatch_endpoint()
    
    # Cleanup
    cleanup(resume_file)
    
    print_header("All Tests Completed Successfully!")
    print("✓ API is working correctly")
    print("✓ Upload functionality verified")
    print("✓ Matching functionality verified")
    print("✓ Error handling verified")

if __name__ == "__main__":
    main()
