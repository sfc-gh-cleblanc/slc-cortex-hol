import streamlit as st

st.title("Capital Management AI Workshop")
st.markdown("Building Intelligence for Portfolio Analytics with Snowflake Cortex")

st.write("")

st.markdown("#### How this workshop works")

st.markdown("""
This guide provides **step-by-step instructions** for each session. You'll work through a mix of:

- **Cortex Code prompts** — copy into Cortex Code to build infrastructure and write SQL/Python
- **Snowsight UI walkthroughs** — follow guided steps to create semantic views, search services, and agents
- **Interactive exploration** — paste questions into CoWork for collaborative analysis

All sections build on each other sequentially — work through them in order.
""")

st.write("")

st.markdown("#### The scenario")
with st.container(border=True):
    st.markdown("""
Capital Management manages pension plans, registered accounts (RRSP, RRIF, TFSA), and institutional portfolios
on behalf of thousands of Canadian clients. Portfolio managers and analysts need to track position-level performance,
extract insights from investment research documents, monitor risk concentrations, and surface timely recommendations
— all while handling a growing volume of unstructured research reports, compliance notes, and market commentary.

We'll build a complete AI-powered portfolio intelligence platform covering:

| Data type | Examples |
|-----------|---------|
| **Structured** | Client accounts, portfolio positions, securities reference, asset class benchmarks, analyst recommendations |
| **Unstructured** | Research reports, investment memos, fund prospectuses, market commentary, risk assessments, compliance notes |
| **Reference** | Asset class definitions, benchmark indices, risk profiles |
""")

st.write("")

st.markdown("#### What we're building")

with st.container(border=True):
    st.markdown("""
In this workshop, we build a complete AI-powered portfolio analytics platform:

**1. Data Foundation** — Load structured portfolio data and upload investment research documents into Snowflake.

**2. AI-Powered Extraction** — Use Cortex AI functions (AI_EXTRACT, AI_CLASSIFY, AI_COMPLETE) to transform unstructured analyst notes and investment documents into queryable structured data at scale.

**3. Cortex Search** — Parse and chunk PDF investment documents, then create a Cortex Search service that enables semantic search across research reports, fund prospectuses, and compliance documents.

**4. Natural Language Analytics** — Create a Semantic View over portfolio tables using the Autopilot and query them with plain English via Cortex Analyst.

**5. AI Agents** — Create a Cortex Agent that combines structured portfolio analytics with document search for self-service portfolio intelligence.

**6. Collaborative Analysis** — Use CoWork to explore portfolio data and research documents collaboratively with AI assistance.

**7. Operations Dashboard** — Deploy a Streamlit app with live KPIs, charts, and AI-powered investment insights.
""")

st.write("")

st.markdown("#### Prerequisites")
with st.container(border=True):
    st.markdown("""
- Snowflake account with **ACCOUNTADMIN** role — see **Getting Started** in the sidebar to provision a free trial
- **Cortex Code** open in Snowsight and connected to your account
- Cross-region inference enabled (for Cortex LLM functions)
""")

st.write(""); st.write("")
st.caption("Capital Management AI Workshop — TBD")
