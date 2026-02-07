import pandas as pd
import numpy as np
from typing import Dict, List, Any
from datetime import datetime

class TrendDeclineAgent:
    """
    Unified Intelligence Agent for Brand-Specific Campaign Trend Decline Prediction.
    Rule-based, explainable, and business-focused.
    """
    
    def __init__(self):
        self.name = "Trend Decline Intelligence Agent"

    def analyze_brand_trend(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Main entry point for analyzing a brand's campaign trend.
        """
        # 1. Signal Analysis
        signals = self._analyze_signals(data)
        
        # 2. Decline Prediction
        prediction = self._predict_decline(signals)
        
        # 3. Explainability
        insights = self._generate_explainable_insights(signals, prediction)
        
        # 4. Graph Data
        graph_data = self._get_graph_signals(data, prediction)
        
        # 5. Business Insights (merged into unified schema logic)
        
        # Construct Unified Response
        response = {
            "brand_name": data['brand_name'].iloc[0] if 'brand_name' in data.columns else "Unknown Brand",
            "campaign_name": data['campaign_name'].iloc[0] if 'campaign_name' in data.columns else "Unknown Campaign",
            "decline_probability": float(prediction['decline_probability']),
            "lifecycle_stage": prediction['lifecycle_stage'],
            "health_score": float(prediction['health_score']),
            "collapse_eta_days": prediction['collapse_eta_days'],
            "decline_drivers": signals['drivers'],
            "explainable_insights": insights,
            "graph_data": graph_data
        }
        
        return response

    def _analyze_signals(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze signals: Decay, Polarity, Disengagement, Saturation.
        """
        # Get latest and previous metrics (assuming sorted by date)
        latest = df.iloc[-1]
        prev = df.iloc[-2] if len(df) > 1 else latest
        
        # 1. Engagement Decay Velocity
        # Normalize: Negative growth is bad.
        eng_change = latest.get('engagement_growth_or_drop', 0)
        engagement_decay = 0.0
        if eng_change < 0:
            engagement_decay = min(abs(eng_change) * 2, 1.0) # Scale decay to 0-1
            
        # 2. Sentiment Polarity Shift
        # Score -1 to 1. Shift towards -1 is bad.
        sent_score = latest.get('sentiment_score', 0)
        sentiment_risk = 0.0
        if sent_score < 0:
            sentiment_risk = min(abs(sent_score), 1.0)
            
        # 3. Influencer Disengagement
        # Ratio 0-1. Lower is bad.
        inf_ratio = latest.get('influencer_participation_ratio', 0)
        disengagement = 0.0
        if inf_ratio < 0.2: # Threshold
            disengagement = (0.2 - inf_ratio) / 0.2
            
        # 4. Content Saturation
        # High volume + Low engagement = Saturation
        vol = latest.get('content_volume', 0)
        saturation = 0.0
        # Simple heuristic: If volume high but engagement decay high
        if vol > 1000 and engagement_decay > 0.3:
            saturation = 0.7 + (engagement_decay * 0.3)
        elif vol > 500:
            saturation = 0.4
            
        return {
            "engagement_decay": engagement_decay,
            "sentiment_risk": sentiment_risk,
            "disengagement": disengagement,
            "saturation": saturation,
            "drivers": {
                "engagement": "High Decay" if engagement_decay > 0.5 else "Stable",
                "sentiment": "Negative Shift" if sentiment_risk > 0.4 else "Neutral/Positive",
                "influencer": "Disengaging" if disengagement > 0.5 else "Active",
                "saturation": "Saturated" if saturation > 0.6 else "Healthy"
            },
            "metrics": {
                "latest_engagement": latest.get('engagement_rate', 0),
                "latest_sentiment": sent_score,
                "latest_influencer": inf_ratio
            }
        }

    def _predict_decline(self, signals: Dict) -> Dict[str, Any]:
        """
        Weighted fusion logic for decline prediction.
        """
        w_eng = 0.4
        w_sent = 0.25
        w_inf = 0.2
        w_sat = 0.15
        
        prob = (
            (signals['engagement_decay'] * w_eng) +
            (signals['sentiment_risk'] * w_sent) +
            (signals['disengagement'] * w_inf) +
            (signals['saturation'] * w_sat)
        )
        
        # Cap at 0.99
        prob = min(prob, 0.99)
        
        # Lifecycle Stage
        if prob > 0.8: stage = "Collapse"
        elif prob > 0.5: stage = "Decline"
        elif prob > 0.2: stage = "Peak"
        else: stage = "Growth"
        
        # Health Score (Inverse of decline prob, scaled)
        health = (1.0 - prob) * 100
        
        # ETA Calculation (Heuristic)
        if stage == "Collapse": eta = "1-3 days"
        elif stage == "Decline": eta = "5-10 days"
        elif stage == "Peak": eta = "15-20 days"
        else: eta = "N/A (Growth Phase)"
        
        return {
            "decline_probability": round(prob, 2),
            "lifecycle_stage": stage,
            "health_score": round(health, 1),
            "collapse_eta_days": eta
        }

    def _generate_explainable_insights(self, signals: Dict, prediction: Dict) -> str:
        """
        Generate human-readable reasoning.
        """
        reasons = []
        
        if signals['engagement_decay'] > 0.4:
            reasons.append("Engagement is dropping rapidly, indicating audience fatigue.")
        if signals['sentiment_risk'] > 0.4:
            reasons.append("Sentiment has turned negative, suggesting brand reputation risks.")
        if signals['disengagement'] > 0.4:
            reasons.append("Key influencers are withdrawing from the campaign.")
        if signals['saturation'] > 0.6:
            reasons.append("Content volume is too high relative to engagement (Saturation).")
            
        if not reasons:
            reasons.append("Campaign metrics are currently stable.")
            
        stage_info = f"The campaign is in the {prediction['lifecycle_stage']} phase."
        
        return f"{stage_info} {' '.join(reasons)}"

    def _get_graph_signals(self, df: pd.DataFrame, prediction: Dict) -> Dict[str, List]:
        """
        Prepare time-series arrays.
        """
        # Ensure date format
        dates = df['date'].tolist() if 'date' in df.columns else range(len(df))
        
        # Simple projection for decline curve
        decline_curve = [prediction['decline_probability']] * len(df) # Flat line for now or historical if we tracked it
        
        return {
            "engagement_trend": df['engagement_rate'].tolist(),
            "sentiment_trend": df['sentiment_score'].tolist(),
            "influencer_trend": df['influencer_participation_ratio'].tolist(),
            "decline_curve": decline_curve,
            "dates": dates
        }

# Singleton instance
trend_agent = TrendDeclineAgent()

# Hooks
def analyze_brand_trend(data): return trend_agent.analyze_brand_trend(data)
