import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(7, "Streamlit", "25 min", "Portfolio dashboard with KPIs, charts, and AI-powered investment insights")

render_technologies_used([
    {"name": "Streamlit in Snowflake (SiS)", "description": "Deploy Python-based data apps directly within Snowflake. Apps run on container runtime with full Python package support, access data natively via Snowpark, and inherit Snowflake's security model.", "icon": "web"},
    {"name": "Compute Pool", "description": "A managed pool of container nodes that powers SiS apps. Provides CPU/GPU resources, auto-scales, and supports any Python package from pip.", "icon": "memory"},
    {"name": "AI SQL Functions in Apps", "description": "Use Cortex AI functions (AI_CLASSIFY, AI_COMPLETE) directly within Streamlit apps to provide real-time AI-powered investment insights alongside traditional KPIs and charts.", "icon": "auto_fix_high"},
])

st.markdown("---")

st.markdown("#### :material/folder_open: Create a new Workspace")
with st.container(border=True):
    st.markdown("""
1. In Snowsight, navigate to **Projects > Workspaces** in the left sidebar
2. Click **+ Workspace** (top right)
3. Name it **`Streamlit Dashboard`** and click **Create**

You'll use this workspace to build and iterate on the portfolio dashboard app with Cortex Code.
""")

st.write("")

st.markdown("#### :material/open_in_new: Open Cortex Code in the Workspace")
with st.container(border=True):
    st.markdown("""
Inside your new workspace, open Cortex Code and paste the prompts below.
Workspaces provides an IDE-like environment where Cortex Code can create and edit Streamlit app files directly.
""")


PROMPT_7_1 = """In SLC_PORTFOLIO_AI.PORTFOLIO_ANALYTICS, create a Streamlit app called PORTFOLIO_DASHBOARD. The dashboard should display the following:

- KPI cards at the top showing:
  - Total AUM (SUM of MARKET_VALUE from POSITIONS where STATUS = 'Active')
  - Number of Active Clients (COUNT of distinct CLIENT_ID from POSITIONS where STATUS = 'Active')
  - Avg Portfolio Value (total AUM / number of active clients)
  - Total Unrealized Gain/Loss (SUM of UNREALIZED_GAIN_LOSS from POSITIONS where STATUS = 'Active')
- A pie chart showing total market value by ASSET_CLASS
- A bar chart of the top 10 securities by total market value (join POSITIONS to SECURITIES for security names)
- A horizontal bar chart showing total portfolio value by ACCOUNT_TYPE (from CLIENTS joined to POSITIONS)
- An AI Insights section at the bottom that uses AI_CLASSIFY on 5 recent analyst notes to show real-time recommendation categorization

Include a tab in the dashboard that gives descriptions of each metric, where the data is coming from and how often it is updated.

Use st.connection("snowflake") for the Snowflake connection and make it visually clean with st.columns for layout."""

render_prompt("7.1", "Create the Streamlit App", PROMPT_7_1)

render_explanation("What this prompt does", """
Creates a full **Streamlit in Snowflake** application on the **container runtime**:

**Step 1 — Compute pool**:
```sql
CREATE COMPUTE POOL PORTFOLIO_COMPUTE_POOL
  MIN_NODES = 1 MAX_NODES = 1
  INSTANCE_FAMILY = CPU_X64_S;
```

**Step 2 — External Access Integration** (so container can install pip packages):
```sql
CREATE NETWORK RULE pypi_network_rule
  MODE = EGRESS TYPE = HOST_PORT
  VALUE_LIST = ('pypi.org', 'files.pythonhosted.org');

CREATE EXTERNAL ACCESS INTEGRATION pypi_access_integration
  ALLOWED_NETWORK_RULES = (pypi_network_rule)
  ENABLED = TRUE;
```

**Step 3 — Stage files and deploy**:
- Write streamlit_app.py and pyproject.toml to a stage
- Create the Streamlit object on the compute pool

**Dashboard KPI pattern**:
```python
conn = st.connection("snowflake")
session = conn.session()
aum = session.sql(
    "SELECT SUM(MARKET_VALUE) AS total FROM POSITIONS WHERE STATUS = 'Active'"
).collect()[0]['TOTAL']
st.metric("Total AUM", f"${aum:,.0f}")
```

**AI Insights section** uses AI_CLASSIFY directly in the app:
```python
insights = session.sql(\"""
    SELECT NOTE_ID, LEFT(NOTE_TEXT, 50) AS PREVIEW,
           AI_CLASSIFY(NOTE_TEXT,
               ['Earnings Update', 'Risk Flag', 'Price Target Revision',
                'Sector Commentary', 'Initiation of Coverage', 'Regulatory Alert']
           ) AS CATEGORY
    FROM ANALYST_NOTES ORDER BY NOTE_DATE DESC LIMIT 5
\""").to_pandas()
st.dataframe(insights)
```

**Key advantages of SiS**:
- **No data movement**: App runs inside Snowflake
- **Security**: Inherits user's role and permissions
- **No infrastructure**: Compute pool auto-manages lifecycle
- **AI-native**: Call Cortex functions directly from app code
""")


PROMPT_7_2 = """Fix the errors shown on this dashboard"""

st.markdown("##### 7.2 — Test and Fix Errors")

