import functools
import pandas as pd
from src.config import settings

def preprocess_restaurants(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize city, cuisines, cost, and rating."""
    # Ensure column names are lower case and stripped
    df.columns = df.columns.str.lower().str.strip()
    
    # Common mappings based on typical Zomato datasets
    column_mapping = {
        'restaurant name': 'name',
        'restaurant_name': 'name',
        'cost': 'cost_for_two',
        'approx cost for two': 'cost_for_two',
        'approx_cost(for two people)': 'cost_for_two',
        'average cost for two': 'cost_for_two',
        'cost (rs.)': 'cost_for_two',
        'aggregate rating': 'rating',
        'rate': 'rating'
    }
    df = df.rename(columns=column_mapping)
    
    if 'listed_in(city)' in df.columns:
        df = df.rename(columns={'listed_in(city)': 'city'})
        if 'location' in df.columns:
            df = df.drop(columns=['location'])
    elif 'location' in df.columns:
        df = df.rename(columns={'location': 'city'})
    
    # Clean data
    if 'cost_for_two' in df.columns:
        # Convert to string, strip commas, extract numeric digits, convert safely to numeric int
        cost_series = df['cost_for_two'].astype(str).str.replace(',', '', regex=False)
        extracted_digits = cost_series.str.extract(r'(\d+)')[0]
        df['cost_for_two'] = pd.to_numeric(extracted_digits, errors='coerce').fillna(0).astype(int)
        
    if 'rating' in df.columns:
        # Extract the first number found (e.g. 4.1 from 4.1/5)
        df['rating'] = df['rating'].astype(str).str.extract(r'(\d+(?:\.\d+)?)')[0]
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0.0)
        
    if 'cuisines' in df.columns:
        df['cuisines'] = df['cuisines'].astype(str).fillna("Unknown")
        
    # Ensure city column exists
    if 'city' not in df.columns:
        if 'location' in df.columns:
            df['city'] = df['location']
        elif 'listed_in(city)' in df.columns:
            df['city'] = df['listed_in(city)']
        else:
            df['city'] = "Bangalore"
            
    df['city'] = df['city'].astype(str).str.strip()
    # Replace 'nan' string values with 'Bangalore'
    df['city'] = df['city'].replace(['nan', 'NaN', 'None', ''], 'Bangalore')
        
    # Add budget band
    if 'cost_for_two' in df.columns:
        df['budget_band'] = df['cost_for_two'].apply(settings.budget.get_budget_band)
        
    if 'name' in df.columns:
        df['name'] = df['name'].astype(str).str.strip()
        
    # Remove duplicates based on restaurant name to prevent UI repeats
    if 'name' in df.columns:
        df = df.drop_duplicates(subset=['name'], keep='first')
        
    return df

@functools.lru_cache(maxsize=1)
def get_restaurant_dataframe() -> pd.DataFrame:
    from src.data.loader import load_restaurants
    raw_df = load_restaurants()
    clean_df = preprocess_restaurants(raw_df)
    return clean_df
