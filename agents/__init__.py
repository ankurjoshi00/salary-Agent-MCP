# agents/__init__.py
"""
Agents package for the Salary Analyzer system.
"""
from .query_parser import QueryParserAgent
from .scraper import ScraperAgent
from .structuring import StructuringAgent
from .report_generator import ReportGeneratorAgent

__all__ = [
    'QueryParserAgent',
    'ScraperAgent', 
    'StructuringAgent',
    'ReportGeneratorAgent'
]

# workflow/__init__.py  
"""
Workflow package for orchestrating multi-agent processes.
"""
# from workflow.manager import WorkflowManager

__all__ = ['WorkflowManager']

# mcp/__init__.py
"""
MCP (Model Context Protocol) package for server implementations.
"""
from .server import SalaryAnalyzerMCP, start_mcp_server

__all__ = ['SalaryAnalyzerMCP', 'start_mcp_server']