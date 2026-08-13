import streamlit as st
from components import render_session_header, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(4, "Cortex Analyst & Semantic Views", "35 min", "Semantic view created via Autopilot, tested with natural language queries")

render_technologies_used([
    {"name": "Semantic View Autopilot", "description": "A UI-guided tool in Snowsight that automatically generates a semantic view from your tables — detecting relationships, creating dimensions, facts, metrics, and synonyms.", "icon": "auto_awesome"},
    {"name": "Cortex Analyst", "description": "Snowflake's text-to-SQL engine that converts natural language questions into SQL queries. Uses a semantic view to understand your data's business meaning, relationships, and metrics.", "icon": "chat"},
    {"name": "Semantic View", "description": "A first-class Snowflake object that describes your data in business terms: tables, relationships, facts, dimensions, metrics, and synonyms. The bridge between natural language and SQL.", "icon": "description"},
])

st.markdown("---")

st.markdown("#### :material/auto_awesome: Create a Semantic View with Autopilot")

st.markdown("""
In this session, you'll use the **Semantic View Autopilot** to create a semantic view over your portfolio data — no SQL required.
The Autopilot analyzes your tables and generates a complete semantic view with relationships, metrics, and dimensions.
""")

st.write("")

st.markdown("##### Step 1: Open the Semantic View Autopilot")
with st.container(border=True):
    st.markdown("""
1. In Snowsight, navigate to **AI & ML** in the left sidebar
2. Click **Cortex Analyst**
3. Click the **Create with Autopilot** button in the top right
""")

st.write("")

st.markdown("##### Step 2: Provide context")
with st.container(border=True):
    st.markdown("""
While providing context is optional, it's extremely useful in creating a high-quality semantic view.
Without it, the model only uses the database schema information, which might lack business nuance.
The Autopilot supports several options for providing context: Tableau workbooks, Power BI reports, existing SQL queries, and others.

For this workshop, we'll skip this step since our table and column names are descriptive enough for the Autopilot to work with.

1. Click **Skip** to proceed to the next step
""")

st.write("")

st.markdown("##### Step 3: Name your semantic view")
with st.container(border=True):
    st.markdown("""
1. Enter the name: `PORTFOLIO_ANALYTICS_VIEW`
2. Set the database to **SLC_PORTFOLIO_AI**
3. Set the schema to **PORTFOLIO_ANALYTICS**
4. Click **Next**
""")

st.write("")

st.markdown("##### Step 4: Select tables")
with st.container(border=True):
    st.markdown("""
1. Select these tables:
   - `CLIENTS`
   - `POSITIONS`
   - `SECURITIES`
   - `ASSET_CLASSES`
   - `EXTRACTED_INVESTMENT_INSIGHTS` (from Session 2)
2. Click **Next**
""")

st.write("")

st.markdown("##### Step 5: Select columns")
with st.container(border=True):
    st.markdown("""
1. Click **Select all** to include all columns from all selected tables
2. Click **Create** to complete the wizard

The Autopilot will analyze your tables and generate a semantic view with auto-detected relationships, dimensions, facts, metrics, and synonyms. This may take a moment.
""")

st.write("")

st.markdown("##### Step 6: Confirm relationships")
with st.container(border=True):
    st.markdown("""
Relationships are shown in the **Suggestions panel** on the right side of the screen — not inline in the main editor.

1. Look for the **Suggestions** tab in the top-right panel (it will show a count, e.g. **Suggestions 9**)
2. Scroll down within the Suggestions panel to the **Relationships** section — it will show **5 detected relationships**
3. For each relationship, click **Review** to inspect the join, then click **Add** to include it in the semantic view
4. Repeat until all 5 relationships are added

The 5 expected relationships are:
| Relationship | Join |
|---|---|
| `EXTRACTED_INVESTMENT_INSIGHTS_TO_SECURITIES` | `EXTRACTED_INVESTMENT_INSIGHTS.SECURITY_ID` → `SECURITIES.SECURITY_ID` |
| `POSITIONS_TO_ASSET_CLASSES` | `POSITIONS` → `ASSET_CLASSES` |
| `POSITIONS_TO_CLIENTS` | `POSITIONS.CLIENT_ID` → `CLIENTS.CLIENT_ID` |
| `POSITIONS_TO_SECURITIES` | `POSITIONS.SECURITY_ID` → `SECURITIES.SECURITY_ID` |
| `SECURITIES_TO_ASSET_CLASSES` | `SECURITIES.ASSET_CLASS` → `ASSET_CLASSES.NAME` |

These relationships define the table joins that Cortex Analyst uses when generating SQL. Adding all of them ensures cross-table questions work correctly.
""")

st.write("")

st.markdown("##### Step 7: Add a verified query")
with st.container(border=True):
    st.markdown("""
**Verified queries** are pre-validated question-and-SQL pairs that guarantee Cortex Analyst returns the correct result for specific questions. They are one of the most important tools for improving accuracy in production.

**Why verified queries matter:**
- They act as "ground truth" — when a user asks a question that matches a verified query, Analyst returns the exact SQL you specified rather than generating its own
- They handle edge cases, business-specific logic, and complex joins that the model might get wrong
- They build trust with end users by ensuring critical questions always produce correct answers

**To add a verified query:**
1. In the suggestions box, click the **Add a verified query** button
2. Enter a question: `What is the total portfolio value under management, the number of active clients, and the average unrealized gain or loss per position?`
3. Click **Generate SQL** to view the generated SQL
4. Click **Run** to execute the query and confirm expected results
5. Click **Save and continue** to add this as a verified query
""")

