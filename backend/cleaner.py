import logging
import re

logger = logging.getLogger(__name__)

class Cleaner:
    
    def clean(self, text: str) -> str:
        if not text:
            return ""
            
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        text = re.sub(r'[ \t]+', ' ', text)
        
        return text.strip()
