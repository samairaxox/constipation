"""
Decline Predictor Agent
Predicts trend decline using aggregated signals from multiple agents.
Uses weighted scoring model to calculate decline probability and lifecycle stage.
"""

import numpy as np
import pandas as pd


class DeclinePredictor:
    def __init__(self):
        self.name = "Decline Predictor"
        self.description = "Predicts trend decline based on multi-signal analysis"
        
        # Signal weights (must sum to 1.0)
        self.WEIGHTS = {
            'engagement': 0.35,      # 35%
            'influencer': 0.25,      # 25%
            'sentiment': 0.20,       # 20%
            'saturation': 0.20       # 20%
        }
        
        # Lifecycle stage thresholds
        self.STAGE_THRESHOLDS = {
            'Growth': (0, 25),
            'Peak': (25, 45),
            'Early Decline': (45, 65),
            'Rapid Collapse': (65, 85),
            'Dead Trend': (85, 100)
        }
    
    def predict(self, aggregated_data):
        """
        Predicts trend decline probability and timeline.
        
        Args:
            aggregated_data (dict): Combined data from all agents
        
        Returns:
            dict: Decline prediction with probability and timeline
        """
        print(f"[{self.name}] Running decline prediction model...")
        
        # Extract agent signals
        signals = self._extract_signals(aggregated_data)
        
        # Normalize signals to 0-100 decline scores
        normalized_scores = self._normalize_signals(signals)
        
        # Calculate weighted decline probability
        decline_probability = self._calculate_weighted_score(normalized_scores)
        
        # Determine lifecycle stage
        lifecycle_stage = self._determine_lifecycle_stage(decline_probability)
        
        # Predict days to collapse
        days_to_collapse = self._estimate_days_to_collapse(
            decline_probability,
            signals,
            lifecycle_stage
        )
        
        # Assign risk level
        risk_level = self._assign_risk_level(decline_probability, lifecycle_stage)
        
        # Assign confidence score
        confidence = self._calculate_confidence(signals)
        
        # Identify contributing factors
        contributing_factors = self._identify_top_factors(normalized_scores)
        
        # Generate early warning signals
        early_warning = self._detect_early_warnings(
            decline_probability,
            normalized_scores,
            signals,
            lifecycle_stage
        )
        
        return {
            "agent": self.name,
            "status": "success",
            "decline_probability": round(decline_probability, 2),
            "lifecycle_stage": lifecycle_stage,
            "days_to_collapse": days_to_collapse,
            "risk_level": risk_level,
            "confidence": round(confidence, 2),
            "early_warning": early_warning,
            "signal_scores": {
                "engagement_score": round(normalized_scores['engagement'], 2),
                "influencer_score": round(normalized_scores['influencer'], 2),
                "sentiment_score": round(normalized_scores['sentiment'], 2),
                "saturation_score": round(normalized_scores['saturation'], 2)
            },
            "weighted_contributions": {
                "engagement_weight": round(normalized_scores['engagement'] * self.WEIGHTS['engagement'], 2),
                "influencer_weight": round(normalized_scores['influencer'] * self.WEIGHTS['influencer'], 2),
                "sentiment_weight": round(normalized_scores['sentiment'] * self.WEIGHTS['sentiment'], 2),
                "saturation_weight": round(normalized_scores['saturation'] * self.WEIGHTS['saturation'], 2)
            },
            "contributing_factors": contributing_factors,
            "recommendations": self._generate_recommendations(
                lifecycle_stage,
                decline_probability,
                contributing_factors
            ),
            "insights": self._generate_insights(
                decline_probability,
                lifecycle_stage,
                days_to_collapse,
                risk_level
            )
        }
    
    def _extract_signals(self, data):
        """
        Extract relevant signals from agent outputs.
        
        Args:
            data (dict): Aggregated agent data
        
        Returns:
            dict: Extracted signals
        """
        signals = {}
        
        # Engagement signals
        if 'engagement' in data:
            eng = data['engagement']
            signals['engagement_decline'] = eng.get('engagement_decline_percent', 0)
            signals['engagement_risk'] = eng.get('risk_level', 'Low')
            signals['decay_speed'] = eng.get('decay_speed', 'slow')
        
        # Influencer signals
        if 'influencers' in data:
            inf = data['influencers']
            signals['influencer_drop'] = inf.get('participation_drop_percent', 0)
            signals['influence_score'] = inf.get('influence_impact_score', 50)
            signals['disengagement'] = inf.get('disengagement_status', 'Stable')
        
        # Sentiment signals
        if 'sentiment' in data:
            sent = data['sentiment']
            signals['sentiment_change'] = sent.get('metrics', {}).get('sentiment_change_percent', 0)
            signals['sentiment_impact'] = sent.get('impact_level', 'Low')
            signals['sentiment_shift'] = sent.get('sentiment_shift', 'Stable')
        
        # Saturation signals
        if 'saturation' in data:
            sat = data['saturation']
            signals['saturation_level'] = sat.get('saturation_score', 0)
            signals['saturation_impact'] = sat.get('saturation_impact_level', 'Low')
            signals['repetition_risk'] = sat.get('repetition_risk', 'Low')
        
        return signals
    
    def _normalize_signals(self, signals):
        """
        Normalize different signals to 0-100 decline score scale.
        Higher score = higher decline risk.
        
        Args:
            signals (dict): Raw signals from agents
        
        Returns:
            dict: Normalized scores (0-100)
        """
        normalized = {}
        
        # Engagement Score (0-100)
        engagement_decline = signals.get('engagement_decline', 0)
        decay_multiplier = {'slow': 0.8, 'moderate': 1.0, 'rapid': 1.3}.get(
            signals.get('decay_speed', 'moderate'), 1.0
        )
        normalized['engagement'] = min(100, engagement_decline * decay_multiplier)
        
        # Influencer Score (0-100)
        influencer_drop = signals.get('influencer_drop', 0)
        influence_penalty = 100 - signals.get('influence_score', 50)
        normalized['influencer'] = (influencer_drop * 0.7) + (influence_penalty * 0.3)
        
        # Sentiment Score (0-100)
        sentiment_change = abs(signals.get('sentiment_change', 0))
        impact_multiplier = {'Low': 0.5, 'Medium': 1.0, 'High': 1.5, 'Critical': 2.0}.get(
            signals.get('sentiment_impact', 'Low'), 1.0
        )
        normalized['sentiment'] = min(100, sentiment_change * impact_multiplier)
        
        # Saturation Score (0-100)
        saturation_level = signals.get('saturation_level', 0)
        normalized['saturation'] = saturation_level  # Already 0-100
        
        return normalized
    
    def _calculate_weighted_score(self, normalized_scores):
        """
        Calculate weighted decline probability.
        
        Args:
            normalized_scores (dict): Normalized signal scores
        
        Returns:
            float: Weighted decline probability (0-100)
        """
        weighted_sum = 0
        
        for signal, weight in self.WEIGHTS.items():
            score = normalized_scores.get(signal, 0)
            weighted_sum += score * weight
        
        return weighted_sum
    
    def _determine_lifecycle_stage(self, decline_probability):
        """
        Determine lifecycle stage based on decline probability.
        
        Args:
            decline_probability (float): Overall decline probability
        
        Returns:
            str: Lifecycle stage
        """
        for stage, (min_val, max_val) in self.STAGE_THRESHOLDS.items():
            if min_val <= decline_probability < max_val:
                return stage
        
        # Edge case: exactly 100
        if decline_probability >= 85:
            return "Dead Trend"
        
        return "Unknown"
    
    def _estimate_days_to_collapse(self, probability, signals, stage):
        """
        Estimate days until trend collapse.
        
        Args:
            probability (float): Decline probability
            signals (dict): Raw signals
            stage (str): Lifecycle stage
        
        Returns:
            str or int: Estimated days or status
        """
        if stage == "Dead Trend":
            return "Already Collapsed"
        
        if stage == "Growth":
            return "60+ days"
        
        if stage == "Peak":
            return "45-60 days"
        
        # Use decay speed and current probability to estimate
        decay_speed = signals.get('decay_speed', 'moderate')
        
        if stage == "Early Decline":
            if decay_speed == "rapid":
                return "15-25 days"
            elif decay_speed == "moderate":
                return "25-35 days"
            else:
                return "35-45 days"
        
        if stage == "Rapid Collapse":
            if decay_speed == "rapid":
                return "5-10 days"
            elif decay_speed == "moderate":
                return "10-15 days"
            else:
                return "15-20 days"
        
        return "Unknown"
    
    def _assign_risk_level(self, probability, stage):
        """
        Assign overall risk level.
        
        Args:
            probability (float): Decline probability
            stage (str): Lifecycle stage
        
        Returns:
            str: Risk level
        """
        if probability >= 75 or stage in ["Rapid Collapse", "Dead Trend"]:
            return "Critical"
        elif probability >= 55 or stage == "Early Decline":
            return "High"
        elif probability >= 35 or stage == "Peak":
            return "Medium"
        else:
            return "Low"
    
    def _calculate_confidence(self, signals):
        """
        Calculate prediction confidence based on signal availability.
        
        Args:
            signals (dict): Available signals
        
        Returns:
            float: Confidence score (0-100)
        """
        # Base confidence on number of available signals
        available_signals = len(signals)
        expected_signals = 12  # Approximate expected signals
        
        signal_coverage = (available_signals / expected_signals) * 100
        
        # Adjust for signal quality/consistency
        base_confidence = min(signal_coverage, 100)
        
        return base_confidence
    
    def _identify_top_factors(self, normalized_scores):
        """
        Identify top contributing factors to decline.
        
        Args:
            normalized_scores (dict): Normalized signal scores
        
        Returns:
            list: Top factors sorted by contribution
        """
        weighted = []
        
        for signal, weight in self.WEIGHTS.items():
            score = normalized_scores.get(signal, 0)
            contribution = score * weight
            weighted.append({
                "factor": signal,
                "contribution": round(contribution, 2),
                "raw_score": round(score, 2)
            })
        
        # Sort by contribution (descending)
        weighted.sort(key=lambda x: x['contribution'], reverse=True)
        
        return weighted
    
    def _generate_recommendations(self, stage, probability, factors):
        """
        Generate actionable recommendations.
        
        Args:
            stage (str): Lifecycle stage
            probability (float): Decline probability
            factors (list): Contributing factors
        
        Returns:
            list: Recommendations
        """
        recommendations = []
        
        # Top factor
        if factors:
            top_factor = factors[0]['factor']
            
            if top_factor == 'engagement' and factors[0]['contribution'] > 20:
                recommendations.append("Boost engagement through interactive content and contests")
            
            if top_factor == 'influencer' and factors[0]['contribution'] > 15:
                recommendations.append("Re-engage key influencers with exclusive opportunities")
            
            if top_factor == 'sentiment' and factors[0]['contribution'] > 15:
                recommendations.append("Address negative sentiment through quality improvements")
            
            if top_factor == 'saturation' and factors[0]['contribution'] > 15:
                recommendations.append("Introduce fresh variations to combat content fatigue")
        
        # Stage-specific recommendations
        if stage == "Early Decline":
            recommendations.append("Monitor metrics daily and activate retention strategies")
        elif stage == "Rapid Collapse":
            recommendations.append("Urgent intervention required - consider pivot or wind-down")
        elif stage == "Peak":
            recommendations.append("Prepare for decline phase - build sustainability strategies")
        
        return recommendations if recommendations else ["Continue current strategy"]
    
    def _generate_insights(self, probability, stage, days, risk):
        """
        Generate human-readable insights.
        """
        if stage == "Dead Trend":
            return f"💀 DEAD TREND: Decline probability {probability:.1f}%. Trend has collapsed. Post-mortem analysis recommended."
        
        elif risk == "Critical":
            return f"🚨 CRITICAL: {stage} with {probability:.1f}% decline probability. Estimated collapse: {days}. Immediate action required."
        
        elif risk == "High":
            return f"⚠️ HIGH RISK: {stage} detected. Decline probability: {probability:.1f}%. Time to collapse: {days}. Activate mitigation strategies."
        
        elif risk == "Medium":
            return f"⚡ MEDIUM RISK: Currently in {stage}. Decline probability: {probability:.1f}%. Monitor closely for deterioration."
        
        else:
            return f"✅ LOW RISK: {stage} with {probability:.1f}% decline probability. Trend is healthy. Continue growth strategies."
    
    def _detect_early_warnings(self, probability, normalized_scores, signals, stage):
        """
        Detect early warning signals before visible collapse.
        
        Args:
            probability (float): Decline probability
            normalized_scores (dict): Normalized signal scores
            signals (dict): Raw signals
            stage (str): Lifecycle stage
        
        Returns:
            dict: Early warning analysis
        """
        warnings = []
        warning_threshold = 45.0  # Threshold for early warning
        
        # Check if trend is approaching critical zone
        approaching_critical = probability > warning_threshold and probability < 65
        
        # Signal-specific warnings
        if normalized_scores.get('engagement', 0) > 40:
            warnings.append("Engagement showing early decline signs")
        
        if normalized_scores.get('influencer', 0) > 35:
            warnings.append("Influencer disengagement detected")
        
        if normalized_scores.get('sentiment', 0) > 30:
            warnings.append("Sentiment deterioration observed")
        
        if normalized_scores.get('saturation', 0) > 60:
            warnings.append("Market saturation approaching critical levels")
        
        # Velocity warnings (rapid changes)
        if signals.get('decay_speed') == 'rapid':
            warnings.append("Rapid decay velocity detected - accelerated decline possible")
        
        # Combined signal warnings
        high_risk_signals = sum(1 for score in normalized_scores.values() if score > 50)
        if high_risk_signals >= 2:
            warnings.append("Multiple signals showing high risk - cascading failure possible")
        
        # Determine warning level
        if len(warnings) >= 4:
            warning_level = "Critical"
        elif len(warnings) >= 2:
            warning_level = "High"
        elif len(warnings) >= 1:
            warning_level = "Moderate"
        else:
            warning_level = "Low"
        
        # Calculate estimated days before warning threshold breach
        if probability < warning_threshold:
            days_to_warning = "Not applicable - no immediate warning"
        elif probability < 65:
            days_to_warning = "5-15 days until critical zone"
        else:
            days_to_warning = "Already in critical zone"
        
        return {
            "warning_level": warning_level,
            "warning_threshold": warning_threshold,
            "approaching_critical": approaching_critical,
            "active_warnings": warnings,
            "warning_count": len(warnings),
            "days_to_critical_zone": days_to_warning,
            "recommended_action": self._get_warning_action(warning_level)
        }
    
    def _get_warning_action(self, warning_level):
        """
        Get recommended action based on warning level.
        """
        actions = {
            "Critical": "Immediate intervention required - deploy emergency retention strategies",
            "High": "Urgent attention needed - activate mitigation measures within 48 hours",
            "Moderate": "Close monitoring required - prepare contingency plans",
            "Low": "Continue routine monitoring"
        }
        return actions.get(warning_level, "Monitor trend performance")


