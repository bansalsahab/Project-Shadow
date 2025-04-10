import os
import nltk
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

def setup_environment():
    """Initialize environment variables and configure the application"""
    # Download NLTK resources if not already downloaded
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)

    # Load environment variables
    load_dotenv()

    # Set Google API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
    
    return api_key

def setup_directories():
    """Create necessary directories for storing data"""
    os.makedirs("data/chunks", exist_ok=True)
    os.makedirs("data/embeddings", exist_ok=True)

def setup_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="Project SHADOW - Intelligence Retrieval",
        page_icon="",
        layout="wide"
    )
