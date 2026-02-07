import os
import requests
import json
import time
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from .models import (
    TrendAnalysisResponse,
    EarlyWarningResponse,
    NarrativeResponse,
    SimulationResponse,
    SimulationRequest,
    ChatResponse
)

# AI Agent Imports
try:
    from agents.orchestrator import TrendOrchestrator
    from agents.decline_predictor import DeclinePredictor
    from agents.simulation_agent import TrendSimulationAgent
    from agents.narrative_agent import NarrativeAgent
    from agents.chat_agent import ChatAgent
except ImportError:
    # Fallback for local testing if run directly
    import sys
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from agents.orchestrator import TrendOrchestrator
    from agents.decline_predictor import DeclinePredictor
    from agents.simulation_agent import TrendSimulationAgent
    from agents.narrative_agent import NarrativeAgent
    from agents.chat_agent import ChatAgent

# ----------------------------------------------------
# 1. Environment & Initialization
# ----------------------------------------------------
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

FEATHERLESS_API_KEY = os.getenv("FEATHERLESS_API_KEY")
print(f"DEBUG: FEATHERLESS_API_KEY loaded: {bool(FEATHERLESS_API_KEY and FEATHERLESS_API_KEY != 'YOUR_API_KEY_HERE')}")

# Initialize Agents Globally
print("[Backend] Initializing AI Agents...")
orchestrator = TrendOrchestrator()
predictor = DeclinePredictor()
simulator = TrendSimulationAgent()
narrator = NarrativeAgent(api_key=FEATHERLESS_API_KEY)
chat_agent = ChatAgent()  # Basic chat agent if available
print("[Backend] AI Agents Ready.")


# ----------------------------------------------------
# 2. Helper Functions
# ----------------------------------------------------
def _convert_to_dataframe(trend_data: dict) -> pd.DataFrame:
    """Converts input dictionary to pandas DataFrame."""
    try:
        # Check if already in suitable format (list of dicts)
        if isinstance(trend_data, list):
            return pd.DataFrame(trend_data)
        
        # Check if dict with list values
        if isinstance(trend_data, dict):
            # If "data" key exists, use that
            if "data" in trend_data and isinstance(trend_data["data"], list):
                return pd.DataFrame(trend_data["data"])
            return pd.DataFrame(trend_data)
            
    except Exception as e:
        print(f"Error converting to DataFrame: {e}")
        # Return empty DF or handle gracefully?
        # For now, return empty to trigger validation errors downstream
        return pd.DataFrame()
    return pd.DataFrame()

# ----------------------------------------------------
# 3. Service Implementations
# ----------------------------------------------------

def analyze_trend_stub(data: dict) -> TrendAnalysisResponse:
    """
    Analyzes trend using the Orchestrator.
    Maps to POST /trend-analysis
    """
    try:
        # Convert input to DataFrame
        df = _convert_to_dataframe(data.get("trend_data", {}))
        trend_name = data.get("trend_name", "Unknown Trend")
        
        if df.empty:
            # Fallback if conversion fails (or empty data)
            print("WARNING: Empty DataFrame. Using mock data for safety.")
            return TrendAnalysisResponse(
                decline_probability=0.0,
                lifecycle_stage="Unknown",
                decline_drivers=["Insufficient Data"]
            )

        # Run Analysis
        results = orchestrator.analyze_trend(df, trend_name)
        
        # Map to Response
        prediction = results.get("prediction", {})
        return TrendAnalysisResponse(
            decline_probability=prediction.get("decline_probability", 0.0),
            lifecycle_stage=prediction.get("lifecycle_stage", "Unknown"),
            decline_drivers=results.get("contributing_factors", []) 
            # Note: models.py calls it decline_drivers, orchestrator calls it contributing_factors
        )
    except Exception as e:
        print(f"Error in analyze_trend: {e}")
        return TrendAnalysisResponse(
            decline_probability=0.0,
            lifecycle_stage="Error",
            decline_drivers=[str(e)]
        )

def get_early_warning_stub(data: dict) -> EarlyWarningResponse:
    """
    Generates early warning using Decline Predictor logic.
    Maps to POST /early-warning
    """
    try:
        # We need trend data to run prediction. 
        # Assuming payload has trend data similar to/same as analyze_trend
        # OR we use the orchestrator to get the full picture first.
        
        # Optimize: If data is minimal, we might not be able to run full orchestrator.
        # But let's assume valid data is passed.
        df = _convert_to_dataframe(data.get("trend_data", {}))
        
        if df.empty:
             return EarlyWarningResponse(
                decline_probability=0.0,
                days_to_collapse="Unknown",
                risk_level="Unknown"
            )

        # Run full analysis to get clean signals for predictor
        # (Orchestrator handles signal extraction)
        analysis_results = orchestrator.analyze_trend(df, data.get("trend_name"))
        prediction = analysis_results.get("prediction", {})
        
        return EarlyWarningResponse(
            decline_probability=prediction.get("decline_probability", 0.0),
            days_to_collapse=str(prediction.get("days_to_collapse", "Unknown")),
            risk_level=prediction.get("risk_level", "Unknown")
        )

    except Exception as e:
        print(f"Error in early_warning: {e}")
        return EarlyWarningResponse(
            decline_probability=0.0,
            days_to_collapse="Error",
            risk_level="Error"
        )

