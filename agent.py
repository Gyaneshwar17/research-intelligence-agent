import os
import google.auth
from google.auth.transport.requests import Request
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

# 1. Fetch Application Default Credentials (ADC) for BigQuery MCP Server
_credentials, project_id = google.auth.default()
_request = Request()
_credentials.refresh(_request)

# Retrieve project ID from environment
project_id = os.getenv("GOOGLE_CLOUD_PROJECT", project_id)
if not project_id:
    raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is not set.")

# 2. Authorization Header Provider for BigQuery MCP Requests
def _adc_auth_header_provider(context=None) -> dict[str, str]:
    if not _credentials.valid:
        _credentials.refresh(_request)
    return {
        "Authorization": f"Bearer {_credentials.token}",
        "x-goog-user-project": project_id
    }

# 3. Configure BigQuery MCP Toolset
bigquery_toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="https://bigquery.googleapis.com/mcp",
        tool_filter=[
            'get_dataset_info',
            'list_table_ids',
            'get_table_info',
            'execute_sql_readonly',  # Ensures safe read-only SQL execution
        ]
    ),
    header_provider=_adc_auth_header_provider
)

# 4. System Prompt Defining Personas, Instructions & Guardrails
SYSTEM_INSTRUCTION = f"""
You are 'Nexus', an enterprise AI Research & IP Intelligence Strategist.
Your primary role is to analyze public research, patent data, and technical literature in BigQuery.

Target Public Dataset: `bigquery-public-data.google_patents_research`

Plan of Action:
1. ALWAYS start by exploring dataset structures using `list_table_ids` and `get_table_info`.
2. Inspect column definitions and distinct values before running analytical queries.
3. Formulate SQL queries using `execute_sql_readonly`. Use project `{project_id}`.
4. Synthesize SQL results into high-level business and technical summaries.
5. Do NOT use LaTeX in your responses. When giving final answers, use Markdown.
"""

# 5. Define Root Agent
root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="research_agent",
    instruction=SYSTEM_INSTRUCTION,
    description="An AI IP Strategist that analyzes Google Patents public datasets via BigQuery MCP.",
    tools=[bigquery_toolset]
)
