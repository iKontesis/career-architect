import streamlit as st
import json
from google import genai
from google.genai.types import Schema, Type

# --- CONFIG & STYLING (ακριβώς ίδια λιτή αισθητική) ---
st.set_page_config(page_title="Career Strategy Architect", page_icon="🛡️", layout="wide")

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
st.subheader("v3.1.1 – Industry / Level / Experience Agnostic")
st.caption("High-Fidelity Semantic Audit • Native Structured Output • ATS + Realistic Gaps")

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ ENGINE STATUS")
    api_key = st.secrets.get("GEMINI_API_KEY")
    if api_key and len(api_key) > 30:
        st.success("✅ Strategic Core: ONLINE")
        st.caption("Gemini 3 Flash Preview • Stateless • v3.1.1")
    else:
        st.error("❌ Strategic Core: OFFLINE")
    
    st.divider()
    st.markdown("**Ioannis Kontesis**  \nAI Transformation Architect  \nOperational Resilience & Strategy Specialist")
    st.caption("100% Stateless | Your data never stored")

# --- SESSION STATE ---
for key in ["audit_json", "portfolio_text", "cv_format"]:
    if key not in st.session_state:
        st.session_state[key] = None

# --- TABS ---
tab_audit, tab_portfolio = st.tabs(["📊 STRATEGIC AUDIT", "🖋️ EXECUTIVE PORTFOLIO"])

