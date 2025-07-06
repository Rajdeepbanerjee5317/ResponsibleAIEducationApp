"""Unit tests for evaluation_service.py"""

import unittest
from unittest.mock import Mock
from services.evaluation_service import (
    generate_safe_text, evaluate_text, load_checklist_from_file,
    UNSAFE_KEYWORDS, DEFAULT_PRINCIPLES
)


class TestEvaluationService(unittest.TestCase):

    def test_generate_safe_text_unsafe_content(self):
        """Test that unsafe content is flagged"""
        is_safe, response = generate_safe_text("violence and hate")
        self.assertFalse(is_safe)
        self.assertIn("unable to generate", response)

    def test_generate_safe_text_photosynthesis(self):
        """Test photosynthesis response generation"""
        is_safe, response = generate_safe_text("explain photosynthesis")
        self.assertTrue(is_safe)
        self.assertIn("Photosynthesis", response)
        self.assertIn("Practice Question", response)

    def test_generate_safe_text_gravity(self):
        """Test gravity response generation"""
        is_safe, response = generate_safe_text("what is gravity")
        self.assertTrue(is_safe)
        self.assertIn("Gravity", response)
        self.assertIn("Practice Question", response)

    def test_generate_safe_text_generic(self):
        """Test generic safe response"""
        is_safe, response = generate_safe_text("safe topic")
        self.assertTrue(is_safe)
        self.assertIn("simulated safe AI response", response)

    def test_generate_safe_text_custom_guidelines(self):
        """Test custom guidelines filtering"""
        custom_guidelines = ["forbidden"]
        is_safe, response = generate_safe_text("forbidden topic", custom_guidelines)
        self.assertFalse(is_safe)
        self.assertIn("ethical checklist", response)

    def test_evaluate_text_bias_detection(self):
        """Test bias detection in text evaluation"""
        text = "he is a doctor and she is a nurse"
        feedback = evaluate_text(text, ["Bias"])
        self.assertIn("Bias", feedback)
        self.assertTrue(any("he is a doctor" in issue for issue in feedback["Bias"]))

    def test_evaluate_text_no_issues(self):
        """Test text with no issues"""
        text = "This is clean educational content"
        feedback = evaluate_text(text, ["Bias"])
        self.assertIn("No specific issues", feedback["Bias"][0])

    def test_evaluate_text_custom_checklist(self):
        """Test evaluation with custom checklist"""
        text = "inappropriate content"
        custom_checklist = ["inappropriate"]
        feedback = evaluate_text(text, [], custom_checklist)
        self.assertIn("Custom Educator Checklist", feedback)
        self.assertTrue(any("inappropriate" in issue for issue in feedback["Custom Educator Checklist"]))

    def test_load_checklist_from_file_valid(self):
        """Test loading valid checklist file"""
        mock_file = Mock()
        mock_file.getvalue.return_value.decode.return_value = "line1\nline2\n\nline3"
        result = load_checklist_from_file(mock_file)
        self.assertEqual(result, ["line1", "line2", "line3"])

    def test_load_checklist_from_file_none(self):
        """Test loading None file"""
        result = load_checklist_from_file(None)
        self.assertEqual(result, [])

    def test_load_checklist_from_file_exception(self):
        """Test loading file with exception"""
        mock_file = Mock()
        mock_file.getvalue.side_effect = Exception("File error")
        result = load_checklist_from_file(mock_file)
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()