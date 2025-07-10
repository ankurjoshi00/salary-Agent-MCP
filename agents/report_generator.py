"""
Report Generation Agent for creating structured salary reports.
"""
import logging
from typing import List
from tabulate import tabulate

from models import ParsedQuery, SalaryData, StructuredSalaryReport

logger = logging.getLogger(__name__)

class ReportGeneratorAgent:
    """Agent responsible for generating final structured reports."""
    
    def generate_report(self, parsed_query: ParsedQuery, structured_data: List[SalaryData]) -> StructuredSalaryReport:
        """Generate a comprehensive salary report."""
        logger.info("📊 Generating final report")
        
        if not structured_data:
            return self._generate_empty_report(parsed_query)
        
        summary_table = self._create_summary_table(structured_data)
        market_insights = self._generate_market_insights(parsed_query, structured_data)
        
        return StructuredSalaryReport(
            job_title=parsed_query.job_title,
            location=parsed_query.location,
            years_experience=parsed_query.years_experience,
            salary_data=structured_data,
            market_insights=market_insights,
            summary_table=summary_table
        )
    
    def _generate_empty_report(self, parsed_query: ParsedQuery) -> StructuredSalaryReport:
        """Generate report when no data is available."""
        return StructuredSalaryReport(
            job_title=parsed_query.job_title,
            location=parsed_query.location,
            years_experience=parsed_query.years_experience,
            salary_data=[],
            market_insights="No salary data found for the specified criteria.",
            summary_table="No data available"
        )
    
    def _create_summary_table(self, structured_data: List[SalaryData]) -> str:
        """Create a formatted summary table."""
        table_data = []
        for data in structured_data:
            row = [
                data.source,
                data.company or "N/A",
                f"{data.currency} {data.min_salary:,.0f}" if data.min_salary else "N/A",
                f"{data.currency} {data.max_salary:,.0f}" if data.max_salary else "N/A",
                f"{data.currency} {data.average_salary:,.0f}" if data.average_salary else "N/A"
            ]
            table_data.append(row)
        
        headers = ["Source", "Company", "Min Salary", "Max Salary", "Average Salary"]
        return tabulate(table_data, headers=headers, tablefmt="grid")
    
    def _generate_market_insights(self, parsed_query: ParsedQuery, structured_data: List[SalaryData]) -> str:
        """Generate market insights from salary data."""
        total_salaries = self._extract_all_salaries(structured_data)
        
        if not total_salaries:
            return "Insufficient data for market analysis."
        
        avg_market_salary = sum(total_salaries) / len(total_salaries)
        min_market_salary = min(total_salaries)
        max_market_salary = max(total_salaries)
        
        return f"""
        **Market Analysis for {parsed_query.job_title} in {parsed_query.location} ({parsed_query.years_experience})**
        
        • Average Market Salary: ${avg_market_salary:,.0f}
        • Salary Range: ${min_market_salary:,.0f} - ${max_market_salary:,.0f}
        • Data Sources: {len(structured_data)} sources analyzed
        • Based on {len(total_salaries)} salary data points
        """
    
    def _extract_all_salaries(self, structured_data: List[SalaryData]) -> List[float]:
        """Extract all salary values for analysis."""
        total_salaries = []
        
        for data in structured_data:
            if data.min_salary and data.max_salary:
                total_salaries.extend([data.min_salary, data.max_salary])
            elif data.average_salary:
                total_salaries.append(data.average_salary)
        
        return total_salaries

    def print_formatted_report(self, report: StructuredSalaryReport):
        """Print a beautifully formatted salary report."""
        print("\n" + "="*80)
        print("📊 SALARY ANALYSIS REPORT")
        print("="*80)
        print(f"🎯 Job Title: {report.job_title}")
        print(f"📍 Location: {report.location}")
        print(f"⏰ Experience Level: {report.years_experience}")
        print("\n" + "-"*80)
        print("📋 SALARY DATA TABLE")
        print("-"*80)
        print(report.summary_table)
        print("\n" + "-"*80)
        print("💡 MARKET INSIGHTS")
        print("-"*80)
        print(report.market_insights)
        print("="*80)