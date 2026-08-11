import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(1, "Data Prep", "30 min", "Database, schema, warehouse, and 6 tables loaded from CSV")

render_technologies_used([
    {"name": "Database & Schema", "description": "Snowflake's organizational hierarchy for objects. A database contains schemas, and schemas contain tables, views, and other objects.", "icon": "database"},
    {"name": "CSV File Format", "description": "Snowflake can infer schema and load data directly from CSV files using file formats and COPY INTO commands.", "icon": "table_chart"},
    {"name": "Virtual Warehouse", "description": "Snowflake's compute engine. A warehouse provides the CPU and memory to execute queries and load data. Scales independently of storage.", "icon": "memory"},
])


PROMPT_1_1 = """Create the following Snowflake objects for our Capital Management AI workshop:

1. A database called SLC_PORTFOLIO_AI
2. A schema called PORTFOLIO_ANALYTICS inside that database
3. A stage called DATA in the schema PORTFOLIO_ANALYTICS with a directory table and server side encryption
4. A stage called INVESTMENT_DOCS in the schema PORTFOLIO_ANALYTICS with a directory table and server side encryption
5. A warehouse called CAPITAL_WH (size MEDIUM, auto-suspend after 60 seconds, auto-resume enabled)
6. Set the session context to use these objects

Execute all SQL and confirm each object was created."""

render_prompt("Prompt 1.1", "Create Database, Schema, Stages & Warehouse", PROMPT_1_1)

render_explanation("What this prompt does", """
Creates the foundational Snowflake objects:

```sql
CREATE DATABASE SLC_PORTFOLIO_AI;
CREATE SCHEMA SLC_PORTFOLIO_AI.PORTFOLIO_ANALYTICS;
CREATE STAGE SLC_PORTFOLIO_AI.PORTFOLIO_ANALYTICS.DATA
  DIRECTORY = (ENABLE = TRUE)
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');
CREATE STAGE SLC_PORTFOLIO_AI.PORTFOLIO_ANALYTICS.INVESTMENT_DOCS
  DIRECTORY = (ENABLE = TRUE)
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');
CREATE WAREHOUSE CAPITAL_WH
  WAREHOUSE_SIZE = 'MEDIUM'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE;

USE DATABASE SLC_PORTFOLIO_AI;
USE SCHEMA PORTFOLIO_ANALYTICS;
USE WAREHOUSE CAPITAL_WH;
```

**Why MEDIUM?** Cortex AI functions (AI_EXTRACT, AI_PARSE_DOCUMENT, AI_CLASSIFY) are compute-intensive.
A MEDIUM warehouse ensures comfortable throughput when processing the batch extraction in Session 2.
With AUTO_SUSPEND = 60 seconds, it pauses immediately after queries finish, minimizing credit usage.
""")


PROMPT_1_2 = """In SLC_PORTFOLIO_AI.PORTFOLIO_ANALYTICS, the 6 CSV files have been uploaded to an internal stage called DATA.

For all 6 tables (CLIENTS, POSITIONS, SECURITIES, ASSET_CLASSES, ANALYST_NOTES, CLIENT_COMMUNICATIONS):

1. Create a file format (CSV with PARSE_HEADER=TRUE, FIELD_OPTIONALLY_ENCLOSED_BY='"')
2. Create the tables with appropriate column types inferred from the data. Ensure to convert the column names to uppercase.
3. Load the data

Use CREATE TABLE with INFER_SCHEMA from a stage and then COPY INTO them. The key requirement is that all 6 tables are created and populated.

Execute all SQL."""

st.markdown("""
**Before running the prompt below, download the workshop data files and upload them to the `DATA` stage:**

1. **Download** the workshop repository as a ZIP file:
   **[Download ZIP](https://github.com/sfc-gh-cleblanc/cortex-hol/archive/refs/heads/main.zip)**
2. **Unzip** the downloaded file. The required CSV data files are located in the `workshop_guide/data/` folder:
   `clients.csv`, `positions.csv`, `securities.csv`, `asset_classes.csv`, `analyst_notes.csv`, `client_communications.csv`
3. In Snowsight, navigate to **Data > Databases > SLC_PORTFOLIO_AI > PORTFOLIO_ANALYTICS > Stages > DATA** and upload all 6 CSV files from that folder.
4. Then copy the prompt below into Cortex Code and execute.
""")

render_prompt("Prompt 1.2", "Load and Create Tables from CSV", PROMPT_1_2)

