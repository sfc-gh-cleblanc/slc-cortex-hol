import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(2, "AI SQL", "40 min", "Structured extraction from analyst notes and investment PDFs; document chunks for Cortex Search")

render_technologies_used([
    {"name": "AI_EXTRACT", "description": "Extracts structured fields from unstructured text or documents. Define a responseFormat schema and get clean JSON back. Works on text columns and staged files via TO_FILE().", "icon": "auto_fix_high"},
    {"name": "AI_CLASSIFY", "description": "Classifies text into predefined categories. Useful for tagging investment documents by type or categorizing analyst recommendations.", "icon": "category"},
    {"name": "AI_PARSE_DOCUMENT", "description": "Extracts full text content from PDFs and other documents stored in a stage. Returns structured text with layout awareness, ready for chunking and indexing.", "icon": "description"},
    {"name": "AI_COMPLETE", "description": "The general-purpose LLM function. Pass a model and prompt to generate free-form text — summaries, recommendations, analysis.", "icon": "view_timeline"},
])


PROMPT_2_1 = """In SLC_PORTFOLIO_AI.PORTFOLIO_ANALYTICS, use Cortex AI functions to extract structured data from the ANALYST_NOTES table.

The NOTE_TEXT column contains free-text investment analyst notes. Use AI_EXTRACT to pull out structured fields from these notes.

1. First, show me 5 sample rows from ANALYST_NOTES so we can see the text format.

2. Then run AI_EXTRACT on 5 sample notes with this responseFormat:
   - ticker_symbol: "What stock ticker symbol is primarily referenced? (e.g., RY, NVDA)"
   - recommendation: "What is the analyst recommendation? (Buy, Hold, Sell, Overweight, Underweight, Market Perform)"
   - price_target: "What is the 12-month price target in dollars, as a number only?"
   - key_risk: "What is the primary risk factor mentioned?"
   - investment_horizon: "What is the investment time horizon? (short-term, medium-term, long-term)"

3. Show the extracted JSON results alongside the original text so we can verify accuracy.

Execute all SQL and show the results."""

render_prompt("Prompt 2.1", "Extract Structured Data from Analyst Notes", PROMPT_2_1)

render_explanation("What this prompt does", """
Uses **AI_EXTRACT** to transform unstructured analyst notes into structured data:

```sql
SELECT
    note_id,
    LEFT(note_text, 80) AS note_preview,
    AI_EXTRACT(
        text => note_text,
        responseFormat => {
            'ticker_symbol': 'What stock ticker symbol is primarily referenced?',
            'recommendation': 'What is the analyst recommendation? (Buy/Hold/Sell/Overweight/Underweight/Market Perform)',
            'price_target': 'What is the 12-month price target in dollars?',
            'key_risk': 'What is the primary risk factor mentioned?',
            'investment_horizon': 'What is the investment time horizon? (short-term/medium-term/long-term)'
        }
    ) AS extracted
FROM ANALYST_NOTES
LIMIT 5;
```

**How AI_EXTRACT works**:
- You define a `responseFormat` — a JSON object where keys are field names and values describe what to extract
- The model reads the text and returns structured JSON matching your schema
- It uses the `arctic-extract` model automatically (no model selection needed)
- Works on any text: analyst notes, emails, reports, legal documents

**Key insight**: The quality of your responseFormat descriptions directly impacts extraction accuracy. Be specific about expected values (e.g., "Buy/Hold/Sell" constrains the output better than just "recommendation").
""")


PROMPT_2_2 = """Now let's do two more AI operations in SLC_PORTFOLIO_AI.PORTFOLIO_ANALYTICS:

PART A - Classify analyst notes by type:
Use AI_CLASSIFY on the NOTE_TEXT from ANALYST_NOTES to categorize each note into one of these categories:
'Earnings Update', 'Risk Flag', 'Price Target Revision', 'Sector Commentary', 'Initiation of Coverage', 'Regulatory Alert'
Show the top 10 results with the classification and confidence score.

PART B - Extract from staged investment documents:
Review the investment documents uploaded to the INVESTMENT_DOCS stage. Use AI_EXTRACT with TO_FILE() to extract from 3 documents:
- document_type: "What type of document is this? (Research Report, Fund Prospectus, Quarterly Report, Investment Memo, Market Commentary, Risk Assessment, Compliance Note)"
- primary_security: "What is the primary security, fund, or asset class discussed?"
- key_recommendation: "What is the key recommendation or conclusion?"
- risk_level: "What overall risk level is implied? (Low, Medium, High)"
- time_horizon: "What investment or reporting time horizon is referenced?"

Execute all SQL and show results."""

render_prompt("Prompt 2.2", "Classify Notes & Extract from Documents", PROMPT_2_2)

