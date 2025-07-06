"""Ethical AI Checklist page for custom guidelines evaluation."""

import streamlit as st
from services.evaluation_service import evaluate_text, load_checklist_from_file

st.set_page_config(page_title="Ethical AI Checklist", page_icon="📋")
st.title("📋 Ethical AI Checklist for Custom Guidelines")
st.markdown("Upload your own safety guidelines to use in evaluations.")

if 'custom_checklist' not in st.session_state:
    st.session_state.custom_checklist = []

st.subheader("Step 1: Upload Your Custom Checklist")
uploaded_file = st.file_uploader("Upload a .txt file with one guideline per line.", type=["txt"])

if uploaded_file:
    st.session_state.custom_checklist = load_checklist_from_file(uploaded_file)
    if st.session_state.custom_checklist:
        st.success("Checklist uploaded successfully!")
    else:
        st.error("Could not read checklist from file.")

if st.session_state.custom_checklist:
    with st.expander("View current custom checklist", expanded=True):
        st.write(st.session_state.custom_checklist)

st.divider()

st.subheader("Step 2: Evaluate Text Against Your Checklist")
text_to_evaluate = st.text_area("Paste text to evaluate with your checklist:", height=150)

if st.button("Evaluate with Custom Checklist", type="primary"):
    if not text_to_evaluate:
        st.warning("Please paste text to evaluate.")
    elif not st.session_state.custom_checklist:
        st.warning("Please upload a checklist first.")
    else:
        with st.spinner("Evaluating..."):
            feedback = evaluate_text(
                text_to_evaluate,
                principles_to_check=[],
                custom_checklist=st.session_state.custom_checklist
            )
            st.subheader("Evaluation Results:")
            if "Custom Educator Checklist" in feedback:
                with st.expander("**Custom Educator Checklist**", expanded=True):
                     for issue in feedback["Custom Educator Checklist"]:
                        is_safe = "No issues detected" in issue
                        st.success("✅ " + issue) if is_safe else st.warning("⚠️ " + issue)