st.write("")

st.markdown("##### Step 8: Add a view description")
with st.container(border=True):
    st.markdown("""
A well-written description helps both AI agents and human users understand when to use this semantic view.
When a Cortex Agent has multiple tools available, it uses the view description to decide whether this is the right tool for a given question.

1. Click the **Edit** button (pencil icon) to the right of the view name at the top
2. In the description field, paste the following description:
""")
    st.code("Portfolio analytics for Capital Management covering client investment accounts, portfolio positions, security reference data, asset class allocations, and AI-extracted analyst insights. Use this view for questions about total assets under management, portfolio performance, unrealized gains and losses, asset class allocation drift, security exposure by sector, client risk profiles, position concentration, analyst recommendation trends, and account type breakdowns.", language="text", wrap_lines=True)
    st.markdown("""
3. Click **Apply** to accept this update

This description will be visible to Cortex Agents when they evaluate which tool to use for a given question — the more specific and comprehensive it is, the better the agent's tool routing will be.
""")

st.write("")

st.markdown("##### Step 9: Save the semantic view")
with st.container(border=True):
    st.markdown("""
Click **Save** to accept all the changes you've made — relationships, verified query, and description.
Your semantic view is now ready for use with Cortex Analyst and Cortex Agents.
""")

st.markdown("---")

st.markdown("#### :material/chat: Test with Natural Language Queries")

st.markdown("""
Click the **Playground** tab on the right side of the semantic view editor. This opens an interactive chat where you can test natural language questions against your view.

Enter each question below one at a time and click **Run** to see the generated SQL and results:
""")

questions = [
    ("1. Top positions", "What are the top 10 securities by total market value across all client portfolios?"),
    ("2. Asset allocation", "Show me the breakdown of total portfolio value by asset class"),
    ("3. Unrealized losses", "Which clients have the largest unrealized losses and what asset classes are driving it?"),
    ("4. Analyst sentiment", "What is the distribution of analyst recommendations — how many Buy, Hold, and Sell ratings do we have?"),
    ("5. Account type analysis", "Compare average portfolio value by account type — which account types have the highest average AUM?"),
    ("6. Sector concentration", "Which sectors represent the largest share of total market value across all positions?"),
]

for title, question in questions:
    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.code(question, language="text", wrap_lines=True)

st.info("""
:material/lightbulb: **Tip:** If any of these test questions produce particularly useful results, you can save them as additional verified queries directly from the Playground by clicking the save option on the result.
""")

render_explanation("What these queries test", """
Each query exercises different capabilities of the semantic view:

1. **"Top 10 securities by total market value"** — Tests GROUP BY on SECURITY_ID, joining to SECURITIES for names, aggregating MARKET_VALUE with ORDER BY DESC.

2. **"Breakdown by asset class"** — Tests joining POSITIONS to ASSET_CLASSES via SECURITIES.ASSET_CLASS, grouping and summing MARKET_VALUE.

3. **"Clients with largest unrealized losses"** — Tests filtering WHERE UNREALIZED_GAIN_LOSS < 0, joining to CLIENTS, GROUP BY client, ORDER BY.

4. **"Analyst recommendation distribution"** — Tests EXTRACTED_INVESTMENT_INSIGHTS.EXTRACTED_RECOMMENDATION, GROUP BY to produce a count/percentage breakdown.

5. **"Average portfolio value by account type"** — Tests CLIENTS.ACCOUNT_TYPE dimension, AVG(PORTFOLIO_VALUE) metric.

6. **"Sector concentration"** — Tests SECURITIES.SECTOR dimension, SUM(MARKET_VALUE) across POSITIONS, percentage of total.

**What to observe**: Look at the generated SQL — does it correctly identify which tables to join, which metrics to use, and how to filter? This demonstrates the power of the semantic layer.
""")


render_key_concepts([
    {"term": "Semantic View Autopilot", "definition": "A UI tool that automatically generates a semantic view by analyzing table structures, detecting foreign key relationships, inferring appropriate dimensions/facts/metrics, and adding synonyms. Significantly reduces the time to create a working semantic view."},
    {"term": "Cortex Analyst", "definition": "Snowflake's text-to-SQL engine. Takes natural language questions and generates SQL queries using a semantic view for context. Supports aggregations, joins, filtering, time-series analysis, and diverse query types."},
    {"term": "Fact vs Dimension vs Metric", "definition": "Facts are raw numeric columns (market_value, cost_basis). Dimensions are categorical/temporal columns for grouping and filtering (asset_class, account_type, province). Metrics are pre-defined aggregations (SUM(market_value), AVG(unrealized_gain_loss))."},
    {"term": "Verified Queries", "definition": "Pre-validated question-SQL pairs stored in the semantic view. When a user asks a matching question, Cortex Analyst returns the verified SQL rather than generating new SQL. Ensures accuracy for critical business questions."},
])

render_what_you_built([
    "PORTFOLIO_ANALYTICS_VIEW semantic view (via Autopilot)",
    "Auto-detected relationships between 5 tables",
    "Natural language queries tested across multiple portfolio analytics patterns",
    "Validated text-to-SQL accuracy for capital management analytics",
])
