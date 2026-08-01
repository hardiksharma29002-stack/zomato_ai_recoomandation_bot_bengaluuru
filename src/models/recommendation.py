from typing import List, Optional
from pydantic import BaseModel, Field

class Recommendation(BaseModel):
    restaurant_name: str
    cuisine: str
    rating: float
    cost_for_two: int
    explanation: str = Field(description="Explanation of why this restaurant was recommended based on user preferences")

class RecommendationResponse(BaseModel):
    summary: Optional[str] = Field(default=None, description="A one-line summary of the top picks")
    recommendations: List[Recommendation]
