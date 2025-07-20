# Responsible AI Education App

A Streamlit application that helps users learn to write better AI prompts and evaluate AI-generated content through multiple educational tools.

## Features

- **Free Text Generation**: Create content with AI safety guardrails
- **Personalized Q&A**: Get educational explanations with practice questions
- **Responsible Prompting**: Learn to write better prompts with real-time feedback
- **Evaluate Outputs**: Check content against responsible AI principles
- **Ethical AI Checklist**: Create custom guidelines for content evaluation

## API Integration

The app integrates with multiple AI models:
- **Google Gemini API**: For content generation and evaluation
- **Hugging Face API**: For fallback content generation

## Local Development

1. Set up API keys in `.streamlit/secrets.toml`:
```toml
HUGGINGFACE_API_TOKEN = "your_token_here"
GEMINI_API_TOKEN = "your_token_here"
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run streamlit_app.py
```

## Deployment to Streamlit Cloud

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select this repository
5. Set the main file path to `streamlit_app.py`
6. Add your API keys in the Streamlit Cloud secrets management
7. Deploy!

## Project Structure

```
ResponsibleAIEducationApp/
├── streamlit_app.py       # Main Streamlit application
├── pages/                 # Streamlit pages for different features
│   ├── Free_Text_Generation.py
│   ├── Personalized_Q&A.py
│   ├── Responsible_Prompting.py
│   ├── Evaluate_Outputs.py
│   └── Ethical_AI_Checklist.py
├── services/              # Backend services
│   ├── evaluation_service.py
│   ├── prompt_service.py
│   └── custom_checklist_service.py
├── .streamlit/            # Streamlit configuration
│   ├── config.toml
│   └── style.css
├── tests/                 # Test files
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Customization

You can customize the app by:
- Adding new scenarios in `services/prompt_service.py`
- Modifying evaluation principles in `services/evaluation_service.py`
- Creating custom checklists through the Ethical AI Checklist page