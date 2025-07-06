"""Responsible Prompting page for prompt quality feedback."""

import streamlit as st
from services.prompt_service import get_scenario, analyze_prompt_quality, get_simulated_response, SCENARIOS

st.set_page_config(page_title="Responsible Prompting", page_icon="🚀")
st.title("🚀 Responsible Prompt Generation")
st.markdown("Get live feedback to fine-tune your prompts.")

selected_key = st.selectbox(
    "Choose a scenario:",
    options=list(SCENARIOS.keys()),
    format_func=lambda key: get_scenario(key).get("description")
)

if selected_key:
    current_scenario = get_scenario(selected_key)
    user_prompt = st.text_area("Write your prompt here:", height=100, key=f"prompt_{selected_key}")

    if st.button("Get AI Response & Feedback", type="primary"):
        if user_prompt:
            simulated_response = get_simulated_response(user_prompt, selected_key)
            feedback_list, quality_score = analyze_prompt_quality(user_prompt, current_scenario)

            st.subheader("Simulated AI Response:")
            st.info(simulated_response)

            st.subheader("Feedback on Your Prompt:")
            for item in feedback_list:
                st.success(f"✅ {item}") if "**Good!**" in item else st.warning(f"💡 {item}")
            
            st.progress(quality_score / 5.0)
            st.caption(f"Prompt Quality Score: {quality_score}/5")
        else:
            st.error("Please write a prompt first.")