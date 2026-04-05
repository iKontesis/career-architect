import streamlit as st
import google.generativeai as genai
import json

# --- 1. CONFIGURATION & NEON EXECUTIVE STYLING ---
st.set_page_config(page_title="Career Strategy Architect", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    /* Global App Background */
    .stApp { background-color: #0F172A !important; color: #F8FAFC !important; }
    
    /* SIDEBAR styling */
    section[data-testid="stSidebar"] { background-color: #1E293B !important; border-right: 1px solid #334155 !important; }
    section[data-testid="stSidebar"] * { color: white !important; }

    /* NEON LABELS - FORCE VISIBILITY (The Fix for Dark Mode) */
    label[data-testid="stWidgetLabel"] p {
        color: #00FBFF !important; /* Neon Cyan */
        font-weight: 900 !important;
        text-transform: uppercase !important;
        font-size: 1.1rem !important;
        text-shadow: 0 0 8px rgba(0, 251, 255, 0.6) !important;
    }

    /* TEXT AREAS - High Contrast */
    .stTextArea textarea { 
        background-color: #1E293B !important; 
        color: #F8FAFC !important; 
        border: 2px solid #334155 !important;
        border-radius: 12px !important;
        font-size: 16px !important;
    }
    .stTextArea textarea:focus {
        border: 2px solid #00FBFF !important;
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
        text-transform: uppercase;
    }
    .stButton button:hover { background-color: #00E5E8 !important; box-shadow: 0 0 20px #00FBFF; }

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
    st.markdown("### 🛡️ PROTOCOL")
    st.caption("Executive Edition 1.1 | Stateless & Secure")

# --- 3. HEADER ---
st.markdown("# 🛡️ CAREER STRATEGY **ARCHITECT**")
st.markdown("#### *High-Level Executive Decision Support System*")
st.divider()

if 'audit_json' not in st.session_state:
    st.session_state.audit_json = None

# --- 4. INPUTS ---
col1, col2 = st.columns(2)
with col1:
    master_cv = st.text_area("📄 MASTER CV SOURCE", height=350, placeholder="Paste professional history...")
with col2:
    job_desc = st.text_area("💼 TARGET JOB DESCRIPTION", height=350, placeholder="Paste target requirements...")

# --- 5. STAGE A: AUDIT ---
if st.button("RUN STRATEGIC AUDIT"):
    if not api_key:
        st.error("Missing API Key. Please provide it in the sidebar.")
    elif len(master_cv) < 50 or len(job_desc) < 50:
        st.warning("Insufficient data. Please provide more content for analysis.")
    else:
        with st.spinner("CONNECTING TO STRATEGIC ENGINE..."):
            try:
                # SIMPLE CONFIGURATION (Transport set to 'rest' for stability)
                genai.configure(api_key=api_key, transport='rest')
                
                # Try creating the model - Using the most stable identifier
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                audit_prompt = f"""
                Analyze the CV vs JD. Output ONLY a valid JSON object.
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
                
                if response.text:
                    clean_text = response.text.replace('```json', '').replace('```', '').strip()
                    st.session_state.audit_json = json.loads(clean_text)
                    st.rerun()
                else:
                    st.error("Empty response from AI. Possible API restriction.")
                    
            except Exception as e:
                # EXPLANATORY ERROR HANDLING
                err_msg = str(e)
                if "404" in err_msg:
                    st.error("STRATEGIC LINK FAILURE (404): The AI Model identifier has moved. Attempting recovery...")
                    st.info("Try using 'gemini-1.5-flash-latest' if this persists.")
                else:
                    st.error(f"Audit System Offline: {err_msg}")

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
        <h3 style="color: #00FBFF; margin-top:0;">Verdict: {res['verdict']['level']} ({res['verdict']['score']}/100)</h3>
        <p style="color: #00FBFF;"><strong>Proposed Strategy:</strong> {res['pivot']}</p>
        <p><i>{res['verdict']['recommendation']}</i></p>
        <p style="color: #94A3B8;"><strong>Critical Gaps:</strong> {", ".join(res['missing'])}</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # --- 7. STAGE B: SYNTHESIS ---
    if st.button("CONSTRUCT EXECUTIVE PORTFOLIO"):
        with st.spinner("Synthesizing Executive Narrative..."):
            try:
                model_pro = genai.GenerativeModel('gemini-1.5-pro')
                arch_prompt = f"Create CV and Cover Letter based on: {json.dumps(res)}. CV Source: {master_cv}. No Oxford commas."
                final_res = model_pro.generate_content(arch_prompt)
                st.markdown("## 🖋️ TAILOR-MADE PORTFOLIO")
                st.markdown(final_res.text)
                st.download_button("Download TXT", final_res.text, file_name="executive_portfolio.txt")
            except Exception as e:
                st.error(f"Synthesis Error: {str(e)}")
