import pandas as pd
from src.models.preferences import UserPreferences
from src.services.filter import filter_restaurants

def test_filter_exact_location():
    prefs = UserPreferences(
        location="Bangalore",
        budget="medium",
        cuisine="",
        min_rating=0.0
    )
    df = pd.DataFrame([
        {"city": "Bangalore", "name": "A", "rating": 4.0, "budget_band": "medium", "cuisines": "Italian"},
        {"city": "Mumbai", "name": "B", "rating": 4.0, "budget_band": "medium", "cuisines": "Italian"}
    ])
    filtered, suggestions = filter_restaurants(df, prefs)
    assert len(filtered) == 1
    assert filtered.iloc[0]['name'] == "A"
    assert not suggestions

def test_filter_empty_result_gives_suggestions():
    prefs = UserPreferences(
        location="Mars",
        budget="medium",
        cuisine="",
        min_rating=0.0
    )
    df = pd.DataFrame([
        {"city": "Bangalore", "name": "A"}
    ])
    filtered, suggestions = filter_restaurants(df, prefs)
    assert len(filtered) == 1
    assert filtered.iloc[0]['name'] == 'A'
    assert any("Mars" in s for s in suggestions)
