from typing import List, Dict
import numpy as np
from werkzeug.datastructures import FileStorage
from sqlalchemy import text
from services.document_parser import DocumentParser
from services.embedding_service import get_embedding_service

class ResumeService:
    """Handle resume processing and matching"""
    
    def __init__(self, db_session):
        """
        Initialize resume service
        
        Args:
            db_session: SQLAlchemy database session
        """
        self.db = db_session
        self.parser = DocumentParser()
        self.embedding_service = get_embedding_service()
    
    def process_resume(self, file: FileStorage) -> Dict[str, str]:
        """
        Process uploaded resume file
        
        Args:
            file: Uploaded file from request
            
        Returns:
            Dictionary with success message and extracted text preview
        """
        print("--- CHECKPOINT 1: Service started ---")
        
        try:
            print("--- CHECKPOINT 2: Getting Stream ---")
            filename = file.filename
            
            print("--- CHECKPOINT 3: Calling Parser ---")
            raw_text = self.parser.extract_from_stream(file.stream, filename)
            
            if not raw_text or len(raw_text.strip()) == 0:
                raise ValueError("No text could be extracted from the document")
            
            print(f"--- CHECKPOINT 4: Text extracted ({len(raw_text)} chars) ---")
            
            print("--- CHECKPOINT 5: Generating embeddings ---")
            vectors = self.embedding_service.return_embeds(raw_text)
            
            # Convert numpy array to list for PostgreSQL
            vec_list = vectors.tolist()
            
            print("--- CHECKPOINT 6: Inserting into db! ---")
            sql = text("""
                INSERT INTO candidate_profiles (full_text, embedding) 
                VALUES (:text, :embedding::vector)
            """)
            
            self.db.execute(sql, {
                'text': raw_text,
                'embedding': str(vec_list)
            })
            self.db.commit()
            
            print("--- SUCCESS: Saved to Postgres! ---")
            print(f"Extracted text preview: {raw_text[:200]}...")
            
            return {
                'message': 'Resume processed successfully!',
                'filename': filename,
                'text_length': len(raw_text),
                'preview': raw_text[:200] + '...' if len(raw_text) > 200 else raw_text
            }
            
        except Exception as e:
            self.db.rollback()
            print(f"--- CRASH REPORT ---")
            print(f"Error: {str(e)}")
            raise RuntimeError(f"Failed to process resume: {str(e)}")
    
    def find_matching_resumes(self, job_description: str, limit: int = 20) -> List[Dict]:
        """
        Find resumes matching job description using vector similarity
        
        Args:
            job_description: Job description text
            limit: Maximum number of results
            
        Returns:
            List of matching resumes with scores
        """
        print(f"Received Job Description: {job_description[:100]}...")
        
        if not job_description or len(job_description.strip()) == 0:
            raise ValueError("Job description cannot be empty")
        
        # Generate embedding for job description
        jd_vector = self.embedding_service.return_embeds(job_description)
        jd_vec_list = jd_vector.tolist()
        
        # Query database with cosine similarity
        sql = text("""
            SELECT 
                1 - (embedding <=> :embedding::vector) as score,
                full_text,
                id
            FROM candidate_profiles
            ORDER BY score DESC
            LIMIT :limit
        """)
        
        results = self.db.execute(sql, {
            'embedding': str(jd_vec_list),
            'limit': limit
        }).fetchall()
        
        # Format results
        return [
            {
                'id': row[2],
                'score': float(row[0]),
                'text': row[1],
                'formatted': f"Match Score: {row[0]:.2f} | {row[1][:200]}..."
            }
            for row in results
        ]
