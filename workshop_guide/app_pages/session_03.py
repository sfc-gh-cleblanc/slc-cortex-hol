import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(3, "Cortex Search", "30 min", "Search service over investment documents, tested with semantic queries")

render_technologies_used([
    {"name": "Cortex Search Service", "description": "A Snowflake-native semantic search service. Builds an embedding index over a text column and enables natural language retrieval with optional attribute-based filtering. Results are ranked by relevance, not keywords.", "icon": "search"},
    {"name": "DOCUMENT_CHUNKS table", "description": "The source table for the search service, created in Session 2. Contains parsed PDF text split into ~500-token chunks with document_type and security_ticker metadata for filtering.", "icon": "table_chart"},
    {"name": "Hybrid Search", "description": "Cortex Search combines dense vector embeddings (semantic similarity) with sparse BM25 (keyword matching) to produce high-quality results for both concept-level and specific-term queries.", "icon": "auto_awesome"},
])

st.markdown("---")

st.markdown("#### :material/search: Create the Cortex Search Service")
st.markdown("""
In this session, you'll create a Cortex Search service over the `DOCUMENT_CHUNKS` table built in Session 2.
The service embeds and indexes the `chunk_text` column, enabling semantic search across all 15 investment documents.
""")

PROMPT_3_1 = """In SLC_PORTFOLIO_AI.PORTFOLIO_ANALYTICS, create a Cortex Search service over the DOCUMENT_CHUNKS table.

The search service should:
1. Index the chunk_text column as the searchable content
2. Include document_type and security_ticker as filterable attributes (ATTRIBUTES clause)
3. Also include document_name and chunk_index as attributes for display
4. Use CAPITAL_WH for indexing compute
5. Set TARGET_LAG to '1 day'
6. Name the service INVESTMENT_DOCS_SEARCH

Create the service and then check its status to confirm indexing has started.

Use SHOW CORTEX SEARCH SERVICES to verify it was created."""

render_prompt("Prompt 3.1", "Create the Cortex Search Service", PROMPT_3_1)

render_explanation("What this prompt does", """
Creates a Cortex Search service and begins building the embedding index:

```sql
CREATE OR REPLACE CORTEX SEARCH SERVICE INVESTMENT_DOCS_SEARCH
  ON chunk_text
  ATTRIBUTES document_type, security_ticker, document_name, chunk_index
  TARGET_LAG = '1 day'
  WAREHOUSE = CAPITAL_WH
  AS (
    SELECT chunk_id, chunk_text, document_type, security_ticker, document_name, chunk_index
    FROM SLC_PORTFOLIO_AI.PORTFOLIO_ANALYTICS.DOCUMENT_CHUNKS
  );

-- Check status
SHOW CORTEX SEARCH SERVICES IN SCHEMA SLC_PORTFOLIO_AI.PORTFOLIO_ANALYTICS;
```

**How Cortex Search builds its index**:
1. Cortex reads every row from the source query (our DOCUMENT_CHUNKS subquery)
2. It generates dense vector embeddings for each `chunk_text` value using Snowflake's embedding model
3. It builds a hybrid index combining those embeddings (semantic search) with BM25 inverted index (keyword search)
4. ATTRIBUTES columns are indexed separately as metadata — no embedding needed for filter-only columns

**TARGET_LAG** defines how fresh the index is. A 1-day lag means new chunks added to DOCUMENT_CHUNKS will be searchable within 24 hours. For real-time search, set `TARGET_LAG = '1 minute'` (incurs more compute cost).
""")

st.write("")
st.markdown("##### :material/check: Confirm the index is ready")
with st.container(border=True):
    st.markdown("""
After creating the service, check its status:

1. In Snowsight, navigate to **AI & ML > Cortex Search**
2. Find `INVESTMENT_DOCS_SEARCH` — you should see it listed with its indexing status
3. Wait until the status shows **Ready** before running the search tests below

Indexing 15 documents with a few hundred chunks typically takes 1-3 minutes.
""")

st.markdown("---")

st.markdown("#### :material/query_stats: Test with SQL Search Queries")

PROMPT_3_2 = """In SLC_PORTFOLIO_AI.PORTFOLIO_ANALYTICS, test the INVESTMENT_DOCS_SEARCH Cortex Search service with three queries.

Use SNOWFLAKE.CORTEX.SEARCH_PREVIEW to run each query:

Query 1 - General research search:
Ask: "What is the analyst outlook for Canadian bank stocks?" 
Return columns: chunk_text, document_name, document_type
Limit: 5 results

Query 2 - Filter by document type:
Ask: "infrastructure investment thesis and rising rate impact"
Filter to document_type = 'Investment Memo' only
Return: chunk_text, document_name
Limit: 3 results

Query 3 - Security-specific search:
Ask: "NVIDIA artificial intelligence revenue growth data center"
Filter to document_type = 'Research Report'
Return: chunk_text, document_name, security_ticker
Limit: 3 results

Parse and display the results from each query. Show the chunk_text content so we can verify relevance.

Execute all SQL."""

render_prompt("Prompt 3.2", "Test Cortex Search Queries", PROMPT_3_2)

