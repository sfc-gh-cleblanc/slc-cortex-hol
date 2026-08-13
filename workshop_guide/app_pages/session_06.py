import streamlit as st
from components import render_session_header, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(6, "CoWork", "20 min", "Collaborative AI analysis of portfolio data and investment research")

render_technologies_used([
    {"name": "Snowflake CoWork", "description": "An AI-powered collaborative workspace inside Snowsight where you can analyze data, generate insights, and share findings with your team — all through natural language conversation.", "icon": "group"},
    {"name": "Agent Integration", "description": "CoWork leverages your Cortex Agents to answer questions. The PORTFOLIO_ANALYST_AGENT from Session 5 powers both data analytics and research document search.", "icon": "smart_toy"},
    {"name": "Sharing & Collaboration", "description": "CoWork sessions can be shared with team members, creating a collaborative space for portfolio review and investment decision support.", "icon": "share"},
])

st.markdown("---")

st.markdown("#### :material/open_in_new: Open CoWork")
with st.container(border=True):
    st.markdown("""
Open Snowflake CoWork using one of these methods:

- **In Snowsight:** Navigate to **AI & ML** in the left sidebar and select **Snowflake CoWork**
- **In any browser:** Go to **[ai.snowflake.com](https://ai.snowflake.com)**

Start a new conversation. CoWork will have access to the `PORTFOLIO_ANALYST_AGENT` you added in Session 5.

Paste each question below into CoWork one at a time and observe how it generates queries, searches documents, and produces visualizations.
""")

st.write("")

st.markdown("#### :material/chat: Questions to ask CoWork")
st.caption("Copy and paste each question into CoWork individually. They build on each other in sequence.")

questions = [
    ("1. Portfolio Overview",
     "Show me a summary of our assets under management — total portfolio value, number of active clients, average portfolio size by account type, and the top 5 asset classes by total value."),
    ("2. Investment Recommendations",
     "What are the latest investment recommendations, price targets, key risks, investment horizons, and suggested portfolio actions across our tracked tickers?"),
    ("3. Analyst Sentiment",
     "What is the current distribution of analyst recommendations (Buy, Hold, Sell, Overweight, Underweight) across our held securities? Are there any securities where the analyst rating appears inconsistent with our current position size?"),
    ("4. Research: Infrastructure",
     "Search our investment research documents for the infrastructure allocation thesis. What were the key reasons for increasing the infrastructure weight, and what risks were identified?"),
    ("5. Asset Allocation Drift",
     "Compare our current asset class allocations to the target allocations from the ASSET_CLASSES table. Which asset classes are most over- or under-weight? What trades would bring us back within the tolerance bands?"),
    ("6. Executive Summary",
     "Generate an executive summary of our portfolio health that I could share with the Investment Committee. Include total AUM, top concentration risks, analyst sentiment overview, and two or three key items from our recent research documents."),
]

for i, (title, question) in enumerate(questions):
    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.code(question, language="text", wrap_lines=True)
    if i == 0:
        st.info("""
:material/save: **Save the chart as an artifact:** After CoWork responds with a visualization, click the **Save** icon on the chart to save it as an artifact. Artifacts persist in your CoWork session and can be shared with teammates.
""")
    if i == 1:
        st.success("""
:material/verified: **Verified query in action:** This question matches the verified query we created in Session 4. Cortex Analyst uses the pre-validated SQL rather than generating new SQL — giving you confidence the result is accurate.
""")
    if i == 3:
        st.info("""
:material/search: **Document search in action:** This question cannot be answered from the structured tables — it requires searching the investment documents indexed in Cortex Search. Watch how the agent automatically routes this to the Investment Research tool.
""")

st.info("""
:material/lightbulb: **Tip — MCP Integration:** If CoWork were connected to your email system via MCP (Model Context Protocol) under **Capabilities**, you could ask it to automatically draft and send that executive summary directly to the Investment Committee — no copy-paste required. MCP connectors allow CoWork to take actions in external systems like email, Slack, Jira, and more, turning analysis into automated workflows.
""")

st.write("")

render_explanation("How CoWork works with multiple agent tools", """
**CoWork** uses your PORTFOLIO_ANALYST_AGENT, which has two tools. Here's how it handles different question types:

**Structured data questions** (Questions 1, 2, 3, 5):
1. CoWork routes the question to the PORTFOLIO_ANALYST_AGENT
2. The agent determines a semantic view query is needed
3. Cortex Analyst generates SQL against PORTFOLIO_ANALYTICS_VIEW
4. Results are displayed with automatic visualizations

**Document search questions** (Question 4):
1. CoWork routes the question to the agent
2. The agent determines Cortex Search is the right tool
3. INVESTMENT_DOCS_SEARCH returns the most relevant document chunks
4. The agent synthesizes a natural language summary from the retrieved passages

**Mixed questions** (Question 6 — Executive Summary):
1. The agent decides it needs both tools
2. Calls Cortex Analyst for quantitative metrics (AUM, drift, sentiment distribution)
3. Calls Cortex Search for relevant research document passages
4. Synthesizes all results into a coherent executive narrative

**What CoWork adds over direct Cortex Analyst or Cortex Search**:
- Maintains conversation context for follow-up questions
- Can combine answers from multiple tools in a single response
- Generates charts and visualizations automatically
- Session can be shared with team members for collaborative review
""")


render_key_concepts([
    {"term": "CoWork", "definition": "Snowflake's collaborative AI workspace for data exploration. Provides a conversational interface that queries data, searches documents, creates visualizations, and generates insights. Designed for business analysts and team collaboration."},
    {"term": "Multi-Tool Agent in CoWork", "definition": "When the underlying agent has multiple tools (semantic view + Cortex Search), CoWork automatically benefits from both. Questions about data go to structured analytics; questions about research go to document search."},
    {"term": "Context Maintenance", "definition": "CoWork maintains conversation history so follow-up questions build on previous analysis. Ask 'Show concentration risk by client' then 'Now filter to just Pension accounts' — it remembers the context."},
])

render_what_you_built([
    "Explored portfolio data through conversational AI in CoWork",
    "Generated visualizations and cross-table analysis",
    "Searched investment research documents for qualitative context",
    "Identified concentration risks and allocation drift",
    "Created an executive portfolio summary combining data and research",
])
