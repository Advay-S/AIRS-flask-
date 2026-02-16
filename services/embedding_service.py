from sentence_transformers import SentenceTransformer
import numpy as np
from typing import Union, List

class EmbeddingService:
    """Service for generating text embeddings using sentence transformers"""
    
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        """
        Initialize the embedding model
        
        Args:
            model_name: Name of the sentence transformer model
        """
        print(f"Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        print("Model loaded successfully!")
    
    def return_embeds(self, text: Union[str, List[str]]) -> np.ndarray:
        """
        Generate embeddings for the given text
        
        Args:
            text: Input text or list of texts to embed
            
        Returns:
            numpy array of embeddings (384 dimensions for all-MiniLM-L6-v2)
        """
        try:
            embeddings = self.model.encode(text, convert_to_numpy=True)
            return embeddings
        except Exception as e:
            raise RuntimeError(f"Error generating embeddings: {str(e)}")
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embeddings"""
        return self.model.get_sentence_embedding_dimension()

# Singleton instance
_embedding_service = None

def get_embedding_service():
    """Get or create the singleton embedding service"""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service
