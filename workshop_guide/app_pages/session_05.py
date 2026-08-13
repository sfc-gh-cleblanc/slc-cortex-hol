import streamlit as st
from components import render_session_header, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(5, "Cortex Agents", "25 min", "Cortex Agent with semantic view + Cortex Search tools for portfolio analytics")

render_technologies_used([
    {"name": "Cortex Agent", "description": "An orchestrating AI that plans tasks, selects tools, executes them, reflects on results, and generates responses. Created as a first-class Snowflake object via the Snowsight UI.", "icon": "smart_toy"},
    {"name": "Dual Tool Routing", "description": "The agent uses both a semantic view tool (for structured portfolio data) and a Cortex Search tool (for investment research documents) — routing each question to the appropriate tool automatically.", "icon": "route"},
    {"name": "Agent Instructions", "description": "Custom instructions that define the agent's role, behavior, domain expertise, and response style. Shapes how the agent interprets and answers questions.", "icon": "edit_note"},
])

st.markdown("---")

st.markdown("#### :material/smart_toy: Create a Cortex Agent")

st.markdown("""
In this session, you'll create a Cortex Agent using the Snowsight UI. The agent will use both your semantic view from Session 4
and the Cortex Search service from Session 3 as tools — enabling it to answer both structured portfolio questions
and unstructured research document questions in a single conversational interface.
""")

st.write("")

st.markdown("##### Step 1: Open the Agent Builder")
with st.container(border=True):
    st.markdown("""
1. In Snowsight, navigate to **AI & ML** in the left sidebar
2. Click **Cortex Agents**
3. Click **Create Agent** (or the **+** button)
""")

st.write("")

st.markdown("##### Step 2: Configure the agent")
with st.container(border=True):
    st.markdown("""
1. Set the database to **SLC_PORTFOLIO_AI** and schema to **PORTFOLIO_ANALYTICS**
2. Enter the object name: `PORTFOLIO_ANALYST_AGENT`
3. Enter the display name: `Portfolio Analyst Agent`
4. Click **Create agent**
""")

st.write("")

st.markdown("##### Step 3: Write agent instructions")
with st.container(border=True):
    st.markdown("""
1. Click the **Configuration** tab
2. Click the **Instructions** sub-tab

**Orchestration instructions** — paste the following into the orchestration instructions box:
""")
    st.code("""You are a portfolio analytics assistant for Sun Life Capital. Your role is to help portfolio managers, analysts, and relationship managers understand client holdings, identify risk concentrations, surface investment signals, and answer questions about research documents.

When answering questions:
- Use the Portfolio Data tool for structured queries about positions, clients, performance, allocations, and analyst recommendations
- Use the Investment Research tool for questions about research reports, investment memos, fund prospectuses, risk assessments, and compliance documents
- When a question involves both data and research context (e.g., "What do we hold in Canadian banks and what does our research say about them?"), use both tools and synthesize the answer
- Format currency amounts in CAD; note when values are in USD
- Flag any concentration risk, unusual position sizes, or analyst sentiment changes
- Be concise but thorough — include context that helps portfolio managers make decisions

Domain context:
- Account types: Pension, RRSP, RRIF, TFSA, Institutional, Non-Registered
- Risk profiles: Conservative, Moderate, Balanced, Growth, Aggressive
- Key metrics: unrealized gain/loss, portfolio drift from target allocation, recommendation distribution
- Asset classes: Canadian Equity, US Equity, International Equity, Fixed Income, Real Estate, Infrastructure, Cash, Alternatives
- Key benchmarks: S&P/TSX Composite, S&P 500, MSCI EAFE, FTSE Canada Universe Bond""", language="text", wrap_lines=True)
    st.markdown("""
**Response instructions** — paste the following into the response instructions box:
""")
    st.code("Always use charts and visualizations to show data whenever possible. Prefer bar charts for comparisons, line charts for trends over time, and tables for detailed breakdowns. When citing research documents, mention the source document name.", language="text", wrap_lines=True)

st.write("")

