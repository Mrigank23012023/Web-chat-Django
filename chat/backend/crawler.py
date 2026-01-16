import logging
import time
from typing import List, Dict, Set
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from chat.config import Config
from collections import deque

logger = logging.getLogger(__name__)

class Crawler:
    
    def crawl(self, start_url: str, limit: int = Config.MAX_PAGES_CRAWL) -> List[Dict[str, str]]:
        if not start_url:
            raise ValueError("URL cannot be empty")
            
        logger.info(f"Starting crawl for {start_url} with limit {limit}")
        
        base_domain = urlparse(start_url).netloc
        queue = deque([start_url])
        visited: Set[str] = set([start_url])
        results: List[Dict[str, str]] = []
        
        headers = {"User-Agent": Config.USER_AGENT}

        while queue and len(results) < limit:
            current_url = queue.popleft()
            
            try:
                time.sleep(0.5)

                logger.info(f"Fetching: {current_url}")
                response = requests.get(current_url, timeout=Config.REQUEST_TIMEOUT, headers=headers)
                
                if response.status_code != 200:
                    logger.warning(f"Failed to fetch {current_url}: Status {response.status_code}")
                    continue
                
                final_domain = urlparse(response.url).netloc
                if final_domain != base_domain:
                    logger.warning(f"Redirected off-domain to {final_domain}. Skipping.")
                    continue

                if "text/html" not in response.headers.get("Content-Type", "").lower():
                    logger.warning(f"Skipping non-HTML content: {current_url}")
                    continue

                html_content = response.text
                results.append({"url": response.url, "html": html_content}) 
                
                if len(results) < limit:
                    soup = BeautifulSoup(html_content, 'html.parser')
                    for link in soup.find_all('a', href=True):
                        raw_href = link['href']
                        absolute_url = urljoin(current_url, raw_href)
                        
                        parsed_href = urlparse(absolute_url)
                        clean_url = parsed_href._replace(fragment="").geturl()

                        if parsed_href.netloc == base_domain and clean_url not in visited:
                            visited.add(clean_url)
                            queue.append(clean_url)
                            
            except Exception as e:
                logger.error(f"Error crawling {current_url}: {e}")
                continue
                
        logger.info(f"Crawl complete. Visited {len(results)} pages.")
        return results
