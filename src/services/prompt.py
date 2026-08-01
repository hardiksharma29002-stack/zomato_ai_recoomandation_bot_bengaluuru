import json
import pandas as pd
from typing import List, Dict, Any
from src.models.preferences import UserPreferences
from src.models.recommendation import RecommendationResponse

def build_recommendation_prompt(prefs: UserPreferences, candidates: pd.DataFrame) -> str:
    """
    Build a grounded prompt for the LLM based on user preferences and filtered candidates.
    """
    
    # Convert candidates DataFrame to a JSON string for the prompt
    candidate_list = candidates[['name', 'cuisines', 'rating', 'cost_for_two']].to_dict('records')
    candidates_json = json.dumps(candidate_list, indent=2)
    
    schema = RecommendationResponse.model_json_schema()
    schema_json = json.dumps(schema, indent=2)
    
    extra = f"\nAdditional preferences: {prefs.extra_preferences}" if prefs.extra_preferences else ""
    
    prompt = f"""You are an AI restaurant recommendation assistant.
Recommend ONLY from the provided list of candidates below. DO NOT invent or hallucinate any restaurants that are not in the candidate list.

USER PREFERENCES:
- Location: {prefs.location}
- Preferred Cuisine: {prefs.cuisine}
- Budget Band: {prefs.budget}
- Minimum Rating: {prefs.min_rating}{extra}

CANDIDATES (Filtered list):
{candidates_json}

RANKING PRIORITY:
1. Cuisine match (prioritize the preferred cuisine)
2. Highest rating
3. Budget fit
4. Any extra preferences specified

INSTRUCTIONS:
1. Review the candidates and select the best matches according to the ranking priority.
2. Provide a brief explanation for why each was recommended.
3. You MUST output EXACTLY {prefs.num_results} recommendations. If there are fewer candidates than {prefs.num_results}, output all of them.
4. Output the result strictly in JSON format matching the schema below.

EXPECTED JSON SCHEMA:
{schema_json}

Output ONLY valid JSON. No markdown formatting, no preamble, no postamble.
"""
    return prompt
