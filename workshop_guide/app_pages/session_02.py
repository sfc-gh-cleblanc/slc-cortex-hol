import streamlit as st
from components import render_session_header, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(2, "AI SQL", "40 min", "Structured extraction from analyst notes and investment PDFs; document chunks for Cortex Search")

render_technologies_used([
    {"name": "AI_EXTRACT", "description": "Extracts structured fields from unstructured text or documents. Define a responseFormat schema and get clean JSON back. Works on text columns and staged files via TO_FILE().", "icon": "auto_fix_high"},
    {"name": "AI_CLASSIFY", "description": "Classifies text into predefined categories. Useful for tagging investment documents by type or categorizing analyst recommendations.", "icon": "category"},
    {"name": "AI_PARSE_DOCUMENT", "description": "Extracts full text content from PDFs and other documents stored in a stage. Returns structured text with layout awareness, ready for chunking and indexing.", "icon": "description"},
    {"name": "AI_COMPLETE", "description": "The general-purpose LLM function. Pass a model and prompt to generate free-form text — summaries, recommendations, analysis.", "icon": "view_timeline"},
])

st.write("")

# ── Notebook upload instructions ─────────────────────────────────────────────
st.markdown("### :material/upload_file: Upload the Session 2 Notebook")

with st.container(border=True):
    st.markdown("""
**This session runs inside a Snowflake Workspace notebook** — not via Cortex Code prompts.
The notebook file (`session_02_ai_sql.ipynb`) is included in your workshop materials.

Follow the steps below to upload it and run it.
""")

st.write("")

# Step 1
with st.container(border=True):
    st.markdown("#### :material/counter_1: Create a new Workspace")
    st.markdown("""
1. In Snowsight, click **Projects** in the left navigation
2. Select **Workspaces**
3. Click **+ Workspace** (top right)
4. Name it **`AI SQL Workshop`** and click **Create**
""")

# Step 2
with st.container(border=True):
    st.markdown("#### :material/counter_2: Upload the notebook file")
    st.markdown("""
1. Inside your new workspace, click **Upload** (the upload icon in the file panel on the left)
2. Select the file **`session_02_ai_sql.ipynb`** from your workshop materials
3. The notebook will appear in the workspace file list
4. Click the file to open it
""")

# Step 3
with st.container(border=True):
    st.markdown("#### :material/counter_3: Connect and run the notebook")
    st.markdown("""
1. When the notebook opens, click **Connect** in the top toolbar

> **Why Connect?** Snowflake Workspace notebooks run on a compute pool service — a small container environment separate from your warehouse. The first time you connect on a new trial account, no compute pool service exists yet, so Snowflake will prompt you to create one.

2. If prompted to create a new service, **accept the defaults** and click **Create and Connect** — this provisions a compute pool and attaches it to your notebook (takes about 30 seconds)
3. Once connected, run cells **top to bottom** using **Shift + Enter** or the **Run All** button
4. The setup cells set your database context — make sure these run successfully before the SQL cells
5. Two cells create large tables and will take **1–3 minutes each** — a progress indicator will appear while they run
""")

st.write("")

render_explanation("What the notebook builds", """
The notebook walks through 7 steps in order:

| Step | What it does |
|------|-------------|
| Setup | Gets the active Snowpark session and sets database context |
| 1 | Preview 5 rows from `ANALYST_NOTES` |
| 2 | `AI_EXTRACT` — pull 5 structured fields from 5 sample notes |
| 3 | `AI_CLASSIFY` — categorise 10 notes into event types |
| 4 | `AI_EXTRACT` with `TO_FILE()` — extract metadata from 3 staged PDFs |
| 5 | Batch pipeline → `EXTRACTED_INVESTMENT_INSIGHTS` table (all notes + portfolio actions) |
| 6 | `AI_PARSE_DOCUMENT` — test-parse one PDF to inspect extracted text |
| 7 | Full pipeline → `DOCUMENT_CHUNKS` table (15 PDFs parsed, classified, chunked, ticker-tagged) |
""")

render_explanation("AI_EXTRACT: how it works", """
`AI_EXTRACT` transforms unstructured text into structured JSON using a `responseFormat` schema:

```sql
SELECT
    note_id,
    AI_EXTRACT(
        text => note_text,
        responseFormat => {
            'ticker_symbol':  'What stock ticker symbol is primarily referenced?',
            'recommendation': 'What is the analyst recommendation? (Buy/Hold/Sell)',
            'price_target':   'What is the 12-month price target in dollars?',
            'key_risk':       'What is the primary risk factor mentioned?'
        }
    ) AS extracted
FROM ANALYST_NOTES
LIMIT 5;
```

- Keys are field names; values are extraction instructions
- The model returns a JSON object matching your schema — access fields with `:response:field_name::VARCHAR`
- Uses the `arctic-extract` model automatically — no model selection needed
- Works on text columns **or** staged files via `TO_FILE('@stage', RELATIVE_PATH)`

**Key insight**: Be specific in your descriptions. `'(Buy, Hold, Sell)'` constrains the output better than just `'recommendation'`.
""")

