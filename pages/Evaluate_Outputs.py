"""Evaluate Outputs page for responsible AI principles checking."""

import streamlit as st
import os
from services.evaluation_service import evaluate_text, DEFAULT_PRINCIPLES

# Load custom CSS
def load_css():
    css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".streamlit", "style.css")
    if os.path.exists(css_file):
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load custom CSS
load_css()

st.set_page_config(page_title="Evaluate Outputs", page_icon="⚖️")
st.title("⚖️ Evaluate Outputs Against Responsible AI Principles")
st.markdown("Paste text to check it against common responsible AI principles.")

text_to_evaluate = st.text_area("Paste the text you want to evaluate:", height=200)
principles = st.multiselect(
    "Select principles to evaluate against:",
    options=list(DEFAULT_PRINCIPLES.keys()),
    default=list(DEFAULT_PRINCIPLES.keys())
)

if st.button("Evaluate Text", type="primary"):
    if text_to_evaluate and principles:
        with st.spinner("Evaluating text..."):
            feedback = evaluate_text(text_to_evaluate, principles)
            st.divider()
            st.subheader("Evaluation Results:")
            for principle, issues in feedback.items():
                with st.expander(f"**{principle}**", expanded=True):
                    is_safe = "No specific issues" in issues[0]
                    if is_safe:
                         st.success(f"✅ {issues[0]}")
                    else:
                        for issue in issues:
                            st.warning(f"⚠️ {issue}")
    else:
        st.warning("Please provide text and select at least one principle.")