# Test the predictor
if __name__ == "__main__":
    print("🧪 Testing Decline Predictor\n")
    
    # Simulate aggregated agent outputs
    sample_data = {
        'engagement': {
            'engagement_decline_percent': 65.5,
            'risk_level': 'High',
            'decay_speed': 'rapid'
        },
        'influencers': {
            'participation_drop_percent': 55.2,
            'influence_impact_score': 25.3,
            'disengagement_status': 'Moderate Disengagement'
        },
        'sentiment': {
            'metrics': {'sentiment_change_percent': -32.4},
            'impact_level': 'High',
            'sentiment_shift': 'Positive → Neutral'
        },
        'saturation': {
            'saturation_score': 78.5,
            'saturation_impact_level': 'High',
            'repetition_risk': 'High'
        }
    }
    
    predictor = DeclinePredictor()
    result = predictor.predict(sample_data)
    
    print(f"✅ Status: {result['status']}")
    print(f"📊 Decline Probability: {result['decline_probability']}%")
    print(f"🔄 Lifecycle Stage: {result['lifecycle_stage']}")
    print(f"⏰ Days to Collapse: {result['days_to_collapse']}")
    print(f"⚠️  Risk Level: {result['risk_level']}")
    print(f"🎯 Confidence: {result['confidence']}%")
    print(f"\n💡 Insights: {result['insights']}")
    
    print("\n📊 Top Contributing Factors:")
    for factor in result['contributing_factors']:
        print(f"  • {factor['factor'].capitalize()}: {factor['contribution']} (score: {factor['raw_score']})")
    
    print("\n📋 Recommendations:")
    for rec in result['recommendations']:
        print(f"  • {rec}")
    
    print("\n✅ Decline Predictor test complete!")
