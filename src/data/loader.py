import functools
import os
import pandas as pd
from datasets import load_dataset

@functools.lru_cache(maxsize=1)
def load_restaurants() -> pd.DataFrame:
    """Load the Zomato dataset from local cache or Hugging Face."""
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    local_path = os.path.join(project_root, "data", "zomato.csv")
    
    if os.path.exists(local_path):
        try:
            print("Loading dataset from local cache...")
            return pd.read_csv(local_path)
        except Exception as e:
            print(f"Error loading local CSV: {e}")
            
    print("Fetching dataset from Hugging Face (this may take a moment on first run)...")
    try:
        dataset = load_dataset("ManikaSaini/zomato-restaurant-recommendation", split="train")
        df = dataset.to_pandas()
        # Save locally for instant startup in future
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        df.to_csv(local_path, index=False)
        print("Dataset cached locally successfully.")
        return df
    except Exception as e:
        print(f"Error loading from Hugging Face: {e}")
        if os.path.exists(local_path):
            return pd.read_csv(local_path)
        # Create a minimal fallback DataFrame if internet/HF is completely unreachable
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
