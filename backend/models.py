from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class TrendAnalysisRequest(BaseModel):
    trend_data: Dict[str, Any]

class TrendAnalysisResponse(BaseModel):
    decline_probability: float
    lifecycle_stage: str
    decline_drivers: List[str]

class EarlyWarningResponse(BaseModel):
    decline_probability: float
    days_to_collapse: int
    risk_level: str

class NarrativeRequest(BaseModel):
    trend_data: Dict[str, Any]

class NarrativeResponse(BaseModel):
    explanation: str
    source: str
    model: str

class SimulationRequest(BaseModel):
    influencer_ratio: float
    engagement_rate: float
    engagement_rate: float
    sentiment_score: float

class SimulationResponse(BaseModel):
    new_decline_probability: float
    recovery_timeline: str
    ai_explanation: str

class ChatRequest(BaseModel):
    user_query: str
    trend_context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