render_explanation("What this prompt does", """
Uses the SEARCH_PREVIEW function to query the Cortex Search service directly from SQL:

```sql
-- Query 1: General semantic search
SELECT PARSE_JSON(
    SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
        'SLC_PORTFOLIO_AI.PORTFOLIO_ANALYTICS.INVESTMENT_DOCS_SEARCH',
        '{
            "query": "What is the analyst outlook for Canadian bank stocks?",
            "columns": ["chunk_text", "document_name", "document_type"],
            "limit": 5
        }'
    )
)['results'] AS search_results;

-- Query 2: Filter by document type
SELECT PARSE_JSON(
    SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
        'SLC_PORTFOLIO_AI.PORTFOLIO_ANALYTICS.INVESTMENT_DOCS_SEARCH',
        '{
            "query": "infrastructure investment thesis rising rate impact",
            "columns": ["chunk_text", "document_name"],
            "filter": {"@eq": {"document_type": "Investment Memo"}},
            "limit": 3
        }'
    )
)['results'] AS filtered_results;

-- Query 3: Security-specific with type filter
SELECT PARSE_JSON(
    SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
        'SLC_PORTFOLIO_AI.PORTFOLIO_ANALYTICS.INVESTMENT_DOCS_SEARCH',
        '{
            "query": "NVIDIA artificial intelligence revenue growth data center",
            "columns": ["chunk_text", "document_name", "security_ticker"],
            "filter": {"@eq": {"document_type": "Research Report"}},
            "limit": 3
        }'
    )
)['results'] AS nvda_results;
```

**Filter syntax**: The `filter` field accepts a JSON expression:
- `{"@eq": {"field": "value"}}` — exact match
- `{"@in": {"field": ["v1", "v2"]}}` — match any of the values
- `{"@and": [...]}` / `{"@or": [...]}` — compound filters

**Semantic vs. keyword search**: The query `"NVIDIA AI revenue"` will return relevant chunks even if those exact words aren't present — it matches on *meaning*, not just string overlap. This is what makes Cortex Search powerful for investment research where the same concept may be described in many ways.
""")

st.write("")

st.markdown("##### :material/lightbulb: Explore the Search UI")
with st.container(border=True):
    st.markdown("""
After running the SQL tests, try the interactive search UI:

1. In Snowsight, navigate to **AI & ML > Cortex Search**
2. Click on `INVESTMENT_DOCS_SEARCH`
3. Click **Preview** to open the interactive search interface
4. Try these questions:
""")
    questions = [
        "What risks are associated with our fixed income portfolio?",
        "What are the ESG screening criteria updates?",
        "Which companies have been upgraded by analysts recently?",
        "What are the compliance requirements for personal trading?",
        "How is the Bank of Canada rate cycle affecting our portfolio positioning?",
    ]
    for q in questions:
        st.code(q, language="text", wrap_lines=True)
    st.markdown("""
Observe how Cortex Search returns the most relevant passages from across all 15 documents — regardless of which specific document contains the answer.
""")

st.info("""
:material/smart_toy: **Coming up in Session 5**: The `INVESTMENT_DOCS_SEARCH` service you created here will be added as a tool on the Portfolio Analyst Agent. This enables the agent to answer both structured data questions (via the semantic view) and document research questions (via Cortex Search) in a single conversational interface.
""")

st.markdown("---")

render_explanation("How Cortex Search works", """
**Cortex Search** builds a hybrid retrieval index over a text column:

1. **Embedding generation**: Each chunk is passed through an embedding model that converts text into a dense vector representing its semantic meaning.
2. **Hybrid index**: The dense vector index (approximate nearest-neighbor search) is combined with a sparse BM25 index (keyword matching) to handle both semantic and exact-term queries.
3. **Query processing**: At search time, the query is embedded and both the semantic and keyword components are scored. Results are re-ranked by a fusion algorithm that combines both scores.
4. **Attribute filtering**: ATTRIBUTES columns are indexed as metadata. Filters are applied before scoring, reducing the search space and improving performance and precision.

**Cortex Search vs. full-text search**:
- Full-text search: finds documents containing the exact query words
- Cortex Search: finds documents with *similar meaning*, even if different words are used
- Example: query "fixed income duration risk" will find chunks discussing "bond sensitivity to interest rate changes" even without exact word overlap
""")


render_key_concepts([
    {"term": "Cortex Search Service", "definition": "A Snowflake-native search service created with CREATE CORTEX SEARCH SERVICE. It indexes a text column from a table or query, builds an embedding index, and enables semantic retrieval via SEARCH_PREVIEW or the REST API."},
    {"term": "Embedding Index", "definition": "A searchable index of dense vector representations of text. Each chunk is represented as a high-dimensional vector. Similar meanings produce similar vectors, enabling semantic retrieval by nearest-neighbor search."},
    {"term": "Hybrid Search", "definition": "A retrieval strategy that combines dense vector search (semantic similarity) with sparse BM25 (keyword frequency) scoring. Produces better results than either method alone, especially for mixed natural language and specific-term queries."},
    {"term": "ATTRIBUTES clause", "definition": "Columns specified as ATTRIBUTES in a Cortex Search service are indexed as metadata, not as embedding inputs. They can be used as filter conditions in search queries without contributing to semantic matching."},
    {"term": "TARGET_LAG", "definition": "How frequently Cortex Search refreshes its index from the source table. Set to '1 day' for batch use cases, '1 minute' for near-real-time search. Lower lag = more compute cost."},
])

render_what_you_built([
    "INVESTMENT_DOCS_SEARCH — Cortex Search service over 15 investment PDFs",
    "Semantic search tested across multiple query patterns",
    "Document-type filtering with @eq filter syntax demonstrated",
    "Search service ready to be added as an agent tool in Session 5",
])
