import streamlit as st
import json
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
    .stButton button { background-color: #2563EB; color: white; border-radius: 6px; font-weight: 700; padding: 0.8rem; }
    .report-card { background-color: #1E293B; padding: 28px; border-radius: 14px; border: 1px solid #334155; box-shadow: 0 10px 20px -5px rgba(0,0,0,0.4); }
    .gap-item { background-color: #1E293B; padding: 14px 18px; border-radius: 10px; border-left: 5px solid #F87171; margin-bottom: 12px; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ CAREER STRATEGY ARCHITECT")
st.subheader("High-Fidelity Semantic Audit & Executive Portfolio Synthesis")

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ ENGINE STATUS")
    
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
    
    🛡️ Stateless Architecture | **v2.5.0**  
    Powered by Google GenAI SDK
    """)

# --- SESSION STATE ---
if 'audit_json' not in st.session_state:
    st.session_state.audit_json = None

# --- INPUTS ---
col1, col2 = st.columns(2)
with col1:
    master_cv = st.text_area("📄 MASTER CV SOURCE (English)", height=420, 
                             placeholder="Paste your full master CV here...")
with col2:
    job_desc = st.text_area("💼 TARGET JOB DESCRIPTION", height=420, 
                            placeholder="Paste the full job description here...")

st.divider()

# --- AUDIT BUTTON ---
if st.button("🚀 RUN STRATEGIC AUDIT", type="primary", use_container_width=True):
    if not api_key or len(api_key) < 30:
        st.error("**System Error:** GEMINI_API_KEY is not configured in Streamlit Secrets.")
    elif len(master_cv.strip()) < 150 or len(job_desc.strip()) < 150:
        st.warning("Please provide sufficient data for both CV and Job Description.")
    else:
        with st.spinner("Executing Strategic Semantic Audit..."):
            try:
                client = genai.Client(api_key=api_key)

                audit_prompt = f"""
Analyze the CV against the Job Description for a senior/executive role.
Return ONLY valid JSON with this exact structure:

{{
  "verdict": {{"level": "string", "score": integer, "recommendation": "string"}},
  "matrix": {{"hierarchy": integer, "hard_skills": integer, "evidence": integer, "soft_skills": integer}},
  "pivot": "string",
  "gaps": [
    {{"gap": "description of the gap", "severity": integer}}   // severity 1-5 (1=minor/covered, 5=critical)
  ]
}}

CV:
{master_cv}

JD:
{job_desc}
"""

                json_schema = { ... }  # (το ίδιο αυστηρό schema όπως πριν – μπορείς να το κρατήσεις από προηγούμενη έκδοση)

                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=audit_prompt,
                    config={
                        "response_mime_type": "application/json",
                        "response_json_schema": json_schema
                    }
                )

                parsed = json.loads(response.text)

                st.session_state.audit_json = {
                    "verdict": parsed.get("verdict", {}),
                    "matrix": parsed.get("matrix", {}),
                    "pivot": parsed.get("pivot", ""),
                    "gaps": parsed.get("gaps", [])
                }

                st.success("✅ Audit completed!")
                st.rerun()

            except Exception as e:
                error_str = str(e).lower()
                if "429" in error_str or "quota" in error_str:
                    st.error("⛔ Rate limit reached")
                    st.warning("This app uses the owner's personal Gemini key. Wait 60-90 seconds and retry.")
                else:
                    st.error(f"Error: {str(e)[:200]}")

# --- EXECUTIVE DASHBOARD ---
if st.session_state.audit_json:
    res = st.session_state.audit_json
    verdict = res.get("verdict", {})
    matrix = res.get("matrix", {})

    st.markdown("## 📊 EXECUTIVE INTELLIGENCE REPORT")

    # Top Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("HIERARCHY", f"{matrix.get('hierarchy', 0)}%")
    m2.metric("HARD SKILLS", f"{matrix.get('hard_skills', 0)}%")
    m3.metric("EVIDENCE", f"{matrix.get('evidence', 0)}%")
    m4.metric("SOFT SKILLS", f"{matrix.get('soft_skills', 0)}%")

    st.divider()

    col_l, col_r = st.columns([2, 1])

    with col_l:
        st.markdown(f"""
        <div class="report-card">
            <h2>Verdict: <strong>{verdict.get('level', 'N/A')}</strong> ({verdict.get('score', 0)}/100)</h2>
            <p style="color:#94A3B8; font-size:1.05rem;">{verdict.get('recommendation', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)

    with col_r:
        st.markdown(f"""
        <div class="report-card" style="height:100%;">
            <h3>Strategic Pivot</h3>
            <p>{res.get('pivot', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)

    # Critical Gaps – Bullet points με severity
    st.markdown("### 🔴 Critical Gaps")
    gaps = res.get("gaps", [])
    if gaps:
        for g in gaps:
            severity = g.get("severity", 3)
            color = "#F87171" if severity >= 4 else "#FB923C" if severity == 3 else "#94A3B8"
            st.markdown(f"""
            <div class="gap-item" style="border-left-color:{color};">
                <strong>{g.get('gap', '')}</strong> 
                <span style="float:right; color:{color}; font-weight:600;">Severity: {severity}/5</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("No critical gaps identified.")

    st.divider()

    # Portfolio Button
    if st.button("🖋️ CONSTRUCT EXECUTIVE PORTFOLIO (CV + Cover Letter)", type="secondary", use_container_width=True):
        st.info("Portfolio synthesis (tailored CV + Cover Letter) is under development and will be available in v2.6.0")

# --- FOOTER ---
st.divider()
st.caption("Developed by Ioannis Kontesis • 100% Stateless • Your data is never stored • Powered by Gemini 3 Flash Preview • v2.5.0")
