import streamlit as st
import google.generativeai as genai
import json

# --- 1. CONFIGURATION & EXECUTIVE STYLING ---
st.set_page_config(page_title="Executive Portfolio Architect", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    /* Global App Background */
    .stApp { background-color: #0F172A !important; color: #F1F5F9 !important; font-family: 'Inter', sans-serif !important; }
    
    /* SIDEBAR styling */
    section[data-testid="stSidebar"] { 
        background-color: #1E293B !important; 
        border-right: 1px solid #334155 !important;
    }
    
    /* STICKY FOOTER for Sidebar */
    [data-testid="stSidebarUserContent"] {
        display: flex;
        flex-direction: column;
        height: 85vh;
    }
    
    .sidebar-footer {
        margin-top: auto;
        padding-top: 20px;
        border-top: 1px solid #334155;
        font-size: 0.85rem;
        color: #94A3B8;
    }
    
    .sidebar-footer strong { color: #F8FAFC; font-size: 0.95rem; }
    .sidebar-footer a { color: #60A5FA; text-decoration: none; }

    /* EXECUTIVE LABELS */
    label[data-testid="stWidgetLabel"] p {
        color: #94A3B8 !important; 
        font-weight: 700 !important;
        text-transform: uppercase !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.1em !important;
    }

    /* TEXT AREAS */
    .stTextArea textarea { 
        background-color: #1E293B !important; 
        color: #FFFFFF !important; 
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
        font-size: 15px !important;
    }
    
    /* HEADERS */
    h1 { font-size: 2.5rem !important; font-weight: 800 !important; letter-spacing: -0.03em !important; color: #F8FAFC !important; }
    h2 { font-size: 1.6rem !important; border-bottom: 1px solid #334155; padding-bottom: 10px; color: #F8FAFC !important; }

    /* METRICS */
    [data-testid="stMetricValue"] { color: #60A5FA !important; font-weight: 800 !important; }
    [data-testid="stMetricLabel"] { color: #94A3B8 !important; text-transform: uppercase !important; font-size: 0.8rem !important; }

    /* BUTTONS */
    .stButton button { 
        background-color: #2563EB !important; color: white !important; border-radius: 6px !important;
        font-weight: 700 !important; padding: 0.8rem 2rem !important; width: 100% !important; border: none !important;
        text-transform: uppercase; letter-spacing: 0.05em;
    }
    .stButton button:hover { background-color: #1D4ED8 !important; box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3) !important; }

    /* REPORT CARD */
    .report-card { 
        background-color: #1E293B !important; padding: 25px !important; border-radius: 12px !important; 
        border: 1px solid #334155 !important; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2) !important;
    }
    
    .executive-guide {
        font-size: 1rem; color: #94A3B8; background-color: #1E293B; padding: 20px;
        border-radius: 10px; border-left: 4px solid #3B82F6; margin-bottom: 25px;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR WITH STICKY SIGNATURE ---
with st.sidebar:
    st.markdown("## ⚙️ ENGINE STATUS")
    if "GEMINI_API_KEY" in st.secrets:
        st.success("Strategic Core: ACTIVE")
    else:
        st.error("Strategic Core: OFFLINE")
        
    st.divider()
    
    # THE SIGNATURE FOOTER (Sticky-like)
    st.markdown(f"""
        <div class="sidebar-footer">
            <strong>Ioannis Kontesis</strong><br>
            AI Transformation Architect<br>
            Operational Resilience & Strategy Specialist<br>
            Finance & Risk Professional<br><br>
            🔗 <a href="https://linkedin.com/in/ikontesis" target="_blank">LinkedIn</a> | 
            𝕏 <a href="https://x.com/@ikontesis" target="_blank">Twitter</a><br><br>
            🛡️ Stateless Architecture | v2.3<br>
            <span style="font-size: 0.7rem; opacity: 0.5;">Powered by Gemini 3.1</span>
        </div>
        """, unsafe_allow_html=True)

# --- 3. APP HEADER ---
st.markdown("# 🛡️ CAREER STRATEGY **ARCHITECT**")
st.markdown("#### *High-Level Executive Decision Support System*")
st.divider()

# API Init
if api_key := st.secrets.get("GEMINI_API_KEY"):
    genai.configure(api_key=api_key, transport='rest')

if 'audit_json' not in st.session_state:
    st.session_state.audit_json = None

# --- 4. EXECUTIVE GUIDE ---
st.markdown("""
    <div class="executive-guide">
        <strong>Executive Protocol:</strong> This system de-risks career transitions by performing a 
        high-fidelity semantic audit between your professional trajectory and market requirements. 
        It ensures your narrative is optimized for high-stakes, risk-aware leadership roles.
    </div>
    """, unsafe_allow_html=True)

# --- 5. INPUT AREA ---
col1, col2 = st.columns(2)
with col1:
    master_cv = st.text_area("📄 MASTER CV SOURCE", height=380, placeholder="Paste your full experience history...")
with col2:
    job_desc = st.text_area("💼 TARGET JOB DESCRIPTION", height=380, placeholder="Paste target role requirements...")

st.divider()

# --- 6. STAGE A: AUDIT ---
if st.button("RUN STRATEGIC AUDIT"):
    if len(master_cv) < 50 or len(job_desc) < 50:
        st.warning("INSUFFICIENT DATA: Provide more context to proceed.")
    else:
        with st.spinner("Analyzing semantic alignment..."):
            try:
                model = genai.GenerativeModel('gemini-3-flash-preview')
                audit_prompt = f"""
                Analyze CV vs JD. Output ONLY valid JSON:
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
                clean_json = response.text.replace('```json', '').replace('```', '').strip()
                st.session_state.audit_json = json.loads(clean_json)
                st.rerun()
            except Exception as e:
                st.error(f"Audit Error: {str(e)}")

# --- 7. DISPLAY RESULTS ---
if st.session_state.audit_json:
    res = st.session_state.audit_json
    st.markdown("## 📊 STRATEGIC INTELLIGENCE REPORT")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("HIERARCHY", f"{res['matrix']['hierarchy']}%")
    m2.metric("SKILLS", f"{res['matrix']['hard_skills']}%")
    m3.metric("EVIDENCE", f"{res['matrix']['evidence']}%")
    m4.metric("COMPATIBILITY", f"{res['matrix']['soft_skills']}%")

    st.markdown(f"""
    <div class="report-card">
        <h3 style="margin-top:0;">Verdict: {res['verdict']['level']} ({res['verdict']['score']}/100)</h3>
        <p style="color: #60A5FA; font-size: 1.1rem;"><strong>Strategy:</strong> {res['pivot']}</p>
        <p style="font-style: italic;">{res['verdict']['recommendation']}</p>
        <p style="color: #94A3B8;"><strong>Gaps:</strong> {", ".join(res['missing'])}</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # --- 8. STAGE B: SYNTHESIS ---
    if st.button("CONSTRUCT EXECUTIVE PORTFOLIO"):
        with st.spinner("Synthesizing Narrative..."):
            try:
                model_pro = genai.GenerativeModel('gemini-3-pro-preview')
                arch_prompt = f"Create high-impact CV and Cover Letter based on: {json.dumps(res)}. Source: {master_cv}. Executive tone."
                final_res = model_pro.generate_content(arch_prompt)
                st.markdown("## 🖋️ TAILOR-MADE PORTFOLIO")
                st.markdown(final_res.text)
                st.download_button("Download TXT", final_res.text, file_name="executive_portfolio.txt")
            except Exception as e:
                fallback = genai.GenerativeModel('gemini-3-flash-preview')
                final_res = fallback.generate_content(arch_prompt)
                st.markdown(final_res.text)
                st.download_button("Download TXT", final_res.text, file_name="executive_portfolio.txt")
