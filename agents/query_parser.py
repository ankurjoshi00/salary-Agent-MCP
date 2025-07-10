"""
Query Parser Agent for extracting job details from user queries.
"""
import json
import re
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# In /Users/user/Desktop/salary_agent/agents/query_parser.py


from config import config
from models import ParsedQuery

logger = logging.getLogger(__name__)

class QueryParserAgent:
    """Agent responsible for parsing user queries into structured data."""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=config.gemini_model, 
            temperature=config.gemini_temperature
        )
        self.prompt = PromptTemplate(
            template="""
            You are a query parser for job salary searches. Extract the following information from the user query:
            
            Query: "{query}"
            
            Extract:
            1. Job Title (e.g., "Data Scientist", "Software Engineer")
            2. Location (e.g., "USA", "Toronto", "New York")
            3. Years of Experience (e.g., "2 years", "3-5 years", "entry level")
            
            If any information is missing, make reasonable assumptions based on context.
            
            Return in this exact JSON format:
            {{
                "job_title": "extracted job title",
                "location": "extracted location", 
                "years_experience": "extracted experience level"
            }}
            """,
            input_variables=["query"]
        )
    
    def parse_query_sync(self, query: str) -> ParsedQuery:
        """Synchronous version of parse_query for LangGraph compatibility."""
        logger.info(f"🔍 Parsing query: {query}")
        
        chain = self.prompt | self.llm
        response = chain.invoke({"query": query})
        
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
            if json_match:
                parsed_data = json.loads(json_match.group())
                return ParsedQuery(
                    job_title=parsed_data.get("job_title", "Data Scientist"),
                    location=parsed_data.get("location", "USA"),
                    years_experience=parsed_data.get("years_experience", "2 years"),
                    original_query=query
                )
        except Exception as e:
            logger.error(f"Error parsing LLM response: {e}")
        
        # Fallback parsing using regex
        return self._fallback_parse(query)
    
    async def parse_query(self, query: str) -> ParsedQuery:
        """Async version for MCP tools."""
        return self.parse_query_sync(query)
    
    def _fallback_parse(self, query: str) -> ParsedQuery:
        """Fallback parsing method using regex patterns."""
        job_title = "Data Scientist"  # Default
        location = "USA"  # Default
        years_experience = "2 years"  # Default
        
        # Extract job title patterns
        job_patterns = [
            r"(data scientist|software engineer|developer|analyst|engineer)",
            r"(scientist|engineer|developer|analyst)"
        ]
        for pattern in job_patterns:
            match = re.search(pattern, query.lower())
            if match:
                job_title = match.group(1).title()
                break
        
        # Extract location patterns
        location_patterns = [
            r"in (usa|america|united states|canada|toronto|new york|california|texas)",
            r"(usa|america|united states|canada|toronto|new york|california|texas)"
        ]
        for pattern in location_patterns:
            match = re.search(pattern, query.lower())
            if match:
                location = match.group(1).upper() if len(match.group(1)) <= 3 else match.group(1).title()
                break
        
        # Extract experience patterns
        exp_patterns = [
            r"(\d+)\s*(?:year|yr)s?\s*(?:experience|exp)?",
            r"(\d+-\d+)\s*(?:year|yr)s?\s*(?:experience|exp)?",
            r"(entry level|junior|senior|mid level)"
        ]
        for pattern in exp_patterns:
            match = re.search(pattern, query.lower())
            if match:
                years_experience = match.group(1) + " years" if match.group(1).isdigit() else match.group(1)
                break
        
        return ParsedQuery(
            job_title=job_title,
            location=location,
            years_experience=years_experience,
            original_query=query
        )