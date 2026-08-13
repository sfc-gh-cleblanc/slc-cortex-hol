import streamlit as st

st.title("Workshop Agenda")

AGENDA = [
    ("Introductions & Overview", "15 min", None),
    ("Session 1: Data Prep", "30 min", "1"),
    ("Session 2: AI SQL", "40 min", "2"),
    ("Session 3: Cortex Search", "30 min", "3"),
    ("Session 4: Cortex Analyst & Semantic Views", "35 min", "4"),
    (":orange-badge[BREAK]", "15 min", None),
    ("Session 5: Cortex Agents", "25 min", "5"),
    ("Session 6: CoWork", "20 min", "6"),
    ("Session 7: Streamlit", "25 min", "7"),
]

for title, duration, session_num in AGENDA:
    if session_num:
        col1, col2 = st.columns([4, 1])
        col1.markdown(f":material/play_circle: **{title}**")
        col2.markdown(f":gray-badge[{duration}]")
    elif "BREAK" in title:
        col1, col2 = st.columns([4, 1])
        col1.markdown(f"{title}")
        col2.markdown(f":gray-badge[{duration}]")
    else:
        col1, col2 = st.columns([4, 1])
        col1.markdown(f":gray[{title}]")
        col2.markdown(f":gray-badge[{duration}]")

st.write(""); st.write("")

st.markdown("##### What you'll build")
st.markdown("""
| Object Type | Count | Examples |
|-------------|-------|---------|
| **Tables** | 7 | Clients, positions, securities, asset classes, analyst notes, communications, document chunks |
| **AI Extractions** | 1 | EXTRACTED_INVESTMENT_INSIGHTS materialized table |
| **Cortex Search Service** | 1 | INVESTMENT_DOCS_SEARCH over 15 parsed investment PDFs |
| **Semantic Views** | 1 | Portfolio analytics semantic view (via Autopilot) |
| **Cortex Agents** | 1 | Portfolio analyst agent with semantic view + search tools |
| **Streamlit Apps** | 1 | Portfolio dashboard with KPIs and charts |
""")

st.write("")

st.markdown("##### Total duration")
with st.container(border=True):
    st.markdown("""
:material/schedule: **~4 hours**
(including 15-minute break between Block 1 and Block 2)

Capital Management AI Workshop — August 21, 2026
""")
