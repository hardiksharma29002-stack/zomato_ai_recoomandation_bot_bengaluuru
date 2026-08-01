from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from src.models.preferences import UserPreferences
from src.models.recommendation import RecommendationResponse
from src.services.recommender import get_recommendations

app = FastAPI(title="Zomato AI API")

# Allow CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, lock this down
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/api/v1")

@router.post("/recommend", response_model=RecommendationResponse)
async def recommend(prefs: UserPreferences):
    try:
        response = get_recommendations(prefs, top_n=prefs.num_results)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/meta")
async def get_meta():
    from src.data.loader import load_restaurants
    from src.config import settings
    try:
        df = load_restaurants()
        locations = sorted([loc for loc in df['city'].dropna().unique().tolist() if str(loc).strip() and str(loc).lower() != 'nan'])
        
        # Extract top 12 cuisines
        cuisine_counts = {}
        for c in df['cuisines'].dropna():
            for cuisine in str(c).split(','):
                cleaned = cuisine.strip()
                if cleaned and cleaned.lower() not in ['nan', 'unknown', 'none']:
                    cuisine_counts[cleaned] = cuisine_counts.get(cleaned, 0) + 1
        
        cuisines = [c[0] for c in sorted(cuisine_counts.items(), key=lambda x: x[1], reverse=True)[:12]]
        cuisines.insert(0, "Any")
        if not locations:
            locations = ["Banashankari", "Indiranagar", "Koramangala", "BTM", "Jayanagar", "MG Road"]
        if not cuisines:
            cuisines = ["North Indian", "Chinese", "South Indian", "Fast Food", "Biryani", "Desserts", "Beverages", "Continental", "Cafe", "Street Food", "Italian", "Bakery"]

        return {
            "locations": locations,
            "cuisines": cuisines,
            "budget": {
                "low_max": settings.budget.low_max,
                "medium_max": settings.budget.medium_max
            }
        }
    except Exception as e:
        print(f"Error generating meta response: {e}")
        return {
            "locations": ["Banashankari", "Indiranagar", "Koramangala", "BTM", "Jayanagar", "MG Road"],
            "cuisines": ["North Indian", "Chinese", "South Indian", "Fast Food", "Biryani", "Desserts", "Beverages", "Continental", "Cafe", "Street Food", "Italian", "Bakery"],
            "budget": {
                "low_max": settings.budget.low_max,
                "medium_max": settings.budget.medium_max
            }
        }

app.include_router(router)

frontend_dist = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "dist")
if os.path.isdir(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")
