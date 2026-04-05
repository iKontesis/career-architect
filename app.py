import streamlit as st
import google.generativeai as genai
import json

# --- 1. CONFIGURATION & NEON EXECUTIVE STYLING ---
st.set_page_config(page_title="Career Strategy Architect", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    /* Global Background */
    .stApp { background-color: #0F172A !important; color: #F8FAFC !important; }
    
    /* SIDEBAR styling */
    section[data-testid="stSidebar"] { background-color: #1E293B !important; border-right: 1px solid #334155 !important; }
    section[data-testid="stSidebar"] * { color: white !important; }

    /* NEON LABELS (Visible in ANY mode) */
    label[data-testid="stWidgetLabel"] p {
        color: #00FBFF !important; /* Hyper Neon Cyan */
        font-weight: 900 !important;
        text-transform: uppercase !important;
        font-size: 1.2rem !important;
        text-shadow: 0 0 10px rgba(0, 251, 255, 0.5) !important;
    }

    /* TEXT AREAS */
    .stTextArea textarea { 
        background-color: #1E293B !important; 
        color: #F8FAFC !important; 
        border: 2px solid #334155 !important;
        border-radius: 12px !important;
        font-size: 16px !important;
    }
    
    /* HEADERS */
    h1, h2, h3 { color: #F8FAFC !important; font-weight: 800 !important; }

    /* METRICS */
    [data-testid="stMetricValue"] { color: #00FBFF !important; font-weight: 800 !important; }
    [data-testid="stMetricLabel"] { color: #94A3B8 !important; }

    /* BUTTONS */
    .stButton button { 
        background-color: #00FBFF !important; 
        color: #0F172A !important; 
        border: none !important;
        border-radius: 10px !important;
        font-weight: 900 !important;
        padding: 1rem 2rem !important;
        width: 100% !important;
        transition: 0.3s;
    }
    .stButton button:hover { background-color: #00E5E8 !important; box-shadow: 0 0 25px #00FBFF; }

    /* REPORT CARD */
    .report-card { 
        background-color: #1E293B !important; 
        padding: 30px !important; 
        border-radius: 20px !important; 
        border: 2px solid #334155 !important;
        color: #F8FAFC !important;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("## ⚙️ SYSTEM SETTINGS")
    api_key = st.text_input("Gemini API Key", type="password")
    st.divider()
    st.info("PROTOCOL: Stateless Architecture. Version 1.0 Stable.")

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
    elif len(master_cv) < 50:
        st.warning("Insufficient CV data.")
    else:
        with st.spinner("FORCE ACCESSING STABLE API..."):
            try:
                # THE SILVER BULLET: Force API Version 1 and REST transport
                genai.configure(
                    api_key=api_key, 
                    transport='rest',
                    client_options={'api_version': 'v1'}
                )
                
                # Try the most robust model string
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                audit_prompt = f"""
                Analyze CV vs JD. Output ONLY valid JSON.
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
                
                if response.text:
                    clean_text = response.text.replace('```json', '').replace('```', '').strip()
                    st.session_state.audit_json = json.loads(clean_text)
                    st.rerun()
                else:
                    st.error("AI node returned no data.")
                    
            except Exception as e:
                st.error(f"Critical System Error: {str(e)}")

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
        <h3 style="color: #00FBFF;">Verdict: {res['verdict']['level']} ({res['verdict']['score']}/100)</h3>
        <p style="color: #00FBFF;"><strong>Strategy:</strong> {res['pivot']}</p>
        <p><i>{res['verdict']['recommendation']}</i></p>
        <p style="color: #94A3B8;"><strong>Gaps:</strong> {", ".join(res['missing'])}</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # --- 7. STAGE B: SYNTHESIS ---
    if st.button("CONSTRUCT PORTFOLIO"):
        with st.spinner("Synthesizing..."):
            try:
                # Force stable version for Pro as well
                model_pro = genai.GenerativeModel('gemini-1.5-pro')
                arch_prompt = f"Create CV and Cover Letter based on: {json.dumps(res)}. CV Source: {master_cv}. No Oxford commas."
                final_res = model_pro.generate_content(arch_prompt)
                st.markdown(final_res.text)
                st.download_button("Download TXT", final_res.text, file_name="portfolio.txt")
            except Exception as e:
                st.error(f"Synthesis Error: {str(e)}")
