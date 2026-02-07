"""
AI Intelligence Layer API
Backend integration functions for FastAPI consumption.
Provides callable functions with structured JSON outputs.
"""

import os
import pandas as pd
from typing import Dict, Optional, List

try:
    from agents.orchestrator import TrendOrchestrator
    from agents.narrative_agent import NarrativeAgent
    from agents.simulation_agent import TrendSimulationAgent
    from utils.data_generator import generate_trend_data
except ImportError:
    # Fallback for different import paths
    import sys
    sys.path.append('.')
    from agents.orchestrator import TrendOrchestrator
    from agents.narrative_agent import NarrativeAgent
    from agents.simulation_agent import TrendSimulationAgent
    from utils.data_generator import generate_trend_data


class AIIntelligenceLayer:
    """
    Unified AI Intelligence Layer for trend decline prediction.
    Provides standardized API functions for backend consumption.
    """
    
    def __init__(self, featherless_api_key: Optional[str] = None):
        """
        Initialize AI intelligence layer with all agents.
        
        Args:
            featherless_api_key (str): Optional API key for Featherless AI
        """
        self.orchestrator = TrendOrchestrator()
        self.narrative_agent = NarrativeAgent(api_key=featherless_api_key)
        self.simulation_agent = TrendSimulationAgent()
    
    def analyze_trend(self, data: pd.DataFrame, trend_name: Optional[str] = None) -> Dict:
        """
        Complete trend analysis with all agents.
        
        Args:
            data (pd.DataFrame): Trend time-series data
            trend_name (str): Optional trend name
        
        Returns:
            dict: Unified analysis results in standardized format
        """
        # Run orchestrator
        orchestrator_results = self.orchestrator.analyze_trend(data, trend_name)
        
        # Generate narrative
        narrative_results = self.narrative_agent.generate(orchestrator_results)
        
        # Build unified output
        unified_output = self._build_unified_output(
            orchestrator_results,
            narrative_results
        )
        
        return unified_output
    
    def predict_decline(self, data: pd.DataFrame) -> Dict:
        """
        Predict trend decline probability.
        
        Args:
            data (pd.DataFrame): Trend data
        
        Returns:
            dict: Decline prediction in standardized format
        """
        # Run full analysis
        results = self.analyze_trend(data)
        
        # Extract prediction-specific data
        return {
            "decline_probability": results['decline_probability'],
            "lifecycle_stage": results['lifecycle_stage'],
            "risk_level": results['prediction']['risk_level'],
            "days_to_collapse": results['days_to_collapse'],
            "early_warning": results['early_warning'],
            "confidence": results['prediction']['confidence']
        }
    
    def generate_trend_narrative(self, analysis_data: Dict) -> Dict:
        """
        Generate AI narrative explanation from analysis data.
        
        Args:
            analysis_data (dict): Trend analysis data
        
        Returns:
            dict: Narrative explanation
        """
        narrative_result = self.narrative_agent.generate(analysis_data)
        
        return {
            "narrative_explanation": narrative_result['narrative_explanation'],
            "key_insights": narrative_result.get('key_insights', []),
            "tone": narrative_result.get('tone', 'informative')
        }
    
    def simulate_trend_recovery(self, baseline_data: Dict, scenario_params: Dict, scenario_name: str = "Recovery Scenario") -> Dict:
        """
        Simulate what-if scenario for trend recovery.
        
        Args:
            baseline_data (dict): Original trend analysis
            scenario_params (dict): Modified parameters
            scenario_name (str): Name of scenario
        
        Returns:
            dict: Simulation results with AI explanation
        """
        # Run simulation
        simulation_result = self.simulation_agent.simulate(
            baseline_data,
            scenario_params,
            scenario_name
        )
        
        # Generate AI explanation
        explanation = self.narrative_agent.generate_simulation_explanation(simulation_result)
        
        return {
            "scenario_name": simulation_result['scenario_name'],
            "original_decline_probability": simulation_result['original_decline_probability'],
            "new_decline_probability": simulation_result['new_decline_probability'],
            "original_lifecycle_stage": simulation_result['original_lifecycle_stage'],
            "new_lifecycle_stage": simulation_result['new_lifecycle_stage'],
            "impact_analysis": simulation_result['impact_analysis'],
            "recovery_potential": simulation_result['recovery_potential'],
            "explanation": explanation,
            "parameter_changes": simulation_result['parameter_changes']
        }
    
    def _build_unified_output(self, orchestrator_results: Dict, narrative_results: Dict) -> Dict:
        """
        Build unified output schema for API consumption.
        
        Args:
            orchestrator_results (dict): Orchestrator output
            narrative_results (dict): Narrative agent output
        
        Returns:
            dict: Standardized unified output
        """
        prediction = orchestrator_results.get('prediction', {})
        early_warning = prediction.get('early_warning', {})
        signal_details = orchestrator_results.get('signal_details', {})
        
        # Build decline drivers
        decline_drivers = {}
        
        if signal_details.get('engagement'):
            decline_drivers['engagement'] = {
                "decline_percent": signal_details['engagement'].get('engagement_decline_percent', 0),
                "risk_level": signal_details['engagement'].get('risk_level', 'Unknown')
            }
        
        if signal_details.get('sentiment'):
            decline_drivers['sentiment'] = {
                "shift": signal_details['sentiment'].get('sentiment_shift', 'Unknown'),
                "impact_level": signal_details['sentiment'].get('impact_level', 'Unknown')
            }
        
        if signal_details.get('influencer'):
            decline_drivers['influencer'] = {
                "participation_drop": signal_details['influencer'].get('participation_drop_percent', 0),
                "disengagement": signal_details['influencer'].get('disengagement_status', 'Unknown')
            }
        
        if signal_details.get('saturation'):
            decline_drivers['saturation'] = {
                "saturation_score": signal_details['saturation'].get('saturation_score', 0),
                "fatigue_detected": signal_details['saturation'].get('fatigue_detected', False)
            }
        
        # Build unified schema
        return {
            "trend_name": orchestrator_results.get('metadata', {}).get('trend_name', 'Unknown'),
            "decline_probability": prediction.get('decline_probability', 0),
            "lifecycle_stage": prediction.get('lifecycle_stage', 'Unknown'),
            "days_to_collapse": prediction.get('days_to_collapse', 'Unknown'),
            "early_warning": {
                "warning_level": early_warning.get('warning_level', 'Low'),
                "active_warnings": early_warning.get('active_warnings', []),
                "warning_count": early_warning.get('warning_count', 0),
                "recommended_action": early_warning.get('recommended_action', '')
            },
            "decline_drivers": decline_drivers,
            "narrative_explanation": narrative_results.get('narrative_explanation', ''),
            "strategy_recommendations": narrative_results.get('strategy_recommendations', []),
            "simulation_results": {},  # Populated when simulation is run
            "prediction": {
                "risk_level": prediction.get('risk_level', 'Unknown'),
                "confidence": prediction.get('confidence', 0),
                "contributing_factors": prediction.get('contributing_factors', [])
            },
            "metadata": orchestrator_results.get('metadata', {}),
            "alerts": orchestrator_results.get('alerts', [])
        }


