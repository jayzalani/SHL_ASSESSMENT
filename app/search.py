import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional
from .gemini import rerank_with_gemini
from .tracing import trace_recommendation

def search_assessments(
    query: str, 
    df: pd.DataFrame, 
    embedding_model,
    embeddings_array: np.ndarray,
    gemini_model,
    top_k: int = 10, 
    duration_limit: Optional[int] = None
):
    """Search for relevant assessments based on query"""
    # Generate embedding for the query
    query_embedding = embedding_model.encode([query])[0]
    
    # Compute cosine similarity between query and all assessments
    similarities = np.dot(embeddings_array, query_embedding) / (
        np.linalg.norm(embeddings_array, axis=1) * np.linalg.norm(query_embedding)
    )
    
    # Get indices of top similar assessments
    top_indices = np.argsort(similarities)[::-1]
    
    # Filter by duration if specified
    if duration_limit:
        filtered_indices = [idx for idx in top_indices if df.iloc[idx]['duration'] <= duration_limit]
        top_indices = filtered_indices if filtered_indices else top_indices
    
    # Get the top K assessments
    top_indices = top_indices[:min(top_k*2, len(top_indices))]  # Get more candidates for reranking
    
    # Prepare the candidates
    candidates = df.iloc[top_indices].copy()
    candidates['similarity_score'] = similarities[top_indices]
    
    # Store vector search results for tracing
    vector_results = candidates.copy()
    
    # Use Gemini to rerank and filter the candidates
    reranked_results = rerank_with_gemini(query, candidates, gemini_model)
    
    # Trace the recommendation process
    trace_id = trace_recommendation(
        query=query,
        params={"duration_limit": duration_limit},
        vector_results=vector_results,
        gemini_results=reranked_results,
        final_results=reranked_results
    )
    
    return reranked_results, trace_id