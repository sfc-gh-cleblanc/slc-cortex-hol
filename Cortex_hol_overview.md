# Capital Management AI Workshop — Overview

**Audience:** Capital Management  
**Date:** TBD  
**Total Duration:** ~4 hours (including break)  
**Platform:** Snowflake (Trial Account)  
**Trial Signup:** https://signup.snowflake.com/?t=5e52c965fa2b4d430e74c67647f2d2ec1fb3bc1dc72710dd25cf5f919cef5e06&cloud=aws&region=us-east-2

---

## Workshop Context

This hands-on workshop walks participants through building a complete AI-powered portfolio analytics platform on Snowflake. The scenario centers on capital management — participants load portfolio data, extract insights from unstructured investment analyst notes and PDF documents using Cortex AI functions, build a searchable document intelligence layer with Cortex Search, create a natural language analytics layer with Semantic Views, deploy a multi-tool AI agent, and build a Streamlit dashboard.

The workshop is delivered as a multi-page Streamlit guide application. Each session contains numbered prompts that participants copy into Cortex Code (Snowflake's AI coding assistant) or follow as UI-guided steps within Snowsight.

---

## Time Estimates

| Session | Duration |
|---------|----------|
| Introductions & Overview | 15 min |
| 1. Data Prep | 30 min |
| 2. AI SQL | 40 min |
| 3. Cortex Search | 30 min |
| 4. Cortex Analyst & Semantic Views | 35 min |
| **Break** | **15 min** |
| 5. Cortex Agents | 25 min |
| 6. CoWork | 20 min |
| 7. Streamlit | 25 min |
| Summary & Next Steps | 15 min |
| **Total** | **~4 hrs** |

---

## Block 1: Data & Intelligence

### Session 1 — Data Prep (30 min)

**Objective:** Establish the Snowflake environment and load all workshop data.

Participants create a database (`SLC_PORTFOLIO_AI`), schema (`PORTFOLIO_ANALYTICS`), warehouse (`CAPITAL_WH`), and two internal stages (`DATA` for CSVs, `INVESTMENT_DOCS` for PDFs). They upload synthetic CSV files covering clients, positions, securities, asset classes, analyst notes, and client communications. Tables are created using `INFER_SCHEMA` and populated via `COPY INTO`. Investment document PDFs are uploaded to the `INVESTMENT_DOCS` stage. The session ends with verification queries confirming all tables, row counts, and document uploads.

**Key outcome:** A fully populated Snowflake environment with 6 tables of structured data and 15 investment PDF documents ready for AI processing.

---

### Session 2 — AI SQL (40 min)

**Objective:** Use Cortex AI functions to extract structured insights from analyst notes and parse/chunk investment PDFs for Cortex Search.

Participants:

1. Use `AI_EXTRACT` with a `responseFormat` schema to pull structured fields from free-text analyst notes (ticker, recommendation, price target, key risk, investment horizon)
2. Use `AI_CLASSIFY` to categorize analyst notes into event types (Earnings Update, Risk Flag, Price Target Revision, etc.)
3. Use `AI_EXTRACT` on staged PDF documents via `TO_FILE()` to extract document-level metadata
4. Build a batch extraction pipeline materializing results into `EXTRACTED_INVESTMENT_INSIGHTS`
5. Use `AI_PARSE_DOCUMENT` to extract full text from all 15 investment PDFs
6. Use `SNOWFLAKE.CORTEX.SPLIT_TEXT_RECURSIVE_CHARACTER` to chunk documents into ~500-token segments
7. Create the `DOCUMENT_CHUNKS` table as the source for Cortex Search

**Key outcome:** Analyst notes transformed into structured data, and all 15 investment PDFs parsed, classified, and chunked into a searchable `DOCUMENT_CHUNKS` table.

---

### Session 3 — Cortex Search (30 min)

**Objective:** Create a Cortex Search service over the investment document chunks and test semantic retrieval.

Participants:

1. Create `INVESTMENT_DOCS_SEARCH` — a Cortex Search service indexing `chunk_text` with `document_type` and `security_ticker` as filterable attributes
2. Test the search service using `SNOWFLAKE.CORTEX.SEARCH_PREVIEW` with natural language queries
3. Test attribute-based filtering (filter by document_type = 'Investment Memo')
4. Explore the interactive search UI in Snowsight

**Key outcome:** A deployed Cortex Search service that enables semantic retrieval across 15 investment documents, ready to be used as an agent tool.

---

### Session 4 — Cortex Analyst & Semantic Views (35 min)

**Objective:** Create a semantic layer over portfolio data and query it with natural language.

This session is UI-guided. Participants use the **Semantic View Autopilot** in Snowsight to:

1. Select tables from `SLC_PORTFOLIO_AI.PORTFOLIO_ANALYTICS`: CLIENTS, POSITIONS, SECURITIES, ASSET_CLASSES, EXTRACTED_INVESTMENT_INSIGHTS
2. Let the Autopilot generate `PORTFOLIO_ANALYTICS_VIEW` with auto-detected relationships, dimensions, facts, metrics, and synonyms
3. Review and accept relationships (POSITIONS → CLIENTS, POSITIONS → SECURITIES, SECURITIES → ASSET_CLASSES, INSIGHTS → SECURITIES)
4. Add a verified query for total AUM and allocation breakdown
5. Add a view description for agent tool routing
6. Test with natural language questions (top securities by value, allocation by asset class, analyst recommendation distribution, etc.)

**Key outcome:** A working semantic view that enables natural language queries over portfolio data, created through the Autopilot UI.

---

## Break (15 min)

---

## Block 2: Agents & Apps

### Session 5 — Cortex Agents (25 min)

**Objective:** Create a multi-tool AI agent combining structured portfolio analytics with investment document search.

Participants create a Cortex Agent using the Snowsight UI:

1. Create `PORTFOLIO_ANALYST_AGENT` in `SLC_PORTFOLIO_AI.PORTFOLIO_ANALYTICS`
2. Write orchestration instructions for the portfolio analytics domain
3. Add `PORTFOLIO_ANALYTICS_VIEW` as the **Portfolio Data** tool (semantic view)
4. Add `INVESTMENT_DOCS_SEARCH` as the **Investment Research** tool (Cortex Search) — this is the key differentiator from a single-tool agent
5. Add sample questions demonstrating both data and document queries
6. Test cross-tool queries that require both structured data and research document context
7. Add to CoWork for collaborative use in Session 6

**Key outcome:** A deployed Cortex Agent with two tools — structured analytics and document search — capable of answering both quantitative portfolio questions and qualitative research questions in a unified interface.

---

### Session 6 — CoWork (20 min)

**Objective:** Use the multi-tool agent in CoWork for collaborative portfolio analysis.

Participants open CoWork and interact with PORTFOLIO_ANALYST_AGENT:
- "Show me a summary of our assets under management by account type"
- "Which securities represent concentration risk at the client level?"
- "Search our research documents for the infrastructure investment thesis"
- "Compare current asset class allocations to targets — where are we out of bounds?"
- "Generate a board-ready executive summary combining portfolio metrics and recent research highlights"

**Key outcome:** Hands-on experience with CoWork as a collaborative analysis tool, demonstrating how the dual-tool agent integrates structured data and document research into team workflows.

---

### Session 7 — Streamlit (25 min)

**Objective:** Build and deploy a Streamlit portfolio dashboard with KPIs and AI-powered insights.

Participants use Cortex Code to create a Streamlit in Snowflake app (`PORTFOLIO_DASHBOARD`) with:
- KPI cards: Total AUM, Active Clients, Average Portfolio Value, Total Unrealized Gain/Loss
- Charts: Asset allocation by class (pie), Top 10 securities by value (bar), Portfolio value by account type (horizontal bar)
- An AI Insights section demonstrating AI_CLASSIFY on recent analyst notes inline
- Deploy on container runtime with a compute pool

**Key outcome:** A deployed Streamlit dashboard presenting key portfolio KPIs and charts, demonstrating Streamlit in Snowflake on container runtime.

---

## Summary of Snowflake Technologies Covered

| Technology | Session |
|-----------|---------|
| Database, Schema, Warehouse, Stage | 1 |
| INFER_SCHEMA, COPY INTO | 1 |
| AI_EXTRACT, AI_CLASSIFY, AI_COMPLETE | 2 |
| AI_PARSE_DOCUMENT, TO_FILE() | 2 |
| SPLIT_TEXT_RECURSIVE_CHARACTER, Chunking | 2 |
| Cortex Search Service | 3 |
| SEARCH_PREVIEW, Attribute Filtering | 3 |
| Semantic View Autopilot | 4 |
| Cortex Analyst | 4 |
| Cortex Agents (dual tool — semantic view + search) | 5 |
| CoWork | 6 |
| Streamlit in Snowflake (Container Runtime) | 7 |
| Compute Pools | 7 |
