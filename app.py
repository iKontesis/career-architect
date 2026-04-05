import streamlit as st
import google.generativeai as genai
import json

# --- 1. CONFIGURATION & EXECUTIVE STYLING ---
st.set_page_config(page_title="Career Strategy Architect", page_icon="🛡️", layout="wide")

# The Nuclear CSS Option (Standardized for all modes)
st.markdown("""
    <style>
    .stApp { background-color: #0F172A !important; color: #F8FAFC !important; }
    section[data-testid="stSidebar"] { background-color: #1E293B !important; border-right: 1px solid #334155 !important; }
    h1, h2, h3, h4, h5, h6 { color: #F8FAFC !important; font-weight: 800 !important; }
    label[data-testid="stWidgetLabel"] p { color: #94A3B8 !important; font-weight: 600 !important; text-transform: uppercase !important; }
    .stTextArea textarea { background-color: #1E293B !important; color: #F8FAFC !important; border: 1px solid #334155 !important; border-radius: 12px !important; }
    .stTextArea textarea::placeholder { color: #475569 !important; }
    [data-testid="stMetricValue"] { color: #3B82F6 !important; font-weight: 800 !important; }
    [data-testid="stMetricLabel"] { color: #94A3B8 !important; }
    .stButton button { 
        background-color: #3B82F6 !important; color: white !important; border: none !important; border-radius: 8px !important;
        font-weight: bold !important; padding: 0.8rem 2.5rem !important; width: 100% !important; text-transform: uppercase;
    }
    .stButton button:hover { background-color: #2563EB !important; box-shadow: 0 0 20px rgba(59, 130, 246, 0.4) !important; }
    .report-card { background-color: #1E293B !important; padding: 30px !important; border-radius: 20px !important; border: 1px solid #475569 !important; color: #F8FAFC !important; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("## ⚙️ SYSTEM SETTINGS")
    api_key = st.text_input("Gemini API Key", type="password", help="Enter your Google AI Studio API Key")
    st.divider()
    st.markdown("### 🛡️ PRIVACY PROTOCOL")
    st.caption("Stateless processing: No CV data or API keys are stored.")

# --- 3. APP HEADER ---
st.markdown("# 🛡️ CAREER STRATEGY **ARCHITECT**")
st.markdown("#### *High-Level Executive Decision Support System*")
st.divider()

if 'audit_json' not in st.session_state:
    st.session_state.audit_json = None

# --- 4. INPUT AREA ---
col1, col2 = st.columns(2)
with col1:
    master_cv = st.text_area("📄 MASTER CV SOURCE", height=350, placeholder="Paste professional history...")
with col2:
    job_desc = st.text_area("💼 TARGET JOB DESCRIPTION", height=350, placeholder="Paste target requirements...")

# --- 5. STAGE A: THE GATEKEEPER (AUDIT) ---
if st.button("RUN STRATEGIC AUDIT"):
    if not api_key:
        st.error("ERROR: Missing API Key.")
    elif len(master_cv) < 50 or len(job_desc) < 50:
        st.warning("ERROR: Insufficient input data.")
    else:
        with st.spinner("EXECUTING SEMANTIC AUDIT..."):
            try:
                # FIX 1: Explicit Configuration
                genai.configure(api_key=api_key)
                
                # FIX 2: Use the shortest possible model string
                # Some environments fail with 'models/...' prefix
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                audit_prompt = f"""
                Analyze the CV and JD provided. Output ONLY a valid JSON object.
                Schema:
                {{
                    "verdict": {{"level": "string", "score": number, "recommendation": "string"}},
                    "matrix": {{"hierarchy": number, "hard_skills": number, "evidence": number, "soft_skills": number}},
                    "missing": ["string"],
                    "pivot": "string"
                }}
                Rules: No Oxford commas.
                CV: {master_cv}
                JD: {job_desc}
                """
                
                # FIX 3: Add a small safety check for the response
                response = model.generate_content(audit_prompt)
                
                if not response.text:
                    st.error("Empty response from AI. Check your API quota.")
                else:
                    clean_json = response.text.replace('```json', '').replace('```', '').strip()
                    st.session_state.audit_json = json.loads(clean_json)
                    st.rerun()
            except Exception as e:
                # FIX 4: Improved Error Reporting
                st.error(f"AUDIT ERROR: {str(e)}")
                st.info("Tip: Ensure your API Key is from Google AI Studio and has 'Gemini 1.5 Flash' enabled.")

# --- 6. RESULTS DASHBOARD ---
if st.session_state.audit_json:
    res = st.session_state.audit_json
    st.markdown("## 📊 STRATEGIC INTELLIGENCE REPORT")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("HIERARCHY", f"{res['matrix']['hierarchy']}%")
    m2.metric("HARD SKILLS", f"{res['matrix']['hard_skills']}%")
    m3.metric("EVIDENCE", f"{res['matrix']['evidence']}%")
    m4.metric("SOFT SKILLS", f"{res['matrix']['soft_skills']}%")

    st.markdown(f"""
    <div class="report-card">
        <h2 style="margin-top:0;">VERDICT: {res['verdict']['level']} ({res['verdict']['score']}/100)</h2>
        <p style="font-size: 1.2rem; color: #3B82F6;"><strong>STRATEGIC PIVOT:</strong> {res['pivot']}</p>
        <p style="font-style: italic; color: #F8FAFC;">"{res['verdict']['recommendation']}"</p>
        <p style="color: #94A3B8; font-weight: 600;">CRITICAL GAPS: {", ".join(res['missing'])}</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # --- 7. STAGE B: THE ARCHITECT (GENERATION) ---
    if st.button("CONSTRUCT EXECUTIVE PORTFOLIO"):
        with st.spinner("SYNTHESIZING NARRATIVE..."):
            try:
                genai.configure(api_key=api_key)
                model_pro = genai.GenerativeModel('gemini-1.5-pro')
                
                arch_prompt = f"""
                Generate high-impact CV and Cover Letter.
                Strategy: {res['pivot']}
                Audit JSON: {json.dumps(res)}
                CV Source: {master_cv}
                Rules: NO Oxford commas. Professional tone. Pure Markdown.
                """
                
                final_response = model_pro.generate_content(arch_prompt)
                st.markdown("## 🖋️ TAILOR-MADE EXECUTIVE PORTFOLIO")
                st.markdown(final_response.text)
                
                st.download_button(
                    label="📥 DOWNLOAD PORTFOLIO (TXT)",
                    data=final_response.text,
                    file_name="executive_portfolio.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"SYNTHESIS ERROR: {str(e)}")
