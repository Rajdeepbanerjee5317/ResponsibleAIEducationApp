"""Free Text Generation page with safety guardrails."""

import streamlit as st
import os
from services.evaluation_service import generate_safe_text,generate_safe_free_text

# Load custom CSS
def load_css():
    css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".streamlit", "style.css")
    if os.path.exists(css_file):
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load custom CSS
load_css()

st.set_page_config(page_title="Free Text Generation", page_icon="✍️")
st.title("✍️ Free Text Generation with Safe AI Guardrails")
st.markdown("Generate text on a topic, with automatic safety filtering.")

prompt = st.text_area("What do you want to write about?", height=150)

if st.button("Generate Text", type="primary"):
    if prompt:
        with st.spinner("Generating text..."):
            is_safe, response = generate_safe_free_text(prompt)
            st.divider()
            st.subheader("Generated Response:")
            if is_safe:
                st.info(response)
            else:
                st.error(f"⚠️ **Content Flagged:** {response}")
    else:
        st.warning("Please enter a prompt.")