# CareerLens: Your Resume's Secret Weapon

[![Watch Demo Video](https://img.shields.io/badge/Watch%20Demo-YouTube-red?style=for-the-badge&logo=youtube)](https://www.youtube.com/watch?v=uJHp1qOUCXw)

![CareerLens Logo](https://png.pngtree.com/png-vector/20220708/ourmid/pngtree-analyzing-data-png-image_5744358.png)

## 📖 Overview

CareerLens is an AI-powered resume analysis tool built with Streamlit and Google's Gemini 1.5 Pro model. It helps users extract valuable insights from resumes, analyze content, and receive detailed feedback through an intuitive chat interface.

## ✨ Features

- **Resume Text Extraction**: Support for PDF, DOCX, and TXT files
- **AI-Powered Analysis**: Comprehensive breakdown of resume content
- **Interactive Chat**: Ask specific questions about the uploaded resume
- **ATS Compatibility Scoring**: Evaluate resume performance with Applicant Tracking Systems
- **Resume Statistics**: Word count and character count tracking
- **Clean User Interface**: Modern, intuitive UI with responsive design

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/Sanjana-m55/careerlens.git
cd careerlens

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 📋 Requirements

```
streamlit==1.27.2
google-generativeai==0.3.1
python-dotenv==1.0.0
PyPDF2==3.0.1
docx2txt==0.8
python-pptx==0.6.21
```

## 🔑 API Key Setup

1. Create a `.env` file in the project root directory
2. Add your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```
3. Alternatively, you can input your API key directly in the Streamlit app sidebar

## 🏃‍♂️ Running the App

```bash
streamlit run app.py
```

## 📱 Usage

1. **Input API Key**: Enter your Google Gemini API key in the sidebar
2. **Upload Resume**: Choose a PDF, DOCX, or TXT file
3. **View Analysis**: Review comprehensive breakdown of resume content
4. **Chat with AI**: Ask specific questions about the resume
5. **Get Improvement Tips**: Receive suggestions to enhance resume quality

## 🔍 Analysis Features

- Basic Information Extraction
- Professional Summary Generation
- Skills Identification
- Experience Summary
- Education & Certification Listing
- Achievement Highlights
- Strength Assessment
- Areas for Improvement
- ATS Compatibility Scoring

## 🔄 Project Structure

```
careerlens/
├── app.py                 # Main Streamlit application
├── utils.py               # Utility functions for text extraction and AI processing
├── .env                   # Environment variables (API keys)
├── requirements.txt       # Dependencies
├── README.md              # Project documentation
└── assets/                # Images and static files
```

## 📊 Screenshots

| Resume Analysis | Chat Interface |
|:---------------:|:--------------:|
| ![Analysis](https://png.pngtree.com/png-vector/20220708/ourmid/pngtree-analyzing-data-png-image_5744358.png) | ![Chat](https://blog.qburst.com/wp-content/uploads/2020/09/Conversational-AI-Chatbot-Architecture-Overview.png) |

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Google Gemini](https://ai.google.dev/) for providing the AI model
- [Streamlit](https://streamlit.io/) for the web application framework
