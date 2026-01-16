import logging
from typing import List

logger = logging.getLogger(__name__)

class Retriever:
    
    def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        if not query:
            return []
            
        logger.info(f"Retrieving top {top_k} results for query: {query}")
        return []
