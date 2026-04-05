import streamlit as st
import json
import plotly.graph_objects as go
from google import genai
from google.genai import types

# --- CONFIGURATION & STYLING ---
st.set_page_config(
    page_title="Career Strategy Architect",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp { background-color: #0F172A; color: #F1F5F9; }
    section[data-testid="stSidebar"] { background-color: #1E293B; border-right: 1px solid #334155; }
    .stButton button { background-color: #2563EB; color: white; border-radius: 6px; font-weight: 700; }
    .report-card { background-color: #1E293B; padding: 20px; border-radius: 12px; border: 1px solid #334155; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ CAREER STRATEGY ARCHITECT")
st.subheader("High-Fidelity Semantic Audit & Portfolio Synthesis")

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ ENGINE STATUS")
    api_key = st.text_input("Gemini API Key", type="password", placeholder="Enter your key here")
    
    if api_key and len(api_key) > 30:
        st.success("✅ API Key accepted")
    else:
        st.info("Enter your Gemini API Key to enable the engine")
    
    st.divider()
    st.markdown("""
    **Ioannis Kontesis**  
    AI Transformation Architect  
    Operational Resilience & Strategy Specialist  
    Finance & Risk Professional
    
    🔗 [LinkedIn](https://linkedin.com/in/ikontesis) | [𝕏](https://x.com/@ikontesis)
    
    🛡️ Stateless Architecture | **v2.4.0**  
    Powered by Google GenAI SDK
    """)

# --- SESSION STATE ---
if 'audit_json' not in st.session_state:
    st.session_state.audit_json = None

# --- INPUTS ---
col1, col2 = st.columns(2)
with col1:
    master_cv = st.text_area("📄 MASTER CV SOURCE (English)", height=400, 
                             placeholder="Paste your full master CV here...")
with col2:
    job_desc = st.text_area("💼 TARGET JOB DESCRIPTION", height=400, 
                            placeholder="Paste the full job description here...")

st.divider()

# --- AUDIT BUTTON ---
if st.button("🚀 RUN STRATEGIC AUDIT", type="primary", use_container_width=True):
    if not api_key or len(api_key) < 30:
        st.error("Please enter a valid Gemini API Key in the sidebar.")
    elif len(master_cv.strip()) < 150 or len(job_desc.strip()) < 150:
        st.warning("Please provide sufficient data for both CV and Job Description.")
    else:
        with st.spinner("Executing Strategic Semantic Audit with Gemini 3.1..."):
            try:
                client = genai.Client(api_key=api_key)

                audit_prompt = f"""
Analyze the candidate's CV against the target Job Description for a senior/executive position.

Return **ONLY** a valid JSON object with exactly the following structure. No extra text, no markdown.

CV:
{master_cv}

JD:
{job_desc}
"""

                json_schema = {
                    "type": "object",
                    "properties": {
                        "verdict": {
                            "type": "object",
                            "properties": {
                                "level": {"type": "string"},
                                "score": {"type": "integer"},
                                "recommendation": {"type": "string"}
                            },
                            "required": ["level", "score", "recommendation"]
                        },
                        "matrix": {
                            "type": "object",
                            "properties": {
                                "hierarchy": {"type": "integer"},
                                "hard_skills": {"type": "integer"},
                                "evidence": {"type": "integer"},
                                "soft_skills": {"type": "integer"}
                            },
                            "required": ["hierarchy", "hard_skills", "evidence", "soft_skills"]
                        },
                        "missing": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "pivot": {"type": "string"}
                    },
                    "required": ["verdict", "matrix", "missing", "pivot"]
                }

                response = client.models.generate_content(
                    model="gemini-3.1-flash",   # ← πιο σταθερό & διαθέσιμο μοντέλο
                    contents=audit_prompt,
                    config={
                        "response_mime_type": "application/json",
                        "response_json_schema": json_schema
                    }
                )

                parsed = json.loads(response.text)

                # Defensive population
                st.session_state.audit_json = {
                    "verdict": parsed.get("verdict", {"level": "Pending", "score": 0, "recommendation": "Retry audit"}),
                    "matrix": parsed.get("matrix", {"hierarchy": 0, "hard_skills": 0, "evidence": 0, "soft_skills": 0}),
                    "missing": parsed.get("missing", []),
                    "pivot": parsed.get("pivot", "No pivot identified.")
                }

                st.success("✅ Strategic Audit completed successfully!")
                st.rerun()

            except Exception as e:
                st.error(f"Audit failed: {str(e)[:300]}")
                st.info("Tip: Try again in 30-60 seconds if you hit rate limits.")

# --- RESULTS DASHBOARD ---
if st.session_state.audit_json:
    res = st.session_state.audit_json
    verdict = res.get("verdict", {})
    matrix = res.get("matrix", {})

    st.markdown("## 📊 STRATEGIC INTELLIGENCE REPORT")

    c1, c2, c3 = st.columns([1, 2, 1])

    with c1:
        st.metric("Overall Match", f"{verdict.get('score', 0)}/100", 
                  delta=verdict.get('level', 'N/A'))
        st.write(f"**Recommendation:** {verdict.get('recommendation', 'N/A')}")

    with c2:
        categories = ['Hierarchy', 'Hard Skills', 'Evidence', 'Soft Skills']
        values = [
            matrix.get('hierarchy', 0),
            matrix.get('hard_skills', 0),
            matrix.get('evidence', 0),
            matrix.get('soft_skills', 0)
        ]

        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            line_color='#00ffcc'
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            title="Semantic Alignment Radar",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    with c3:
        st.subheader("Strategic Pivot")
        st.info(res.get('pivot', 'N/A'))

    st.subheader("🔴 Critical Gaps")
    if res.get('missing'):
        st.write(", ".join(res.get('missing', [])))
    else:
        st.success("No major gaps detected.")

    st.divider()

    # Placeholder για Stage B (Portfolio Synthesis) – μπορείς να το επεκτείνεις αργότερα
    if st.button("🖋️ CONSTRUCT EXECUTIVE PORTFOLIO"):
        st.info("Portfolio synthesis coming in v2.5 – currently under development.")

# --- FOOTER ---
st.divider()
st.caption("Developed by Ioannis Kontesis • Stateless • No data stored • Powered by Google GenAI SDK (Gemini 3.1)")
