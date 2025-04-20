import pandas as pd
import numpy as np
import re
from sentence_transformers import SentenceTransformer
from .config import EMBEDDING_MODEL, DATA_PATH

def load_and_preprocess_data():
    """Load and preprocess the SHL assessment data"""
    # Load the CSV data
    df = pd.read_csv(DATA_PATH)
    
    # Clean and preprocess the assessment descriptions
    def preprocess_text(text):
        if isinstance(text, str):
            # Remove special characters and extra spaces
            text = re.sub(r'[^\w\s]', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()
            return text
        return ""
    
    # Apply preprocessing to title and description
    df['processed_title'] = df['title'].apply(preprocess_text)
    df['processed_description'] = df['description'].apply(preprocess_text)
    
    # Create a combined text field for embedding
    df['combined_text'] = df['processed_title'] + " " + df['processed_description'] + " " + df['test_type']
    
    return df

def create_embeddings(df):
    """Create embeddings for the assessment data"""
    # Initialize the sentence transformer model
    model = SentenceTransformer(EMBEDDING_MODEL)
    
    # Generate embeddings for all assessments
    embeddings = model.encode(df['combined_text'].tolist(), show_progress_bar=True)
    
    # Create a numpy array of embeddings for efficient similarity search
    embeddings_array = np.array(embeddings)
    
    return model, embeddings_array