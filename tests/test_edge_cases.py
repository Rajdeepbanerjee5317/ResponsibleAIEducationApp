"""Edge case tests for the application"""

import unittest
from services.evaluation_service import generate_safe_text, evaluate_text
from services.prompt_service import analyze_prompt_quality, get_simulated_response


class TestEdgeCases(unittest.TestCase):

    def test_empty_inputs(self):
        """Test handling of empty inputs"""
        # Empty text generation
        is_safe, response = generate_safe_text("")
        self.assertTrue(is_safe)
        
        # Empty text evaluation
        feedback = evaluate_text("", ["Bias"])
        self.assertIn("Bias", feedback)
        
        # Empty prompt analysis
        feedback, score = analyze_prompt_quality("", {"keywords_for_good_prompt": []})
        self.assertEqual(score, 0)

    def test_whitespace_only_inputs(self):
        """Test handling of whitespace-only inputs"""
        is_safe, response = generate_safe_text("   \n\t   ")
        self.assertTrue(is_safe)
        
        feedback, score = analyze_prompt_quality("   ", {"keywords_for_good_prompt": []})
        self.assertEqual(score, 0)

    def test_very_long_inputs(self):
        """Test handling of very long inputs"""
        long_text = "word " * 1000
        is_safe, response = generate_safe_text(long_text)
        self.assertTrue(is_safe)
        
        feedback = evaluate_text(long_text, ["Bias"])
        self.assertIn("Bias", feedback)

    def test_special_characters(self):
        """Test handling of special characters"""
        special_text = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        is_safe, response = generate_safe_text(special_text)
        self.assertTrue(is_safe)
        
        feedback = evaluate_text(special_text, ["Bias"])
        self.assertIn("Bias", feedback)

    def test_unicode_characters(self):
        """Test handling of unicode characters"""
        unicode_text = "Hello 世界 🌍 café naïve résumé"
        is_safe, response = generate_safe_text(unicode_text)
        self.assertTrue(is_safe)

    def test_case_sensitivity(self):
        """Test case sensitivity in keyword detection"""
        # Test uppercase unsafe keywords
        is_safe, response = generate_safe_text("VIOLENCE and HATE")
        self.assertFalse(is_safe)
        
        # Test mixed case
        is_safe, response = generate_safe_text("Violence And Hate")
        self.assertFalse(is_safe)

    def test_partial_keyword_matches(self):
        """Test that partial keyword matches don't trigger false positives"""
        # "violent" contains "violence" but shouldn't trigger
        is_safe, response = generate_safe_text("nonviolent protest")
        self.assertTrue(is_safe)

    def test_multiple_unsafe_keywords(self):
        """Test text with multiple unsafe keywords"""
        is_safe, response = generate_safe_text("violence hate illegal explicit")
        self.assertFalse(is_safe)

    def test_boundary_conditions_prompt_analysis(self):
        """Test boundary conditions for prompt analysis"""
        scenario_data = {"keywords_for_good_prompt": ["test"]}
        
        # Exactly 5 words (boundary)
        feedback, score = analyze_prompt_quality("one two three four five", scenario_data)
        self.assertGreaterEqual(score, 0)
        
        # 4 words (short)
        feedback, score = analyze_prompt_quality("one two three four", scenario_data)
        self.assertTrue(any("quite short" in f for f in feedback))

    def test_invalid_scenario_keys(self):
        """Test handling of invalid scenario keys"""
        response = get_simulated_response("test", "NonExistentScenario")
        self.assertEqual(response, "Thinking...")

    def test_none_inputs(self):
        """Test handling of None inputs where applicable"""
        # Custom guidelines as None
        is_safe, response = generate_safe_text("test", None)
        self.assertTrue(is_safe)


if __name__ == '__main__':
    unittest.main()