def featherless_narrative_agent(trend_data: dict) -> NarrativeResponse:
    """
    Generates narrative using NarrativeAgent (with Featherless AI).
    Maps to POST /trend-narrative
    """
    try:
        # The input 'trend_data' here is likely the RAW data payload from the request.
        # But 'NarrativeAgent.generate' expects the *analysis results* (from Orchestrator).
        # We must first ANALYZE the data to get the insights, THEN generate the narrative.
        
        # 1. Analyze
        df = _convert_to_dataframe(trend_data.get("trend_data", {}))
        if df.empty:
             return NarrativeResponse(
                explanation="Insufficient data to generate narrative.",
                source="System",
                model="None"
            )
            
        analysis_results = orchestrator.analyze_trend(df, trend_data.get("trend_name"))
        
        # 2. Generate Narrative
        # NarrativeAgent.generate returns a dict with 'narrative_explanation'
        narrative_output = narrator.generate(analysis_results)
        
        return NarrativeResponse(
            explanation=narrative_output.get("narrative_explanation", "No explanation generated."),
            source="Featherless.ai" if narrator.use_ai else "Local Template",
            model=narrator.model if narrator.use_ai else "Rule-Based"
        )

    except Exception as e:
        print(f"Error in narrative_agent: {e}")
        return NarrativeResponse(
            explanation=f"Error generating narrative: {e}",
            source="System Error",
            model="None"
        )

def run_simulation_stub(data: SimulationRequest) -> SimulationResponse:
    """
    Runs simulation using TrendSimulationAgent.
    Maps to POST /simulate-recovery
    """
    try:
        # The input is a SimulationRequest object (pydantic model) or dict?
        # Check main.py. It passes 'request' which is Pydantic model. 
        # But wait, services.py signatures in original file were (influencer_ratio, ...).
        # We need to adapt to match main.py calls OR update main.py.
        # Let's see original services.py: 
        # def run_simulation_stub(influencer_ratio: float, ...)
        
        # We should check if we can get the full trend context. 
        # Simulation requires baseline data. 
        # If the request only has the *changes*, we assume a "Standard Baseline" 
        # or we need the user to pass the baseline in the request.
        # For this hackathon, we'll create a synthetic baseline from the "current" values implied.
        
        # Construct synthetic baseline data based on "current" implementation assumptions
        # or simplified logic since we don't have full state persistence.
        
        current_influencer = 0.2  # Default
        current_engagement = 0.1
        current_sentiment = 0.5
        
        # We'll use the inputs as "target" values and compare against a fixed baseline 
        # to show the "simulation" effect (delta).
        
        baseline_data = {
            'decline_prediction': {
                'decline_probability': 65.0, # Baseline
                'lifecycle_stage': 'Early Decline',
                'days_to_collapse': '30 days'
            },
            'signal_details': {
                'engagement': {'engagement_decline_percent': 40.0}, # Corresponds to ~0.1
                'sentiment': {'metrics': {'sentiment_change_percent': -10.0}},
                'influencers': {'participation_drop_percent': 30.0}
            }
        }
        
        # Calculate "boost" or "drop" based on input vs baseline assumptions
        # This is a simplification for the demo API which seems stateless.
        
        # Create params dict for agent
        params = {
            'influencer_boost': (data.influencer_ratio - current_influencer) / current_influencer,
            'engagement_boost': (data.engagement_rate - current_engagement) / current_engagement,
            'sentiment_improvement': (data.sentiment_score - current_sentiment) / current_sentiment
        }
        
        result = simulator.simulate(baseline_data, params, "User Simulation")
        
        explanation = narrator.generate_simulation_explanation(result)
        
        return SimulationResponse(
            new_decline_probability=result.get("new_decline_probability", 0.0),
            recovery_timeline="Unknown" if result.get("new_decline_probability") > 80 else "3-6 Weeks", # Logic from agent not fully exposing timeline string directly in same format
            ai_explanation=explanation
        )

    except Exception as e:
        print(f"Error in simulation: {e}")
        return SimulationResponse(
            new_decline_probability=0.0,
            recovery_timeline="Error",
            ai_explanation=str(e)
        )

def chat_stub(query: str, context: dict = None) -> ChatResponse:
    """
    Chat interaction.
    Maps to POST /chat-analysis
    """
    try:
        # Basic integration 
        response = chat_agent.chat(query, context) if hasattr(chat_agent, 'chat') else "Chat agent not fully implemented."
        return ChatResponse(response=response)
    except Exception as e:
        return ChatResponse(response=f"Error: {e}")
