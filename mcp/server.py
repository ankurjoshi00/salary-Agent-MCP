"""
FastMCP Server implementation for the Salary Analyzer system.
"""
import asyncio
from typing import Dict, Any
from fastmcp import FastMCP

from models import ParsedQuery
from agents.query_parser import QueryParserAgent
from agents.scraper import ScraperAgent
from agents.structuring import StructuringAgent

class SalaryAnalyzerMCP:
    """MCP Server for Salary Analyzer with tool endpoints."""
    
    def __init__(self):
        self.mcp = FastMCP("SalaryAnalyzer")
        self.setup_tools()
        
    def setup_tools(self):
        """Setup MCP tools for agent communication."""
        
        @self.mcp.tool()
        async def parse_salary_query(query: str) -> Dict[str, Any]:
            """Parse user query to extract job title, location, and experience."""
            try:
                parser_agent = QueryParserAgent()
                result = await parser_agent.parse_query(query)
                return {"success": True, "data": result.__dict__}
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        @self.mcp.tool()
        async def scrape_salary_data(parsed_query: Dict[str, Any]) -> Dict[str, Any]:
            """Scrape salary data based on parsed query."""
            try:
                scraper_agent = ScraperAgent()
                result = await scraper_agent.scrape_data(ParsedQuery(**parsed_query))
                return {"success": True, "data": result}
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        @self.mcp.tool()
        async def structure_salary_data(raw_data: list, parsed_query: Dict[str, Any]) -> Dict[str, Any]:
            """Structure and format scraped salary data."""
            try:
                structuring_agent = StructuringAgent()
                result = await structuring_agent.structure_data(raw_data, ParsedQuery(**parsed_query))
                return {"success": True, "data": [item.__dict__ for item in result]}
            except Exception as e:
                return {"success": False, "error": str(e)}

    async def start_server(self):
        """Start the MCP server."""
        await self.mcp.run()

async def start_mcp_server():
    """Start the MCP server for agent communication."""
    mcp_server = SalaryAnalyzerMCP()
    await mcp_server.start_server()