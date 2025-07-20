"""Evaluation service for responsible AI content analysis."""

import os
from typing import Dict, List, Optional, Tuple
import streamlit as st
import requests
#from huggingface_hub import InferenceClient
import google.generativeai as genai # Import the Google Generative AI library
import json

# Load environment variables from .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Constants
UNSAFE_KEYWORDS = ["violence", "hate", "self-harm", "illegal", "explicit"]

DEFAULT_PRINCIPLES = {
    "Bias": ["gender bias", "racial bias", "stereotypes", "he is a doctor", "she is a nurse"],
    "Misinformation": ["false claims", "unverified facts", "conspiracy"],
    "Harmful Content": UNSAFE_KEYWORDS,
    "Lack of Clarity": ["vague", "unclear", "ambiguous"]
}

def _call_gemini_api(prompt: str) -> Tuple[bool, str]:
    """Call Google Gemini 1.5 Flash API."""
    # Retrieve Gemini API key from environment variables or Streamlit secrets
    gemini_api_key = getattr(st.secrets, 'GEMINI_API_TOKEN', os.getenv('GEMINI_API_TOKEN', ''))

    if not gemini_api_key:
        return (False, "Gemini API key not found. Please set 'GEMINI_API_TOKEN' in your environment or Streamlit secrets.")

    # Configure the Google Generative AI library with your API key
    genai.configure(api_key=gemini_api_key)

    try:
        # Initialize the GenerativeModel for Gemini 1.5 Flash
        model = genai.GenerativeModel('gemini-1.5-flash-8b')#.gemini-1.5-flash

        system_prompt = "You are a helpful educational assistant. Provide clear, accurate explanations suitable for students."
        user_prompt = f"Explain {prompt} in simple terms with an example and include a practice question at the end."

        # Construct the content for the Gemini API call
        # Gemini API typically takes messages in a specific role-based format
        messages = [
            {"role": "user", "parts": [system_prompt]}, # System prompt can be part of the user's initial message
            {"role": "model", "parts": ["Okay, I understand. I will provide clear, accurate explanations suitable for students, including an example and a practice question."]}, # Example model response to establish role
            {"role": "user", "parts": [user_prompt]}
        ]

        # Generate content using the Gemini model
        response = model.generate_content(
            messages,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=256,  # Use max_output_tokens for Gemini
                temperature=0.7,
                top_p=0.9,
            ),
        )
        print(f"Debug - Gemini API response: {response}")
        # Extract the text from the response
        if response.parts:
            return (True, response.parts[0].text)
        elif response.candidates:
            # Fallback for older response structures or different candidate access
            for candidate in response.candidates:
                if candidate.content and candidate.content.parts:
                    return (True, candidate.content.parts[0].text)
        return (False, "No valid content found in Gemini API response.")

    except Exception as e:
        return (False, f"Error calling Gemini API: {e}")

