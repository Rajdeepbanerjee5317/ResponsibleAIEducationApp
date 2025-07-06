"""Personalized Q&A page for safe educational content generation."""

import streamlit as st
from services.evaluation_service import generate_safe_text

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