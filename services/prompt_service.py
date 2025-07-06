"""Prompt analysis service for educational scenarios."""

from typing import Dict, List, Tuple
from langchain_core.prompts import PromptTemplate

SCENARIOS = {
    "Explain Photosynthesis": {
        "description": "You need to explain photosynthesis to a 5th-grade student.",
        "keywords_for_good_prompt": ["simple", "easy", "explain", "5th grade", "10 year old", "example", "analogy"],
        "ideal_prompt_template": PromptTemplate.from_template(
            "Explain photosynthesis in a simple way for a {age_group} using an {analogy_type}. Keep it {brevity_level}."
        ),
        "simulated_responses": {
            "basic": "Photosynthesis is how plants make food using sunlight, water, and air.",
            "good_age_appropriate": "Imagine plants are like little chefs! They take sunlight, water, and air to make sugary food and give us oxygen.",
        }
    },
    "Arguments for School Uniforms": {
        "description": "You need to get arguments *for* implementing school uniforms.",
        "keywords_for_good_prompt": ["arguments for", "benefits", "advantages", "reasons to have"],
        "ideal_prompt_template": PromptTemplate.from_template(
            "List {num_arguments} arguments in favor of implementing school uniforms. Present them as {output_format}."
        ),
        "simulated_responses": {
            "basic": "School uniforms can promote equality.",
            "one_sided_strong": "School uniforms foster discipline, reduce distractions, and eliminate clothing-based disparities.",
        }
    },
}

def get_scenario(key: str) -> Dict:
    """Returns the data for a selected scenario."""
    return SCENARIOS.get(key, {})

def analyze_prompt_quality(user_prompt_text: str, scenario_data: Dict) -> Tuple[List[str], int]:
    """Analyzes the prompt and returns feedback and a score."""
    feedback = []
    score = 0
    prompt_lower = user_prompt_text.lower()
    
    if not user_prompt_text.strip():
        feedback.append("Your prompt is empty. Please write something!")
        return feedback, 0

    found_keywords = [kw for kw in scenario_data.get("keywords_for_good_prompt", []) if kw in prompt_lower]
    if found_keywords:
        feedback.append(f"**Good!** You've used relevant terms like: `{', '.join(found_keywords)}`.")
        score += 2
    else:
        feedback.append(f"Consider using terms like: **{', '.join(scenario_data.get('keywords_for_good_prompt', [])[:3])}**...")

    if len(user_prompt_text.split()) < 5:
        feedback.append("Your prompt is quite short. More detail can lead to better AI responses.")
    else:
        score += 1
    
    score = max(0, min(score, 5))
    return feedback, score

def get_simulated_response(prompt_text: str, scenario_key: str) -> str:
    """Generates a simulated AI response based on the prompt."""
    scenario = get_scenario(scenario_key)
    prompt_lower = prompt_text.lower()
    
    if ("simple" in prompt_lower or "5th grade" in prompt_lower) and "Photosynthesis" in scenario_key:
        return scenario.get("simulated_responses", {}).get("good_age_appropriate")
    if "arguments for" in prompt_lower and "Uniforms" in scenario_key:
        return scenario.get("simulated_responses", {}).get("one_sided_strong")
        
    return scenario.get("simulated_responses", {}).get("basic", "Thinking...")