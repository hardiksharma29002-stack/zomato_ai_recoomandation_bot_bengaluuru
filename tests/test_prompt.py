import pandas as pd
from src.models.preferences import UserPreferences
from src.services.prompt import build_recommendation_prompt

def test_prompt_contains_candidates():
    prefs = UserPreferences(
        location="Bangalore",
        budget="medium",
        cuisine="Italian",
        min_rating=4.0,
        extra_preferences="Needs a nice view"
    )
    
    candidates = pd.DataFrame([
        {"name": "Luigi's", "cuisines": "Italian", "rating": 4.5, "cost_for_two": 1000},
        {"name": "Mario's", "cuisines": "Italian, Pizza", "rating": 4.2, "cost_for_two": 1200}
    ])
    
    prompt = build_recommendation_prompt(prefs, candidates)
    
    assert "Luigi's" in prompt
    assert "Mario's" in prompt
    assert "Bangalore" in prompt
    assert "Italian" in prompt
    assert "Needs a nice view" in prompt
