import functools
import os
import pandas as pd

@functools.lru_cache(maxsize=1)
def load_restaurants() -> pd.DataFrame:
    """Load the Zomato subset dataset from local cache."""
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    local_path = os.path.join(project_root, "data", "zomato_subset.csv")
    
    if os.path.exists(local_path):
        try:
            print("Loading dataset from local cache...")
            return pd.read_csv(local_path)
        except Exception as e:
            print(f"Error loading local CSV: {e}")
            
    # Create a minimal fallback DataFrame if not found
    print("Creating emergency fallback dataset...")
    fallback_data = {
        "name": ["Jalsa", "Spice Elephant", "San Churro", "Addhuri Udupi", "Grand Village"],
        "city": ["Banashankari", "Banashankari", "Banashankari", "Banashankari", "Banashankari"],
        "location": ["Banashankari", "Banashankari", "Banashankari", "Banashankari", "Banashankari"],
        "cuisines": ["North Indian, Mughlai", "Chinese, Thai", "Cafe, Desserts", "South Indian", "North Indian"],
        "rating": [4.1, 4.1, 3.8, 3.7, 3.8],
        "cost_for_two": [800, 800, 800, 300, 600]
    }
    return pd.DataFrame(fallback_data)
