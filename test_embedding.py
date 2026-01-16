
import os
import logging
import sys
from dotenv import load_dotenv

# Load env vars
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_embedding():
    print("Testing Embedding Configuration...")
    
    try:
        from chat.config import Config
        print(f"Provider: {Config.EMBEDDING_PROVIDER}")
        print(f"Model: {Config.EMBEDDING_MODEL_NAME}")
        
        token = Config.HUGGINGFACEHUB_API_TOKEN
        if token:
             print(f"Token found: {token[:4]}...{token[-4:]}")
        else:
             print("❌ Token NOT found in Config")
             return

        from chat.backend.embedder import Embedder
        embedder = Embedder()
        func = embedder.get_embedding_function()
        
        print(f"Embedding Function: {type(func)}")
        
        # Test generation
        text = "Hello, world!"
        print(f"Generating embedding for: '{text}'")
        vector = func.embed_query(text)
        
        print(f"✅ Success! Vector length: {len(vector)}")
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("You might need to run: pip install taggingface_hub langchain-huggingface")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"❌ Verification Failed: {repr(e)}")

if __name__ == "__main__":
    test_embedding()
