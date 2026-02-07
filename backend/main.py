from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.services import get_available_brands_service, analyze_brand_service
from backend.models import UnifiedResponseSchema

app = FastAPI(title="Trend Decline Intelligence Agent")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    return {"status": "Backend running", "mode": "Brand-Specific Trend Decline"}

@app.get("/available-brands")
async def get_available_brands():
    """
    Returns list of curated brands (H&M, Blinkit, Zomato, Crocs).
    """
    return get_available_brands_service()

@app.post("/analyze-brand/{brand_id}", response_model=UnifiedResponseSchema)
async def analyze_brand(brand_id: str):
    """
    Analyzes specific brand campaign trend using the Unified Intelligence Agent.
    """
    try:
        return analyze_brand_service(brand_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Placeholder for compatibility if frontend still calls old route
# But we are revamping so we prefer cleaner API.
