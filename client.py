"""
Example FastMCP client to interact with the Salary Analyzer MCP server.
"""
import asyncio
import logging
from fastmcp.client import FastMCPClient # Corrected import: trying from fastmcp.client directly

# Set up basic logging for the client
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def main():
    """
    Main asynchronous function to run the MCP client.
    """
    # Initialize the FastMCPClient, specifying the name of the server it should connect to.
    # By default, FastMCP uses stdio for communication, so no host/port is needed for local testing.
    client = FastMCPClient("SalaryAnalyzer")
    
    # Example query to send to the parse_salary_query tool
    query = "data engineer salary of 5 year experience candidate in pune"
    logger.info(f"Attempting to parse query: '{query}' using the MCP server...")

    try:
        # Call the remote tool. The method name matches the tool name defined in server.py.
        # The arguments passed here will be sent to the remote tool function.
        response = await client.call("parse_salary_query", query=query)

        if response.get("success"):
            parsed_data = response.get("data")
            logger.info("Successfully parsed query:")
            logger.info(f"  Job Title: {parsed_data.get('job_title')}")
            logger.info(f"  Location: {parsed_data.get('location')}")
            logger.info(f"  Experience: {parsed_data.get('experience_years')} years")
            
            # Now, you could proceed to call other tools with the parsed data
            # For example, calling scrape_salary_data:
            logger.info("Attempting to scrape salary data...")
            scrape_response = await client.call("scrape_salary_data", parsed_query=parsed_data)
            
            if scrape_response.get("success"):
                raw_data = scrape_response.get("data")
                logger.info(f"Successfully scraped {len(raw_data)} items of raw data.")
                # print(f"Raw Data: {raw_data}") # Uncomment to see raw data
                
                # And then structure the data:
                logger.info("Attempting to structure salary data...")
                structure_response = await client.call("structure_salary_data", raw_data=raw_data, parsed_query=parsed_data)
                
                if structure_response.get("success"):
                    structured_data = structure_response.get("data")
                    logger.info(f"Successfully structured {len(structured_data)} items of salary data.")
                    for item in structured_data:
                        logger.info(f"  - Min: {item.get('min_salary')}, Max: {item.get('max_salary')}, Avg: {item.get('avg_salary')}")
                else:
                    logger.error(f"Failed to structure data: {structure_response.get('error')}")

            else:
                logger.error(f"Failed to scrape data: {scrape_response.get('error')}")

        else:
            logger.error(f"Failed to parse query: {response.get('error')}")

    except Exception as e:
        logger.error(f"An error occurred while communicating with the MCP server: {e}")
    finally:
        # It's good practice to close the client connection when done
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