with st.container(border=True):
    st.markdown("""
1. Open the `streamlit_app.py` file in the Workspaces editor
2. Click **Run** in the top-right to preview the dashboard

**Are there any errors?** It's common for the Streamlit skill to assume packages are available that aren't yet installed, or to reference columns slightly differently than expected. If you see errors on the dashboard:

3. Paste the following into Cortex Code:
""")
    st.code("Fix the errors shown on this dashboard", language="text", wrap_lines=True)
    st.markdown("""
4. Click **Keep All** to accept all of the code updates Cortex Code suggests
5. Click **Run** again in the code page to reload the dashboard
6. Repeat steps 3-5 if any errors remain — keep iterating until the dashboard loads cleanly
""")

st.write("")

st.markdown("##### 7.3 — Deploy Your App")

with st.container(border=True):
    st.markdown("""
Once the dashboard is running without errors, click **Deploy** in the top-right of the Workspaces editor. The Deploy app dialog has the following fields:

**App details**

| Field | Value | Notes |
|-------|-------|-------|
| **App title** | `portfolio-dashboard` | Displayed in the top left of the app |
| **App ID** | `PORTFOLIO_DASHBOARD` | Used in the URL — auto-populated |
| **Deployed app owner role matches preview role** | ✅ Checked | Ensures the app runs as ACCOUNTADMIN |

**Execution tab**

| Field | Value | Notes |
|-------|-------|-------|
| **App location** | `SLC_PORTFOLIO_AI` / `PORTFOLIO_ANALYTICS` | Where the Streamlit object is created |
| **Compute pool** | `SYSTEM_COMPUTE_POOL_CPU` | Default — leave as-is |
| **Query warehouse** | `CAPITAL_WH` | ⚠️ **Change this** — the default will be a system warehouse, not your workshop warehouse |

> **Important:** Always check the **Query warehouse** field before deploying. The default is usually a system compute pool warehouse that won't have access to your data. Set it to **CAPITAL_WH**.

Click **Deploy** to publish.

Once deployed, the app becomes a first-class Snowflake object. Other users in your account can discover it from the **Projects > Streamlit** menu in Snowsight and access it based on their role permissions.
""")

st.info("""
:material/lightbulb: **Sharing your app:** After deployment, grant access to other roles:
```sql
GRANT USAGE ON STREAMLIT SLC_PORTFOLIO_AI.PORTFOLIO_ANALYTICS.PORTFOLIO_DASHBOARD TO ROLE <role_name>;
```
This is how teams publish internal data apps — analysts build in Workspaces, deploy to a shared schema, and stakeholders access via the Streamlit projects menu.
""")

render_explanation("Troubleshooting tips", """
**Common errors and fixes:**

- **ModuleNotFoundError** (e.g., `plotly`, `pandas`) — The app references a package not installed in Workspaces. Cortex Code will add the missing import or switch to a built-in Streamlit chart method.
- **Column not found** — The SQL references a column name with wrong casing or spelling. Cortex Code will query INFORMATION_SCHEMA to find the correct name.
- **Connection errors** — Ensure `st.connection("snowflake")` is used (not `snowflake.connector`).

**The iterative pattern:** In Workspaces, you can continuously prompt Cortex Code to fix issues, accept changes, and re-run — this rapid feedback loop is how production Streamlit apps are built and refined.

This completes the workshop — you've built a complete AI-powered portfolio analytics platform from data loading through to a deployed application!
""")

st.write("")

st.markdown("---")

st.markdown("#### :material/star: Bonus: Add an AI Chat Interface")

with st.container(border=True):
    st.markdown("""
Want to take your dashboard further? Add a chat interface that lets portfolio managers ask natural language questions about the data directly within the dashboard.

Paste the following prompt into Cortex Code in your Workspace:
""")
    st.code(
        "Add an 'Ask AI' tab to the portfolio dashboard that lets users type questions about the portfolio "
        "and receive AI-generated answers based on the current portfolio data.",
        language="text",
        wrap_lines=True
    )
    st.markdown("""
Click **Keep All** and **Run** to test the new tab.
""")

st.markdown("---")


render_key_concepts([
    {"term": "Container Runtime", "definition": "The current SiS execution environment. Apps run on a compute pool, support any Python package via pip, and use versioned stage syntax. Replaces the legacy warehouse runtime."},
    {"term": "Compute Pool", "definition": "A managed pool of container nodes. Choose an instance family (CPU_X64_S, GPU_NV_S, etc.), set min/max nodes, and Snowflake handles provisioning and scaling."},
    {"term": "External Access Integration", "definition": "Required for container runtime apps that install pip packages. Container nodes can't reach the internet by default — you must allow egress to pypi.org via network rules."},
    {"term": "AI Functions in Apps", "definition": "Cortex AI functions (AI_CLASSIFY, AI_EXTRACT, AI_COMPLETE) can be called directly from Streamlit app SQL queries, enabling real-time AI-powered features without external services."},
])

render_what_you_built([
    "PORTFOLIO_COMPUTE_POOL — compute pool for container runtime",
    "PORTFOLIO_DASHBOARD — Streamlit app with portfolio KPIs and charts",
    "Asset allocation pie chart and top securities bar chart",
    "AI Insights section using AI_CLASSIFY for real-time analyst note categorization",
])