render_explanation("DOCUMENT_CHUNKS pipeline: step by step", """
The notebook cell uses three CTEs so each PDF is parsed only once:

```sql
CREATE OR REPLACE TABLE DOCUMENT_CHUNKS AS
WITH parsed AS (
    -- Parse each PDF once; reuse full_text in the next CTE
    SELECT
        RELATIVE_PATH AS document_name,
        AI_PARSE_DOCUMENT(TO_FILE('@INVESTMENT_DOCS', RELATIVE_PATH), {'mode': 'LAYOUT'}):content::VARCHAR AS full_text
    FROM DIRECTORY('@INVESTMENT_DOCS')
),
classified AS (
    -- Classify document type using the already-parsed text
    SELECT document_name, full_text,
        AI_CLASSIFY(full_text, ['Research Report', 'Investment Memo', ...])):label::VARCHAR AS document_type
    FROM parsed
),
chunks AS (
    -- Split each document into ~500-token chunks with 50-token overlap
    SELECT document_name, document_type, chunk.value::VARCHAR AS chunk_text, chunk.index AS chunk_index
    FROM classified,
    LATERAL FLATTEN(input => SNOWFLAKE.CORTEX.SPLIT_TEXT_RECURSIVE_CHARACTER(full_text, 'none', 500, 50)) AS chunk
)
SELECT UUID_STRING() AS chunk_id, document_name, document_type, chunk_text, chunk_index,
    AI_EXTRACT(chunk_text, {'security_ticker': '...'}):response:security_ticker::VARCHAR AS security_ticker
FROM chunks
WHERE LENGTH(chunk_text) > 100;
```

**Why three CTEs?** `AI_CLASSIFY` can't reference `full_text` as a column alias in the same SELECT — it needs to be in a separate CTE. Splitting parsing and classification also means each PDF is parsed only once rather than twice.

**Why chunk size matters**: Cortex Search ranks at the chunk level — it returns the most relevant chunks, not entire documents. 500 tokens balances precision vs. context. The 50-token overlap ensures sentences split across chunk boundaries are partially repeated in both chunks.
""")


render_key_concepts([
    {"term": "AI_PARSE_DOCUMENT", "definition": "A Cortex AI function that extracts text from PDFs and other documents stored in a Snowflake stage. The LAYOUT mode preserves document structure. Returns a structured JSON object with a 'content' field containing the extracted text."},
    {"term": "AI_EXTRACT", "definition": "A Cortex AI function that extracts structured fields from unstructured text or files. You define a responseFormat schema (field names + descriptions) and it returns JSON. Uses the arctic-extract model automatically."},
    {"term": "AI_CLASSIFY", "definition": "A Cortex AI function that assigns text to one of N predefined categories. Returns the chosen label and a confidence score (0-1). No model selection needed."},
    {"term": "SPLIT_TEXT_RECURSIVE_CHARACTER", "definition": "A Snowflake built-in function that splits text into chunks of a specified token length with configurable overlap. The recursive strategy respects paragraph and sentence boundaries where possible, producing semantically coherent chunks."},
    {"term": "Chunking Strategy", "definition": "The process of dividing long documents into shorter segments for indexing. Chunk size (tokens) and overlap control precision vs. context tradeoff. Smaller chunks = more precise retrieval. Overlap prevents context loss at chunk boundaries."},
    {"term": "Batch Extraction", "definition": "The pattern of running AI functions across an entire table or stage and materializing results into a new table. Converts unstructured data into queryable structured columns at scale."},
])

render_what_you_built([
    "AI_EXTRACT pipeline extracting 5 fields from analyst notes",
    "AI_CLASSIFY categorizing analyst notes into 6 event types",
    "Document extraction from staged PDFs using TO_FILE()",
    "EXTRACTED_INVESTMENT_INSIGHTS materialized table (200 rows)",
    "AI_COMPLETE generating per-note portfolio action recommendations",
    "DOCUMENT_CHUNKS table with parsed, classified, and chunked investment PDFs (ready for Cortex Search)",
])
