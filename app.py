import streamlit as st
import google.generativeai as genai
import json

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="Executive Portfolio Architect", page_icon="🛡️", layout="wide")

# Custom CSS for Navy Blue/Slate Aesthetic
st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
    .stTextArea textarea { background-color: #FFFFFF; border-radius: 10px; border: 1px solid #E2E8F0; }
    .stButton button { 
        background-color: #1A365D; color: white; border-radius: 8px; 
        font-weight: bold; border: none; padding: 0.5rem 2rem;
    }
    .stButton button:hover { background-color: #2A4365; color: #E2E8F0; }
    h1, h2, h3 { color: #1A365D; font-family: 'Inter', sans-serif; }
    .report-card { 
        background-color: #FFFFFF; padding: 25px; border-radius: 15px; 
        border-left: 5px solid #1A365D; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- APP HEADER ---
st.markdown("# 🛡️ CAREER STRATEGY **ARCHITECT**")
st.markdown("### Universal Industry-Agnostic Audit & Generation")
st.divider()

# --- SIDEBAR: API SETUP ---
with st.sidebar:
    st.title("Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.info("Your data is processed in real-time and not stored.")
    if api_key:
        genai.configure(api_key=api_key)

# --- INITIALIZING STATE ---
if 'audit_json' not in st.session_state:
    st.session_state.audit_json = None

# --- INPUT AREA ---
col1, col2 = st.columns(2)
with col1:
    master_cv = st.text_area("📄 Paste Master CV", height=300, placeholder="Your full experience source...")
with col2:
    job_desc = st.text_area("💼 Paste Job Description", height=300, placeholder="Target role requirements...")

# --- STAGE A: THE GATEKEEPER (AUDIT) ---
if st.button("RUN STRATEGIC AUDIT"):
    if not api_key:
        st.error("Please enter an API Key in the sidebar.")
    elif len(master_cv) < 100 or len(job_desc) < 100:
        st.warning("Please provide more detailed text for both CV and JD.")
    else:
        with st.spinner("Analyzing alignment..."):
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # STAGE A PROMPT (v6.0)
            audit_prompt = f"""
            ### ROLE: THE CAREER STRATEGY ARCHITECT
            Perform a high-level audit between the CV and JD below.
            Output ONLY a valid JSON object matching this schema:
            {{
                "verdict": {{"level": "string", "score": number, "recommendation": "string"}},
                "matrix": {{"hierarchy": number, "hard_skills": number, "evidence": number, "soft_skills": number}},
                "missing": ["string"],
                "pivot": "string"
            }}
            Rules: No Oxford commas. Industry-agnostic. 
            CV: {master_cv}
            JD: {job_desc}
            """
            
            response = model.generate_content(audit_prompt)
            try:
                # Clean potential markdown from response
                clean_json = response.text.replace('```json', '').replace('```', '').strip()
                st.session_state.audit_json = json.loads(clean_json)
            except:
                st.error("Failed to parse analysis. Please try again.")

# --- DISPLAY AUDIT RESULTS ---
if st.session_state.audit_json:
    res = st.session_state.audit_json
    st.markdown("## 📊 ATS Intelligence Report")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Hierarchy", f"{res['matrix']['hierarchy']}%")
    c2.metric("Hard Skills", f"{res['matrix']['hard_skills']}%")
    c3.metric("Evidence", f"{res['matrix']['evidence']}%")
    c4.metric("Soft Skills", f"{res['matrix']['soft_skills']}%")

    with st.container():
        st.markdown(f"""
        <div class="report-card">
            <h4>Verdict: {res['verdict']['level']} (Score: {res['verdict']['score']}/100)</h4>
            <p><strong>Strategy:</strong> {res['pivot']}</p>
            <p><i>{res['verdict']['recommendation']}</i></p>
            <p style="color: #64748B;"><strong>Critical Gaps:</strong> {", ".join(res['missing'])}</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # --- STAGE B: THE ARCHITECT (GENERATION) ---
    if st.button("CONSTRUCT EXECUTIVE PORTFOLIO"):
        with st.spinner("Architecting documents..."):
            model_pro = genai.GenerativeModel('gemini-1.5-pro')
            
            # STAGE B PROMPT (v6.0)
            arch_prompt = f"""
            ### ROLE: THE CAREER ARCHITECT
            Generate a high-impact, ATS-optimized CV and Cover Letter.
            Strategy: {res['pivot']}
            Master CV: {master_cv}
            Audit Data: {json.dumps(res)}
            Constraints: Use years (2022-2025). NO Oxford commas. Professional Markdown.
            """
            
            final_response = model_pro.generate_content(arch_prompt)
            st.markdown("## 🖋️ Tailor-Made Portfolio")
            st.markdown(final_response.text)
            st.download_button("Download as Text", final_response.text, file_name="executive_portfolio.txt")
