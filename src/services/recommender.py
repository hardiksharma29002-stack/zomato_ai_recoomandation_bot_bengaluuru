import json
from typing import List
import pandas as pd
from src.models.preferences import UserPreferences
from src.models.recommendation import Recommendation, RecommendationResponse
from src.services.filter import filter_restaurants
from src.services.prompt import build_recommendation_prompt
from src.services.llm import LLMClient
from src.data.preprocessor import get_restaurant_dataframe

def get_recommendations(prefs: UserPreferences, top_n: int = 5) -> RecommendationResponse:
    """
    Get recommendations based on user preferences.
    Orchestrates filtering, LLM prompting, and validation.
    """
    df = get_restaurant_dataframe()
    
    candidates_df, suggestions = filter_restaurants(df, prefs)
    
    if candidates_df.empty:
        # Return empty response with suggestions
        return RecommendationResponse(
            summary="No exact matches found. " + " ".join(suggestions),
            recommendations=[]
        )
    
    candidates_df = candidates_df.head(20)
    
    prompt = build_recommendation_prompt(prefs, candidates_df)
    
    llm_client = LLMClient()
    
    max_retries = 1
    llm_response = None
    
    for attempt in range(max_retries + 1):
        try:
            llm_response_dict = llm_client.generate_json(prompt)
            if llm_response_dict:
                if isinstance(llm_response_dict, list):
                    llm_response = RecommendationResponse(recommendations=llm_response_dict)
                else:
                    llm_response = RecommendationResponse(**llm_response_dict)
                break
        except Exception as e:
            print(f"LLM parse error on attempt {attempt}: {e}")
            if attempt == max_retries:
                print("Max retries reached for LLM.")
                
    if not llm_response or not llm_response.recommendations:
        return _fallback_recommendations(candidates_df, top_n)
        
    valid_names = set(candidates_df['name'].str.strip().str.lower().tolist())
    
    valid_recs = []
    for rec in llm_response.recommendations:
        rec_name_clean = rec.restaurant_name.strip().lower()
        
        # Exact match
        if rec_name_clean in valid_names:
            valid_recs.append(rec)
        else:
            # Substring fallback match
            matched = False
            for v_name in valid_names:
                if rec_name_clean in v_name or v_name in rec_name_clean:
                    # Fix the name to match the dataset exactly
                    rec.restaurant_name = candidates_df.loc[candidates_df['name'].str.strip().str.lower() == v_name, 'name'].iloc[0]
                    valid_recs.append(rec)
                    matched = True
                    break
            
            if not matched:
                print(f"Hallucination caught: {rec.restaurant_name}")
            
    if not valid_recs:
        return _fallback_recommendations(candidates_df, top_n)
        
    # Cap to top_n
    llm_response.recommendations = valid_recs[:top_n]
    return llm_response

def _fallback_recommendations(candidates_df: pd.DataFrame, top_n: int) -> RecommendationResponse:
    """Fallback if LLM fails: return top N sorted by rating without explanation."""
    recs = []
    for _, row in candidates_df.head(top_n).iterrows():
        recs.append(
            Recommendation(
                restaurant_name=row['name'],
                cuisine=row['cuisines'],
                rating=float(row['rating']),
                cost_for_two=int(row['cost_for_two']),
                explanation=""
            )
        )
    return RecommendationResponse(
        summary="Here are the top-rated matches based on your criteria.",
        recommendations=recs
    )