with tab_audit:
    col1, col2 = st.columns(2)
    with col1:
        master_cv = st.text_area("📄 MASTER CV SOURCE", height=380, 
                                placeholder="Paste full CV (English or Greek OK)...")
    with col2:
        job_desc = st.text_area("💼 TARGET JOB DESCRIPTION", height=380, 
                               placeholder="Paste full JD...")

    st.divider()

    if st.button("🚀 RUN STRATEGIC AUDIT", type="primary", use_container_width=True):
        if not api_key or len(api_key) < 30:
            st.error("GEMINI_API_KEY missing in secrets.")
        elif len(master_cv.strip()) < 100 or len(job_desc.strip()) < 100:
            st.warning("Both fields required.")
        else:
            with st.spinner("Executing native structured semantic audit..."):
                try:
                    client = genai.Client(api_key=api_key)

                    # === NATIVE JSON SCHEMA με enforced 0-100 για ποσοστά (μόνο εδώ η αλλαγή) ===
                    audit_schema = Schema(
                        type=Type.OBJECT,
                        properties={
                            "detected": Schema(type=Type.OBJECT, properties={
                                "industry": Schema(type=Type.STRING),
                                "level": Schema(type=Type.STRING),
                                "required_years": Schema(type=Type.INTEGER)
                            }),
                            "verdict": Schema(type=Type.OBJECT, properties={
                                "level": Schema(type=Type.STRING),
                                "score": Schema(type=Type.INTEGER, minimum=0, maximum=100),
                                "recommendation": Schema(type=Type.STRING)
                            }),
                            "matrix": Schema(type=Type.OBJECT, properties={
                                "hierarchy": Schema(type=Type.INTEGER, minimum=0, maximum=100),
                                "hard_skills": Schema(type=Type.INTEGER, minimum=0, maximum=100),
                                "evidence": Schema(type=Type.INTEGER, minimum=0, maximum=100),
                                "soft_skills": Schema(type=Type.INTEGER, minimum=0, maximum=100),
                                "ats_compatibility": Schema(type=Type.INTEGER, minimum=0, maximum=100),
                                "keyword_match": Schema(type=Type.INTEGER, minimum=0, maximum=100)
                            }),
                            "pivot": Schema(type=Type.STRING),
                            "gaps": Schema(type=Type.ARRAY, items=Schema(type=Type.OBJECT, properties={
                                "gap": Schema(type=Type.STRING),
                                "severity": Schema(type=Type.INTEGER)
                            })),
                            "roadmap": Schema(type=Type.ARRAY, items=Schema(type=Type.STRING)),
                            "risk_flags": Schema(type=Type.ARRAY, items=Schema(type=Type.STRING)),
                            "transferable_bridge": Schema(type=Type.STRING, nullable=True)
                        },
                        required=["detected", "verdict", "matrix", "pivot", "gaps"]
                    )

                    audit_prompt = f"""
You are a strict, high-precision executive career auditor. 
NEVER invent experience. Map ONLY what exists in the Master CV.
If no direct evidence → write exactly "No direct evidence".

First detect: industry, seniority level, required years from JD.

Then analyse CV vs JD and return ONLY valid JSON matching the schema.

IMPORTANT SCORING RULES (must be followed exactly):
- All scores in "matrix" (hierarchy, hard_skills, evidence, soft_skills, ats_compatibility, keyword_match) MUST be integers 0-100.
- 100 = perfect match, 0 = no match at all.

CV:
{master_cv}

JD:
{job_desc}
"""

                    response = client.models.generate_content(
                        model="gemini-3-flash-preview",
                        contents=audit_prompt,
                        config={
                            "response_mime_type": "application/json",
                            "response_json_schema": audit_schema
                        }
                    )

                    parsed = json.loads(response.text)

                    st.session_state.audit_json = parsed
                    st.session_state.portfolio_text = None
                    st.success("✅ Strategic Audit completed (native schema v3.1.1)!")
                    st.rerun()

                except Exception as e:
                    st.error(f"Audit failed: {str(e)[:250]}")

    # --- DISPLAY AUDIT RESULTS (ακριβώς ίδιο με v3.1.0) ---
    if st.session_state.audit_json:
        res = st.session_state.audit_json
        m = res.get("matrix", {})

        st.markdown("## 📊 EXECUTIVE INTELLIGENCE REPORT")

        det = res.get("detected", {})
        st.info(f"**Detected:** {det.get('industry','N/A')} • {det.get('level','N/A')} • {det.get('required_years','N/A')} years")

        c1, c2, c3, c4, c5, c6 = st.columns(6)
        c1.metric("HIERARCHY", f"{m.get('hierarchy',0)}%")
        c2.metric("HARD SKILLS", f"{m.get('hard_skills',0)}%")
        c3.metric("EVIDENCE", f"{m.get('evidence',0)}%")
        c4.metric("SOFT SKILLS", f"{m.get('soft_skills',0)}%")
        c5.metric("ATS", f"{m.get('ats_compatibility',0)}%")
        c6.metric("KEYWORDS", f"{m.get('keyword_match',0)}%")

        verdict = res.get("verdict", {})
        col_l, col_r = st.columns([2, 1])
        with col_l:
            st.markdown(f"""
            <div class="report-card">
                <h2>Verdict: <strong>{verdict.get('level','N/A')}</strong> ({verdict.get('score',0)}/100)</h2>
                <p>{verdict.get('recommendation','N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
        with col_r:
            st.markdown(f"""
            <div class="report-card" style="height:100%;">
                <h3>Strategic Pivot</h3>
                <p>{res.get('pivot','N/A')}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### 🔴 Critical Gaps")
        for g in res.get("gaps", []):
            sev = g.get("severity", 3)
            color = "#EF4444" if sev >= 4 else "#F59E0B"
            st.markdown(f"""
            <div class="gap-item" style="border-left-color:{color};">
                <strong>{g.get('gap')}</strong>
                <span style="float:right; color:{color};">Severity: {sev}/5</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### 🛠️ Improvement Roadmap")
        for item in res.get("roadmap", []):
            st.success(f"• {item}")

        st.markdown("### ⚠️ Honest Risk Flags")
        for flag in res.get("risk_flags", []):
            st.warning(f"• {flag}")

        if res.get("transferable_bridge"):
            st.markdown("### 🔄 Transferable Skills Bridge")
            st.info(res["transferable_bridge"])

        cv_format = st.toggle("Hybrid CV format (instead of pure Chronological)", value=False, key="cv_format_toggle")
        st.session_state.cv_format = "Hybrid" if cv_format else "Chronological"

        if st.button("🖋️ CONSTRUCT EXECUTIVE PORTFOLIO", type="primary", use_container_width=True):
            with st.spinner("Synthesizing Tailored CV + Cover Letter..."):
                try:
                    client = genai.Client(api_key=api_key)
                    portfolio_prompt = f"""
You are an elite executive CV writer.
Rules:
- NEVER invent experience.
- Use ONLY data from Master CV and Audit Results.
- CV format requested: {st.session_state.cv_format}
- Include "Why this role" paragraph in Cover Letter using ONLY JD + CV evidence.

Audit Results: {json.dumps(res, ensure_ascii=False)}
Master CV: {master_cv}
Job Description: {job_desc}

Output exactly:
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
                    st.success("✅ Portfolio generated!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Portfolio failed: {str(e)[:200]}")

with tab_portfolio:
    if st.session_state.portfolio_text:
        st.markdown("## 🖋️ YOUR TAILOR-MADE EXECUTIVE PORTFOLIO")
        st.markdown(st.session_state.portfolio_text)
        
        st.download_button(
            label="📥 Download as TXT",
            data=st.session_state.portfolio_text,
            file_name="Executive_Portfolio_v3.1.1.txt",
            mime="text/plain",
            use_container_width=True
        )
    else:
        st.info("Run Audit first, then generate Portfolio.")

# --- FOOTER ---
st.divider()
st.caption("v3.1.1 • Agnostic • Native Structured Output • Fixed 0-100 scores • No data stored • Powered by Gemini 3 Flash Preview")
