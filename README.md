# 🔬 Nexus — AI Research & IP Intelligence Agent

Nexus is an AI research agent built with the **Google Agent Development Kit (ADK)**, **Gemini 2.5 Flash**, and the **BigQuery MCP Server**. It translates natural language questions into BigQuery queries to explore and analyze the Google Patents Research Dataset.

---

## 🏗️ Architecture

`User` → `ADK Web UI` → `Nexus Agent` → `Gemini 2.5 Flash` → `BigQuery MCP Server` → `Google Patents Research Dataset`

---

## 🚀 Quickstart

1. **Set Cloud Project:**
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID

## 1 Configure Environment:

```bash
export GOOGLE_GENAI_USE_VERTEXAI="True"
export GOOGLE_CLOUD_PROJECT="$(gcloud config get-value project -q)"
export GOOGLE_CLOUD_LOCATION="us-central1"
export GOOGLE_CLOUD_REGION="us-central1"
```
## 2 Authenticate:
```bash
gcloud auth application-default login
```

## 3 Run the Agent Locally
Start the ADK web development server:

```bash 
uv tool run --with "mcp==1.29.*" --from "google-adk[mcp]==2.4.*" adk web --allow_origins="*" --port 8080 .
```


## 3 Launch Agent:
Open the provided URL and select research_agent.

## 💬 Example Queries
Discovery: "What tables are available in google_patents_research?"

Schema: "Describe the schema of the publications table."

Analysis: "Which organizations have the most patent publications?"

Trends: "Analyze AI-related patent growth over the last 10 years."

## 🛠️ Tech Stack
Framework: Google ADK

LLM: Gemini 2.5 Flash

Protocol: Model Context Protocol (MCP)

Database: BigQuery (Google Patents Research Dataset)

Cloud: Google Cloud Platform (GCP)

