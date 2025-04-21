import streamlit as st
import os
from dotenv import load_dotenv
import tempfile
from utils import extract_text_from_file, get_gemini_response, process_resume, ask_question_about_resume

# Load the environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="CareerLens: Your Resume's Secret Weapon",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better appearance
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4a90e2;
        text-align: center;
        margin-bottom: 20px;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #333;
        margin-bottom: 10px;
    }
    .stat-box {
        background-color: #f5f5f5;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    .navbar {
        background-color: #333;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .navbar a {
        color: white;
        margin-right: 15px;
        text-decoration: none;
        font-weight: bold;
    }
    .navbar a:hover {
        color: #4a90e2;
    }
    .result-section {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 5px;
        margin-top: 20px;
    }
    .chat-container {
        margin-top: 20px;
        padding: 15px;
        border-radius: 5px;
        background-color: #f0f8ff;
    }
    .chat-input {
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 10px;
    }
    .stButton>button {
        background-color: #4a90e2;
        color: white;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #3a7bc8;
    }
    footer {
        visibility: hidden;
    }
    .viewerBadge_container__1QSob {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# App logo
def get_app_logo():
    return """
    <svg width="80" height="80" viewBox="0 0 80 80" fill="none" xmlns="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTf4wFAnOICVitJU0Ku-4uu1g5jUD_Ko96iwg&svg">
        <rect width="80" height="80" rx="10" fill="#4a90e2"/>
        <path d="M20 20H60V30H20V20Z" fill="white"/>
        <path d="M20 35H60V40H20V35Z" fill="white"/>
        <path d="M20 45H40V50H20V45Z" fill="white"/>
        <path d="M20 55H60V60H20V55Z" fill="white"/>
    </svg>
    """

# Initialize session state
if 'resume_text' not in st.session_state:
    st.session_state['resume_text'] = ""
if 'resume_analysis' not in st.session_state:
    st.session_state['resume_analysis'] = None
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "upload"
if 'api_key' not in st.session_state:
    st.session_state['api_key'] = os.getenv("GOOGLE_API_KEY", "")

# Sidebar
with st.sidebar:
    st.markdown(f'<div style="text-align: center;">{get_app_logo()}</div>', unsafe_allow_html=True)
    st.title("CareerLens: Your Resume's Secret Weapon")
    
    # API Key input
    api_key = st.text_input("Google API Key", value=st.session_state['api_key'], type="password", help="Enter your Google Gemini API key")
    if api_key != st.session_state['api_key']:
        st.session_state['api_key'] = api_key
        os.environ["GOOGLE_API_KEY"] = api_key
    
    st.divider()
    
    # Navigation in sidebar
    st.subheader("Navigation")
    nav_selection = st.radio(
        label="Select a page",
        options=["Upload Resume", "Chat with AI", "About"], 
        index=["upload", "chat", "about"].index(st.session_state['current_page']),
        label_visibility="collapsed"
    )
    
    if nav_selection == "Upload Resume":
        st.session_state['current_page'] = "upload"
    elif nav_selection == "Chat with AI":
        st.session_state['current_page'] = "chat"
    else:
        st.session_state['current_page'] = "about"
    
    st.divider()
    
    # Stats and info
    if st.session_state['resume_text']:
        st.subheader("Resume Stats")
        st.write(f"**Word Count:** {len(st.session_state['resume_text'].split())}")
        st.write(f"**Character Count:** {len(st.session_state['resume_text'])}")
    
    st.divider()
    
    # Reset button
    if st.button("Reset Analysis"):
        st.session_state['resume_text'] = ""
        st.session_state['resume_analysis'] = None
        st.session_state['chat_history'] = []
        st.rerun()  # Updated from experimental_rerun()

# Display pages based on navigation
if st.session_state['current_page'] == "upload":
    # Upload Resume Page
    st.markdown("<h1 class='main-header'>Resume Analyzer</h1>", unsafe_allow_html=True)
    
    st.markdown("<h2 class='sub-header'>Upload your resume for AI analysis</h2>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose a resume file", type=["pdf", "docx", "txt"], help="Supported formats: PDF, DOCX, TXT")
    
    if uploaded_file is not None:
        if not st.session_state['api_key']:
            st.error("Please enter your Google API key in the sidebar before analyzing a resume.")
        else:
            with st.spinner("Analyzing your resume..."):
                # Save the uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name
                
                # Extract text from the resume
                resume_text = extract_text_from_file(tmp_file_path)
                st.session_state['resume_text'] = resume_text
                
                # Process the resume with Gemini
                analysis = process_resume(resume_text)
                st.session_state['resume_analysis'] = analysis
                
                # Remove the temporary file
                os.unlink(tmp_file_path)
            
            # Display the analysis results
            if st.session_state['resume_analysis']:
                st.markdown("<div class='result-section'>", unsafe_allow_html=True)
                
                st.markdown("<h2 class='sub-header'>Resume Analysis Results</h2>", unsafe_allow_html=True)
                
                # Display the resume text and analysis
                with st.expander("View Resume Text", expanded=False):
                    st.text_area("Extracted Text", st.session_state['resume_text'], height=200, label_visibility="collapsed")
                
                # Display the analysis
                if "Error:" in st.session_state['resume_analysis']:
                    st.error(st.session_state['resume_analysis'])
                else:
                    st.markdown(st.session_state['resume_analysis'], unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Button to chat about the resume
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if st.button("Ask questions about this resume"):
                        st.session_state['current_page'] = "chat"
                        st.rerun() 

elif st.session_state['current_page'] == "chat":
    # Chat with AI Page
    st.markdown("<h1 class='main-header'>Chat with AI about the Resume</h1>", unsafe_allow_html=True)
    
    if not st.session_state['resume_text']:
        st.warning("Please upload a resume first before chatting!")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Go to Upload Page"):
                st.session_state['current_page'] = "upload"
                st.rerun()  
    elif not st.session_state['api_key']:
        st.error("Please enter your Google API key in the sidebar before chatting.")
    else:
        # Display chat history
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        
        for message in st.session_state['chat_history']:
            role = message["role"]
            content = message["content"]
            
            if role == "user":
                st.markdown(f"<div style='background-color: #e6f7ff; padding: 10px; border-radius: 5px; margin-bottom: 10px;'><strong>You:</strong> {content}</div>", unsafe_allow_html=True)
            else:  # AI
                st.markdown(f"<div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin-bottom: 10px;'><strong>AI:</strong> {content}</div>", unsafe_allow_html=True)
        
        # Chat input
        user_question = st.text_input("Ask a question about the resume:", key="chat_input", placeholder="e.g., What are the key skills in this resume?")
        
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            if st.button("Send"):
                if user_question:
                    # Add user message to chat history
                    st.session_state['chat_history'].append({"role": "user", "content": user_question})
                    
                    # Get AI response
                    with st.spinner("AI is thinking..."):
                        ai_response = ask_question_about_resume(st.session_state['resume_text'], user_question)
                    
                    # Add AI response to chat history
                    st.session_state['chat_history'].append({"role": "ai", "content": ai_response})
                    
                    # Rerun to update the chat display
                    st.rerun()  # Updated from experimental_rerun()
        
        with col2:
            if st.button("Clear Chat"):
                st.session_state['chat_history'] = []
                st.rerun()  # Updated from experimental_rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Sample questions for guidance
        with st.expander("Sample Questions to Ask"):
            st.markdown("""
            - What are the key skills in this resume?
            - How many years of experience does this person have?
            - What are the educational qualifications in this resume?
            - What are the main achievements in this resume?
            - Can you summarize this resume in a few sentences?
            - Is this resume well-optimized for job applications?
            - What improvements could be made to this resume?
            """)

else:  # About page
    st.markdown("<h1 class='main-header'>About CareerLens</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    ## What is CareerLens?
    
    CareerLens is an AI-powered tool that helps you analyze resumes and extract valuable insights. It uses Google's Gemini model to provide intelligent analysis and allows you to chat with the AI about the resume.
    
    ## Features
    
    - **Resume Analysis**: Upload your resume (PDF, DOCX, or TXT) and get an AI-powered analysis.
    - **Information Extraction**: Automatically extract key information like skills, experience, education, etc.
    - **Chat Interface**: Ask questions about the resume and get intelligent answers.
    
    ## How to Use
    
    1. **Setup API Key**: Enter your Google Gemini API key in the sidebar.
    2. **Upload Resume**: Go to the "Upload Resume" page and upload your resume file.
    3. **View Analysis**: After uploading, you'll see the analysis results.
    4. **Chat with AI**: Navigate to the "Chat with AI" page to ask questions about the resume.
    
    ## Technology Stack
    
    - **Streamlit**: For the web interface
    - **Google Gemini**: For AI-powered analysis and chat
    - **Python**: For backend processing
    
    ## Privacy
    
    Your resume data is processed securely and is not stored permanently. All processing happens on-the-fly.
    """)
    
    # Add sample resume screenshots with placeholders
    st.subheader("Sample Screenshots")
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("https://png.pngtree.com/png-vector/20220708/ourmid/pngtree-analyzing-data-png-image_5744358.png?text=Resume+Analysis", caption="Resume Analysis")
    with col2:
        st.image("https://blog.qburst.com/wp-content/uploads/2020/09/Conversational-AI-Chatbot-Architecture-Overview.png?text=Chat+with+AI", caption="Chat with AI")
        
    # Add info about the Gemini model
    st.subheader("About the AI Model")
    st.markdown("""
    This application uses Google's **Gemini 1.5 Pro** model, which is designed for:
    
    - Text analysis and understanding
    - Information extraction from documents
    - Natural language conversation
    - Intelligent question answering
    
    For more information, visit [Google AI Studio](https://ai.google.dev/).
    """)