render_explanation("What this prompt does", """
Demonstrates two additional AI patterns:

**Part A — AI_CLASSIFY**:
```sql
SELECT
    note_id,
    LEFT(note_text, 60) AS preview,
    AI_CLASSIFY(
        text => note_text,
        categories => ['Earnings Update', 'Risk Flag', 'Price Target Revision',
                       'Sector Commentary', 'Initiation of Coverage', 'Regulatory Alert']
    ) AS classification
FROM ANALYST_NOTES
LIMIT 10;
```

AI_CLASSIFY returns a JSON object with `label` (the chosen category) and `score` (confidence 0-1).

**Part B — Document extraction with TO_FILE()**:
```sql
SELECT
    RELATIVE_PATH,
    AI_EXTRACT(
        file => TO_FILE('@INVESTMENT_DOCS', RELATIVE_PATH),
        responseFormat => {
            'document_type': 'What type of document is this?',
            'primary_security': 'What security or asset class is discussed?',
            'key_recommendation': 'What is the key recommendation or conclusion?',
            'risk_level': 'What overall risk level is implied? (Low/Medium/High)',
            'time_horizon': 'What time horizon is referenced?'
        }
    ) AS extracted
FROM DIRECTORY('@INVESTMENT_DOCS')
LIMIT 3;
```

**When to use AI_EXTRACT vs AI_CLASSIFY**:
- **AI_EXTRACT**: Pull multiple structured fields from text (extraction)
- **AI_CLASSIFY**: Assign text to one of N predefined categories (classification)
""")


PROMPT_2_3 = """Now let's build a batch extraction pipeline in SLC_PORTFOLIO_AI.PORTFOLIO_ANALYTICS.

Create a materialized table called EXTRACTED_INVESTMENT_INSIGHTS that runs AI_EXTRACT across ALL rows in ANALYST_NOTES and flattens the results into proper columns:

1. Run AI_EXTRACT on the full ANALYST_NOTES table with the same responseFormat from Prompt 2.1 (ticker_symbol, recommendation, price_target, key_risk, investment_horizon)

2. Flatten the extracted JSON into individual columns using ::VARCHAR casting

3. Include the original note_id, security_id, ticker, analyst_name, note_date, and sentiment alongside the extracted fields

4. Also use AI_COMPLETE to generate a one-sentence PORTFOLIO_ACTION recommendation column. Use model 'claude-sonnet-4-6' and base the action on the recommendation and key_risk. For example: "Add to position on dips — strong buy thesis intact with manageable execution risk" or "Reduce exposure — regulatory overhang limits near-term upside". Include this as a PORTFOLIO_ACTION column.

5. Create this as a table: CREATE TABLE EXTRACTED_INVESTMENT_INSIGHTS AS SELECT ...

6. After creation, show the row count and a sample of 10 rows.

Execute all SQL."""

render_prompt("Prompt 2.3", "Batch Extraction Pipeline", PROMPT_2_3)

render_explanation("What this prompt does", """
Creates a materialized extraction table — the core pattern for production AI pipelines:

```sql
CREATE OR REPLACE TABLE EXTRACTED_INVESTMENT_INSIGHTS AS
WITH extracted AS (
    SELECT
        NOTE_ID, SECURITY_ID, TICKER, ANALYST_NAME, NOTE_DATE, SENTIMENT,
        AI_EXTRACT(
            NOTE_TEXT,
            {
                'ticker_symbol': 'What stock ticker symbol is primarily referenced?',
                'recommendation': 'What is the analyst recommendation?',
                'price_target': 'What is the 12-month price target in dollars?',
                'key_risk': 'What is the primary risk factor mentioned?',
                'investment_horizon': 'What is the investment time horizon?'
            }
        ) AS result
    FROM ANALYST_NOTES
)
SELECT
    NOTE_ID, SECURITY_ID, TICKER, ANALYST_NAME, NOTE_DATE, SENTIMENT,
    result:response:ticker_symbol::VARCHAR AS EXTRACTED_TICKER,
    result:response:recommendation::VARCHAR AS EXTRACTED_RECOMMENDATION,
    result:response:price_target::VARCHAR AS PRICE_TARGET,
    result:response:key_risk::VARCHAR AS KEY_RISK,
    result:response:investment_horizon::VARCHAR AS INVESTMENT_HORIZON,
    AI_COMPLETE(
        'claude-sonnet-4-6',
        'You are a portfolio manager. Based on the recommendation and risk below, write exactly one actionable portfolio action sentence (max 20 words). Recommendation: '
        || result:response:recommendation::VARCHAR
        || '. Key risk: ' || result:response:key_risk::VARCHAR || '.'
    )::VARCHAR AS PORTFOLIO_ACTION
FROM extracted;
```

**Why materialize?** Running AI_EXTRACT and AI_COMPLETE on every query would be slow and expensive.
By materializing once, you pay for extraction once and query the results for free. In production,
use a **Dynamic Table** or **Stream + Task** to incrementally process new notes as they arrive.
""")


