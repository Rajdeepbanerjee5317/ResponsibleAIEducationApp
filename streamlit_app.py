"""Main Streamlit application for Responsible AI Education."""

import streamlit as st

st.set_page_config(
    page_title="Responsible Prompter",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 The Responsible Prompter")
st.caption("A Tool for Safe and Responsible AI in Education")

st.sidebar.success("Select a tool above to begin.")

st.markdown(
    """
    ### Welcome!

    This application is designed to help students and educators use Generative AI safely and responsibly. It provides tools to generate educational content, evaluate text for potential issues, and craft better, safer prompts.

    **👈 Select a tool from the sidebar** to explore the different use cases:

    - **Personalized Q&A:** Get tailored explanations and practice questions on any topic.
    - **Free Text Generation:** Generate text with built-in safety guardrails.
    - **Evaluate Outputs:** Check any text against responsible AI principles.
    - **Ethical AI Checklist:** Use a custom checklist for content evaluation.
    - **Responsible Prompting:** Get live feedback to improve your prompts.
    
    This tool is for educational purposes and uses simulated AI responses to demonstrate key concepts in responsible AI.
    """
)