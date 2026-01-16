import logging
from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from chat.config import Config

logger = logging.getLogger(__name__)

class Chunker:
    
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def chunk(self, text: str, source_url: str, title: str = "Unknown") -> List[Document]:
        if not text:
            logger.warning("Attempted to chunk empty text.")
            return []
            
        metadata = {"source": source_url, "title": title} 
        
        chunks = self.splitter.create_documents([text], metadatas=[metadata])
        
        chunks = [c for c in chunks if c.page_content and c.page_content.strip()]
        
        logger.info(f"Split text into {len(chunks)} chunks for {source_url}.")
        return chunks
