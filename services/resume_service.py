from typing import List, Dict
import logging
import numpy as np
from werkzeug.datastructures import FileStorage
from sqlalchemy import text
from services.document_parser import DocumentParser
from services.embedding_service import get_embedding_service

logger = logging.getLogger(__name__)

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
        logger.info("Resume processing started")
        
        try:
            filename = file.filename
            logger.debug(f"Processing file: {filename}")
            
            logger.debug("Extracting text from document")
            raw_text = self.parser.extract_from_stream(file.stream, filename)
            
            if not raw_text or len(raw_text.strip()) == 0:
                raise ValueError("No text could be extracted from the document")
            
            logger.info(f"Text extracted successfully: {len(raw_text)} characters")
            
            logger.debug("Generating embeddings")
            vectors = self.embedding_service.return_embeds(raw_text)
            
            # Convert numpy array to list for PostgreSQL
            vec_list = vectors.tolist()
            
            logger.debug("Saving to database")
            sql = text("""
                INSERT INTO candidate_profiles (full_text, embedding) 
                VALUES (:text, :embedding::vector)
            """)
            
            self.db.execute(sql, {
                'text': raw_text,
                'embedding': str(vec_list)
            })
            self.db.commit()
            
            logger.info("Resume saved successfully to database")
            logger.debug(f"Text preview: {raw_text[:200]}...")
            
            return {
                'message': 'Resume processed successfully!',
                'filename': filename,
                'text_length': len(raw_text),
                'preview': raw_text[:200] + '...' if len(raw_text) > 200 else raw_text
            }
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to process resume: {str(e)}", exc_info=True)
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
        logger.info(f"Finding matching resumes for job description: {job_description[:100]}...")
        
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
