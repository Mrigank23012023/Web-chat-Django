
import sys
import io
import logging
import traceback
import time

# Force UTF-8 encoding for stdout/stderr to avoid Windows charmap errors
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

print("--- DEPENDENCY CHECK ---")
try:
    import trafilatura
    print(f"Trafilatura Version: {trafilatura.__version__}")
except ImportError as e:
    print(f"Trafilatura Import Error: {e}")

try:
    from lxml import etree
    print(f"LXML Version: {etree.LXML_VERSION}")
except ImportError as e:
    print(f"LXML Import Error: {e}")

try:
    import lxml_html_clean
    print("lxml_html_clean module found.")
except ImportError:
    print("lxml_html_clean module NOT found.")

print("\n--- STARTING PIPELINE ---")

try:
    from chat.backend.crawler import Crawler
    from chat.backend.extractor import Extractor
    from chat.backend.cleaner import Cleaner
    from chat.backend.chunker import Chunker
except Exception as e:
    print(f"Import Error: {e}")
    sys.exit(1)

TEST_URL = "https://www.python.org/"

def debug_indexing():
    print(f"Debugging {TEST_URL}...")
    
    crawler = Crawler()
    try:
        pages = crawler.crawl(TEST_URL, limit=1)
        if not pages:
            print("Crawling returned 0 pages.")
            return
    except Exception as e:
        print(f"Crawling Error: {e}")
        traceback.print_exc()
        return

    print(f"Crawled {len(pages)} pages.")
    
    extractor = Extractor()
    for page in pages:
        print(f"Extracting {page['url']} ({len(page['html'])} bytes)...")
        try:
            # We want to catch the log output too, which goes to stderr
            result = extractor.extract(page['html'])
            if result:
                 print(f"Success! Text length: {len(result['text'])}")
                 
                 cleaner = Cleaner()
                 clean = cleaner.clean(result['text'])
                 print(f"Cleaned length: {len(clean)}")
                 
                 chunker = Chunker()
                 chunks = chunker.chunk(clean, page['url'], result['title'])
                 print(f"Chunks generated: {len(chunks)}")
                 if not chunks:
                     print("CHUNKING RETURNED 0 CHUNKS!")
            else:
                 print("Extraction returned None.")
        except Exception as e:
             print(f"Pipeline Exception: {e}")
             traceback.print_exc()

if __name__ == "__main__":
    debug_indexing()