render_explanation("What this prompt does", """
Loads all 6 data tables from CSV files uploaded to the internal stage `DATA`. Cortex Code will use INFER_SCHEMA to detect column types automatically:

```sql
-- 1. Create CSV file format
CREATE OR REPLACE FILE FORMAT CSV_FORMAT
    TYPE = 'CSV'
    PARSE_HEADER = TRUE
    FIELD_OPTIONALLY_ENCLOSED_BY = '"';

-- 2. Create tables using INFER_SCHEMA (columns uppercase)
CREATE OR REPLACE TABLE CLIENTS
    USING TEMPLATE (
        SELECT ARRAY_AGG(OBJECT_CONSTRUCT('COLUMN_NAME', UPPER("COLUMN_NAME"), 'TYPE', "TYPE", 'NULLABLE', "NULLABLE"))
        FROM TABLE(INFER_SCHEMA(LOCATION => '@DATA/clients.csv', FILE_FORMAT => 'CSV_FORMAT'))
    );
-- (repeated for all 6 tables)

-- 3. Load data
COPY INTO CLIENTS FROM @DATA/clients.csv FILE_FORMAT = 'CSV_FORMAT' MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;
-- (repeated for all 6 tables)
```

**The 6 tables**:
| Table | Rows | Description |
|-------|------|-------------|
| CLIENTS | 200 | Investment accounts with risk profiles and portfolio values |
| POSITIONS | ~800 | Current holdings per client — market value, cost basis, gains/losses |
| SECURITIES | 50 | Ticker reference data — sector, exchange, asset class, beta |
| ASSET_CLASSES | 8 | Asset class definitions with benchmarks and target allocations |
| ANALYST_NOTES | 200 | Free-text investment analyst notes with recommendations |
| CLIENT_COMMUNICATIONS | 100 | Client correspondence — reviews, withdrawals, inquiries |
""")


PROMPT_1_3 = """Run a query in SLC_PORTFOLIO_AI.PORTFOLIO_ANALYTICS that shows every table name and its row count, ordered by row count descending. Format it nicely."""

render_prompt("Prompt 1.3", "Verify All Data Tables", PROMPT_1_3)

render_explanation("What this prompt does", """
A quick verification query:

```sql
SELECT table_name, row_count
FROM SLC_PORTFOLIO_AI.INFORMATION_SCHEMA.TABLES
WHERE table_schema = 'PORTFOLIO_ANALYTICS'
  AND table_type = 'BASE TABLE'
ORDER BY row_count DESC;
```

You should see approximately **1,360 total rows** across 6 tables.
""")


PROMPT_1_4 = """In SLC_PORTFOLIO_AI.PORTFOLIO_ANALYTICS, list the files in the INVESTMENT_DOCS stage to confirm the upload was successful. Show the file names and sizes."""

st.markdown("""
**Upload the investment documents to the `INVESTMENT_DOCS` stage:**

1. From the unzipped workshop repository, locate the `workshop_guide/data/investment_documents/` folder (contains 15 PDF files)
2. In Snowsight, navigate to **Data > Databases > SLC_PORTFOLIO_AI > PORTFOLIO_ANALYTICS > Stages > INVESTMENT_DOCS** and upload all 15 PDF files
3. Then copy the prompt below into Cortex Code to verify the upload
""")

render_prompt("Prompt 1.4", "Upload & Verify Investment Documents", PROMPT_1_4)

render_explanation("What this prompt does", """
Verifies the investment document upload:

```sql
LIST @SLC_PORTFOLIO_AI.PORTFOLIO_ANALYTICS.INVESTMENT_DOCS;
```

You should see 15 PDF files listed. These contain research reports, fund prospectuses, investment memos, market commentary, and compliance documents that we'll process with AI functions in Session 2 to build a searchable document intelligence layer.
""")


render_key_concepts([
    {"term": "Internal Stage", "definition": "A named Snowflake stage that stores files within Snowflake's managed storage. Files are uploaded via Snowsight UI or PUT command and can be used with COPY INTO, INFER_SCHEMA, and AI functions like AI_PARSE_DOCUMENT."},
    {"term": "INFER_SCHEMA", "definition": "A Snowflake table function that automatically detects column names and types from files in a stage. Eliminates manual CREATE TABLE DDL for well-structured CSV/Parquet files."},
    {"term": "File Format", "definition": "A named object specifying how to parse files (CSV delimiters, headers, quoting, compression). Created once and reused across multiple COPY INTO operations."},
])

render_what_you_built([
    "SLC_PORTFOLIO_AI database and PORTFOLIO_ANALYTICS schema",
    "CAPITAL_WH warehouse (Medium, auto-suspend 60s)",
    "6 data tables loaded from CSV (~1,360 total rows)",
    "INVESTMENT_DOCS stage with 15 uploaded investment PDFs",
])
