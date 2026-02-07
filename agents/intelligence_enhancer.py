"""
Intelligence Enhancement Module
Advanced features for explainability and decision intelligence.
Extends existing decline predictor with confidence, ranking, and risk classification.
"""

import numpy as np
from typing import Dict, List, Tuple


class IntelligenceEnhancer:
    """
    Enhances AI predictions with confidence scoring, driver ranking, and risk classification.
    """
    
    def __init__(self):
        self.name = "Intelligence Enhancer"
        
        # Risk classification thresholds
        self.RISK_TIERS = {
            'Low Risk': (0, 30),
            'Moderate Risk': (31, 60),
            'High Risk': (61, 80),
            'Critical Decline': (81, 100)
        }
    
    def calculate_prediction_confidence(self, prediction_data: Dict, signal_data: Dict) -> Dict:
        """
        Calculate confidence score based on signal agreement, data completeness, and volatility.
        
        Args:
            prediction_data (dict): Decline prediction results
            signal_data (dict): Raw signal agent outputs
        
        Returns:
            dict: Confidence analysis
        """
        print(f"[{self.name}] Calculating prediction confidence...")
        
        # Factor 1: Signal Agreement (0-100)
        signal_agreement = self._calculate_signal_agreement(prediction_data)
        
        # Factor 2: Data Completeness (0-100)
        data_completeness = self._calculate_data_completeness(signal_data)
        
        # Factor 3: Signal Volatility (0-100, inverse - lower volatility = higher confidence)
        signal_volatility_score = self._calculate_volatility_score(signal_data)
        
        # Weighted confidence calculation
        confidence_score = (
            signal_agreement * 0.40 +
            data_completeness * 0.35 +
            signal_volatility_score * 0.25
        )
        
        # Determine confidence level
        if confidence_score >= 80:
            confidence_level = "Very High"
        elif confidence_score >= 65:
            confidence_level = "High"
        elif confidence_score >= 50:
            confidence_level = "Moderate"
        else:
            confidence_level = "Low"
        
        return {
            "confidence_score": round(confidence_score, 2),
            "confidence_level": confidence_level,
            "factors": {
                "signal_agreement": round(signal_agreement, 2),
                "data_completeness": round(data_completeness, 2),
                "signal_stability": round(signal_volatility_score, 2)
            },
            "reliability": "High" if confidence_score >= 70 else "Medium" if confidence_score >= 50 else "Low"
        }
    
    def _calculate_signal_agreement(self, prediction_data: Dict) -> float:
        """
        Calculate how well signals agree on decline direction.
        """
        signal_scores = prediction_data.get('signal_scores', {})
        
        if not signal_scores:
            return 50.0  # Neutral
        
        scores = list(signal_scores.values())
        
        # Calculate coefficient of variation (lower = more agreement)
        mean_score = np.mean(scores)
        if mean_score == 0:
            return 100.0
        
        std_score = np.std(scores)
        cv = std_score / mean_score
        
        # Convert to agreement score (0-100, lower CV = higher agreement)
        agreement = max(0, 100 - (cv * 50))
        
        return min(100, agreement)
    
    def _calculate_data_completeness(self, signal_data: Dict) -> float:
        """
        Calculate data completeness score.
        """
        expected_signals = ['engagement', 'sentiment', 'influencers', 'saturation']
        present_signals = sum(1 for signal in expected_signals if signal in signal_data)
        
        completeness = (present_signals / len(expected_signals)) * 100
        
        return completeness
    
    def _calculate_volatility_score(self, signal_data: Dict) -> float:
        """
        Calculate signal volatility score (inverse - lower volatility = higher score).
        """
        # Check for volatility indicators in signal data
        volatility_indicators = []
        
        if 'sentiment' in signal_data:
            volatility = signal_data['sentiment'].get('metrics', {}).get('sentiment_volatility', 0)
            volatility_indicators.append(min(volatility * 10, 100))  # Scale to 0-100
        
        if 'engagement' in signal_data:
            decay_speed = signal_data['engagement'].get('decay_speed', 'moderate')
            decay_scores = {'slow': 20, 'moderate': 50, 'rapid': 80}
            volatility_indicators.append(decay_scores.get(decay_speed, 50))
        
        if not volatility_indicators:
            return 70.0  # Default moderate stability
        
        # Average volatility
        avg_volatility = np.mean(volatility_indicators)
        
        # Invert: lower volatility = higher confidence
        stability_score = 100 - avg_volatility
        
        return max(0, stability_score)
    
    def rank_decline_drivers(self, prediction_data: Dict) -> List[Dict]:
        """
        Rank decline drivers by weighted impact contribution.
        
        Args:
            prediction_data (dict): Prediction results with weighted contributions
        
        Returns:
            list: Ranked drivers with contribution percentages
        """
        print(f"[{self.name}] Ranking decline drivers...")
        
        weighted_contributions = prediction_data.get('weighted_contributions', {})
        
        if not weighted_contributions:
            return []
        
        # Map to readable names
        driver_names = {
            'engagement_weight': 'Engagement Decline',
            'influencer_weight': 'Influencer Disengagement',
            'sentiment_weight': 'Sentiment Shift',
            'saturation_weight': 'Content Saturation'
        }
        
        # Create ranked list
        ranked = []
        for driver_key, contribution in weighted_contributions.items():
            ranked.append({
                'driver': driver_names.get(driver_key, driver_key),
                'contribution': contribution,
                'contribution_percentage': round((contribution / prediction_data.get('decline_probability', 1)) * 100, 1)
            })
        
        # Sort by contribution (descending)
        ranked.sort(key=lambda x: x['contribution'], reverse=True)
        
        # Add rank numbers
        for i, item in enumerate(ranked, 1):
            item['rank'] = i
        
        return ranked
    
    def classify_risk(self, decline_probability: float) -> Dict:
        """
        Map decline probability to human-readable risk tier.
        
        Args:
            decline_probability (float): Decline probability (0-100)
        
        Returns:
            dict: Risk classification
        """
        print(f"[{self.name}] Classifying risk level...")
        
        # Determine risk tier
        risk_label = "Unknown"
        tier_range = (0, 0)
        
        for tier, (min_val, max_val) in self.RISK_TIERS.items():
            if min_val <= decline_probability <= max_val:
                risk_label = tier
                tier_range = (min_val, max_val)
                break
        
        # Determine urgency
        if decline_probability >= 81:
            urgency = "Immediate Action Required"
            action_timeline = "Within 24-48 hours"
        elif decline_probability >= 61:
            urgency = "Urgent"
            action_timeline = "Within 1 week"
        elif decline_probability >= 31:
            urgency = "Moderate"
            action_timeline = "Within 2-4 weeks"
        else:
            urgency = "Low"
            action_timeline = "Routine monitoring"
        
        return {
            "risk_label": risk_label,
            "risk_tier_range": tier_range,
            "decline_probability": round(decline_probability, 2),
            "urgency": urgency,
            "action_timeline": action_timeline,
            "severity_indicator": self._get_severity_emoji(risk_label)
        }
    
    def _get_severity_emoji(self, risk_label: str) -> str:
        """
        Get visual severity indicator.
        """
        emoji_map = {
            'Low Risk': '✅',
            'Moderate Risk': '⚠️',
            'High Risk': '🔴',
            'Critical Decline': '🚨'
        }
        return emoji_map.get(risk_label, '❓')
    
    def detect_lifecycle_stage(self, prediction_data: Dict, timeseries_data: Dict = None) -> Dict:
        """
        Generate lifecycle curve classification with transition timestamps.
        
        Args:
            prediction_data (dict): Prediction results
            timeseries_data (dict): Optional time-series data
        
        Returns:
            dict: Lifecycle visualization data
        """
        print(f"[{self.name}] Detecting lifecycle stage...")
        
        current_stage = prediction_data.get('lifecycle_stage', 'Unknown')
        decline_probability = prediction_data.get('decline_probability', 0)
        
        # Stage progression
        stage_progression = [
            'Growth',
            'Peak',
            'Early Decline',
            'Rapid Collapse',
            'Dead Trend'
        ]
        
        # Find current stage index
        current_index = stage_progression.index(current_stage) if current_stage in stage_progression else -1
        
        # Predict next stage
        next_stage = None
        if current_index >= 0 and current_index < len(stage_progression) - 1:
            next_stage = stage_progression[current_index + 1]
        
        # Estimate stage stability (how long in current stage)
        if decline_probability < 30:
            stage_stability = "Stable"
            transition_risk = "Low"
        elif decline_probability < 60:
            stage_stability = "Transitioning"
            transition_risk = "Moderate"
        else:
            stage_stability = "Unstable"
            transition_risk = "High"
        
        return {
            "current_stage": current_stage,
            "stage_index": current_index + 1,
            "total_stages": len(stage_progression),
            "next_stage": next_stage,
            "stage_stability": stage_stability,
            "transition_risk": transition_risk,
            "stage_progression": stage_progression,
            "lifecycle_visualization": {
                "x_axis": "Time Period",
                "y_axis": "Trend Activity",
                "current_position": current_index + 1,
                "curve_type": "decline" if decline_probability > 50 else "growth"
            }
        }


