import streamlit as st
from components import render_session_header, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

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

st.write("")

st.markdown("##### Step 1: Open Cortex Search in Snowsight")
with st.container(border=True):
    st.markdown("""
1. In Snowsight, navigate to **AI & ML** in the left sidebar
2. Click **Cortex Search**
3. Click **+ Create** to open the Create Search Service wizard
""")

st.write("")

st.markdown("##### Step 2: New service — name and location")
with st.container(border=True):
    st.markdown("""
This is the first screen of the wizard. Fill in the following:

| Field | Value |
|-------|-------|
| **Role** | `ACCOUNTADMIN` |
| **Warehouse** | `CAPITAL_WH` |
| **Service database and schema** | `SLC_PORTFOLIO_AI.PORTFOLIO_ANALYTICS` |
| **Service name** | `INVESTMENT_DOCS_SEARCH` |

Click **Next**.
""")

st.write("")

st.markdown("##### Step 3: Select data — choose the source table")
with st.container(border=True):
    st.markdown("""
1. Select the source table: **DOCUMENT_CHUNKS**
2. Click **Next**
""")

st.write("")

st.markdown("##### Step 4: Select search column")
with st.container(border=True):
    st.markdown("""
1. Select **CHUNK_TEXT** as the search column — this is the column that will be embedded and indexed for semantic retrieval
2. Click **Next**

> **Why CHUNK_TEXT?** Each row in `DOCUMENT_CHUNKS` is a ~500-token segment of a PDF. Embedding at the chunk level gives Cortex Search a focused, semantically coherent unit to index — rather than embedding an entire document as one blob.
""")

st.write("")

st.markdown("##### Step 5: Select attributes — filter columns")
with st.container(border=True):
    st.markdown("""
Attribute columns are indexed as metadata and allow filtering of search results without affecting semantic scoring.

Select the following columns as attributes:
- `DOCUMENT_TYPE`
- `SECURITY_TICKER`
- `DOCUMENT_NAME`
- `CHUNK_INDEX`

Click **Next**.
""")

st.write("")

st.markdown("##### Step 6: Select columns — result columns")
with st.container(border=True):
    st.markdown("""
Select all columns to include in search results. At minimum include:
- `CHUNK_ID`
- `CHUNK_TEXT`
- `DOCUMENT_NAME`
- `DOCUMENT_TYPE`
- `SECURITY_TICKER`
- `CHUNK_INDEX`

Click **Next**.
""")

st.write("")

st.markdown("##### Step 7: Configure indexing — target lag and warehouse")
with st.container(border=True):
    st.markdown("""
1. Set **Target lag** to `1 day`
2. Confirm the warehouse is set to **CAPITAL_WH**
3. Click **Create**
""")

st.write("")

st.markdown("##### Step 8: Wait for indexing to complete")
with st.container(border=True):
    st.markdown("""
After clicking Create, Cortex Search begins building the embedding index over all chunks in `DOCUMENT_CHUNKS`.

1. You'll see `INVESTMENT_DOCS_SEARCH` appear in the Cortex Search list
2. Wait until the status shows **Ready** before proceeding

Indexing the investment documents typically takes 1–3 minutes.
""")

st.markdown("---")

st.markdown("#### :material/query_stats: Test with the Interactive Search UI")

st.markdown("""
With the service ready, use the built-in Preview interface to test semantic search across your investment documents.
""")

st.write("")

st.markdown("##### Step 9: Open the Preview")
with st.container(border=True):
    st.markdown("""
1. In Snowsight, navigate to **AI & ML > Cortex Search**
2. Click on `INVESTMENT_DOCS_SEARCH`
3. Click the **Preview** tab to open the interactive search interface
""")

st.write("")

