"""
FastMCP Server implementation for the Salary Analyzer system.
"""
import asyncio
from typing import Dict, Any
from fastmcp import FastMCP

# Assuming 'models' and 'agents' are correctly structured and accessible
# You might need to adjust these imports based on your exact project structure
# For example, if ParsedQuery is in models/data_models.py, it would be:
# from models.data_models import ParsedQuery
from models import ParsedQuery # Adjust if ParsedQuery is in a sub-module
from agents.query_parser import QueryParserAgent
from agents.scraper import ScraperAgent
from agents.structuring import StructuringAgent

class SalaryAnalyzerMCP:
    """MCP Server for Salary Analyzer with tool endpoints."""
    
    def __init__(self):
        # Initialize FastMCP with a name for your analyzer
        self.mcp = FastMCP("SalaryAnalyzer")
        self.setup_tools()
        
    def setup_tools(self):
        """Setup MCP tools for agent communication."""
        
        @self.mcp.tool()
        async def parse_salary_query(query: str) -> Dict[str, Any]:
            """
            Parse user query to extract job title, location, and experience.
            This tool will be exposed via the MCP server.
            """
            try:
                parser_agent = QueryParserAgent()
                # Await the async method of the agent
                result = await parser_agent.parse_query(query)
                # Convert the result object to a dictionary for serialization
                return {"success": True, "data": result.__dict__}
            except Exception as e:
                # Return error details if something goes wrong
                return {"success": False, "error": str(e)}
        
        @self.mcp.tool()
        async def scrape_salary_data(parsed_query: Dict[str, Any]) -> Dict[str, Any]:
            """
            Scrape salary data based on parsed query.
            This tool will be exposed via the MCP server.
            """
            try:
                scraper_agent = ScraperAgent()
                # Reconstruct ParsedQuery object from dictionary for the agent
                result = await scraper_agent.scrape_data(ParsedQuery(**parsed_query))
                # Return the scraped data
                return {"success": True, "data": result}
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        @self.mcp.tool()
        async def structure_salary_data(raw_data: list, parsed_query: Dict[str, Any]) -> Dict[str, Any]:
            """
            Structure and format scraped salary data.
            This tool will be exposed via the MCP server.
            """
            try:
                structuring_agent = StructuringAgent()
                # Reconstruct ParsedQuery object from dictionary for the agent
                result = await structuring_agent.structure_data(raw_data, ParsedQuery(**parsed_query))
                # Convert list of objects to list of dictionaries for serialization
                return {"success": True, "data": [item.__dict__ for item in result]}
            except Exception as e:
                return {"success": False, "error": str(e)}

    async def start_server(self):
        """
        Start the FastMCP server. This method is designed to be awaited
        within an existing event loop, or called by a top-level runner.
        """
        print("FastMCP server is ready to run...")
        # The .run() method of FastMCP is a blocking call that starts the server
        # and manages its own event loop internally (via anyio).
        await self.mcp.run()

async def start_mcp_server():
    """
    Convenience function to instantiate and start the MCP server.
    This function is async and expects to be awaited.
    """
    mcp_server = SalaryAnalyzerMCP()
    await mcp_server.start_server()

