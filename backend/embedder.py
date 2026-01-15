import logging
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import Config

logger = logging.getLogger(__name__)

class Embedder:
    
    def __init__(self):
        self.model_name = Config.EMBEDDING_MODEL_NAME
        
    def get_embedding_function(self):
        logger.info(f"Loading embedding model: {self.model_name}")
        output = HuggingFaceEmbeddings(model_name=self.model_name)
        logger.info("Embedding model loaded successfully.")
        return output
