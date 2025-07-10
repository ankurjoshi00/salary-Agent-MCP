"""
Workflow Manager for orchestrating the multi-agent salary analysis process.
"""
import logging
from langgraph.graph import StateGraph, END

from models import AgentState, StructuredSalaryReport
from agents.query_parser import QueryParserAgent
from agents.scraper import ScraperAgent
from agents.structuring import StructuringAgent
from agents.report_generator import ReportGeneratorAgent

logger = logging.getLogger(__name__)

class WorkflowManager:
    """Manages the multi-agent workflow for salary analysis."""
    
    def __init__(self):
        self.query_parser = QueryParserAgent()
        self.scraper = ScraperAgent()
        self.structuring_agent = StructuringAgent()
        self.report_generator = ReportGeneratorAgent()
        self.workflow = self._build_workflow()
    
    def _build_workflow(self):
        """Build the multi-agent workflow."""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("parser", self._query_parser_node)
        workflow.add_node("scraper", self._scraper_node)
        workflow.add_node("structuring", self._structuring_node)
        workflow.add_node("report_generator", self._report_generation_node)
        
        # Define edges
        workflow.set_entry_point("parser")
        workflow.add_edge("parser", "scraper")
        workflow.add_edge("scraper", "structuring")
        workflow.add_edge("structuring", "report_generator")
        workflow.add_edge("report_generator", END)
        
        return workflow.compile()
    
    def _query_parser_node(self, state: AgentState):
        """Parse the user query."""
        logger.info("--- 🔍 INVOKING QUERY PARSER AGENT ---")
        parsed_query = self.query_parser.parse_query_sync(state['original_query'])
        return {"parsed_query": parsed_query}
    
    def _scraper_node(self, state: AgentState):
        """Scrape salary data."""
        logger.info("--- 🕷️ INVOKING SCRAPER AGENT ---")
        scraped_data = self.scraper.scrape_data_sync(state['parsed_query'])
        logger.info(f'Scraped data: {len(scraped_data)} items')
        return {"scraped_data": scraped_data}
    
    def _structuring_node(self, state: AgentState):
        """Structure the scraped data."""
        logger.info("--- 🏗️ INVOKING STRUCTURING AGENT ---")
        structured_data = self.structuring_agent.structure_data_sync(
            state['scraped_data'], 
            state['parsed_query']
        )
        return {"structured_data": structured_data}
    
    def _report_generation_node(self, state: AgentState):
        """Generate final structured report."""
        logger.info("--- 📊 GENERATING FINAL REPORT ---")
        
        final_report = self.report_generator.generate_report(
            state['parsed_query'],
            state['structured_data']
        )
        
        return {"final_report": final_report}
    
    def analyze_salary(self, query: str) -> StructuredSalaryReport:
        """Execute the complete salary analysis workflow."""
        logger.info(f"🚀 Starting salary analysis for: '{query}'")
        
        initial_state = {
            "original_query": query,
            "parsed_query": None,
            "scraped_data": [],
            "structured_data": [],
            "final_report": None,
            "errors": []
        }
        
        try:
            final_state = self.workflow.invoke(initial_state)
            return final_state['final_report']
        except Exception as e:
            logger.error(f"Error in salary analysis: {e}")
            raise