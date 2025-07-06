# AI Prompt Quality Analyzer

A Streamlit application that helps users learn to write better AI prompts by analyzing prompt quality across different educational scenarios.

## Features

- **Multiple Scenarios**: Practice with different educational topics
- **Real-time Analysis**: Get instant feedback on your prompts
- **Simulated Responses**: See how AI might respond to your prompts
- **Educational Tips**: Learn best practices for prompt writing

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
streamlit run app.py
```

## Deployment to Streamlit Cloud

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select this repository
5. Set the main file path to `app.py`
6. Deploy!

## Project Structure

```
streamlit_app/
├── app.py                 # Main Streamlit application
├── backend/
│   └── prompt_analyzer.py # Backend logic for prompt analysis
├── requirements.txt       # Python dependencies
└── README.md             # This file
```