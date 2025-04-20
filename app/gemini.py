import google.generativeai as genai
import json
import pandas as pd
from .config import GEMINI_API_KEY, GEMINI_MODEL

def setup_gemini():
    """Configure and set up the Google Gemini model"""
    # Set API key
    genai.configure(api_key=GEMINI_API_KEY)
    
    # For older API versions, just return the genai module
    return genai

def extract_parameters(query: str, genai_client):
    """Extract relevant parameters from the query using Gemini"""
    prompt = f"""Extract the following parameters from this job description or query:
    
    Query: "{query}"
    
    1. Maximum assessment duration in minutes (if specified)
    2. Skills or technologies mentioned
    3. Job level (entry, mid, senior, etc.)
    
    Return a JSON object with these fields:
    {{
        "duration_limit": <number or null>,
        "skills": ["skill1", "skill2", ...],
        "level": "<level or null>"
    }}"""
    
    try:
        # Generate content using the older API version
        model = genai_client.models.get_model(GEMINI_MODEL)
        response = model.generate_content(prompt)
        
        # Handle the response based on its structure
        response_text = response.text if hasattr(response, 'text') else str(response)
        params = json.loads(response_text)
        return params
    except Exception as e:
        print(f"Error in extract_parameters: {e}")
        return {"duration_limit": None, "skills": [], "level": None}

def rerank_with_gemini(query: str, candidates: pd.DataFrame, genai_client):
    """Rerank assessment candidates using Gemini"""
    # Prepare data for Gemini
    assessment_info = candidates[['title', 'description', 'duration', 'test_type']].to_dict('records')
    
    # Create prompt for Gemini
    prompt = f"""Given the job description or query: "{query}", 
    rank the following assessments based on relevance:
    
    {json.dumps(assessment_info, indent=2)}
    
    Return a JSON array with the indices of the assessments in order of relevance, 
    from most relevant to least relevant. Only include assessments that are actually 
    relevant to the query. Format: [0, 3, 1, ...]"""
    
    try:
        # Generate content using the older API version
        model = genai_client.models.get_model(GEMINI_MODEL)
        response = model.generate_content(prompt)
        
        # Handle the response based on its structure
        response_text = response.text if hasattr(response, 'text') else str(response)
        ranked_indices = json.loads(response_text)
        
        # Make sure the indices are valid
        ranked_indices = [i for i in ranked_indices if i < len(candidates)]
        
        # Return the reranked results (maximum 10)
        return candidates.iloc[ranked_indices[:min(10, len(ranked_indices))]]
    except Exception as e:
        print(f"Error in rerank_with_gemini: {e}")
        # If Gemini fails, return the original ranking
        return candidates.iloc[:min(10, len(candidates))]