def _call_mistral_api(prompt: str) -> Tuple[bool, str]:
    """Call Mistral via Hugging Face API as a fallback."""
    api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
    token = getattr(st.secrets, 'HUGGINGFACE_API_TOKEN', os.getenv('HUGGINGFACE_API_TOKEN', ''))
    
    if not token:
        return (False, "Hugging Face API token not found.")

    headers = {"Authorization": f"Bearer {token}"}
    
    safe_prompt = f"""<s>[INST] You are an educational AI assistant. Provide a safe, accurate explanation about: {prompt}
Guidelines:
- Keep explanations clear and educational
- Include a practice question at the end
- Use simple language for students [/INST]"""
    
    payload = {
        "inputs": safe_prompt,
        "parameters": {"max_new_tokens": 250, "temperature": 0.7}
    }

    try:
        print("Debug - Calling Mistral API...")
        response = requests.post(api_url, headers=headers, json=payload, timeout=20)
        print(f"Debug - Mistral API Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0 and 'generated_text' in result[0]:
                generated_text = result[0]['generated_text'].replace(safe_prompt, '').strip()
                return (True, generated_text)
        elif response.status_code == 503:
            return (False, "Mistral model is loading, please try again shortly.")
        else:
            print(f"Debug - Mistral API Error: {response.text}")
            return (False, f"Mistral API error ({response.status_code})")

    except requests.exceptions.RequestException as e:
        print(f"Debug - Mistral API request exception: {str(e)}")
        return (False, f"Mistral API connection error: {e}")

    return (False, "No valid response from Mistral.")

def _call_llm_safely(prompt: str) -> Tuple[bool, str]:
    """Call Gemini with fallback to Mistral."""
    # 1. Try Llama 2 API first
    is_successful, response = _call_gemini_api(prompt)
    if is_successful:
        return (True, response)
    
    # 2. If Llama fails, fall back to Mistral API
    print("Debug - Gemini API failed or was unavailable. Falling back to Mistral API.")
    is_successful, response = _call_mistral_api(prompt)
    if is_successful:
        return (True, response)
    
    # 3. If both fail, return the last error message
    print("Debug - All API fallbacks failed.")
    return (False, response) # Return the final error from Mistral

def generate_safe_text(prompt: str, custom_guidelines: Optional[List[str]] = None) -> Tuple[bool, str]:
    """
    Generates safe educational content using LLMs with fallbacks.
    Returns a tuple: (is_safe, response_text).
    """
    prompt_lower = prompt.lower()
    
    # Check for unsafe content before calling any API
    if any(keyword in prompt_lower for keyword in UNSAFE_KEYWORDS):
        return (False, "I am unable to generate a response to this prompt as it may violate safety guidelines.")
    
    # Check against custom guidelines
    if custom_guidelines and any(keyword.lower() in prompt_lower for keyword in custom_guidelines):
        return (False, "I am unable to generate a response as it conflicts with the provided ethical checklist.")
    
    # Try LLM with fallback logic
    is_successful, llm_response = _call_llm_safely(prompt)
    if is_successful:
        return (True, llm_response)
            
    # Fallback to predefined responses if all APIs fail
    print("Debug - All LLM services failed. Using predefined fallback responses.")
    topic_responses = {
        "photosynthesis": "**Photosynthesis Explained:**\n\nPhotosynthesis is the process plants use to convert light energy into chemical energy...\n\n**Practice Question:** What are the three main 'ingredients' a plant needs for photosynthesis?",
        "gravity": "**Understanding Gravity:**\n\nGravity is the invisible force that pulls objects toward each other...\n\n**Practice Question:** Why do you fall back to the ground when you jump?",
        "machine learning": "**Machine Learning Explained:**\n\nMachine learning is a type of artificial intelligence where computers learn patterns from data to make predictions or decisions without being explicitly programmed for each task.\n\n**Practice Question:** Can you think of an app on your phone that might use machine learning?",
    }
    
    for topic, response in topic_responses.items():
        if topic in prompt_lower:
            return (True, response)
    
    # Generic fallback if no specific topic matches
    return (False, f"LLM services are currently unavailable. Unable to generate a response for '{prompt.title()}'.")

def generate_safe_free_text(prompt: str, custom_guidelines: Optional[List[str]] = None) -> Tuple[bool, str]:
    """
    Generates safe educational content using LLMs with fallbacks.
    Returns a tuple: (is_safe, response_text).
    """
    is_safe, response = generate_safe_text(prompt, custom_guidelines)
    
    if is_safe:
        print(f"Debug evaluate text: {response}")
        evaluation = evaluate_text(response, ["Bias", "Harmful Content", "Misinformation"])
        if any(issues for issues in evaluation.values() if issues):
            return (False, "Generated content flagged for safety review")
        return (True, response)  # Return the safe response
    else:
        return (False, response)  # Return the error message

def _call_gemini_for_evaluation(text_to_evaluate: str, principles_to_check: List[str]) -> Tuple[bool, str]:
    """Call Google Gemini 1.5 Flash API for content evaluation."""
    gemini_api_key = getattr(st.secrets, 'GEMINI_API_TOKEN', os.getenv('GEMINI_API_TOKEN', ''))
    if not gemini_api_key:
        return (False, "Gemini API key not found.")

    genai.configure(api_key=gemini_api_key)

    try:
        model = genai.GenerativeModel('gemini-1.5-flash-8b')

        system_prompt = f"""You are an expert AI content safety evaluator. Your task is to analyze the user-provided text based on a specific list of principles.
            The principles to check are: {", ".join(principles_to_check)}.
            Your response MUST be a valid JSON object.
            The JSON object should have a key for each principle you were asked to evaluate.
            The value for each key should be a list of strings.
            - If you find specific issues related to a principle, each string in the list should describe one issue found.
            - If you find no issues for a principle, the list should contain a single string: "No issues detected."
            Do not include any text outside of the JSON object itself.
            """
        messages = [
            {"role": "user", "parts": [system_prompt]},
            {"role": "model", "parts": [f"Okay, I will analyze the text against the following principles: {', '.join(principles_to_check)} and return a single JSON object with the results."]},
            {"role": "user", "parts": [text_to_evaluate]}
        ]
        
        response = model.generate_content(
            messages,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=1024,
                temperature=0.1,
            ),
        )
        print(f"Debug - Gemini API response for evaluate test: {response}.")
        if response.parts:
            raw_text = response.parts[0].text
            # Clean up the response to ensure it's valid JSON
            json_text = raw_text.strip().lstrip("```json").rstrip("```")
            return (True, json_text)
        elif response.candidates:
            for candidate in response.candidates:
                if candidate.content and candidate.content.parts:
                    raw_text = candidate.content.parts[0].text
                    json_text = raw_text.strip().lstrip("```json").rstrip("```")
                    return (True, json_text)

        return (False, "No valid content found in Gemini API response.")
    except Exception as e:
        return (False, f"Error calling Gemini API for evaluation: {e}")

