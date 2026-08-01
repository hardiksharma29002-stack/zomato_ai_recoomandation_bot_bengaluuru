import argparse
import sys
import uvicorn
from src.data.preprocessor import get_restaurant_dataframe
from src.models.preferences import UserPreferences
from src.services.filter import filter_restaurants

def run_server():
    print("Starting Zomato AI FastAPI Server...")
    uvicorn.run("src.api.router:app", host="127.0.0.1", port=8000, reload=True)

def main():
    parser = argparse.ArgumentParser(description="Zomato AI Recommendation CLI / Server")
    parser.add_argument("--location", help="City to search in")
    parser.add_argument("--budget", choices=["low", "medium", "high"], help="Budget band")
    parser.add_argument("--cuisine", help="Preferred cuisine")
    parser.add_argument("--min-rating", type=float, help="Minimum rating (0.0 to 5.0)", dest="min_rating")
    parser.add_argument("--extra-preferences", type=str, default="", help="Any extra preferences")
    parser.add_argument("--server", action="store_true", help="Run the FastAPI server")
    
    args = parser.parse_args()

    # Default to running the server if no CLI arguments are provided
    if args.server or not any(vars(args).values()):
        run_server()
        return
    
    if not all([args.location, args.budget, args.cuisine, args.min_rating is not None]):
        print("For CLI filter mode, --location, --budget, --cuisine, and --min-rating are required.")
        sys.exit(1)
    
    try:
        prefs = UserPreferences(
            location=args.location,
            budget=args.budget,
            cuisine=args.cuisine,
            min_rating=args.min_rating,
            extra_preferences=args.extra_preferences
        )
    except Exception as e:
        print(f"Validation Error: {e}")
        sys.exit(1)
        
    print("Loading dataset...")
    df = get_restaurant_dataframe()
    
    print(f"\nFiltering for: {prefs.location}, {prefs.budget} budget, {prefs.cuisine}, {prefs.min_rating}+ rating")
    filtered_df, suggestions = filter_restaurants(df, prefs)
    
    if filtered_df.empty:
        print("\nNo restaurants found matching your criteria.")
        for suggestion in suggestions:
            print(f"- {suggestion}")
    else:
        print(f"\nFound {len(filtered_df)} matches (capped at 20):")
        display_cols = ['name', 'cuisines', 'rating', 'cost_for_two']
        display_cols = [c for c in display_cols if c in filtered_df.columns]
        print(filtered_df[display_cols].to_string(index=False))

if __name__ == "__main__":
    main()
