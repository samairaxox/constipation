from pydantic import BaseModel
from typing import List, Dict, Optional, Any

# --- Unified Response Schema ---

class DeclineDrivers(BaseModel):
    engagement: str
    sentiment: str
    influencer: str
    saturation: str

class GraphData(BaseModel):
    engagement_trend: List[float]
    sentiment_trend: List[float]
    influencer_trend: List[float]
    decline_curve: List[float]
    dates: List[Any] = [] # Optional for now

class UnifiedResponseSchema(BaseModel):
    brand_name: str
    campaign_name: str
    decline_probability: float
    lifecycle_stage: str
    health_score: float
    collapse_eta_days: str
    decline_drivers: DeclineDrivers
    explainable_insights: str
    graph_data: GraphData

# --- Request Models ---
class TrendAnalysisRequest(BaseModel):
    brand_name: str
    campaign_data: List[Dict[str, Any]] # Time-series data points