st.markdown("##### Step 4: Add the semantic view as the Portfolio_Data tool")
with st.container(border=True):
    st.markdown("""
1. Click the **Tools** sub-tab (still under Configuration)
2. Next to **Query structured data**, click the **+ Add semantic view** button
3. Select `PORTFOLIO_ANALYTICS_VIEW` (the semantic view created in Session 4)
4. Give the tool a name: `Portfolio_Data`
5. Click **Generate with Cortex** to create a detailed description for the tool
6. Click **Add**
""")

st.write("")

st.markdown("##### Step 5: Add the Cortex Search service as the Investment Research tool")
with st.container(border=True):
    st.markdown("""
This step adds document search as a second tool — enabling the agent to answer questions about research reports,
fund prospectuses, market commentary, and compliance documents.

1. Still in the **Tools** sub-tab, click the **+ Add search** button next to **Search documents**
2. Select `INVESTMENT_DOCS_SEARCH` (the Cortex Search service created in Session 3)
3. Give the tool a name: `Investment_Research`
4. Paste the following into the **Description** field:
""")
    st.code(
        "Searches investment documents including research reports, fund prospectuses, quarterly reports, "
        "investment memos, market commentary, risk assessments, and compliance notes. Use this tool to answer "
        "questions about investment thesis, analyst recommendations, risk factors, ESG criteria, compliance "
        "requirements, and document-level research across all indexed securities.",
        language="text",
        wrap_lines=True
    )
    st.markdown("""
5. Under **Advanced configuration**, set the following:

| Field | Value | Notes |
|-------|-------|-------|
| **Max results** | `5` | Maximum chunks the agent can retrieve per query |
| **Target results** | `3` | Target number of high-quality results |
| **ID column** | `CHUNK_ID` | Used to generate hyperlinks to the source |
| **Title column** | `DOCUMENT_NAME` | Shown in citations and source cards |

6. Leave **Indexed columns** empty and click **Add**

Your agent now has two tools:
- **Portfolio_Data** — structured queries via Cortex Analyst
- **Investment_Research** — semantic search via Cortex Search
""")

st.markdown("""
**All available agent tool types:**

| Tool type | Description |
|-----------|-------------|
| **Query structured data** | Semantic views — the agent generates SQL via Cortex Analyst to answer data questions |
| **Search documents** | Cortex Search services — retrieves relevant passages from unstructured document collections |
| **Web search** | Enables the agent to search the internet for real-time information |
| **Custom tools** | SQL UDFs or stored procedures — extend the agent with custom business logic or external API calls |

Using both structured and document search tools together creates a much more capable agent than either alone.
""")

st.write("")

st.markdown("##### Step 6: Add sample questions")
with st.container(border=True):
    st.markdown("""
1. Click the **General** sub-tab (under Configuration)
2. Click **Add question** for each of the following sample questions:
""")
    st.code("What is our total assets under management and how is it distributed by asset class?", language="text", wrap_lines=True)
    st.code("Which clients have the highest concentration risk in a single security?", language="text", wrap_lines=True)
    st.code("What do our research reports say about the outlook for Canadian banks?", language="text", wrap_lines=True)
    st.code("Show me the distribution of analyst recommendations across our held securities", language="text", wrap_lines=True)

st.write("")

st.markdown("##### Step 7: Save the agent")
with st.container(border=True):
    st.markdown("""
Click the **Save** button to save all your configuration — instructions, tools, and sample questions.
The agent must be saved before it can be tested.
""")

st.write("")

st.markdown("##### Step 8: Test the agent")
with st.container(border=True):
    st.markdown("""
1. Click the **Preview** tab to open the agent's chat interface
2. Test your agent by entering these queries one at a time — notice how the agent routes each to the appropriate tool:
""")
    test_queries = [
        ("Structured data query", "What is our total portfolio value and how is it broken down by asset class?"),
        ("Document search query", "What does our research say about the infrastructure investment thesis?"),
        ("Cross-tool query", "What is our current exposure to Canadian bank stocks, and what do our analysts say about the outlook?"),
        ("Risk query", "Which clients have unrealized losses greater than 20% and what positions are driving it?"),
        ("Document + risk", "What ESG screening criteria updates should I be aware of for our equity holdings?"),
    ]
    for label, query in test_queries:
        with st.container(border=True):
            st.markdown(f"**{label}**")
            st.code(query, language="text", wrap_lines=True)
    st.markdown("""
Observe how the agent:
- Routes pure data questions to the Portfolio Data (semantic view) tool
- Routes document questions to the Investment Research (Cortex Search) tool
- Uses **both tools** for cross-tool questions, then synthesizes a combined answer
""")

