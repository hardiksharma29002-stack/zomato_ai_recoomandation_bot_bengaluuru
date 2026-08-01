import pandas as pd
from typing import Tuple, List
from src.models.preferences import UserPreferences

def filter_restaurants(df: pd.DataFrame, prefs: UserPreferences) -> Tuple[pd.DataFrame, List[str]]:
    """
    Filter restaurants using a scoring system to ensure we return as many results as requested.
    location -> strict match
    rating, budget, cuisine -> soft match (prioritized)
    """
    suggestions = []
    filtered = df.copy()
    
    # Filter by location (exact match, ignoring case)
    if not filtered.empty and 'city' in filtered.columns:
        mask = filtered['city'].str.lower() == prefs.location.lower()
        if mask.any():
            filtered = filtered[mask]
        else:
            suggestions.append(f"No restaurants found in '{prefs.location}'. Showing from other areas.")
            
    if filtered.empty:
        return filtered, suggestions
        
    filtered = filtered.copy()
    filtered['match_score'] = 0
    
    # Rating match (+5 points)
    if 'rating' in filtered.columns:
        mask = filtered['rating'] >= prefs.min_rating
        filtered.loc[mask, 'match_score'] += 5
        if not mask.any():
            suggestions.append(f"Not enough restaurants with a rating of {prefs.min_rating}+.")
            
    # Budget match (+10 points)
    if 'budget_band' in filtered.columns:
        mask = filtered['budget_band'].str.lower() == prefs.budget.lower()
        filtered.loc[mask, 'match_score'] += 10
        if not mask.any():
            suggestions.append(f"Not enough restaurants for the '{prefs.budget}' budget.")
            
    # Cuisine match (+5 points)
    if 'cuisines' in filtered.columns and prefs.cuisine and prefs.cuisine.lower() != "any":
        mask = filtered['cuisines'].str.contains(prefs.cuisine, case=False, na=False)
        filtered.loc[mask, 'match_score'] += 5
        if not mask.any():
            suggestions.append(f"Not enough restaurants serving '{prefs.cuisine}'.")
            
    # Sort by match_score descending, then rating descending
    if 'rating' in filtered.columns:
        filtered = filtered.sort_values(by=['match_score', 'rating'], ascending=[False, False])
    else:
        filtered = filtered.sort_values(by=['match_score'], ascending=[False])
        
    # Take top N
    filtered = filtered.head(prefs.num_results)
    
    # Clean up the temporary column
    filtered = filtered.drop(columns=['match_score'])
        
    return filtered, suggestions
