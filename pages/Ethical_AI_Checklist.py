"""Ethical AI Checklist page for custom guidelines evaluation."""

import streamlit as st
from services.custom_checklist_service import ChecklistService

# Page configuration
st.set_page_config(page_title="Ethical AI Checklist", page_icon="📋", layout="wide")

# --- UI Components ---
st.title("📋 Ethical AI Checklist for Custom Guidelines")
st.markdown("Upload your own safety guidelines to evaluate text using the Gemini API. This tool helps you ensure that content aligns with your specific ethical standards.")

# Instantiate the service class
# Caching the service instance to maintain state across reruns
@st.cache_resource
def get_checklist_service():
    return ChecklistService()

checklist_service = get_checklist_service()

# Initialize session state for the checklist
if 'custom_checklist' not in st.session_state:
    st.session_state.custom_checklist = []

# --- Main Page Layout ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Step 1: Define Your Checklist")
    
    # Option to upload or manually enter a checklist
    input_method = st.radio(
        "How would you like to provide your checklist?",
        ("Upload a .txt file", "Enter manually"),
        horizontal=True
    )

    if input_method == "Upload a .txt file":
        st.info("Create a `.txt` file where each line is a separate rule or guideline you want to check for.")
        uploaded_file = st.file_uploader("Upload your checklist file.", type=["txt"])
        if uploaded_file:
            st.session_state.custom_checklist = checklist_service.load_checklist_from_file(uploaded_file)
            if st.session_state.custom_checklist:
                st.success(f"Checklist with {len(st.session_state.custom_checklist)} items uploaded successfully!")
            else:
                st.error("Could not read any guidelines from the uploaded file.")
    else:
        manual_checklist = st.text_area("Enter each guideline on a new line:", height=150)
        if manual_checklist:
            st.session_state.custom_checklist = [line.strip() for line in manual_checklist.split('\n') if line.strip()]


    if st.session_state.custom_checklist:
        with st.expander("View Current Custom Checklist", expanded=False):
            for i, item in enumerate(st.session_state.custom_checklist, 1):
                st.markdown(f"{i}. {item}")

with col2:
    st.subheader("Step 2: Evaluate Text")
    text_to_evaluate = st.text_area("Paste the text you want to evaluate against your custom checklist:", height=200, key="text_for_custom_eval")

    if st.button("Evaluate with Custom Checklist", type="primary", use_container_width=True):
        if not text_to_evaluate:
            st.warning("Please paste text to evaluate.")
        elif not st.session_state.custom_checklist:
            st.warning("Please provide a checklist first.")
        else:
            with st.spinner("Analyzing text against your custom checklist..."):
                feedback = checklist_service.evaluate_text_against_checklist(
                    text_to_evaluate,
                    custom_checklist=st.session_state.custom_checklist
                )
                
                st.subheader("Evaluation Results")
                
                if "Custom Educator Checklist" in feedback and feedback["Custom Educator Checklist"]:
                    with st.container():
                        issues_found = []
                        safe_messages = []
                        for issue in feedback["Custom Educator Checklist"]:
                            if "no issues detected" in issue.lower():
                                safe_messages.append(issue)
                            else:
                                issues_found.append(issue)
                        
                        if not issues_found:
                             st.success(f"✅ **Safe:** {safe_messages[0] if safe_messages else 'No issues detected.'}")
                        else:
                            st.error(f"⚠️ **Issues Found:** {len(issues_found)} potential violation(s) detected.")
                            for issue in issues_found:
                                st.warning(issue)

                elif "API Error" in feedback:
                     st.error(f"An error occurred during evaluation: {feedback['API Error'][0]}")
                else:
                     st.info("No specific feedback was returned for the custom checklist.")
