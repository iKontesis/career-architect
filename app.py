import streamlit as st
import google.generativeai as genai
import json

# --- 1. CONFIGURATION & EXTREME STYLING ---
st.set_page_config(page_title="Career Strategy Architect", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    /* Global Background */
    .stApp { background-color: #0F172A !important; color: #F8FAFC !important; }
    
    /* SIDEBAR styling */
    section[data-testid="stSidebar"] { background-color: #1E293B !important; border-right: 1px solid #334155 !important; }
    section[data-testid="stSidebar"] * { color: white !important; }

    /* LABELS (The Fix for the invisible headers) */
    label[data-testid="stWidgetLabel"] p {
        color: #22D3EE !important; /* Bright Neon Cyan */
        font-weight: 800 !important;
        text-transform: uppercase !important;
        font-size: 1rem !important;
        letter-spacing: 0.1em !important;
    }

    /* TEXT AREAS */
    .stTextArea textarea { 
        background-color: #1E293B !important; 
        color: #F8FAFC !important; 
        border: 2px solid #334155 !important;
        border-radius: 12px !important;
    }
    
    /* HEADERS */
    h1, h2, h3 { color: #F8FAFC !important; font-weight: 800 !important; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }

    /* METRICS */
    [data-testid="stMetricValue"] { color: #22D3EE !important; font-weight: 800 !important; }
    [data-testid="stMetricLabel"] { color: #94A3B8 !important; }

    /* BUTTONS */
    .stButton button { 
        background-color: #0891B2 !important; 
        color: white !important; 
        border: none !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        padding: 1rem 2rem !important;
        width: 100% !important;
    }
    .stButton button:hover { background-color: #0E7490 !important; box-shadow: 0 0 15px #22D3EE; }

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
    st.markdown("## ⚙️ SETTINGS")
    api_key = st.text_input("Gemini API Key", type="password")
    st.divider()
    st.info("Stateless Architecture: Your data remains private.")

# --- 3. HEADER ---
st.markdown("# 🛡️ CAREER STRATEGY **ARCHITECT**")
st.markdown("#### *High-Level Executive Decision Support System*")
st.divider()

if 'audit_json' not in st.session_state:
    st.session_state.audit_json = None

# --- 4. INPUTS ---
col1, col2 = st.columns(2)
with col1:
    master_cv = st.text_area("📄 MASTER CV CONTENT", height=350, placeholder="Paste your CV here...")
with col2:
    job_desc = st.text_area("💼 JOB DESCRIPTION", height=350, placeholder="Paste the JD here...")

# --- 5. STAGE A: AUDIT ---
if st.button("RUN STRATEGIC AUDIT"):
    if not api_key:
        st.error("Missing API Key.")
    elif len(master_cv) < 50:
        st.warning("Please provide more CV content.")
    else:
        with st.spinner("Analyzing..."):
            try:
                # FIX: Force REST transport to avoid gRPC 404 errors on Streamlit
                genai.configure(api_key=api_key, transport='rest')
                
                # FIX: Direct model string
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                audit_prompt = f"""
                Perform a strategic audit. Output ONLY valid JSON.
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
                st.error(f"System Error: {str(e)}")

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
        <h3>Verdict: {res['verdict']['level']} ({res['verdict']['score']}/100)</h3>
        <p style="color: #22D3EE;"><strong>Strategy:</strong> {res['pivot']}</p>
        <p><i>{res['verdict']['recommendation']}</i></p>
        <p style="color: #94A3B8;"><strong>Gaps:</strong> {", ".join(res['missing'])}</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # --- 7. STAGE B: SYNTHESIS ---
    if st.button("CONSTRUCT PORTFOLIO"):
        with st.spinner("Writing..."):
            try:
                # Same fix for the Pro model
                model_pro = genai.GenerativeModel('gemini-1.5-pro')
                arch_prompt = f"Create CV and Cover Letter based on: {json.dumps(res)}. CV Source: {master_cv}. No Oxford commas."
                final_res = model_pro.generate_content(arch_prompt)
                st.markdown(final_res.text)
                st.download_button("Download TXT", final_res.text, file_name="portfolio.txt")
            except Exception as e:
                st.error(f"Synthesis Error: {str(e)}")
