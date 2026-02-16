from typing import BinaryIO
import PyPDF2
import docx

class DocumentParser:
    """Extract text from various document formats"""
    
    @staticmethod
    def extract_from_stream(file_stream: BinaryIO, filename: str = '') -> str:
        """
        Extract text from file stream
        
        Args:
            file_stream: Binary file stream
            filename: Original filename (used to determine file type)
            
        Returns:
            Extracted text content
        """
        try:
            # Determine file type from extension
            ext = filename.lower().split('.')[-1] if filename else ''
            
            if ext == 'pdf':
                return DocumentParser._extract_pdf(file_stream)
            elif ext in ['docx', 'doc']:
                return DocumentParser._extract_docx(file_stream)
            elif ext == 'txt':
                return DocumentParser._extract_txt(file_stream)
            else:
                # Try PDF as default
                try:
                    return DocumentParser._extract_pdf(file_stream)
                except:
                    # Fallback to text
                    return DocumentParser._extract_txt(file_stream)
                
        except Exception as e:
            raise Exception(f"Error parsing document: {str(e)}")
    
    @staticmethod
    def _extract_pdf(file_stream: BinaryIO) -> str:
        """Extract text from PDF"""
        pdf_reader = PyPDF2.PdfReader(file_stream)
        text = []
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
        return '\n'.join(text)
    
    @staticmethod
    def _extract_docx(file_stream: BinaryIO) -> str:
        """Extract text from DOCX"""
        doc = docx.Document(file_stream)
        text = []
        for para in doc.paragraphs:
            if para.text.strip():
                text.append(para.text)
        return '\n'.join(text)
    
    @staticmethod
    def _extract_txt(file_stream: BinaryIO) -> str:
        """Extract text from plain text file"""
        return file_stream.read().decode('utf-8', errors='ignore')
