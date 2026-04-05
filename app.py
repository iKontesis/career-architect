import streamlit as st
import google.genai as genai
from google.genai import types
import json
import plotly.graph_objects as go
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="Career Strategy Architect v2.3.5", layout="wide")
st.title("🚀 Career Strategy Architect v2.3.5")
st.subheader("AI-Driven Professional Alignment & Semantic Audit")

# --- SIDEBAR: API KEY ---
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.info("Stateless mode: Your key is not stored.")

# --- SESSION STATE INITIALIZATION ---
if 'audit_json' not in st.session_state:
    st.session_state.audit_json = None

# --- INPUT SECTION ---
col1, col2 = st.columns(2)
with col1:
    master_cv = st.text_area("PASTE MASTER CV (Source of Truth)", height=300)
with col2:
    job_desc = st.text_area("PASTE JOB DESCRIPTION (Target)", height=300)

# --- 5. STAGE A: STRATEGIC AUDIT ---
if st.button("RUN STRATEGIC AUDIT"):
    if not api_key:
        st.error("Please provide an API Key in the sidebar.")
    elif len(master_cv) < 200 or len(job_desc) < 200:
        st.warning("Please provide more detailed CV and Job Description data.")
    else:
        client = genai.Client(api_key=api_key)
        
        with st.spinner("Executing Strategic Semantic Audit (Gemini 3.1 Flash)..."):
            try:
                # Προετοιμασία του Audit Prompt
                audit_prompt = f"""Analyze the CV against the JD for a senior executive role.
                Focus on hierarchy alignment, hard skills match, evidence of impact, and soft skills.
                
                CV: {master_cv}
                JD: {job_desc}"""

                # Κλήση με το νέο SDK και JSON Schema
                response = client.models.generate_content(
                    model="gemini-3.1-flash",
                    config=types.GenerateContentConfig(
                        system_instruction="You are a strict JSON engine. Output ONLY a valid JSON object with keys: verdict (level, score, recommendation), matrix (hierarchy, hard_skills, evidence, soft_skills), missing (list), pivot (string).",
                        response_mime_type="application/json"
                    ),
                    contents=audit_prompt
                )
                
                # Ασφαλές Parsing
                parsed_data = json.loads(response.text)
                
                # Defensive Check για τα κλειδιά (Fixes KeyError)
                st.session_state.audit_json = {
                    "verdict": parsed_data.get("verdict", {"level": "Audit Pending", "score": 0, "recommendation": "N/A"}),
                    "matrix": parsed_data.get("matrix", {"hierarchy": 0, "hard_skills": 0, "evidence": 0, "soft_skills": 0}),
                    "missing": parsed_data.get("missing", ["No data returned"]),
                    "pivot": parsed_data.get("pivot", "Retry audit for strategic direction.")
                }
                
                st.success("Audit Completed Successfully!")
                st.rerun()

            except Exception as e:
                st.error(f"Audit Engine Error: {str(e)}")

# --- 6. DASHBOARD & ANALYSIS ---
if st.session_state.audit_json:
    res = st.session_state.audit_json
    verdict = res.get('verdict', {})
    matrix = res.get('matrix', {})
    
    st.divider()
    c1, c2, c3 = st.columns([1, 2, 1])
    
    with c1:
        st.metric("Match Score", f"{verdict.get('score', 0)}/100")
        st.write(f"**Level:** {verdict.get('level', 'N/A')}")
        st.write(f"**Action:** {verdict.get('recommendation', 'N/A')}")

    with c2:
        # RADAR CHART
        categories = ['Hierarchy', 'Hard Skills', 'Evidence', 'Soft Skills']
        values = [
            matrix.get('hierarchy', 0), 
            matrix.get('hard_skills', 0), 
            matrix.get('evidence', 0), 
            matrix.get('soft_skills', 0)
        ]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values, theta=categories, fill='toself', name='Alignment',
            line_color='#00ffcc'
        ))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, 
                          title="Semantic Alignment Matrix", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    with c3:
        st.subheader("Strategic Pivot")
        st.info(res.get('pivot', 'No pivot instructions available.'))
        
    st.subheader("🔴 Missing Critical Elements")
    st.write(", ".join(res.get('missing', [])))

# --- FOOTER ---
st.divider()
st.caption("Developed by Ioannis Kontesis | Powered by Gemini 3.1 & Stateless Python Architecture")