# Test the enhancer
if __name__ == "__main__":
    print("🧪 Testing Intelligence Enhancer\n")
    
    # Sample prediction data
    sample_prediction = {
        'decline_probability': 67.5,
        'lifecycle_stage': 'Early Decline',
        'signal_scores': {
            'engagement_score': 55.0,
            'influencer_score': 45.0,
            'sentiment_score': 32.0,
            'saturation_score': 75.0
        },
        'weighted_contributions': {
            'engagement_weight': 19.25,
            'influencer_weight': 11.25,
            'sentiment_weight': 6.4,
            'saturation_weight': 15.0
        }
    }
    
    sample_signals = {
        'engagement': {'decay_speed': 'rapid'},
        'sentiment': {'metrics': {'sentiment_volatility': 0.15}},
        'influencers': {},
        'saturation': {}
    }
    
    enhancer = IntelligenceEnhancer()
    
    # Test confidence scoring
    confidence = enhancer.calculate_prediction_confidence(sample_prediction, sample_signals)
    print(f"✅ Confidence Score: {confidence['confidence_score']}%")
    print(f"   Level: {confidence['confidence_level']}")
    print(f"   Factors: {confidence['factors']}")
    
    # Test driver ranking
    ranking = enhancer.rank_decline_drivers(sample_prediction)
    print(f"\n✅ Driver Ranking:")
    for driver in ranking:
        print(f"   {driver['rank']}. {driver['driver']}: {driver['contribution_percentage']}%")
    
    # Test risk classification
    risk = enhancer.classify_risk(sample_prediction['decline_probability'])
    print(f"\n✅ Risk Classification: {risk['severity_indicator']} {risk['risk_label']}")
    print(f"   Urgency: {risk['urgency']}")
    print(f"   Timeline: {risk['action_timeline']}")
    
    # Test lifecycle detection
    lifecycle = enhancer.detect_lifecycle_stage(sample_prediction)
    print(f"\n✅ Lifecycle Stage: {lifecycle['current_stage']}")
    print(f"   Next Stage: {lifecycle['next_stage']}")
    print(f"   Stability: {lifecycle['stage_stability']}")
    
    print("\n✅ Intelligence Enhancer test complete!")
