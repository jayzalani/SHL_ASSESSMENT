from fastapi import FastAPI, HTTPException
from app.models import QueryModel, RecommendationResponse, HealthResponse, AssessmentRecommendation
from app.data_processing import load_and_preprocess_data, create_embeddings
from app.search import search_assessments
from app.gemini import setup_gemini, extract_parameters

# Initialize the application
app = FastAPI(title="SHL Assessment Recommendation API")

# Load and preprocess data
print("Loading and preprocessing data...")
df = load_and_preprocess_data()
embedding_model, embeddings_array = create_embeddings(df)
gemini_model = setup_gemini()
print("Data and models loaded successfully!")

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

@app.post("/recommend", response_model=RecommendationResponse)
def recommend_assessments(request: QueryModel):
    """Recommend assessments based on query"""
    query = request.query
    
    # Extract parameters from the query
    params = extract_parameters(query, gemini_model)
    
    # Search for relevant assessments
    results, trace_id = search_assessments(
        query=query,
        df=df,
        embedding_model=embedding_model,
        embeddings_array=embeddings_array,
        gemini_model=gemini_model,
        top_k=10,
        duration_limit=params.get("duration_limit")
    )
    
    # Format the response
    recommendations = []
    for _, row in results.iterrows():
        recommendation = AssessmentRecommendation(
            name=row["title"],
            url=row["url"],
            remote_testing_support=row["remote_support"],
            adaptive_support=row["adaptive_support"],
            duration=int(row["duration"]),
            test_type=row["test_type"]
        )
        recommendations.append(recommendation)
    
    return {"recommendations": recommendations}