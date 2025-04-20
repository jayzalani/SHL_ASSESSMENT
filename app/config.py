import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API keys and configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Model configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
GEMINI_MODEL = "gemini-pro"

# Data paths
DATA_PATH = "data/shl_assessments.csv"

# API configuration
API_HOST = "0.0.0.0"
API_PORT = int(os.getenv("PORT", 8000))

# Streamlit configuration
STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", 8501))