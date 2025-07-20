"""Service for handling custom ethical AI checklists."""

from typing import Dict, List, Tuple
import google.generativeai as genai
import os
import streamlit as st
import json

class ChecklistService:
    """Manages loading and evaluating custom checklists."""

    def load_checklist_from_file(self, uploaded_file) -> List[str]:
        """
        Reads a .txt file and returns a list of guidelines.

        Args:
            uploaded_file: The file-like object from a Streamlit file uploader.

        Returns:
            A list of strings, where each string is a guideline.
        """
        if not uploaded_file:
            return []
        try:
            # Ensure the file pointer is at the beginning
            uploaded_file.seek(0)
            checklist = [line.strip() for line in uploaded_file.getvalue().decode("utf-8").splitlines() if line.strip()]
            return checklist
        except Exception as e:
            st.error(f"Error reading checklist file: {e}")
            return []

    def _call_gemini_for_checklist_evaluation(self, text_to_evaluate: str, custom_checklist: List[str]) -> Tuple[bool, str]:
        """
        Calls the Google Gemini 1.5 Flash API for custom checklist evaluation.

        Args:
            text_to_evaluate: The text to be analyzed.
            custom_checklist: A list of custom guidelines.

        Returns:
            A tuple containing a success boolean and the API response as a string.
        """
        gemini_api_key = getattr(st.secrets, 'GEMINI_API_TOKEN', os.getenv('GEMINI_API_TOKEN', ''))
        if not gemini_api_key:
            return (False, "Gemini API key not found. Please set 'GEMINI_API_TOKEN' in your environment or Streamlit secrets.")

        genai.configure(api_key=gemini_api_key)

        try:
            model = genai.GenerativeModel('gemini-1.5-flash')

            # FIX: Create the checklist string outside the f-string to avoid backslash error.
            checklist_str = "\n- ".join(custom_checklist)
            
            system_prompt = f"""You are an expert AI content safety evaluator. Your task is to analyze the user-provided text based on a custom checklist of guidelines.
                            The custom checklist is:
                            - {checklist_str}
                            Your response MUST be a valid JSON object.
                            The JSON object should have one key: "Custom Educator Checklist".
                            The value for this key should be a list of strings.
                            - If you find specific issues where the text violates a guideline from the checklist, each string in the list should describe the violation and which guideline it relates to.
                            - If you find no issues, the list should contain a single string: "No issues detected."
                            Do not include any text outside of the JSON object itself.
                            """
            messages = [
                {"role": "user", "parts": [system_prompt]},
                {"role": "model", "parts": ["Okay, I will analyze the text against the provided custom checklist and return a single JSON object with the results."]},
                {"role": "user", "parts": [text_to_evaluate]}
            ]

            response = model.generate_content(
                messages,
                generation_config=genai.types.GenerationConfig(
                    response_mime_type="application/json",
                    temperature=0.1,
                ),
            )

            if response.parts:
                return (True, response.parts[0].text)
            elif response.candidates:
                for candidate in response.candidates:
                    if candidate.content and candidate.content.parts:
                        return (True, candidate.content.parts[0].text)

            return (False, "No valid content found in Gemini API response.")
        except Exception as e:
            return (False, f"Error calling Gemini API for checklist evaluation: {e}")


    def evaluate_text_against_checklist(self, text_to_evaluate: str, custom_checklist: List[str]) -> Dict[str, List[str]]:
        """
        Evaluates text against a custom checklist using the Gemini API.
        Falls back to simple keyword matching if the API fails.

        Args:
            text_to_evaluate: The text to be analyzed.
            custom_checklist: The list of guidelines to check against.

        Returns:
            A dictionary containing the evaluation feedback.
        """
        if not custom_checklist:
            return {"Custom Educator Checklist": ["No checklist was provided for evaluation."]}

        is_successful, response_str = self._call_gemini_for_checklist_evaluation(text_to_evaluate, custom_checklist)

        if is_successful:
            try:
                feedback = json.loads(response_str)
                if "Custom Educator Checklist" not in feedback:
                    feedback = {"Custom Educator Checklist": ["The LLM evaluation did not return the expected result format."]}
                return feedback
            except json.JSONDecodeError:
                return {"API Error": [f"Failed to decode the API's JSON response: {response_str}"]}
        else:
            # Fallback to simple keyword matching if API fails
            print(f"Debug - Gemini checklist evaluation failed with error: {response_str}. Falling back to keyword matching.")
            text_lower = text_to_evaluate.lower()
            custom_issues = [f"Detected text that potentially matches custom checklist item: '{item}'." for item in custom_checklist if item.lower() in text_lower]
            if not custom_issues:
                custom_issues = ["No issues detected based on keyword matching (API fallback)."]
            return {"Custom Educator Checklist": custom_issues}