# Convenience functions for direct API consumption

def analyze_trend(data: pd.DataFrame, trend_name: Optional[str] = None, api_key: Optional[str] = None) -> Dict:
    """
    Analyze trend and return complete insights.
    
    Args:
        data (pd.DataFrame): Trend time-series data
        trend_name (str): Optional trend name
        api_key (str): Optional Featherless AI API key
    
    Returns:
        dict: Complete trend analysis
    """
    ai_layer = AIIntelligenceLayer(featherless_api_key=api_key)
    return ai_layer.analyze_trend(data, trend_name)


def predict_decline(data: pd.DataFrame, api_key: Optional[str] = None) -> Dict:
    """
    Predict trend decline probability.
    
    Args:
        data (pd.DataFrame): Trend data
        api_key (str): Optional Featherless AI API key
    
    Returns:
        dict: Decline prediction
    """
    ai_layer = AIIntelligenceLayer(featherless_api_key=api_key)
    return ai_layer.predict_decline(data)


def generate_trend_narrative(analysis_data: Dict, api_key: Optional[str] = None) -> Dict:
    """
    Generate AI narrative from analysis data.
    
    Args:
        analysis_data (dict): Trend analysis data
        api_key (str): Optional Featherless AI API key
    
    Returns:
        dict: Narrative explanation
    """
    ai_layer = AIIntelligenceLayer(featherless_api_key=api_key)
    return ai_layer.generate_trend_narrative(analysis_data)


def simulate_trend_recovery(baseline_data: Dict, scenario_params: Dict, scenario_name: str = "Recovery Scenario", api_key: Optional[str] = None) -> Dict:
    """
    Simulate what-if recovery scenario.
    
    Args:
        baseline_data (dict): Original analysis
        scenario_params (dict): Modified parameters
        scenario_name (str): Scenario name
        api_key (str): Optional Featherless AI API key
    
    Returns:
        dict: Simulation results with explanation
    """
    ai_layer = AIIntelligenceLayer(featherless_api_key=api_key)
    return ai_layer.simulate_trend_recovery(baseline_data, scenario_params, scenario_name)


# Test the API layer
if __name__ == "__main__":
    print("🧪 Testing AI Intelligence Layer API\n")
    
    # Generate sample data
    print("📊 Generating sample trend data...")
    trend_data = generate_trend_data("Test Trend", total_days=60, export_json=False)
    
    # Test analyze_trend function
    print("\n🔍 Test 1: analyze_trend()")
    results = analyze_trend(trend_data, "Viral Dance Challenge")
    
    print(f"✅ Trend: {results['trend_name']}")
    print(f"📊 Decline Probability: {results['decline_probability']}%")
    print(f"🔄 Lifecycle: {results['lifecycle_stage']}")
    print(f"⚠️  Early Warning: {results['early_warning']['warning_level']}")
    
    # Test predict_decline function
    print("\n🔍 Test 2: predict_decline()")
    prediction = predict_decline(trend_data)
    print(f"✅ Decline: {prediction['decline_probability']}%")
    print(f"⏰ Days to Collapse: {prediction['days_to_collapse']}")
    
    print("\n✅ AI Intelligence Layer API tests complete!")
