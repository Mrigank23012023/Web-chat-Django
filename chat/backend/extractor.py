import logging
import trafilatura
import re
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class Extractor:
    
    def extract(self, html_content: str) -> Dict[str, Optional[str]]:
        if not html_content:
            logger.warning("Empty HTML content provided for extraction.")
            return None
            
        try:
            # Try Trafilatura first
            data = trafilatura.bare_extraction(
                html_content, 
                include_comments=False, 
                include_tables=True
            )
            
            text = None
            title = "Unknown Title"
            
            if data and data.get('text'):
                text = data['text']
                title = data.get('title', 'Unknown Title')
            
            # Fallback to BeautifulSoup if Trafilatura failed
            if not text:
                logger.warning("Trafilatura failed/empty. using BeautifulSoup fallback.")
                try:
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(html_content, 'html.parser')
                    
                    # Remove unwanted tags
                    for tag in soup(["script", "style", "nav", "footer", "header", "meta", "noscript", "svg", "button"]):
                        tag.decompose()
                        
                    title = soup.title.string.strip() if soup.title and soup.title.string else "Unknown Title"
                    
                    # Get text
                    text = soup.get_text(separator='\n\n')
                except Exception as e:
                    logger.error(f"BS4 Fallback failed: {e}")
                    return None
            
            if not text:
                logger.warning("Extraction returned empty data after fallback.")
                return None
            
            text = text.replace('\xa0', ' ')
            text = re.sub(r'\n{3,}', '\n\n', text)
            
            if len(text) < 10:
                logger.warning(f"Extracted content too short ({len(text)} chars). Skipping.")
                return None
            
            compression_ratio = len(text) / len(html_content) if len(html_content) > 0 else 0
            logger.info(f"Extraction successful. Size: {len(text)} chars (Ratio: {compression_ratio:.2f})")
                
            return {"text": text, "title": title}
            
        except Exception as e:
            logger.error(f"Extraction failed: {e}")
            return None