PROMPT_2_4 = """Now let's build the document intelligence pipeline for Cortex Search in SLC_PORTFOLIO_AI.PORTFOLIO_ANALYTICS.

I need to create a DOCUMENT_CHUNKS table that will serve as the source for a Cortex Search service.

1. First, test AI_PARSE_DOCUMENT on a single PDF from the INVESTMENT_DOCS stage to see the extracted text:
   SELECT AI_PARSE_DOCUMENT(
       TO_FILE('@INVESTMENT_DOCS', <first_file_from_directory>),
       {'mode': 'LAYOUT'}
   ) AS parsed_doc
   Get the first file by querying DIRECTORY(@INVESTMENT_DOCS) LIMIT 1.

2. Then create the DOCUMENT_CHUNKS table using this pipeline:
   a. Parse every PDF in @INVESTMENT_DOCS using AI_PARSE_DOCUMENT with mode 'LAYOUT'
   b. Classify each document type using AI_CLASSIFY into: 'Research Report', 'Fund Prospectus', 'Quarterly Report', 'Investment Memo', 'Market Commentary', 'Risk Assessment', 'Compliance Note'
   c. Chunk the parsed text into segments of approximately 500 tokens with 50-token overlap using SNOWFLAKE.CORTEX.SPLIT_TEXT_RECURSIVE_CHARACTER
   d. For each chunk, extract the primary security ticker using AI_EXTRACT
   e. Include: chunk_id (UUID), document_name, document_type, chunk_text, chunk_index, security_ticker
   f. Filter out chunks shorter than 100 characters

   CREATE OR REPLACE TABLE DOCUMENT_CHUNKS AS ...

3. After creation, show the row count, a breakdown by document_type, and a sample of 5 rows.

Execute all SQL."""

render_prompt("Prompt 2.4", "Parse, Classify & Chunk Investment Documents", PROMPT_2_4)

render_explanation("What this prompt does", """
This is the key pipeline that transforms raw PDFs into a searchable knowledge base for Cortex Search.
It chains four operations in a single CREATE TABLE AS:

```sql
CREATE OR REPLACE TABLE DOCUMENT_CHUNKS AS
WITH parsed AS (
    SELECT
        RELATIVE_PATH AS document_name,
        AI_PARSE_DOCUMENT(
            TO_FILE('@INVESTMENT_DOCS', RELATIVE_PATH),
            {'mode': 'LAYOUT'}
        ):content::VARCHAR AS full_text,
        AI_CLASSIFY(
            AI_PARSE_DOCUMENT(
                TO_FILE('@INVESTMENT_DOCS', RELATIVE_PATH),
                {'mode': 'LAYOUT'}
            ):content::VARCHAR,
            ['Research Report', 'Fund Prospectus', 'Quarterly Report',
             'Investment Memo', 'Market Commentary', 'Risk Assessment', 'Compliance Note']
        ):label::VARCHAR AS document_type
    FROM DIRECTORY('@INVESTMENT_DOCS')
),
chunks AS (
    SELECT
        document_name,
        document_type,
        chunk.value::VARCHAR AS chunk_text,
        chunk.index AS chunk_index
    FROM parsed,
    LATERAL FLATTEN(
        input => SNOWFLAKE.CORTEX.SPLIT_TEXT_RECURSIVE_CHARACTER(
            full_text, 'none', 500, 50
        )
    ) AS chunk
)
SELECT
    UUID_STRING() AS chunk_id,
    document_name,
    document_type,
    chunk_text,
    chunk_index,
    AI_EXTRACT(
        chunk_text,
        {'security_ticker': 'What stock ticker symbol is primarily referenced? Return null if none mentioned.'}
    ):response:security_ticker::VARCHAR AS security_ticker
FROM chunks
WHERE LENGTH(chunk_text) > 100;
```

**Step-by-step breakdown**:

1. **AI_PARSE_DOCUMENT** (`mode: LAYOUT`): Extracts full text from each PDF with spatial layout awareness — preserves paragraph structure, headers, and table content better than simple text extraction.

2. **AI_CLASSIFY** (per document): Assigns a document type label to each PDF. This becomes a filter attribute on the Cortex Search service — users can filter by document_type without requiring an embedding lookup.

3. **SPLIT_TEXT_RECURSIVE_CHARACTER**: Snowflake's built-in chunking function. `500` = target chunk size in tokens, `50` = overlap between consecutive chunks. Overlap ensures context is preserved at chunk boundaries — a sentence split across chunks is partially repeated in both.

4. **AI_EXTRACT** (per chunk): Tags each chunk with the primary security ticker. Combined with document_type, this enables precise filtering like "show me all Risk Assessment chunks mentioning RY".

**Why chunk size matters**: Cortex Search operates at the chunk level — it returns the most relevant chunks, not entire documents. Smaller chunks (300-500 tokens) return more precise results. Larger chunks (800+ tokens) provide more context but reduce precision.

**Production pattern**: In production, use a **Stream + Task** on the stage directory table to automatically process new documents as they are uploaded, keeping DOCUMENT_CHUNKS fresh without full reprocessing.
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
