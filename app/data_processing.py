import pandas as pd
import numpy as np
import re
from sentence_transformers import SentenceTransformer
from .config import EMBEDDING_MODEL, DATA_PATH

def load_and_preprocess_data():
    """Load and preprocess the SHL assessment data"""

    df = pd.read_csv(DATA_PATH)
    
   
    def preprocess_text(text):
        if isinstance(text, str):
            
            text = re.sub(r'[^\w\s]', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()
            return text
        return ""
    

    df['processed_title'] = df['title'].apply(preprocess_text)
    df['processed_description'] = df['description'].apply(preprocess_text)
    
   
    df['combined_text'] = df['processed_title'] + " " + df['processed_description'] + " " + df['test_type']
    
    return df

def create_embeddings(df):
    """Create embeddings for the assessment data"""
 
    model = SentenceTransformer(EMBEDDING_MODEL)
    
   
    embeddings = model.encode(df['combined_text'].tolist(), show_progress_bar=True)
    
   
    embeddings_array = np.array(embeddings)
    
    return model, embeddings_array