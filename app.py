import streamlit as st
import google.generativeai as genai
import json

# --- 1. CONFIGURATION & QUIET LUXURY STYLING (The Bloomberg Look) ---
st.set_page_config(page_title="Executive Portfolio Architect", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    /* Global App Background - Deep Midnight Slate */
    .stApp { background-color: #0F172A !important; color: #F1F5F9 !important; font-family: 'Inter', sans-serif !important; }
    
    /* SIDEBAR styling - Solid Dark Slate */
    section[data-testid="stSidebar"] { background-color: #1E293B !important; border-right: 1px solid #334155 !important; }
    section[data-testid="stSidebar"] * { color: #E2E8F0 !important; }

    /* EXECUTIVE LABELS - Steel Blue (Visible & Elegant) */
    label[data-testid="stWidgetLabel"] p {
        color: #94A3B8 !important; 
        font-weight: 700 !important;
        text-transform: uppercase !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.1em !important;
        margin-bottom: 0.5rem;
    }

    /* TEXT AREAS - Slate Navy */
    .stTextArea textarea { 
        background-color: #1E293B !important; 
        color: #FFFFFF !important; 
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
        font-size: 15px !important;
        padding: 15px !important;
        font-family: 'Monaco', monospace !important;
    }
    .stTextArea textarea:focus { border: 1px solid #3B82F6 !important; box-shadow: 0 0 10px rgba(59, 130, 246, 0.2) !important; }
    
    /* HEADERS - Boardroom Slate */
    h1, h2, h3 { color: #F8FAFC !important; font-weight: 800 !important; letter-spacing: -0.03em !important; }
    h1 { font-size: 2.8rem !important; margin-bottom: 0.5rem !important; }
    h2 { font-size: 1.8rem !important; border-bottom: 2px solid #334155; padding-bottom: 10px; margin-top: 30px; }

    /* METRICS - Electric Blue for Data */
    [data-testid="stMetricValue"] { color: #60A5FA !important; font-weight: 800 !important; font-size: 2.5rem !important; }
    [data-testid="stMetricLabel"] { color: #94A3B8 !important; font-weight: 600 !important; text-transform: uppercase !important; }

    /* BUTTONS - Solid Executive Blue */
    .stButton button { 
        background-color: #2563EB !important; 
        color: white !important; 
        border-radius: 6px !important;
        font-weight: 700 !important;
        padding: 0.85rem 2rem !important;
        width: 100% !important;
        border: none !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-size: 1rem !important;
    }
    .stButton button:hover { background-color: #1D4ED8 !important; box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4) !important; }

    /* REPORT CARD - Glassmorphism */
    .report-card { 
        background-color: #1E293B !important; 
        padding: 30px !important; 
        border-radius: 12px !important; 
        border: 1px solid #334155 !important;
        color: #F8FAFC !important;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3) !important;
        margin-top: 15px;
    }
    
    /* Executive Guide Text */
    .executive-guide {
        font-size: 1.1rem;
        color: #94A3B8;
        background-color: #1E293B;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        margin-bottom: 20px;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR & SIGNATURE LOGIC ---
with st.sidebar:
    # THE SIGNATURE BLOCK
    st.markdown("## ⚙️ SYSTEM")
    if "GEMINI_API_KEY" in st.secrets:
        st.success("Strategic Engine: ACTIVE")
    else:
        st.error("Engine: OFFLINE")
        
    st.divider()
    st.markdown("### 🖋️ SIGNATURE")
    st.markdown("""
        <div style="font-size: 1.1rem; color: white;">
            <strong>Ioannis Kontesis</strong><br>
            AI Transformation Architect<br>
            Operational Risk Specialist<br>
            <br>
            <a href="https://linkedin.com/in/ikontesis" target="_blank" style="text-decoration:none; color:#60A5FA;">Connect on LinkedIn</a><br>
            <a href="https://x.com/@ikontesis" target="_blank" style="text-decoration:none; color:#94A3B8;">Follow on X (Twitter)</a>
        </div>
        """, unsafe_allow_html=True)
        
    st.divider()
    st.caption("Stateless Architecture | Stateless Processing")
    st.caption("Executive Portfolio Architect v2.3")

# --- 3. APP HEADER ---
col_head, col_ver = st.columns([7, 1])
with col_head:
    st.markdown("# 🛡️ CAREER STRATEGY **ARCHITECT**")
    st.markdown("#### *High-Level Executive Decision Support System*")

# Initialize Session State
if 'audit_json' not in st.session_state:
    st.session_state.audit_json = None
if api_key := st.secrets.get("GEMINI_API_KEY"):
    genai.configure(api_key=api_key, transport='rest')
else:
    st.error("ACCESS DENIED: Missing Internal System Key.")

st.divider()

# --- 4. EXECUTIVE GUIDE ---
st.markdown("""
    <div class="executive-guide">
        <strong>Executive Protocol:</strong> In the era of Agentic AI, the primary challenge facing modern enterprise is not the availability of GenAI, but the safe and profitable 
        operationalization of LLM workflows within legacy corporate architectures. This system provides actionable intelligence 
        by auditing your master professional experience against a target job description, ensuring your semantic positioning 
        aligns with high-stakes, risk-aware leadership roles. <strong>It de-risks your career transformation.</strong>
    </div>
    """, unsafe_allow_html=True)

# --- 5. INPUT AREA ---
col1, col2 = st.columns(2)
with col1:
    st.markdown("### 1. Master Experience Source")
    master_cv = st.text_area("Master Experience Source", height=380, placeholder="Paste your full, unedited professional history (years-only format)...")
with col2:
    st.markdown("### 2. Target Job Description")
    job_desc = st.text_area("Target Job Description", height=380, placeholder="Paste the target role requirements here...")

st.divider()

# --- 6. STAGE A: THE GATEKEEPER (AUDIT) ---
if st.button("RUN STRATEGIC SEMANTIC AUDIT"):
    if len(master_cv) < 50 or len(job_desc) < 50:
        st.warning("INSUFFICIENT INPUT: Both CV and JD are required to perform a semantic audit.")
    else:
        with st.spinner("Executing Strategic Semantic Audit..."):
            try:
                # Use base model names for dynamic routing
                model = genai.GenerativeModel('gemini-3-flash-preview')
                
                audit_prompt = f"""
                You are THE CAREER STRATEGY ARCHITECT.
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
                st.error(f"Audit System Error: {str(e)}")

# --- 7. DISPLAY DASHBOARD ---
if st.session_state.audit_json:
    res = st.session_state.audit_json
    st.markdown("## 📊 STRATEGIC INTELLIGENCE REPORT")
    
    # Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Hierarchy Match", f"{res['matrix']['hierarchy']}%")
    m2.metric("Semantic Skills", f"{res['matrix']['hard_skills']}%")
    m3.metric("Evidence of Impact", f"{res['matrix']['evidence']}%")
    m4.metric("Role Compatibility", f"{res['matrix']['soft_skills']}%")

    # Verdict Card
    st.markdown(f"""
    <div class="report-card">
        <h2 style="margin-top:0;">VERDICT: {res['verdict']['level']} ({res['verdict']['score']}/100)</h2>
        <p style="font-size: 1.25rem; color: #60A5FA;"><strong>PROPOSED STRATEGY:</strong> {res['pivot']}</p>
        <p style="font-style: italic; color: #F8FAFC;">"{res['verdict']['recommendation']}"</p>
        <p style="color: #94A3B8; font-weight: 600;">CRITICAL SEMANTIC GAPS: {", ".join(res['missing'])}</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # --- 8. STAGE B: THE ARCHITECT (SYNTHESIS) ---
    if st.button("CONSTRUCT EXECUTIVE PORTFOLIO"):
        with st.spinner("SYNTHESIZING EXECUTIVE NARRATIVE WITH GEMINI 3 PRO..."):
            try:
                # Primary attempt with Gemini 3 Pro
                model_pro = genai.GenerativeModel('gemini-3-pro-preview')
                arch_prompt = f"Create high-impact CV and Cover Letter based on: {json.dumps(res)}. Source: {master_cv}. No Oxford commas. Professional Executive tone. Pure Markdown."
                final_res = model_pro.generate_content(arch_prompt)
                st.markdown("## 🖋️ TAILOR-MADE PORTFOLIO")
                st.markdown(final_res.text)
                st.download_button("Download TXT", final_res.text, file_name="portfolio.txt")
            except Exception as e:
                # Fallback to Flash for Synthesis
                try:
                    fallback = genai.GenerativeModel('gemini-3-flash-preview')
                    final_res = fallback.generate_content(arch_prompt)
                    st.markdown("## 🖋️ TAILOR-MADE PORTFOLIO (High-Speed Engine)")
                    st.markdown(final_res.text)
                    st.download_button("Download TXT", final_res.text, file_name="portfolio.txt")
                except Exception as e2:
                    st.error(f"Synthesis Failure: {str(e2)}")
