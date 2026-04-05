import streamlit as st
import google.generativeai as genai
import json

# --- 1. CONFIGURATION & EXECUTUVE STYLING ---
st.set_page_config(page_title="Career Strategy Architect", page_icon="🛡️", layout="wide")

# The Nuclear CSS Option: High-Contrast Executive Dark Theme
st.markdown("""
    <style>
    /* Global App Background (Deep Navy) */
    .stApp {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
    }

    /* Sidebar (Solid Navy) */
    section[data-testid="stSidebar"] {
        background-color: #1E293B !important;
        border-right: 1px solid #334155 !important;
    }

    /* Headers & Text Visibility */
    h1, h2, h3, h4, h5, h6 {
        color: #F8FAFC !important;
        font-weight: 800 !important;
    }
    
    label[data-testid="stWidgetLabel"] p {
        color: #94A3B8 !important; 
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    /* Text Areas (Darker Slate with Light Text) */
    .stTextArea textarea { 
        background-color: #1E293B !important; 
        color: #F8FAFC !important; 
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        font-family: 'Inter', sans-serif !important;
        padding: 15px !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #475569 !important;
    }

    /* Metrics (Large & Vibrant) */
    [data-testid="stMetricValue"] {
        color: #3B82F6 !important; 
        font-weight: 800 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
    }

    /* Buttons (Executive Blue) */
    .stButton button { 
        background-color: #3B82F6 !important; 
        color: white !important; 
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        padding: 0.8rem 2.5rem !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    .stButton button:hover {
        background-color: #2563EB !important;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.4) !important;
        transform: translateY(-2px) !important;
    }

    /* Report Card (Glassmorphism effect) */
    .report-card { 
        background-color: #1E293B !important; 
        padding: 30px !important; 
        border-radius: 20px !important; 
        border: 1px solid #475569 !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5) !important;
        color: #F8FAFC !important;
        margin-top: 20px !important;
    }
    
    .stAlert {
        background-color: #1E293B !important;
        color: white !important;
        border: 1px solid #334155 !important;
    }

    /* Clean UI: Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.markdown("## ⚙️ SYSTEM SETTINGS")
    api_key = st.text_input("Gemini API Key", type="password", help="Enter your Google AI Studio API Key")
    if api_key:
        genai.configure(api_key=api_key)
    st.divider()
    st.markdown("### 🛡️ PRIVACY PROTOCOL")
    st.caption("This application performs stateless processing. No CV data or API keys are persisted or stored.")

# --- 3. APP HEADER ---
st.markdown("# 🛡️ CAREER STRATEGY **ARCHITECT**")
st.markdown("#### *High-Level Executive Decision Support System*")
st.divider()

# Initializing Session State
if 'audit_json' not in st.session_state:
    st.session_state.audit_json = None

# --- 4. INPUT INTERFACE ---
col1, col2 = st.columns(2)
with col1:
    master_cv = st.text_area("📄 MASTER CV SOURCE", height=350, placeholder="Paste your full professional history...")
with col2:
    job_desc = st.text_area("💼 TARGET JOB DESCRIPTION", height=350, placeholder="Paste the target role requirements...")

# --- 5. STAGE A: THE GATEKEEPER (AUDIT) ---
if st.button("RUN STRATEGIC AUDIT"):
    if not api_key:
        st.error("SYSTEM ERROR: Missing API Key in Settings.")
    elif len(master_cv) < 50 or len(job_desc) < 50:
        st.warning("INPUT ERROR: Insufficient data to perform audit.")
    else:
        with st.spinner("EXECUTING SEMANTIC AUDIT..."):
            try:
                # Using base model names for maximum compatibility
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                audit_prompt = f"""
                ### ROLE: THE CAREER STRATEGY ARCHITECT
                Task: Perform a deep semantic audit between the CV and JD provided.
                Rules: No Oxford commas. Industry-agnostic. No conversational text.
                Output ONLY a valid JSON object matching this schema:
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
                st.error(f"AUDIT SYSTEM OFFLINE: {str(e)}")

# --- 6. DISPLAY AUDIT DASHBOARD ---
if st.session_state.audit_json:
    res = st.session_state.audit_json
    st.markdown("## 📊 STRATEGIC INTELLIGENCE REPORT")
    
    # Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("HIERARCHY", f"{res['matrix']['hierarchy']}%")
    m2.metric("HARD SKILLS", f"{res['matrix']['hard_skills']}%")
    m3.metric("EVIDENCE", f"{res['matrix']['evidence']}%")
    m4.metric("SOFT SKILLS", f"{res['matrix']['soft_skills']}%")

    # Verdict Card
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
                # Use Gemini Pro for higher quality text synthesis
                model_pro = genai.GenerativeModel('gemini-1.5-pro')
                
                arch_prompt = f"""
                ### ROLE: THE CAREER ARCHITECT
                Task: Generate a high-impact, ATS-optimized CV and Cover Letter based on the provided strategy.
                Strategy: {res['pivot']}
                Audit Intelligence: {json.dumps(res)}
                Source Materials: {master_cv}
                Constraints: Use years (2022-2025). NO Oxford commas. Professional Executive tone. Pure Markdown.
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
                st.error(f"SYNTHESIS SYSTEM OFFLINE: {str(e)}")
