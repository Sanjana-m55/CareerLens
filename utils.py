import os
import google.generativeai as genai
from PyPDF2 import PdfReader
import docx2txt
import tempfile

def extract_text_from_file(file_path):
    """Extract text from various file types"""
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension == '.docx':
        return extract_text_from_docx(file_path)
    elif file_extension == '.txt':
        return extract_text_from_txt(file_path)
    else:
        return "Unsupported file format"

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
    except Exception as e:
        text = f"Error extracting text from PDF: {str(e)}"
    return text

def extract_text_from_docx(docx_path):
    """Extract text from DOCX file"""
    try:
        text = docx2txt.process(docx_path)
        return text
    except Exception as e:
        return f"Error extracting text from DOCX: {str(e)}"

def extract_text_from_txt(txt_path):
    """Extract text from TXT file"""
    try:
        with open(txt_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error extracting text from TXT: {str(e)}"

def get_gemini_response(prompt):
    """Get response from Gemini API"""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "Error: Google API key not configured. Please set the GOOGLE_API_KEY environment variable."
    
    try:
        # Configure the API with the current key
        genai.configure(api_key=api_key)
        
        # Using the correct model name (as of April 2025)
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: Google API key not configured properly. Error details: {str(e)}"

def process_resume(resume_text):
    """Process resume text with Gemini"""
    prompt = f"""
    Analyze the following resume and provide a detailed breakdown:
    
    Resume:
    {resume_text}
    
    Please provide the following information in a well-structured format using Markdown:
    
    1. **Basic Information**: Extract name, contact details, and location
    2. **Professional Summary**: Summarize the candidate's profile in 2-3 sentences
    3. **Skills**: List the technical and soft skills found in the resume
    4. **Experience**: Summarize work experience, including company names, positions, and duration
    5. **Education**: List educational qualifications with institutions and years
    6. **Certifications**: List any certifications mentioned
    7. **Achievements**: Highlight key achievements
    8. **Strengths**: What are the candidate's main strengths based on the resume?
    9. **Areas for Improvement**: Suggestions for improving the resume
    10. **ATS Compatibility Score**: Rate how well the resume would perform with Applicant Tracking Systems on a scale of 1-10 and explain why
    
    Format your response using Markdown with proper headings, bullet points, and sections.
    """
    
    return get_gemini_response(prompt)

def ask_question_about_resume(resume_text, question):
    """Ask a specific question about the resume"""
    prompt = f"""
    I have the following resume:
    
    {resume_text}
    
    Based on the content of this resume, please answer the following question:
    {question}
    
    Provide a detailed and helpful response based only on the information available in the resume. If the resume doesn't contain information relevant to the question, please mention that.
    """
    
    return get_gemini_response(prompt)