"""Unit tests for constants and data structures"""

import unittest
from services.evaluation_service import UNSAFE_KEYWORDS, DEFAULT_PRINCIPLES
from services.prompt_service import SCENARIOS


class TestConstants(unittest.TestCase):

    def test_unsafe_keywords_not_empty(self):
        """Test that unsafe keywords list is not empty"""
        self.assertGreater(len(UNSAFE_KEYWORDS), 0)
        self.assertIn("violence", UNSAFE_KEYWORDS)
        self.assertIn("hate", UNSAFE_KEYWORDS)

    def test_default_principles_structure(self):
        """Test default principles structure"""
        self.assertIn("Bias", DEFAULT_PRINCIPLES)
        self.assertIn("Misinformation", DEFAULT_PRINCIPLES)
        self.assertIn("Harmful Content", DEFAULT_PRINCIPLES)
        self.assertIn("Lack of Clarity", DEFAULT_PRINCIPLES)
        
        for principle, keywords in DEFAULT_PRINCIPLES.items():
            self.assertIsInstance(keywords, list)
            self.assertGreater(len(keywords), 0)

    def test_scenarios_completeness(self):
        """Test that all scenarios have required fields"""
        required_fields = ["description", "keywords_for_good_prompt", "simulated_responses"]
        
        for scenario_name, scenario_data in SCENARIOS.items():
            for field in required_fields:
                self.assertIn(field, scenario_data, f"Missing {field} in {scenario_name}")
            
            self.assertIsInstance(scenario_data["keywords_for_good_prompt"], list)
            self.assertIsInstance(scenario_data["simulated_responses"], dict)

    def test_scenarios_content(self):
        """Test specific scenario content"""
        photosynthesis = SCENARIOS["Explain Photosynthesis"]
        self.assertIn("5th-grade", photosynthesis["description"])
        self.assertIn("simple", photosynthesis["keywords_for_good_prompt"])
        
        uniforms = SCENARIOS["Arguments for School Uniforms"]
        self.assertIn("arguments for", uniforms["keywords_for_good_prompt"])


if __name__ == '__main__':
    unittest.main()