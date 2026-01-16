
import logging
from chat.backend.extractor import Extractor
from unittest.mock import patch

# Setup logging
logging.basicConfig(level=logging.INFO)

def test_fallback_logic():
    html_content = """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <p>This is some test content that BeautifulSoup should find.</p>
        </body>
    </html>
    """
    
    print("--- Testing Extraction Fallback ---")
    
    # Mock trafilatura to raise an exception (Simulating Render crash)
    with patch('trafilatura.bare_extraction', side_effect=Exception("Simulated Render Crash")):
        extractor = Extractor()
        result = extractor.extract(html_content)
        
        if result and "BeautifulSoup" in str(result.get('text', '')): 
            # Note: The text extraction won't say "BeautifulSoup", it says the content.
            pass
            
        if result and "test content" in result['text']:
            print("✅ SUCCESS: Fallback worked! Text extracted despite Trafilatura crash.")
            print(f"Extracted: {result['text']}")
        else:
            print("❌ FAILURE: Fallback did not run or failed.")
            print(f"Result: {result}")

if __name__ == "__main__":
    test_fallback_logic()
