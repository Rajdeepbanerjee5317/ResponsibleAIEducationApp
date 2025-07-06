"""Integration tests for Streamlit pages"""

import unittest
from unittest.mock import patch, Mock
import sys
import os

# Add the parent directory to the path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestStreamlitPages(unittest.TestCase):

    @patch('streamlit.set_page_config')
    @patch('streamlit.title')
    @patch('streamlit.markdown')
    @patch('streamlit.text_input')
    @patch('streamlit.button')
    @patch('streamlit.spinner')
    @patch('streamlit.subheader')
    @patch('streamlit.error')
    @patch('streamlit.warning')
    def test_personalized_qa_page_structure(self, mock_warning, mock_error, mock_subheader, 
                                          mock_spinner, mock_button, mock_text_input, 
                                          mock_markdown, mock_title, mock_config):
        """Test Personalized Q&A page structure"""
        mock_text_input.return_value = "photosynthesis"
        mock_button.return_value = True
        
        # Import and test the page
        with patch('services.evaluation_service.generate_safe_text') as mock_generate:
            mock_generate.return_value = (True, "Test response")
            import pages.Personalized_QA as pqa
            
            mock_config.assert_called()
            mock_title.assert_called()

    @patch('streamlit.set_page_config')
    @patch('streamlit.title')
    @patch('streamlit.markdown')
    @patch('streamlit.text_area')
    @patch('streamlit.button')
    def test_free_text_generation_page_structure(self, mock_button, mock_text_area, 
                                               mock_markdown, mock_title, mock_config):
        """Test Free Text Generation page structure"""
        mock_text_area.return_value = "test prompt"
        mock_button.return_value = False
        
        import pages.Free_Text_Generation as ftg
        
        mock_config.assert_called()
        mock_title.assert_called()

    @patch('streamlit.set_page_config')
    @patch('streamlit.title')
    @patch('streamlit.markdown')
    @patch('streamlit.text_area')
    @patch('streamlit.multiselect')
    @patch('streamlit.button')
    def test_evaluate_outputs_page_structure(self, mock_button, mock_multiselect, 
                                           mock_text_area, mock_markdown, mock_title, mock_config):
        """Test Evaluate Outputs page structure"""
        mock_text_area.return_value = "test text"
        mock_multiselect.return_value = ["Bias"]
        mock_button.return_value = False
        
        import pages.Evaluate_Outputs as eo
        
        mock_config.assert_called()
        mock_title.assert_called()

    @patch('streamlit.session_state', {'custom_checklist': []})
    @patch('streamlit.set_page_config')
    @patch('streamlit.title')
    @patch('streamlit.markdown')
    @patch('streamlit.subheader')
    @patch('streamlit.file_uploader')
    @patch('streamlit.text_area')
    @patch('streamlit.button')
    def test_ethical_checklist_page_structure(self, mock_button, mock_text_area, 
                                            mock_file_uploader, mock_subheader, 
                                            mock_markdown, mock_title, mock_config):
        """Test Ethical AI Checklist page structure"""
        mock_file_uploader.return_value = None
        mock_text_area.return_value = "test text"
        mock_button.return_value = False
        
        import pages.Ethical_AI_Checklist as eac
        
        mock_config.assert_called()
        mock_title.assert_called()

    @patch('streamlit.set_page_config')
    @patch('streamlit.title')
    @patch('streamlit.markdown')
    @patch('streamlit.selectbox')
    @patch('streamlit.text_area')
    @patch('streamlit.button')
    def test_responsible_prompting_page_structure(self, mock_button, mock_text_area, 
                                                mock_selectbox, mock_markdown, mock_title, mock_config):
        """Test Responsible Prompting page structure"""
        mock_selectbox.return_value = "Explain Photosynthesis"
        mock_text_area.return_value = "test prompt"
        mock_button.return_value = False
        
        import pages.Responsible_Prompting as rp
        
        mock_config.assert_called()
        mock_title.assert_called()


class TestMainApp(unittest.TestCase):

    @patch('streamlit.set_page_config')
    @patch('streamlit.title')
    @patch('streamlit.caption')
    @patch('streamlit.sidebar')
    @patch('streamlit.markdown')
    def test_main_app_structure(self, mock_markdown, mock_sidebar, mock_caption, mock_title, mock_config):
        """Test main app structure"""
        mock_sidebar.success = Mock()
        
        import streamlit_app
        
        mock_config.assert_called_with(
            page_title="Responsible Prompter",
            page_icon="🎓",
            layout="wide"
        )
        mock_title.assert_called()
        mock_caption.assert_called()


if __name__ == '__main__':
    unittest.main()