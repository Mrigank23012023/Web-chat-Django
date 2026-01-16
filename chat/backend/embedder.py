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
                # Use Inference API to avoid loading model in memory (OOM fix for Render)
                # Switch to langchain_huggingface (newer) to avoid KeyErrors
                from langchain_huggingface import HuggingFaceEndpointEmbeddings
                
                api_key = Config.HUGGINGFACEHUB_API_TOKEN
                if not api_key:
                    raise ValueError("HUGGINGFACEHUB_API_TOKEN is missing. Please add it to your environment variables.")

                embeddings = HuggingFaceEndpointEmbeddings(
                    huggingfacehub_api_token=api_key,
                    model=self.model_name
                )
                logger.info(f"HuggingFace API embeddings initialized successfully ({self.model_name})")
                return embeddings
                logger.info(f"HuggingFace API embeddings initialized successfully ({self.model_name})")
                return embeddings
            except Exception as e:
                logger.error(f"Failed to initialize HuggingFace embeddings: {e}")
                raise e
        else:
            # Fallback or error for unsupported providers
            raise ValueError(f"Unsupported embedding provider: {self.provider}")
