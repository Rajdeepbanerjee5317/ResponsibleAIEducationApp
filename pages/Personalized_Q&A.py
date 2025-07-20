"""Personalized Q&A page for safe educational content generation."""

import streamlit as st
import os
from services.evaluation_service import generate_safe_text

# Load custom CSS
def load_css():
    css_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".streamlit", "style.css")
    if os.path.exists(css_file):
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load custom CSS
load_css()

st.set_page_config(page_title="Personalized Q&A", page_icon="❓")
st.title("❓ Personalized Question & Answer Generation")
st.markdown("Enter a topic to receive a safe, tailored explanation.")

topic = st.text_input("Enter a topic or concept:", placeholder="e.g., Photosynthesis")

if st.button("Generate Explanation", type="primary"):
    if topic:
        with st.spinner("Generating explanation..."):
            is_safe, response = generate_safe_text(topic)
            st.divider()
            st.subheader("Generated Response:")
            if is_safe:
                st.markdown(response)
            else:
                st.error(f"⚠️ **Content Flagged:** {response}")
    else:
        st.warning("Please enter a topic.")