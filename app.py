import streamlit as st
import google.generativeai as genai
import json

# --- 1. CONFIGURATION & QUIET LUXURY STYLING ---
st.set_page_config(page_title="Career Strategy Architect", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    /* Global App Background - Deep Midnight */
    .stApp { background-color: #0F172A !important; color: #F8FAFC !important; }
    
    /* SIDEBAR styling - Solid Slate */
    section[data-testid="stSidebar"] { background-color: #1E293B !important; border-right: 1px solid #334155 !important; }
    section[data-testid="stSidebar"] * { color: #E2E8F0 !important; }

    /* EXECUTIVE LABELS - Steel Blue (Visible & Elegant) */
    label[data-testid="stWidgetLabel"] p {
        color: #94A3B8 !important; /* Soft Slate Blue */
        font-weight: 700 !important;
        text-transform: uppercase !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.1em !important;
    }

    /* TEXT AREAS - Slate Navy */
    .stTextArea textarea { 
        background-color: #1E293B !important; 
        color: #F1F5F9 !important; 
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
        font-size: 15px !important;
    }
    .stTextArea textarea:focus { border: 1px solid #3B82F6 !important; box-shadow: 0 0 10px rgba(59, 130, 246, 0.2) !important; }
    
    /* HEADERS */
    h1, h2, h3 { color: #F8FAFC !important; font-weight: 800 !important; letter-spacing: -0.02em !important; }

    /* METRICS - Electric Blue for Data */
    [data-testid="stMetricValue"] { color: #60A5FA !important; font-weight: 800 !important; }
    [data-testid="stMetricLabel"] { color: #64748B !important; }

    /* BUTTONS - Solid Executive Blue */
    .stButton button { 
        background-color: #2563EB !important; 
        color: white !important; 
        border-radius: 6px !important;
        font-weight: 700 !important;
        padding: 0.75rem 2rem !important;
        width: 100% !important;
        border: none !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .stButton button:hover { background-color: #1D4ED8 !important; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important; }

    /* REPORT CARD - Glassmorphism */
    .report-card { 
        background-color: #1E293B !important; 
        padding: 30px !important; 
        border-radius: 12px !important; 
        border: 1px solid #334155 !important;
        color: #F8FAFC !important;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2) !important;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("## ⚙️ SYSTEM SETTINGS")
    api_key = st.text_input("Gemini API Key", type="password")
    st.divider()
    st.markdown("### 🛡️ STATUS")
    if api_key:
        st.success("API Key Active")
    st.caption("Executive Portfolio Architect v2.1")

# --- 3. HEADER ---
st.markdown("# 🛡️ CAREER STRATEGY **ARCHITECT**")
st.markdown("#### *High-Level Executive Decision Support System*")
st.divider()

if 'audit_json' not in st.session_state:
    st.session_state.audit_json = None

# --- 4. INPUTS ---
col1, col2 = st.columns(2)
with col1:
    master_cv = st.text_area("📄 MASTER CV SOURCE", height=350)
with col2:
    job_desc = st.text_area("💼 TARGET JOB DESCRIPTION", height=350)

# --- 5. STAGE A: AUDIT ---
if st.button("RUN STRATEGIC AUDIT"):
    if not api_key:
        st.error("Missing API Key.")
    else:
        with st.spinner("Executing Strategic Audit..."):
            try:
                genai.configure(api_key=api_key, transport='rest')
                model = genai.GenerativeModel('gemini-3-flash-preview')
                
                audit_prompt = f"""
                Analyze CV vs JD. Output ONLY valid JSON.
                Schema:
                {{
                    "verdict": {{"level": "string", "score": number, "recommendation": "string"}},
                    "matrix": {{"hierarchy": number, "hard_skills": number, "evidence": number, "soft_skills": number}},
                    "missing": ["string"],
                    "pivot": "string"
                }}
                CV: {master_cv}
                JD: {job_desc}
                """
                response = model.generate_content(audit_prompt)
                clean_text = response.text.replace('```json', '').replace('```', '').strip()
                st.session_state.audit_json = json.loads(clean_text)
                st.rerun()
            except Exception as e:
                st.error(f"Audit Error: {str(e)}")

# --- 6. DASHBOARD ---
if st.session_state.audit_json:
    res = st.session_state.audit_json
    st.markdown("## 📊 AUDIT RESULTS")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("HIERARCHY", f"{res['matrix']['hierarchy']}%")
    m2.metric("SKILLS", f"{res['matrix']['hard_skills']}%")
    m3.metric("EVIDENCE", f"{res['matrix']['evidence']}%")
    m4.metric("FIT", f"{res['matrix']['soft_skills']}%")

    st.markdown(f"""
    <div class="report-card">
        <h3 style="margin-top:0;">Verdict: {res['verdict']['level']} ({res['verdict']['score']}/100)</h3>
        <p style="color: #60A5FA; font-size: 1.1rem;"><strong>Proposed Strategy:</strong> {res['pivot']}</p>
        <p style="font-style: italic;">{res['verdict']['recommendation']}</p>
        <p style="color: #94A3B8;"><strong>Critical Gaps:</strong> {", ".join(res['missing'])}</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # --- 7. STAGE B: SYNTHESIS ---
    if st.button("CONSTRUCT EXECUTIVE PORTFOLIO"):
        with st.spinner("Synthesizing Narrative..."):
            try:
                # Primary attempt with 3-pro
                model_pro = genai.GenerativeModel('gemini-3-pro-preview')
                arch_prompt = f"Create high-impact CV and Cover Letter based on: {json.dumps(res)}. CV Source: {master_cv}. No Oxford commas."
                final_res = model_pro.generate_content(arch_prompt)
                st.markdown("## 🖋️ TAILOR-MADE PORTFOLIO")
                st.markdown(final_res.text)
                st.download_button("Download TXT", final_res.text, file_name="portfolio.txt")
            except Exception as e:
                # Silent Fallback to Flash
                fallback = genai.GenerativeModel('gemini-3-flash-preview')
                final_res = fallback.generate_content(arch_prompt)
                st.markdown("## 🖋️ TAILOR-MADE PORTFOLIO (High-Speed Engine)")
                st.markdown(final_res.text)
                st.download_button("Download TXT", final_res.text, file_name="portfolio.txt")
