"""
Data models for the Salary Analyzer system.
"""
from dataclasses import dataclass
from typing import TypedDict, List, Optional

@dataclass
class ParsedQuery:
    """Parsed user query data model."""
    job_title: str
    location: str
    years_experience: str
    original_query: str

@dataclass
class SalaryData:
    """Salary data model."""
    min_salary: Optional[float]
    max_salary: Optional[float]
    average_salary: Optional[float]
    currency: str
    source: str
    company: Optional[str] = None

@dataclass
class StructuredSalaryReport:
    """Final structured salary report model."""
    job_title: str
    location: str
    years_experience: str
    salary_data: List[SalaryData]
    market_insights: str
    summary_table: str

class AgentState(TypedDict):
    """Agent workflow state model."""
    original_query: str
    parsed_query: ParsedQuery
    scraped_data: List[dict]
    structured_data: List[SalaryData]
    final_report: StructuredSalaryReport
    errors: List[str]