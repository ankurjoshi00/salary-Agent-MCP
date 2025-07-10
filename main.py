"""
Main application entry point for the Salary Analyzer system.
"""
import sys
import logging
# import asyncio # No longer needed directly in main.py for MCP mode
from typing import List

from workflow.manager import WorkflowManager
from agents.report_generator import ReportGeneratorAgent
# We will import SalaryAnalyzerMCP directly for the --mcp mode
from agents.server import SalaryAnalyzerMCP, start_mcp_server # Keep start_mcp_server for other modes if needed, but not for --mcp directly

# Set up basic logging (optional, but good practice)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SalaryAnalyzerApp:
    """Main application class for the Salary Analyzer system."""
    
    def __init__(self):
        self.workflow_manager = WorkflowManager()
        self.report_generator = ReportGeneratorAgent()
    
    def run_analysis(self, query: str):
        """Run salary analysis for a single query."""
        try:
            # Note: analyze_salary might be an async function.
            # If so, this run_analysis method would need to be async too,
            # and called with asyncio.run() or awaited in an existing loop.
            # For now, assuming it's synchronous or handled internally.
            report = self.workflow_manager.analyze_salary(query)
            self.report_generator.print_formatted_report(report)
            return report
        except Exception as e:
            logger.error(f"Failed to analyze query '{query}': {e}")
            return None
    
    def run_batch_analysis(self, queries: List[str]):
        """Run salary analysis for multiple queries."""
        results = []
        for query in queries:
            print(f"\n{'='*50}")
            print(f"Processing: {query}")
            print('='*50)
            result = self.run_analysis(query)
            results.append(result)
        return results

def main():
    """Main entry point of the application."""
    # Example test queries
    test_queries = [
        "data engineer salary of 5 year experience candidate in pune",
        "software engineer salary 3 years experience in bangalore"
    ]
    
    # Check command line arguments for execution mode
    if len(sys.argv) > 1 and sys.argv[1] == "--mcp":
        # Start MCP server mode
        logger.info("🚀 Starting MCP Server...")
        # Instantiate SalaryAnalyzerMCP and directly call its mcp.run() method.
        # This allows fastmcp to manage the event loop itself, preventing RuntimeError.
        mcp_analyzer = SalaryAnalyzerMCP()
        mcp_analyzer.mcp.run() # This call blocks until the server is stopped
    elif len(sys.argv) > 1 and sys.argv[1] == "--query":
        # Single query mode
        if len(sys.argv) > 2:
            query = " ".join(sys.argv[2:])
            app = SalaryAnalyzerApp()
            app.run_analysis(query)
        else:
            print("Please provide a query: python main.py --query 'your salary query here'")
    else:
        # Default batch analysis mode
        logger.info("🚀 Starting Salary Analyzer - Batch Mode")
        app = SalaryAnalyzerApp()
        # Process only the first query for quick testing in batch mode
        app.run_batch_analysis(test_queries[:1])

if __name__ == "__main__":
    main()