st.markdown("##### Step 10: Run these test queries")
with st.container(border=True):
    st.markdown("Enter each question below one at a time and observe which document chunks are returned:")

    questions = [
        ("1. General research", "What is the analyst outlook for Canadian bank stocks?"),
        ("2. Infrastructure thesis", "infrastructure investment thesis and rising rate impact"),
        ("3. Risk assessment", "What risks are associated with our fixed income portfolio?"),
        ("4. ESG criteria", "What are the ESG screening criteria updates?"),
        ("5. Compliance", "What are the compliance requirements for personal trading?"),
        ("6. Rate cycle", "How is the Bank of Canada rate cycle affecting our portfolio positioning?"),
    ]
    for title, q in questions:
        with st.container(border=True):
            st.markdown(f"**{title}**")
            st.code(q, language="text", wrap_lines=True)

    st.markdown("""
**What to observe**:
- Results are drawn from across all 15 documents — regardless of which specific file contains the answer
- The most semantically relevant chunks appear first, even if the exact query words don't appear in the text
- Try using the filter panel to narrow results by `DOCUMENT_TYPE` (e.g., filter to "Investment Memo" only)
""")

st.write("")

st.markdown("##### Step 11: Test attribute filtering")
with st.container(border=True):
    st.markdown("""
The attribute columns you configured allow precise filtering alongside semantic search:

1. In the Preview interface, find the **Filters** panel
2. Set `DOCUMENT_TYPE` = `Investment Memo`
3. Search for: `infrastructure investment thesis`
4. Confirm only chunks from the investment memo documents are returned

Try a second filter:
- Set `DOCUMENT_TYPE` = `Research Report`
- Search for: `NVIDIA artificial intelligence data center revenue`
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
    {"term": "Cortex Search Service", "definition": "A Snowflake-native search service created via the Snowsight UI or SQL. It indexes a text column from a table or query, builds an embedding index, and enables semantic retrieval through the Preview UI or the REST API."},
    {"term": "Embedding Index", "definition": "A searchable index of dense vector representations of text. Each chunk is represented as a high-dimensional vector. Similar meanings produce similar vectors, enabling semantic retrieval by nearest-neighbor search."},
    {"term": "Hybrid Search", "definition": "A retrieval strategy that combines dense vector search (semantic similarity) with sparse BM25 (keyword frequency) scoring. Produces better results than either method alone, especially for mixed natural language and specific-term queries."},
    {"term": "Attribute Columns", "definition": "Columns configured as filterable metadata on a Cortex Search service. They are indexed separately from the search column and allow results to be filtered by value (e.g., document_type = 'Research Report') without affecting semantic scoring."},
    {"term": "TARGET_LAG", "definition": "How frequently Cortex Search refreshes its index from the source table. Set to '1 day' for batch use cases, '1 minute' for near-real-time search. Lower lag = more compute cost."},
])

render_what_you_built([
    "INVESTMENT_DOCS_SEARCH — Cortex Search service over 15 investment PDFs",
    "Semantic search tested across multiple query patterns via the Preview UI",
    "Attribute filtering by document_type demonstrated",
    "Search service ready to be added as an agent tool in Session 5",
])

st.markdown("---")

st.info("""
:material/terminal: **Everything above can also be done with a single Cortex Code prompt.** If you prefer to set up the search service programmatically rather than through the UI, paste the following into Cortex Code:

```sql
CREATE OR REPLACE CORTEX SEARCH SERVICE SLC_PORTFOLIO_AI.PORTFOLIO_ANALYTICS.INVESTMENT_DOCS_SEARCH
  ON chunk_text
  ATTRIBUTES document_type, security_ticker, document_name, chunk_index
  TARGET_LAG = '1 day'
  WAREHOUSE = CAPITAL_WH
  AS (
    SELECT chunk_id, chunk_text, document_type, security_ticker, document_name, chunk_index
    FROM SLC_PORTFOLIO_AI.PORTFOLIO_ANALYTICS.DOCUMENT_CHUNKS
  );

SHOW CORTEX SEARCH SERVICES IN SCHEMA SLC_PORTFOLIO_AI.PORTFOLIO_ANALYTICS;
```

The UI and the SQL produce identical results — the UI is simply a guided wrapper around this DDL.
""")
