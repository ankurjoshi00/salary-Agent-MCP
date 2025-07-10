# Salary Analyzer - Multi-Agent System

A structured, agentic salary analysis system that uses multiple specialized agents to parse queries, scrape data, structure information, and generate comprehensive salary reports.

## 🏗️ Architecture

```
salary-analyzer/
├── config.py                 # Configuration management
├── models.py                 # Data models and schemas
├── agents/
│   ├── query_parser.py       # Query parsing agent
│   ├── scraper.py           # Data scraping agent
│   ├── structuring.py       # Data structuring agent
│   └── report_generator.py  # Report generation agent
├── workflow/
│   └── manager.py           # Workflow orchestration
├── mcp/
│   └── server.py            # MCP server implementation
├── main.py                  # Application entry point
├── requirements.txt         # Dependencies
└── README.md               # This file
```

## 🤖 Agents

### 1. Query Parser Agent (`agents/query_parser.py`)
- Extracts job title, location, and experience from user queries
- Uses LLM with fallback regex parsing
- Handles ambiguous queries with reasonable defaults

### 2. Scraper Agent (`agents/scraper.py`)
- Scrapes salary data from Google Custom Search API
- Implements rate limiting and error handling
- Generates multiple search strategies for comprehensive data

### 3. Structuring Agent (`agents/structuring.py`)
- Converts raw search results into structured salary data
- Uses LLM to extract salary ranges, averages, and sources
- Handles various salary formats and currencies

### 4. Report Generator Agent (`agents/report_generator.py`)
- Creates comprehensive salary reports with tables and insights
- Calculates market statistics and salary ranges
- Formats output for easy consumption

## 🔧 Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure API keys:**
   - Update `config.py` with your Google API key and Custom Search Engine ID
   - Or set environment variables:
```bash
export GOOGLE_API_KEY="your_api_key"
export GOOGLE_CSE_ID="your_cse_id"
```

## 🚀 Usage

### Basic Analysis
```bash
python main.py
```

### Single Query
```bash
python main.py --query "data scientist salary 3 years experience in bangalore"
```

### MCP Server Mode
```bash
python main.py --mcp
```

## 📊 Example Output

```
================================================================================
📊 SALARY ANALYSIS REPORT
================================================================================
🎯 Job Title: Data Engineer
📍 Location: Pune
⏰ Experience Level: 5 years

────────────────────────────────────────────────────────────────────────────────
📋 SALARY DATA TABLE
────────────────────────────────────────────────────────────────────────────────
+------------------+---------+-------------+-------------+-----------------+
| Source           | Company | Min Salary  | Max Salary  | Average Salary  |
+------------------+---------+-------------+-------------+-----------------+
| glassdoor.com    | N/A     | USD 80,000  | USD 120,000 | N/A            |
| payscale.com     | N/A     | N/A         | N/A         | USD 95,000     |
+------------------+---------+-------------+-------------+-----------------+

────────────────────────────────────────────────────────────────────────────────
💡 MARKET INSIGHTS
────────────────────────────────────────────────────────────────────────────────
**Market Analysis for Data Engineer in Pune (5 years)**

• Average Market Salary: $98,750
• Salary Range: $80,000 - $120,000
• Data Sources: 2 sources analyzed
• Based on 3 salary data points
================================================================================
```

## 🔄 Workflow

1. **Query Parsing**: Extract structured information from natural language queries
2. **Data Scraping**: Search multiple sources for salary information
3. **Data Structuring**: Convert raw data into structured format
4. **Report Generation**: Create comprehensive analysis with insights

## 🛠️ Extensibility

- **Add new agents**: Implement new agents in the `agents/` directory
- **Modify workflow**: Update `workflow/manager.py` to change agent execution order
- **Add data sources**: Extend `ScraperAgent` with new data sources
- **Custom reports**: Modify `ReportGeneratorAgent` for different output formats

## 📋 Requirements

- Python 3.8+
- Google Custom Search API key
- Internet connection for data scraping

## 🔐 Configuration

The system uses a centralized configuration in `config.py`:
- API credentials
- Model parameters  
- Rate limiting settings
- Default values

## 🧪 Testing

Run individual agents:
```python
from agents.query_parser import QueryParserAgent
parser = QueryParserAgent()
result = parser.parse_query_sync("software engineer salary in mumbai")
```

## 📝 Notes

- Respects API rate limits and implements proper error handling
- Uses LangGraph for workflow orchestration
- Supports both synchronous and asynchronous execution
- MCP server enables external tool integration