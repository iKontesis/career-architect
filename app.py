import streamlit as st
import google.generativeai as genai
import json

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="Executive Portfolio Architect", page_icon="🛡️", layout="wide")

# CSS: Ensuring absolute visibility regardless of Browser Theme (Dark/Light)
st.markdown("""
    <style>
    /* Background and Global Text */
    .main { background-color: #F8FAFC; }
    
    /* Force Labels (Επικεφαλίδες στα κουτάκια) to be Slate Blue */
    label[data-testid="stWidgetLabel"] {
        color: #1E293B !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }

    /* Sidebar Labels should be White */
    section[data-testid="stSidebar"] label[data-testid="stWidgetLabel"] {
        color: white !important;
    }

    /* Text areas: White background, Slate text */
    .stTextArea textarea { 
        background-color: #FFFFFF !important; 
        color: #0F172A !important; 
        border: 1px solid #CBD5E1 !important;
        border-radius: 10px !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] { 
        background-color: #1A365D !important; 
    }
    section[data-testid="stSidebar"] .stMarkdown p {
        color: #E2E8F0 !important;
    }

    /* Buttons */
    .stButton button { 
        background-color: #1A365D !important; 
        color: white !important; 
        border-radius: 8px !important;
        font-weight: bold !important;
        padding: 0.6rem 2rem !important;
    }
    
    h1, h2, h3 { color: #1A365D !important; }
    
    .report-card { 
        background-color: #FFFFFF; 
        padding: 25px; 
        border-radius: 15px; 
        border-left: 5px solid #1A365D; 
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        color: #1E293B;
    }
    </style>
    """, unsafe_allow_html=True)

# --- APP HEADER ---
st.markdown("# 🛡️ CAREER STRATEGY **ARCHITECT**")
st.markdown("### Universal Industry-Agnostic Audit & Generation")
st.divider()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    api_key = st.text_input("Gemini API Key", type="password", help="Enter your Google AI Studio API Key")
    if api_key:
        genai.configure(api_key=api_key)
    st.info("Stateless processing: Your data remains private and is never stored.")

# --- INITIALIZING SESSION STATE ---
if 'audit_json' not in st.session_state:
    st.session_state.audit_json = None

# --- INPUT AREA ---
col1, col2 = st.columns(2)
with col1:
    master_cv = st.text_area("📄 Master CV Content", height=300, placeholder="Paste the text source of your full experience...")
with col2:
    job_desc = st.text_area("💼 Job Description", height=300, placeholder="Paste the requirements of the target role...")

# --- STAGE A: THE GATEKEEPER ---
if st.button("RUN STRATEGIC AUDIT"):
    if not api_key:
        st.error("Missing API Key. Please provide it in the sidebar.")
    elif len(master_cv) < 50 or len(job_desc) < 50:
        st.warning("Insufficient input. Please provide more context to proceed.")
    else:
        with st.spinner("Executing Semantic Audit..."):
            try:
                # FIX: Using direct model name without 'models/' prefix
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                audit_prompt = f"""
                Analyze CV vs JD. Output ONLY a valid JSON object. No markdown, no text.
                JSON Schema:
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
                # Cleaning the output in case the model wraps it in ```json
                raw_text = response.text.replace('```json', '').replace('```', '').strip()
                st.session_state.audit_json = json.loads(raw_text)
                st.rerun()
            except Exception as e:
                st.error(f"Audit Error: {str(e)}")

# --- DISPLAY RESULTS ---
if st.session_state.audit_json:
    res = st.session_state.audit_json
    st.markdown("## 📊 Strategic Intelligence Report")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Hierarchy", f"{res['matrix']['hierarchy']}%")
    m2.metric("Skills", f"{res['matrix']['hard_skills']}%")
    m3.metric("Evidence", f"{res['matrix']['evidence']}%")
    m4.metric("Fit", f"{res['matrix']['soft_skills']}%")

    st.markdown(f"""
    <div class="report-card">
        <h3>Verdict: {res['verdict']['level']} (Score: {res['verdict']['score']}/100)</h3>
        <p><strong>Strategy:</strong> {res['pivot']}</p>
        <p><i>{res['verdict']['recommendation']}</i></p>
        <p style="color: #64748B;"><strong>Critical Semantic Gaps:</strong> {", ".join(res['missing'])}</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # --- STAGE B: THE ARCHITECT ---
    if st.button("CONSTRUCT EXECUTIVE PORTFOLIO"):
        with st.spinner("Synthesizing Executive Narrative..."):
            try:
                model_pro = genai.GenerativeModel('gemini-1.5-pro')
                
                arch_prompt = f"""
                You are THE CAREER ARCHITECT. Synthesize a high-impact, ATS-optimized CV and Cover Letter.
                Strategy: {res['pivot']}
                Audit Results: {json.dumps(res)}
                Master CV Data: {master_cv}
                Constraints: Use years (2022-2025). NO Oxford commas. High-stakes executive tone.
                """
                
                final_res = model_pro.generate_content(arch_prompt)
                st.markdown("## 🖋️ Tailor-Made Portfolio")
                st.markdown(final_res.text)
                st.download_button("Download Portfolio (TXT)", final_res.text, file_name="executive_portfolio.txt")
            except Exception as e:
                st.error(f"Synthesis Error: {str(e)}")
