import streamlit as st
import json
import plotly.graph_objects as go
from google import genai

# --- CONFIG & STYLING ---
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
    
    # Load secret
    api_key = st.secrets.get("GEMINI_API_KEY")
    
    if api_key and len(api_key) > 30:
        st.success("✅ Strategic Core: ONLINE")
        st.caption("Using owner's Gemini API Key (stateless)")
    else:
        st.error("❌ Strategic Core: OFFLINE")
        st.warning("GEMINI_API_KEY is missing in Streamlit Secrets.")
    
    st.divider()
    st.markdown("""
    **Ioannis Kontesis**  
    AI Transformation Architect  
    Operational Resilience & Strategy Specialist  
    Finance & Risk Professional
    
    🔗 [LinkedIn](https://linkedin.com/in/ikontesis) | [𝕏](https://x.com/@ikontesis)
    
    🛡️ Stateless Architecture | **v2.4.1**  
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
        st.error("**System Error:** GEMINI_API_KEY is not configured in Streamlit Secrets. The owner must add it.")
    elif len(master_cv.strip()) < 150 or len(job_desc.strip()) < 150:
        st.warning("Please provide sufficient data for both CV and Job Description.")
    else:
        with st.spinner("Executing Strategic Semantic Audit with Gemini 3 Flash Preview..."):
            try:
                client = genai.Client(api_key=api_key)

                audit_prompt = f"""
Analyze the candidate's CV against the target Job Description for a senior/executive position.

Return **ONLY** a valid JSON object with exactly the following structure. No extra text.

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
                        "missing": {"type": "array", "items": {"type": "string"}},
                        "pivot": {"type": "string"}
                    },
                    "required": ["verdict", "matrix", "missing", "pivot"]
                }

                response = client.models.generate_content(
                    model="gemini-3-flash-preview",        # ← Σωστό μοντέλο από AI Studio
                    contents=audit_prompt,
                    config={
                        "response_mime_type": "application/json",
                        "response_json_schema": json_schema
                    }
                )

                parsed = json.loads(response.text)

                st.session_state.audit_json = {
                    "verdict": parsed.get("verdict", {"level": "Pending", "score": 0, "recommendation": "Retry"}),
                    "matrix": parsed.get("matrix", {"hierarchy": 0, "hard_skills": 0, "evidence": 0, "soft_skills": 0}),
                    "missing": parsed.get("missing", []),
                    "pivot": parsed.get("pivot", "No pivot identified.")
                }

                st.success("✅ Strategic Audit completed successfully!")
                st.rerun()

            except Exception as e:
                error_str = str(e).lower()
                if "429" in error_str or "quota" in error_str or "rate limit" in error_str:
                    st.error("⛔ Rate limit / Quota exceeded.")
                    st.warning("This app uses the **owner's personal Gemini API key**. Please wait 60–90 seconds and try again.")
                else:
                    st.error(f"Audit failed: {str(e)[:250]}")

# --- RESULTS (όπως πριν) ---
if st.session_state.audit_json:
    # ... (το ίδιο dashboard με radar chart που είχαμε πριν – μπορείς να το κρατήσεις ακριβώς όπως στο προηγούμενο version)

    # Για συντομία, βάλε εδώ το παλιό σου results block με metrics + radar + gaps + pivot

# --- FOOTER ---
st.divider()
st.caption("Developed by Ioannis Kontesis • 100% Stateless • Your data is never stored • Powered by Gemini 3 Flash Preview")
