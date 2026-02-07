import pandas as pd
from typing import List, Dict, Any
from backend.trend_decline_agent import analyze_brand_trend
from backend.models import UnifiedResponseSchema

# ----------------------------------------------------
# 1. Curated Mock Data Service
# ----------------------------------------------------
class MockDataService:
    """
    Serves curated campaign data for specific brands.
    NO synthetic generation. Data is hardcoded as per requirements.
    """
    def __init__(self):
        self.brands = {
            "hm": {
                "brand_name": "H&M",
                "campaign_name": "Conscious Collection 2026",
                "data": [
                   {"date": "2026-01-01", "engagement_rate": 0.045, "engagement_growth_or_drop": 0.005, "sentiment_score": 0.0, "influencer_participation_ratio": 0.25, "content_volume": 400, "hashtag_density": 0.12},
                   {"date": "2026-01-02", "engagement_rate": 0.048, "engagement_growth_or_drop": 0.003, "sentiment_score": 0.1, "influencer_participation_ratio": 0.28, "content_volume": 450, "hashtag_density": 0.15},
                   {"date": "2026-01-03", "engagement_rate": 0.052, "engagement_growth_or_drop": 0.004, "sentiment_score": 0.2, "influencer_participation_ratio": 0.30, "content_volume": 600, "hashtag_density": 0.18},
                   {"date": "2026-01-04", "engagement_rate": 0.040, "engagement_growth_or_drop": -0.012, "sentiment_score": -0.1, "influencer_participation_ratio": 0.25, "content_volume": 800, "hashtag_density": 0.22},
                   {"date": "2026-01-05", "engagement_rate": 0.035, "engagement_growth_or_drop": -0.005, "sentiment_score": -0.3, "influencer_participation_ratio": 0.20, "content_volume": 900, "hashtag_density": 0.25},
                   {"date": "2026-01-06", "engagement_rate": 0.028, "engagement_growth_or_drop": -0.007, "sentiment_score": -0.5, "influencer_participation_ratio": 0.15, "content_volume": 1200, "hashtag_density": 0.30}
                ]
            },
            "blinkit": {
                "brand_name": "Blinkit",
                "campaign_name": "10 Min Delivery Challenge",
                "data": [
                    {"date": "2026-02-01", "engagement_rate": 0.08, "engagement_growth_or_drop": 0.01, "sentiment_score": 0.6, "influencer_participation_ratio": 0.40, "content_volume": 200, "hashtag_density": 0.10},
                    {"date": "2026-02-02", "engagement_rate": 0.085, "engagement_growth_or_drop": 0.005, "sentiment_score": 0.65, "influencer_participation_ratio": 0.42, "content_volume": 250, "hashtag_density": 0.12},
                    {"date": "2026-02-03", "engagement_rate": 0.09, "engagement_growth_or_drop": 0.005, "sentiment_score": 0.7, "influencer_participation_ratio": 0.45, "content_volume": 300, "hashtag_density": 0.14},
                    {"date": "2026-02-04", "engagement_rate": 0.092, "engagement_growth_or_drop": 0.002, "sentiment_score": 0.72, "influencer_participation_ratio": 0.46, "content_volume": 350, "hashtag_density": 0.15}
                ]
            },
            "zomato": {
                "brand_name": "Zomato",
                "campaign_name": "Zomatoland Returns",
                "data": [
                    {"date": "2026-03-01", "engagement_rate": 0.06, "engagement_growth_or_drop": 0.0, "sentiment_score": 0.4, "influencer_participation_ratio": 0.30, "content_volume": 500, "hashtag_density": 0.20},
                    {"date": "2026-03-02", "engagement_rate": 0.055, "engagement_growth_or_drop": -0.005, "sentiment_score": 0.2, "influencer_participation_ratio": 0.28, "content_volume": 600, "hashtag_density": 0.22},
                    {"date": "2026-03-03", "engagement_rate": 0.050, "engagement_growth_or_drop": -0.005, "sentiment_score": 0.0, "influencer_participation_ratio": 0.25, "content_volume": 700, "hashtag_density": 0.25},
                    {"date": "2026-03-04", "engagement_rate": 0.040, "engagement_growth_or_drop": -0.010, "sentiment_score": -0.2, "influencer_participation_ratio": 0.20, "content_volume": 850, "hashtag_density": 0.30}
                ]
            },
            "crocs": {
                "brand_name": "Crocs",
                "campaign_name": "Shrek Collab",
                "data": [
                    {"date": "2026-04-01", "engagement_rate": 0.12, "engagement_growth_or_drop": 0.02, "sentiment_score": 0.8, "influencer_participation_ratio": 0.50, "content_volume": 1000, "hashtag_density": 0.40},
                    {"date": "2026-04-02", "engagement_rate": 0.13, "engagement_growth_or_drop": 0.01, "sentiment_score": 0.85, "influencer_participation_ratio": 0.55, "content_volume": 1500, "hashtag_density": 0.45},
                    {"date": "2026-04-03", "engagement_rate": 0.11, "engagement_growth_or_drop": -0.02, "sentiment_score": 0.6, "influencer_participation_ratio": 0.50, "content_volume": 2000, "hashtag_density": 0.50},
                    {"date": "2026-04-04", "engagement_rate": 0.08, "engagement_growth_or_drop": -0.03, "sentiment_score": 0.3, "influencer_participation_ratio": 0.40, "content_volume": 2500, "hashtag_density": 0.60} # Saturation example
                ]
            }
        }

    def get_brands(self):
        return [{"id": k, "name": v["brand_name"]} for k, v in self.brands.items()]

    def get_brand_data(self, brand_id: str) -> Dict[str, Any]:
        return self.brands.get(brand_id)

mock_service = MockDataService()

# ----------------------------------------------------
# 2. Service Endpoints
# ----------------------------------------------------

def get_available_brands_service():
    """Returns list of curated brands."""
    return {"brands": mock_service.get_brands()}

def analyze_brand_service(brand_id: str) -> UnifiedResponseSchema:
    """
    Analyzes specific brand campaign trend.
    """
    brand_data = mock_service.get_brand_data(brand_id)
    if not brand_data:
        raise ValueError(f"Brand {brand_id} not found")
        
    df = pd.DataFrame(brand_data['data'])
    # Attach metadata to DF for agent convenience
    df['brand_name'] = brand_data['brand_name']
    df['campaign_name'] = brand_data['campaign_name']
    
    # Analyze
    result = analyze_brand_trend(df)
    
    return UnifiedResponseSchema(**result)

# Legacy stub for compatibility if needed (deprecated)
def analyze_trend_stub(data):
    pass
