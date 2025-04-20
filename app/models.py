from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class QueryModel(BaseModel):
    query: str

class AssessmentRecommendation(BaseModel):
    name: str
    url: str
    remote_testing_support: str
    adaptive_support: str
    duration: int
    test_type: str

class RecommendationResponse(BaseModel):
    recommendations: List[AssessmentRecommendation]

class HealthResponse(BaseModel):
    status: str
    message: str