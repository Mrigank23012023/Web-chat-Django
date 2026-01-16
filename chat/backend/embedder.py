import logging
from langchain_community.embeddings import HuggingFaceEmbeddings
from chat.config import Config
import logging

logger = logging.getLogger(__name__)

class Embedder:
    
    def __init__(self):
        # Default to huggingface if not specified
        self.provider = getattr(Config, "EMBEDDING_PROVIDER", "huggingface")
        self.model_name = Config.EMBEDDING_MODEL_NAME
        
    def get_embedding_function(self):
        logger.info(f"Initializing {self.provider} embeddings with model: {self.model_name}")
        
        if self.provider == "huggingface":
            try:
                embeddings = HuggingFaceEmbeddings(model_name=self.model_name)
                logger.info(f"HuggingFace embeddings initialized successfully ({self.model_name})")
                return embeddings
            except Exception as e:
                logger.error(f"Failed to initialize HuggingFace embeddings: {e}")
                raise e
        else:
            # Fallback or error for unsupported providers
            raise ValueError(f"Unsupported embedding provider: {self.provider}")
