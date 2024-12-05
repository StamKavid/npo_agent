# 🌟 NPO Audit Agent: Empowering Nonprofit Impact Analysis 

## Overview

The NPO Audit Agent is an advanced AI-powered tool designed to conduct comprehensive audits of nonprofit organizations by extracting, analyzing, and generating insights from their online presence. Leveraging state-of-the-art language models and intelligent graph-based workflows, this tool provides strategic recommendations to help nonprofits enhance their mission and effectiveness.

## 🎯 Project Purpose

In the complex landscape of nonprofit organizations, understanding and optimizing an organization's strategic alignment is crucial. The NPO Audit Agent automates the process of:
- Extracting content from organizational websites
- Analyzing mission statements
- Generating stakeholder perspectives
- Creating actionable recommendations
- Scoring potential organizational impact

## 🏗️ System Architecture

**[Architecture Diagram Placeholder]**

*Diagram Elements:*
- Content Extraction Node
- Mission Analysis Node
- Stakeholder Perspective Generation Node
- Recommendation Generation Node
- Audit Scoring Node

## 🛠️ Prerequisites

Before running the NPO Audit Agent, ensure you have:

- Python 3.9+
- pip package manager
- OpenAI API Key (for language model) - LM Studio
- Firecrawl API Key (for web scraping)
- LMStudio (Meta-Llama-3.1-8B-Instruct-GGUF model)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/npo-audit-agent.git
cd npo-audit-agent
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables
Create a `.env` file in the project root with the following:
```
OPENAI_API_KEY=your_openai_api_key
FIRECRAWL_API_KEY=your_firecrawl_api_key
LOCAL_LLM_BASE_URL=http://localhost:1234/v1  # Optional local LLM endpoint
LOGGING_LEVEL=INFO
```

## 🖥️ Running the NPO Audit Agent

### From Command Line
```bash
python -m src.run https://example-nonprofit.org
```

### From VS Code
1. Open the project in VS Code
2. Open the integrated terminal
3. Activate virtual environment
4. Run the script or use the Run and Debug panel

### From GitBash
```bash
source venv/bin/activate
python -m src.run https://example-nonprofit.org
```

## 📋 Configuration Options

- `url`: Nonprofit website or Facebook page URL
- `platform`: 'website' or 'facebook' (Facebook implementation pending)

## 🧠 How It Works

The NPO Audit Agent uses a LangGraph-based workflow:
1. **Content Extraction**: Scrapes website content
2. **Mission Analysis**: Examines organizational mission
3. **Stakeholder Perspectives**: Identifies key stakeholder viewpoints
4. **Recommendation Generation**: Creates strategic suggestions
5. **Audit Scoring**: Evaluates potential organizational impact

## 🔍 Advanced Usage

Customize the agent by modifying:
- `/src/config/settings.py` for configuration
- Individual node implementations in `/src/nodes/`

## 🛡️ Error Handling

The agent includes robust error management:
- `ContentExtractionError`
- `LLMAnalysisError`
- Comprehensive logging

## 🤝 Contributing

Contributions are welcome! Please see `CONTRIBUTING.md` for guidelines.

## 📄 License

This project is licensed under [LICENSE TYPE]. See `LICENSE` file for details.

## 💡 Future Roadmap
- Test with more powerful LLM
- Facebook page analysis
- Enhanced multi-platform support
- More granular stakeholder analysis
- Machine learning model for predictive recommendations

## 🚨 Disclaimer

This is an AI-assisted tool. Recommendations should be reviewed by human experts.

---