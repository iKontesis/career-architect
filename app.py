import streamlit as st
import google.generativeai as genai
import json

# --- 1. CONFIGURATION & EXECUTIVE STYLING ---
st.set_page_config(page_title="Executive Portfolio Architect", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0F172A !important; color: #F1F5F9 !important; font-family: 'Inter', sans-serif !important; }
    section[data-testid="stSidebar"] { background-color: #1E293B !important; border-right: 1px solid #334155 !important; }
    [data-testid="stSidebarUserContent"] { display: flex; flex-direction: column; height: 90vh; }
    .sidebar-footer { margin-top: auto; padding-top: 20px; border-top: 1px solid #334155; font-size: 0.8rem; color: #94A3B8; }
    .sidebar-footer strong { color: #F8FAFC; font-size: 0.9rem; }
    .sidebar-footer a { color: #60A5FA; text-decoration: none; }
    label[data-testid="stWidgetLabel"] p { color: #94A3B8 !important; font-weight: 700 !important; text-transform: uppercase !important; font-size: 0.8rem !important; letter-spacing: 0.08em !important; }
    .stTextArea textarea { background-color: #1E293B !important; color: #FFFFFF !important; border: 1px solid #475569 !important; border-radius: 8px !important; font-size: 15px !important; }
    h1 { font-size: 2.5rem !important; font-weight: 800 !important; letter-spacing: -0.02em !important; color: #F8FAFC !important; }
    h2 { font-size: 1.6rem !important; border-bottom: 1px solid #334155; padding-bottom: 10px; color: #F8FAFC !important; margin-top: 30px; }
    [data-testid="stMetricValue"] { color: #60A5FA !important; font-weight: 800 !important; }
    [data-testid="stMetricLabel"] { color: #94A3B8 !important; text-transform: uppercase !important; font-size: 0.75rem !important; }
    .stButton button { background-color: #2563EB !important; color: white !important; border-radius: 6px !important; font-weight: 700 !important; padding: 0.8rem 2rem !important; width: 100% !important; border: none !important; text-transform: uppercase; letter-spacing: 0.05em; }
    .stButton button:hover { background-color: #1D4ED8 !important; box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3) !important; }
    .report-card { background-color: #1E293B !important; padding: 25px !important; border-radius: 12px !important; border: 1px solid #334155 !important; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2) !important; }
    .executive-intro { font-size: 1rem; color: #F1F5F9; background-color: #1E293B; padding: 25px; border-radius: 12px; border-left: 5px solid #3B82F6; margin-bottom: 30px; }
    .operational-note { font-size: 0.85rem; color: #94A3B8; background-color: #112240; padding: 15px; border: 1px solid #334155; border-radius: 8px; margin-top: 40px; margin-bottom: 20px; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("## ⚙️ ENGINE STATUS")
    api_key = st.secrets.get("GEMINI_API_KEY")
    if api_key:
        st.success("Strategic Core: ONLINE")
        genai.configure(api_key=api_key, transport='rest')
    else:
        st.error("Strategic Core: OFFLINE")

    st.divider()
    st.markdown(f"""
        <div class="sidebar-footer">
            <strong>Ioannis Kontesis</strong><br>
            AI Transformation Architect<br>
            Operational Resilience & Strategy Specialist<br>
            Finance & Risk Professional<br><br>
            🔗 <a href="https://linkedin.com/in/ikontesis" target="_blank">LinkedIn</a> | 
            𝕏 <a href="https://x.com/@ikontesis" target="_blank">Twitter</a><br><br>
            🛡️ Stateless Architecture | v2.3.2<br>
            <span style="font-size: 0.7rem; opacity: 0.4;">Powered by Gemini 3.1</span>
        </div>
        """, unsafe_allow_html=True)

# --- 3. HEADER & INTRO ---
st.markdown("# 🛡️ CAREER STRATEGY **ARCHITECT**")
st.markdown("#### *High-Fidelity Semantic Audit & Portfolio Synthesis*")
st.divider()

st.markdown("""
    <div class="executive-intro">
        <strong>Stop guessing. Audit your career path with precision AI.</strong><br><br>
        • <strong>Gap Detection:</strong> Pinpoint exactly what recruiters are looking for.<br>
        • <strong>Impact Translation:</strong> Turn your history into a high-value narrative.<br>
        • <strong>Universal Logic:</strong> Built for every industry and every career stage.
    </div>
    """, unsafe_allow_html=True)

if 'audit_json' not in st.session_state:
    st.session_state.audit_json = None

# --- 4. INPUT AREA ---
col1, col2 = st.columns(2)
with col1:
    master_cv = st.text_area("📄 MASTER CV SOURCE", height=380, placeholder="Paste your full history...")
with col2:
    job_desc = st.text_area("💼 TARGET JOB DESCRIPTION", height=380, placeholder="Paste target requirements...")

st.divider()

# --- 5. STAGE A: AUDIT ---
if st.button("RUN STRATEGIC AUDIT"):
    if not api_key:
        st.error("System configuration error: Missing API Key.")
    elif len(master_cv) < 50 or len(job_desc) < 50:
        st.warning("Insufficient data: Please provide both CV and JD.")
    else:
        with st.spinner("Executing Strategic Semantic Audit..."):
            try:
                model = genai.GenerativeModel('gemini-3-flash-preview')
                # FULL PROMPT WITH EXPLICIT SCHEMA TO PREVENT KEYERROR
                audit_prompt = f"""
                Analyze the CV against the Job Description. 
                Output ONLY a valid JSON object with the following structure:
                {{
                    "verdict": {{"level": "string", "score": 85, "recommendation": "string"}},
                    "matrix": {{"hierarchy": 80, "hard_skills": 70, "evidence": 90, "soft_skills": 85}},
                    "missing": ["skill1", "skill2"],
                    "pivot": "strategic narrative direction"
                }}
                No conversation, just JSON.
                CV: {master_cv}
                JD: {job_desc}
                """
                response = model.generate_content(audit_prompt)
                clean_json = response.text.replace('```json', '').replace('```', '').strip()
                st.session_state.audit_json = json.loads(clean_json)
                st.rerun()
            except Exception as e:
                st.error("Audit Engine timing out or returning invalid data. Please wait 30s and try again.")

# --- 6. RESULTS (DEFENSIVE DATA ACCESS) ---
if st.session_state.audit_json:
    res = st.session_state.audit_json
    try:
        st.markdown("## 📊 STRATEGIC INTELLIGENCE REPORT")
        
        # Safe access using .get() to prevent crashes
        matrix = res.get('matrix', {})
        verdict = res.get('verdict', {})
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("HIERARCHY", f"{matrix.get('hierarchy', 0)}%")
        m2.metric("SKILLS", f"{matrix.get('hard_skills', 0)}%")
        m3.metric("EVIDENCE", f"{matrix.get('evidence', 0)}%")
        m4.metric("COMPATIBILITY", f"{matrix.get('soft_skills', 0)}%")

        st.markdown(f"""
        <div class="report-card">
            <h3 style="margin-top:0;">Verdict: {verdict.get('level', 'Analysis Pending')} ({verdict.get('score', 0)}/100)</h3>
            <p style="color: #60A5FA;"><strong>Strategy:</strong> {res.get('pivot', 'N/A')}</p>
            <p><i>{verdict.get('recommendation', 'No specific recommendation provided.')}</i></p>
            <p style="color: #94A3B8;"><strong>Gaps:</strong> {", ".join(res.get('missing', []))}</p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # --- 7. STAGE B: SYNTHESIS ---
        if st.button("CONSTRUCT EXECUTIVE PORTFOLIO"):
            with st.spinner("Synthesizing Portfolio..."):
                try:
                    model_pro = genai.GenerativeModel('gemini-3-pro-preview')
                    arch_prompt = f"Create CV and Cover Letter based on this analysis: {json.dumps(res)}. Source CV: {master_cv}. No Oxford commas."
                    final_res = model_pro.generate_content(arch_prompt)
                    st.markdown("## 🖋️ TAILOR-MADE PORTFOLIO")
                    st.markdown(final_res.text)
                    st.download_button("Download TXT", final_res.text, file_name="executive_portfolio.txt")
                except Exception:
                    fallback = genai.GenerativeModel('gemini-3-flash-preview')
                    final_res = fallback.generate_content(arch_prompt)
                    st.markdown(final_res.text)
                    st.download_button("Download TXT", final_res.text, file_name="executive_portfolio.txt")
                    
    except Exception as e:
        st.error("The AI generated an incomplete report. Please run the audit again.")

# --- 8. THE SHIELD ---
st.markdown("""
    <div class="operational-note">
        <strong>🛡️ Operational Note</strong><br>
        Powered by <strong>Gemini 3.1 (Free Tier)</strong> for universal access.<br>
        • <strong>Error 429?</strong> The engine is at peak capacity. Wait 60s and click again.<br>
        • <strong>Privacy:</strong> 100% stateless. Your data is processed in real-time and never stored.
    </div>
    """, unsafe_allow_html=True)
