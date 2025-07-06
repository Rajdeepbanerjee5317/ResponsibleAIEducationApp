"""Free Text Generation page with safety guardrails."""

import streamlit as st
from services.evaluation_service import generate_safe_text

st.set_page_config(page_title="Free Text Generation", page_icon="✍️")
st.title("✍️ Free Text Generation with Safe AI Guardrails")
st.markdown("Generate text on a topic, with automatic safety filtering.")

prompt = st.text_area("What do you want to write about?", height=150)

if st.button("Generate Text", type="primary"):
    if prompt:
        with st.spinner("Generating text..."):
            is_safe, response = generate_safe_text(prompt)
            st.divider()
            st.subheader("Generated Response:")
            if is_safe:
                st.info(response)
            else:
                st.error(f"⚠️ **Content Flagged:** {response}")
    else:
        st.warning("Please enter a prompt.")