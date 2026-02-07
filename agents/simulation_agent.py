"""
Simulation Agent
Runs what-if scenarios and simulations for trend trajectory forecasting.
Tests modified parameters to predict recovery or collapse timelines.
"""

import numpy as np
import pandas as pd
from typing import Dict, Optional

try:
    from agents.decline_predictor import DeclinePredictor
except ImportError:
    from decline_predictor import DeclinePredictor


class TrendSimulationAgent:
    def __init__(self):
        self.name = "Trend Simulation Agent"
        self.description = "Simulates trend scenarios and forecasts outcomes"
        self.predictor = DeclinePredictor()
    
    def simulate(self, baseline_data: Dict, modified_params: Dict, scenario_name: str = "Modified Scenario") -> Dict:
        """
        Runs simulation with modified parameters.
        
        Args:
            baseline_data (dict): Original trend analysis data
            modified_params (dict): Parameters to modify (influencer_ratio, engagement_rate, etc.)
            scenario_name (str): Name of the simulation scenario
        
        Returns:
            dict: Simulation results with new predictions
        """
        print(f"[{self.name}] Running '{scenario_name}' simulation...")
        
        # Get baseline prediction
        baseline_prediction = baseline_data.get('decline_prediction', {})
        original_prob = baseline_prediction.get('decline_probability', 0)
        
        # Create modified signal data
        modified_signals = self._apply_modifications(baseline_data, modified_params)
        
        # Recalculate prediction with modified data
        new_prediction = self.predictor.predict(modified_signals)
        
        # Calculate impact
        impact_analysis = self._analyze_impact(
            original_prob,
            new_prediction.get('decline_probability', 0),
            modified_params
        )
        
        return {
            "agent": self.name,
            "status": "success",
            "scenario_name": scenario_name,
            "original_decline_probability": round(original_prob, 2),
            "new_decline_probability": round(new_prediction.get('decline_probability', 0), 2),
            "original_lifecycle_stage": baseline_prediction.get('lifecycle_stage', 'Unknown'),
            "new_lifecycle_stage": new_prediction.get('lifecycle_stage', 'Unknown'),
            "original_days_to_collapse": baseline_prediction.get('days_to_collapse', 'Unknown'),
            "new_days_to_collapse": new_prediction.get('days_to_collapse', 'Unknown'),
            "parameter_changes": modified_params,
            "impact_analysis": impact_analysis,
            "recovery_potential": self._assess_recovery_potential(impact_analysis),
            "full_prediction": new_prediction
        }
    
    def run_multiple_scenarios(self, baseline_data: Dict) -> Dict:
        """
        Run multiple predefined simulation scenarios.
        
        Args:
            baseline_data (dict): Original trend analysis
        
        Returns:
            dict: Results from all scenarios
        """
        print(f"[{self.name}] Running multiple scenario simulations...")
        
        scenarios = {
            "optimistic": {
                "params": {
                    "influencer_boost": 0.30,  # +30% influencer participation
                    "engagement_boost": 0.25,  # +25% engagement
                    "sentiment_improvement": 0.20  # +20% sentiment
                },
                "name": "Optimistic Recovery"
            },
            "realistic": {
                "params": {
                    "influencer_boost": 0.15,
                    "engagement_boost": 0.10,
                    "sentiment_improvement": 0.05
                },
                "name": "Realistic Improvement"
            },
            "pessimistic": {
                "params": {
                    "influencer_drop": -0.20,  # -20% influencers
                    "engagement_drop": -0.15,  # -15% engagement
                    "sentiment_decline": -0.10  # -10% sentiment
                },
                "name": "Pessimistic Decline"
            }
        }
        
        results = {}
        
        for scenario_id, config in scenarios.items():
            try:
                result = self.simulate(
                    baseline_data,
                    config['params'],
                    config['name']
                )
                results[scenario_id] = result
            except Exception as e:
                print(f"  ❌ {config['name']} failed: {e}")
                results[scenario_id] = None
        
        return {
            "agent": self.name,
            "status": "success",
            "scenarios": results,
            "most_likely_outcome": self._determine_most_likely(results),
            "best_case": results.get('optimistic'),
            "worst_case": results.get('pessimistic')
        }
    
    def _apply_modifications(self, baseline_data: Dict, modified_params: Dict) -> Dict:
        """
        Apply parameter modifications to create modified signal data.
        
        Args:
            baseline_data (dict): Original data
            modified_params (dict): Parameters to modify
        
        Returns:
            dict: Modified signal data for prediction
        """
        # Copy baseline signals
        signals = {}
        
        # Get original signal data
        original_signals = baseline_data.get('signal_details', {})
        
        # Engagement modifications
        if 'engagement' in original_signals:
            eng = original_signals['engagement'].copy()
            
            if 'engagement_boost' in modified_params:
                # Reduce decline by boost percentage
                current_decline = eng.get('engagement_decline_percent', 0)
                boost = modified_params['engagement_boost']
                eng['engagement_decline_percent'] = max(0, current_decline * (1 - boost))
            
            if 'engagement_drop' in modified_params:
                current_decline = eng.get('engagement_decline_percent', 0)
                drop = abs(modified_params['engagement_drop'])
                eng['engagement_decline_percent'] = current_decline * (1 + drop)
            
            signals['engagement'] = eng
        
        # Sentiment modifications
        if 'sentiment' in original_signals:
            sent = original_signals['sentiment'].copy()
            
            if 'sentiment_improvement' in modified_params:
                # Improve sentiment change
                current_change = sent.get('metrics', {}).get('sentiment_change_percent', 0)
                improvement = modified_params['sentiment_improvement']
                
                if 'metrics' not in sent:
                    sent['metrics'] = {}
                sent['metrics']['sentiment_change_percent'] = current_change * (1 - improvement)
            
            if 'sentiment_decline' in modified_params:
                current_change = sent.get('metrics', {}).get('sentiment_change_percent', 0)
                decline = abs(modified_params['sentiment_decline'])
                
                if 'metrics' not in sent:
                    sent['metrics'] = {}
                sent['metrics']['sentiment_change_percent'] = current_change * (1 + decline)
            
            signals['sentiment'] = sent
        
        # Influencer modifications
        if 'influencers' in original_signals:
            inf = original_signals['influencers'].copy()
            
            if 'influencer_boost' in modified_params:
                drop = inf.get('participation_drop_percent', 0)
                boost = modified_params['influencer_boost']
                inf['participation_drop_percent'] = max(0, drop * (1 - boost))
                
                # Increase impact score
                score = inf.get('influence_impact_score', 50)
                inf['influence_impact_score'] = min(100, score * (1 + boost))
            
            if 'influencer_drop' in modified_params:
                drop = inf.get('participation_drop_percent', 0)
                additional_drop = abs(modified_params['influencer_drop'])
                inf['participation_drop_percent'] = drop * (1 + additional_drop)
            
            signals['influencers'] = inf
        
        # Saturation (usually doesn't change in short-term simulations)
        if 'saturation' in original_signals:
            signals['saturation'] = original_signals['saturation'].copy()
        
        return signals
    
    def _analyze_impact(self, original_prob: float, new_prob: float, params: Dict) -> Dict:
        """
        Analyze the impact of parameter changes.
        
        Args:
            original_prob (float): Original decline probability
            new_prob (float): New decline probability
            params (dict): Modified parameters
        
        Returns:
            dict: Impact analysis
        """
        change = new_prob - original_prob
        percent_change = (change / original_prob * 100) if original_prob > 0 else 0
        
        # Determine impact severity
        if change < -15:
            impact = "Significant Improvement"
        elif change < -5:
            impact = "Moderate Improvement"
        elif change < 5:
            impact = "Minimal Change"
        elif change < 15:
            impact = "Moderate Deterioration"
        else:
            impact = "Significant Deterioration"
        
        return {
            "probability_change": round(change, 2),
            "percent_change": round(percent_change, 2),
            "impact_category": impact,
            "direction": "improvement" if change < 0 else "deterioration" if change > 0 else "neutral"
        }
    
    def _assess_recovery_potential(self, impact: Dict) -> str:
        """
        Assess recovery potential based on impact.
        """
        change = impact.get('probability_change', 0)
        
        if change < -20:
            return "High"
        elif change < -10:
            return "Moderate"
        elif change < 0:
            return "Low"
        else:
            return "None"
    
    def _determine_most_likely(self, scenarios: Dict) -> str:
        """
        Determine most likely scenario outcome.
        """
        # Typically, realistic scenario is most likely
        if scenarios.get('realistic'):
            return "realistic"
        return "unknown"


