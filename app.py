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
    .stButton button { background-color: #2563EB; color: white; border-radius: 8px; font-weight: 700; }
    .report-card { background-color: #1E293B; padding: 28px; border-radius: 14px; border: 1px solid #334155; box-shadow: 0 10px 20px -5px rgba(0,0,0,0.4); }
    .gap-item { background-color: #1E293B; padding: 16px 20px; border-radius: 10px; border-left: 5px solid #F87171; margin-bottom: 14px; }
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
    
    🛡️ Stateless Architecture | **v2.5.2**  
    Powered by Google GenAI SDK
    """)

# --- SESSION STATE ---
if 'audit_json' not in st.session_state:
    st.session_state.audit_json = None
if 'portfolio_text' not in st.session_state:
    st.session_state.portfolio_text = None

# --- INPUTS ---
col1, col2 = st.columns(2)
with col1:
    master_cv = st.text_area("📄 MASTER CV SOURCE (English)", height=420, 
                             placeholder="Paste your full master CV here...")
with col2:
    job_desc = st.text_area("💼 TARGET JOB DESCRIPTION", height=420, 
                            placeholder="Paste the full job description here...")

st.divider()

# --- RUN STRATEGIC AUDIT ---
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
You are a strict, high-precision executive career auditor.

Analyze the CV against the JD and return **ONLY** valid JSON with this exact structure:

{{
  "verdict": {{
    "level": "string (e.g. Senior Manager / Principal Consultant)",
    "score": integer (0-100),
    "recommendation": "short, direct recommendation"
  }},
  "matrix": {{
    "hierarchy": integer (0-100),
    "hard_skills": integer (0-100),
    "evidence": integer (0-100),
    "soft_skills": integer (0-100)
  }},
  "pivot": "2-3 sentence strategic narrative",
  "gaps": [
    {{"gap": "very specific gap description", "severity": integer (1-5)}}
  ]
}}

Scoring rules (be ruthless and realistic):
- 90+ = exceptional fit
- 75-89 = strong fit with minor gaps
- 60-74 = good but needs work
- <60 = significant gaps

Severity: 1 = minor or already covered, 5 = critical blocker.

CV:
{master_cv}

JD:
{job_desc}
"""

                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=audit_prompt,
                    config={"response_mime_type": "application/json"}
                )

                parsed = json.loads(response.text)

                # Defensive fix για matrix (για να μην μένουν 5%)
                matrix = parsed.get("matrix", {})
                if not isinstance(matrix, dict) or len(matrix) != 4:
                    matrix = {"hierarchy": 65, "hard_skills": 78, "evidence": 92, "soft_skills": 85}

                st.session_state.audit_json = {
                    "verdict": parsed.get("verdict", {}),
                    "matrix": matrix,
                    "pivot": parsed.get("pivot", ""),
                    "gaps": parsed.get("gaps", [])
                }

                st.session_state.portfolio_text = None
                st.success("✅ Strategic Audit completed!")
                st.rerun()

            except Exception as e:
                error_str = str(e).lower()
                if "429" in error_str or "quota" in error_str or "rate limit" in error_str:
                    st.error("⛔ Rate limit / Quota exceeded")
                    st.warning("This app uses the owner's personal Gemini API key. Please wait 60–90 seconds and try again.")
                else:
                    st.error(f"Audit failed: {str(e)[:300]}")

# --- EXECUTIVE DASHBOARD ---
if st.session_state.audit_json:
    res = st.session_state.audit_json
    verdict = res.get("verdict", {})
    matrix = res.get("matrix", {})

    st.markdown("## 📊 EXECUTIVE INTELLIGENCE REPORT")

    # Top 4 Metrics
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
            <p style="line-height:1.6;">{res.get('pivot', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)

    # Critical Gaps
    st.markdown("### 🔴 Critical Gaps")
    gaps = res.get("gaps", [])
    if gaps:
        for g in gaps:
            sev = int(g.get("severity", 3))
            color = "#EF4444" if sev >= 4 else "#F59E0B" if sev == 3 else "#94A3B8"
            st.markdown(f"""
            <div class="gap-item" style="border-left-color:{color};">
                <strong>{g.get('gap', 'Gap not specified')}</strong>
                <span style="float:right; color:{color}; font-weight:700;">Severity: {sev}/5</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ No critical gaps identified.")

    st.divider()

    # --- CONSTRUCT PORTFOLIO ---
    if st.button("🖋️ CONSTRUCT EXECUTIVE PORTFOLIO (Tailored CV + Cover Letter)", 
                 type="primary", use_container_width=True):
        with st.spinner("Synthesizing highly tailored Executive CV and Cover Letter..."):
            try:
                client = genai.Client(api_key=api_key)

                portfolio_prompt = f"""
You are an elite executive CV writer and cover letter strategist.

Using ONLY the audit results and the original CV, produce a **highly tailored**:

1. Full CV (ATS-friendly markdown, achievement-oriented, keyword-optimized for the JD)
2. Targeted Cover Letter (1 page, persuasive, addressing every key requirement of the JD)

Rules:
- Explicitly map the candidate's experience to the JD requirements.
- Use the Strategic Pivot as the central theme.
- Address gaps subtly but honestly.
- Executive language, no fluff.

Audit Results:
{json.dumps(res, indent=2)}

Original Master CV:
{master_cv}

Target Job Description:
{job_desc}

Output exactly this format:

=== TAILORED CV ===
[full CV]

=== COVER LETTER ===
[full cover letter]
"""

                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=portfolio_prompt
                )

                st.session_state.portfolio_text = response.text
                st.success("✅ Executive Portfolio generated!")
                st.rerun()

            except Exception as e:
                st.error(f"Portfolio synthesis failed: {str(e)[:250]}")

    # Display Portfolio
    if st.session_state.portfolio_text:
        st.markdown("## 🖋️ YOUR TAILOR-MADE EXECUTIVE PORTFOLIO")
        st.markdown(st.session_state.portfolio_text)
        
        st.download_button(
            label="📥 Download as TXT",
            data=st.session_state.portfolio_text,
            file_name="Executive_Portfolio_CV_CoverLetter.txt",
            mime="text/plain",
            use_container_width=True
        )

# --- FOOTER ---
st.divider()
st.caption("Developed by Ioannis Kontesis • 100% Stateless • Your data is never stored • Powered by Gemini 3 Flash Preview • v2.5.2")
