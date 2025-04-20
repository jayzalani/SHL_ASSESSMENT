import logging
from datetime import datetime
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/recommendation_traces.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def trace_recommendation(query, params, vector_results, gemini_results, final_results):
    """Log the recommendation process to understand how results were generated"""
    trace_id = datetime.now().strftime("%Y%m%d%H%M%S")
    
    logger.info(f"Trace ID: {trace_id}")
    logger.info(f"Query: {query}")
    logger.info(f"Extracted Parameters: {params}")
    
    # Log vector search results
    logger.info("Vector Search Results:")
    for i, (_, row) in enumerate(vector_results.iterrows(), 1):
        logger.info(f"  {i}. {row['title']} (Score: {row['similarity_score']:.4f})")
    
    # Log Gemini reranking
    logger.info("Gemini Reranking Results:")
    for i, (_, row) in enumerate(gemini_results.iterrows(), 1):
        logger.info(f"  {i}. {row['title']}")
    
    # Log final results
    logger.info("Final Recommendations:")
    for i, (_, row) in enumerate(final_results.iterrows(), 1):
        logger.info(f"  {i}. {row['title']}")
    
    logger.info("=" * 50)
    
    return trace_id