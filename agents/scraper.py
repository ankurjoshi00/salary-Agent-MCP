"""
Data Scraper Agent for gathering salary information from web sources.
"""
import time
import requests
import logging
from typing import List, Dict

from config import config
from models import ParsedQuery

logger = logging.getLogger(__name__)

class ScraperAgent:
    """Enhanced scraper agent with multiple search strategies."""
    
    def __init__(self):
        self.api_key = config.google_api_key
        self.cse_id = config.google_cse_id
        self.headers = {
            'User-Agent': 'JobSalaryScraper/2.0 (Educational Project; contact: your-email@example.com)'
        }
    
    def scrape_data_sync(self, parsed_query: ParsedQuery) -> List[dict]:
        """Synchronous version for LangGraph compatibility."""
        logger.info(f"🕷️ Scraping data for: {parsed_query.job_title} in {parsed_query.location}")
        
        search_queries = self._generate_search_queries(parsed_query)
        
        all_results = []
        for query in search_queries[:2]:  # Limit to avoid quota issues
            results = self._search_google_sync(query)
            all_results.extend(results)
            time.sleep(1)  # Rate limiting
        
        return all_results
    
    async def scrape_data(self, parsed_query: ParsedQuery) -> List[dict]:
        """Async version for MCP tools."""
        return self.scrape_data_sync(parsed_query)
    
    def _generate_search_queries(self, parsed_query: ParsedQuery) -> List[str]:
        """Generate search queries for comprehensive data gathering."""
        return [
            f"{parsed_query.job_title} salary {parsed_query.years_experience} {parsed_query.location}",
            f"{parsed_query.job_title} compensation {parsed_query.location} {parsed_query.years_experience}",
            f"average {parsed_query.job_title} salary {parsed_query.location}",
            f"{parsed_query.job_title} pay scale {parsed_query.location} experience"
        ]
    
    def _search_google_sync(self, query: str) -> List[dict]:
        """Synchronous Google Custom Search API."""
        url = f"https://www.googleapis.com/customsearch/v1?key={self.api_key}&cx={self.cse_id}&q={query}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            items = data.get("items", [])
            
            extracted_results = []
            for item in items[:5]:  # Top 5 results per query
                result_info = {
                    "title": item.get("title", "N/A"),
                    "snippet": item.get("snippet", "N/A"),
                    "link": item.get("link", "N/A"),
                    "query": query
                }
                extracted_results.append(result_info)
            
            return extracted_results
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error fetching Google Custom Search API: {e}")
            return [{"error": str(e), "query": query}]
    
    async def _search_google(self, query: str) -> List[dict]:
        """Async version for MCP tools."""
        return self._search_google_sync(query)