def _call_llm_for_evaluation_safely(text_to_evaluate: str, principles_to_check: List[str]) -> Tuple[bool, str]:
    """
    Call Gemini for evaluation with a structure that allows for future fallbacks.
    """
    is_successful, response = _call_gemini_for_evaluation(text_to_evaluate, principles_to_check)
    if is_successful:
        return (True, response)
    
    # Placeholder for a future fallback to another evaluation model
    print("Debug - Gemini evaluation API failed. No fallback available.")
    return (False, response)


def evaluate_text(text_to_evaluate: str, principles_to_check: List[str], custom_checklist: Optional[List[str]] = None) -> Dict[str, List[str]]:
    """
    Evaluates text against responsible AI principles using the Gemini API.
    Returns a dictionary with feedback.
    """
    feedback = {}

    # Step 1: Call LLM safely to get evaluation based on standard principles
    if principles_to_check:
        is_successful, response_str = _call_llm_for_evaluation_safely(text_to_evaluate, principles_to_check)
        if is_successful:
            try:
                # The response from the LLM is expected to be a JSON string
                feedback = json.loads(response_str)
                # Ensure all requested principles are in the feedback dict, even if the LLM missed one
                for principle in principles_to_check:
                    if principle not in feedback:
                        feedback[principle] = ["The LLM evaluation did not return a result for this principle."]
            except json.JSONDecodeError:
                feedback = {"API Error": [f"Failed to decode the API's JSON response: {response_str}"]}
        else:
            # If the API call itself fails, return the error message
            feedback = {"API Error": [response_str]}

    # Step 2: Evaluate against the local custom educator checklist
    if custom_checklist:
        text_lower = text_to_evaluate.lower()
        custom_issues = [f"Detected text that matches custom checklist item: '{item}'." for item in custom_checklist if item.lower() in text_lower]
        if custom_issues:
            # Add to feedback dictionary, creating the key if it doesn't exist
            if "Custom Educator Checklist" in feedback:
                feedback["Custom Educator Checklist"].extend(custom_issues)
            else:
                feedback["Custom Educator Checklist"] = custom_issues
            
    return feedback

def load_checklist_from_file(uploaded_file) -> List[str]:
    """Reads a .txt file and returns a list of guidelines."""
    if not uploaded_file:
        return []
    try:
        checklist = [line.strip() for line in uploaded_file.getvalue().decode("utf-8").splitlines() if line.strip()]
        return checklist
    except Exception:
        return []