st.write("")

st.markdown("##### Step 9: Add to Snowflake CoWork")
with st.container(border=True):
    st.markdown("""
Click the **+ Add to Snowflake CoWork** button to make this agent accessible within CoWork.

**Why this is required:** By default, a Cortex Agent is a Snowflake object callable via SQL or REST API, but not automatically surfaced in CoWork. Adding it to CoWork registers the agent as an available assistant — which is what we'll use in Session 6.

**Methods to access agents:**

| Access method | Use case |
|---------------|----------|
| **CoWork** | Collaborative data exploration with team members |
| **REST API** | Embed the agent in external applications or custom UIs |
| **SQL (CORTEX.AGENT)** | Call the agent programmatically from SQL, stored procedures, or notebooks |
| **Streamlit apps** | Build custom chat interfaces powered by the agent (Session 7) |
""")

st.markdown("---")
st.markdown("---")

render_explanation("How the agent routes between tools", """
**Tool routing** is one of the most powerful capabilities of Cortex Agents. Here's how it works with two tools:

1. **User question received**: "What do we hold in Canadian banks and what does our research say?"
2. **Intent analysis**: The agent recognizes this involves both (a) portfolio holdings data and (b) research document content
3. **Tool planning**: It decides to call both the Portfolio Data tool and the Investment Research tool
4. **Parallel or sequential execution**: Calls Cortex Analyst on the semantic view for holdings data, and Cortex Search for research passages
5. **Synthesis**: Combines the structured data response and the search results into a coherent answer

**How the agent decides which tool to use**:
- The tool **description** is critical — the agent uses it to match questions to tools
- Explicit signals in the question ("what does our research say") point to the search tool
- Questions containing numbers, aggregations, or comparisons point to the data tool
- Ambiguous questions may trigger both tools

**Why this matters for portfolio management**:
An analyst asking "Should we increase our NVDA position?" needs:
- **Structured data**: Current position size, client exposure, unrealized P&L
- **Research documents**: Analyst reports, investment memos, risk assessments

A single agent with both tools answers the full question without the analyst switching between systems.
""")


render_key_concepts([
    {"term": "Cortex Agent", "definition": "A first-class Snowflake object that orchestrates LLMs and tools to answer complex questions. Supports planning, tool use, reflection, and multi-turn conversations. Created via UI or CREATE AGENT SQL."},
    {"term": "Tool Routing", "definition": "The agent's ability to select the appropriate tool for each question, based on the tool descriptions and question intent. With a semantic view + Cortex Search, the agent routes data questions to SQL and document questions to search."},
    {"term": "Cross-Tool Synthesis", "definition": "When the agent calls multiple tools in response to a single question, it synthesizes the results into a unified response. This enables answers that combine quantitative data and qualitative research context."},
    {"term": "Agent Instructions", "definition": "A system prompt that defines the agent's role, behavior, domain expertise, and response style. Good instructions lead to more accurate tool routing, better formatted responses, and domain-appropriate context."},
])

st.write("")

st.markdown("##### :material/science: Advanced topics (not covered in this workshop)")

render_key_concepts([
    {"term": "Agent Evaluations", "definition": "A systematic process for measuring agent quality. Evaluations run a set of test questions against your agent and score responses on metrics like correctness, relevance, and SQL accuracy. They help you quantify improvements when you change instructions, add tools, or modify the semantic view."},
    {"term": "Agent Observability", "definition": "Monitoring and tracing how your agent performs in production. Observability tracks response latency, tool call frequency, error rates, and user satisfaction. Trace-level visibility shows which tools were called, what SQL was generated, and where failures occur."},
])

render_what_you_built([
    "PORTFOLIO_ANALYST_AGENT — Cortex Agent with semantic view + Cortex Search tools",
    "Dual-tool routing for structured data and document research questions",
    "Custom instructions for capital management domain expertise",
    "Tested cross-tool queries combining portfolio data and investment research",
    "Agent ready for CoWork integration (Session 6)",
])