# Test the agent
if __name__ == "__main__":
    print("🧪 Testing Trend Simulation Agent\n")
    
    # Sample baseline data
    baseline_data = {
        'decline_prediction': {
            'decline_probability': 67.5,
            'lifecycle_stage': 'Early Decline',
            'days_to_collapse': '15-25 days'
        },
        'signal_details': {
            'engagement': {
                'engagement_decline_percent': 55.0,
                'risk_level': 'High'
            },
            'sentiment': {
                'metrics': {'sentiment_change_percent': -30.0},
                'impact_level': 'High'
            },
            'influencers': {
                'participation_drop_percent': 45.0,
                'influence_impact_score': 35.0
            },
            'saturation': {
                'saturation_score': 75.0
            }
        }
    }
    
    agent = TrendSimulationAgent()
    
    # Test single scenario
    print("Test 1: Single scenario simulation")
    result = agent.simulate(
        baseline_data,
        {'influencer_boost': 0.30, 'engagement_boost': 0.20},
        "Influencer Re-engagement Campaign"
    )
    
    print(f"✅ Scenario: {result['scenario_name']}")
    print(f"📊 Original Decline: {result['original_decline_probability']}%")
    print(f"📊 New Decline: {result['new_decline_probability']}%")
    print(f"🔄 Impact: {result['impact_analysis']['impact_category']}")
    print(f"💡 Recovery Potential: {result['recovery_potential']}\n")
    
    # Test multiple scenarios
    print("Test 2: Multiple scenario simulation")
    multi_results = agent.run_multiple_scenarios(baseline_data)
    
    print(f"✅ Scenarios run: {len(multi_results['scenarios'])}")
    print(f"📊 Most likely outcome: {multi_results['most_likely_outcome']}")
    
    print("\n✅ Simulation Agent test complete!")
