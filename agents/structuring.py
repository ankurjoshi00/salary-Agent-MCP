"""
Data Structuring Agent for formatting and organizing salary data.
"""
import json
import re
import logging
from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

from config import config
from models import ParsedQuery, SalaryData

logger = logging.getLogger(__name__)

class StructuringAgent:
    """Agent responsible for structuring and formatting salary data."""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=config.gemini_model, 
            temperature=config.gemini_temperature
        )
        self.prompt = PromptTemplate(
            template="""
            You are a salary data analyst. Analyze the following search results and extract structured salary information.
            
            Job Title: {job_title}
            Location: {location}
            Experience: {years_experience}
            
            Search Results:
            {search_results}
            
            Extract salary information and return in this JSON format:
            [
                {{
                    "min_salary": number or null,
                    "max_salary": number or null, 
                    "average_salary": number or null,
                    "currency": "USD" or appropriate currency,
                    "source": "source website/company name",
                    "company": "company name if mentioned or null"
                }}
            ]
            
            Convert salary formats like:
            - "80k-120k" to min_salary: 80000, max_salary: 120000
            - "$95,000" to average_salary: 95000
            - "100-150k USD" to min_salary: 100000, max_salary: 150000
            
            Extract multiple salary data points if available from different sources.
            """,
            input_variables=["job_title", "location", "years_experience", "search_results"]
        )
    
    def structure_data_sync(self, raw_data: List[dict], parsed_query: ParsedQuery) -> List[SalaryData]:
        """Synchronous version for LangGraph compatibility."""
        logger.info("🏗️ Structuring salary data")
        
        search_results_str = self._format_search_results(raw_data)
        
        if not search_results_str:
            return []
        
        chain = self.prompt | self.llm
        response = chain.invoke({
            "job_title": parsed_query.job_title,
            "location": parsed_query.location,
            "years_experience": parsed_query.years_experience,
            "search_results": search_results_str
        })
        
        try:
            # Extract JSON array from response
            json_match = re.search(r'\[.*\]', response.content, re.DOTALL)
            if json_match:
                salary_data_list = json.loads(json_match.group())
                return self._convert_to_salary_data(salary_data_list)
        except Exception as e:
            logger.error(f"Error parsing structured data: {e}")
        
        return []
    
    async def structure_data(self, raw_data: List[dict], parsed_query: ParsedQuery) -> List[SalaryData]:
        """Async version for MCP tools."""
        return self.structure_data_sync(raw_data, parsed_query)
    
    def _format_search_results(self, raw_data: List[dict]) -> str:
        """Format raw search results for LLM processing."""
        return "\n".join([
            f"Title: {item['title']}\nSnippet: {item['snippet']}\nSource: {item['link']}\n---"
            for item in raw_data if 'error' not in item
        ])
    
    def _convert_to_salary_data(self, salary_data_list: List[dict]) -> List[SalaryData]:
        """Convert dictionary list to SalaryData objects."""
        return [
            SalaryData(
                min_salary=item.get("min_salary"),
                max_salary=item.get("max_salary"),
                average_salary=item.get("average_salary"),
                currency=item.get("currency", "USD"),
                source=item.get("source", "Unknown"),
                company=item.get("company")
            )
            for item in salary_data_list
        ]