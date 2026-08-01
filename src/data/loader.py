import functools
import os
import pandas as pd

HF_DATASET_ID = "ManikaSaini/zomato-restaurant-recommendation"
HF_SPLIT = "train"

@functools.lru_cache(maxsize=1)
def load_restaurants() -> pd.DataFrame:
    """Load the Zomato Bengaluru restaurant dataset.

    Priority order:
    1. Local CSV cache (data/zomato_subset.csv) — fast startup
    2. Hugging Face dataset (ManikaSaini/zomato-restaurant-recommendation) — full 51k rows
    3. Hardcoded fallback — safety net when all else fails
    """
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    local_path = os.path.join(project_root, "data", "zomato_subset.parquet")

    # 1. Try local Parquet first (fast path)
    if os.path.exists(local_path):
        try:
            print(f"Loading dataset from local cache: {local_path}")
            df = pd.read_parquet(local_path)
            print(f"  Loaded {len(df):,} rows from local Parquet.")
            return df
        except Exception as e:
            print(f"  Warning: Could not load local Parquet ({e}). Falling back to HuggingFace.")

    # 2. Download from HuggingFace (full dataset)
    try:
        print(f"Downloading dataset from HuggingFace: {HF_DATASET_ID} ...")
        from datasets import load_dataset
        hf_ds = load_dataset(HF_DATASET_ID, split=HF_SPLIT)
        df = hf_ds.to_pandas()
        print(f"  Loaded {len(df):,} rows from HuggingFace.")

        # Save a local cache so subsequent restarts are instant
        try:
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            df.to_parquet(local_path, index=False)
            print(f"  Cached dataset to: {local_path}")
        except Exception as cache_err:
            print(f"  Warning: Could not cache Parquet locally ({cache_err}).")

        return df

    except Exception as e:
        print(f"  Warning: Could not load from HuggingFace ({e}). Using emergency fallback.")

    # 3. Hardcoded fallback
    print("Using emergency fallback dataset (5 restaurants).")
    fallback_data = {
        "name": ["Jalsa", "Spice Elephant", "San Churro", "Addhuri Udupi", "Grand Village"],
        "listed_in(city)": ["Banashankari"] * 5,
        "location": ["Banashankari"] * 5,
        "cuisines": [
            "North Indian, Mughlai",
            "Chinese, Thai",
            "Cafe, Desserts",
            "South Indian",
            "North Indian",
        ],
        "rate": ["4.1/5", "4.1/5", "3.8/5", "3.7/5", "3.8/5"],
        "votes": [775, 787, 504, 211, 166],
        "approx_cost(for two people)": ["800", "800", "800", "300", "600"],
        "online_order": ["Yes", "Yes", "No", "Yes", "Yes"],
        "book_table": ["Yes", "No", "No", "No", "No"],
        "rest_type": [
            "Casual Dining",
            "Casual Dining",
            "Cafe",
            "Quick Bites",
            "Casual Dining",
        ],
        "dish_liked": [
            "Pasta, Lunch Buffet",
            "Momos",
            "Churros",
            "Masala Dosa",
            "Biryani",
        ],
        "listed_in(type)": ["Buffet", "Delivery", "Cafes", "Delivery", "Dine-out"],
        "address": ["Banashankari"] * 5,
        "url": [""] * 5,
        "phone": [""] * 5,
        "reviews_list": ["[]"] * 5,
        "menu_item": ["[]"] * 5,
    }
    return pd.DataFrame(fallback_data)
