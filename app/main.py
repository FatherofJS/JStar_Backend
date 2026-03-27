from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from .rate_limiter import limiter

import cloudinary
import cloudinary.search
from dotenv import load_dotenv
load_dotenv()

from .routes import chart_router, location_router, chat_router
import os
# Create app
app = FastAPI(
    title="JStar Astrology API",
    description="Astrology and Synastry calculation engine",
    version="1.0.0"
)

origins = os.getenv("FRONTEND_URL", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(chart_router)
app.include_router(location_router)
app.include_router(chat_router)


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

@app.get("/fatherofjs")
def get_images():
    result = cloudinary.search.Search()\
        .expression("folder:easter_egg")\
        .sort_by("created_at", "desc")\
        .max_results(50)\
        .execute()

    return result["resources"]

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_BOARD_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_BOARD_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_BOARD_API_SECRET")
)

ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]
CATEGORIES = ["Fashion", "Hành tinh", "Others", "Quotes", "Đồ vật", "Đồ ăn"]

@app.get("/zodiac-board")
def get_zodiac_board():
    all_resources = []
    next_cursor = None

    while True:
        search = cloudinary.search.Search()\
            .expression("resource_type:image AND asset_folder:Natal*")\
            .sort_by("created_at", "desc")\
            .max_results(500)

        if next_cursor:
            search = search.next_cursor(next_cursor)

        result = search.execute()
        all_resources.extend(result.get("resources", []))
        next_cursor = result.get("next_cursor")
        if not next_cursor:
            break

    manifest = {}
    for sign in ZODIAC_SIGNS:
        manifest[sign] = {cat: [] for cat in CATEGORIES}

    for resource in all_resources:
        asset_folder = resource.get("asset_folder", "") 
        public_id = resource["public_id"]                
        
        parts = asset_folder.split("/")
        if len(parts) < 3 or parts[0] != "Natal":
            continue
            
        sign = parts[1]
        category = parts[2]
        
        if sign in manifest and category in manifest[sign]:
            manifest[sign][category].append(public_id)

    return manifest


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

