"""
Enhanced Orchestrator
Integrates all intelligence enhancements into unified analysis pipeline.
Extends existing orchestrator with advanced decision intelligence features.
"""

import sys
sys.path.append('.')

import pandas as pd
from typing import Dict, Optional, List

from agents.orchestrator import TrendOrchestrator
from agents.intelligence_enhancer import IntelligenceEnhancer
from agents.platform_analyzer import PlatformAnalyzer
from agents.executive_intelligence import ExecutiveIntelligence


class EnhancedOrchestrator:
    """
    Enhanced orchestrator with full decision intelligence capabilities.
    Extends base orchestrator with confidence scoring, platform comparison,
    executive summaries, and advanced early warnings.
    """
    
    def __init__(self):
        self.name = "Enhanced Orchestrator"
        
        # Core orchestrator
        self.base_orchestrator = TrendOrchestrator()
        
        # Enhancement modules
        self.intelligence_enhancer = IntelligenceEnhancer()
        self.platform_analyzer = PlatformAnalyzer()
        self.executive_intelligence = ExecutiveIntelligence()
    
    def analyze_trend_enhanced(self, data: pd.DataFrame, trend_name: Optional[str] = None) -> Dict:
        """
        Complete enhanced trend analysis with all intelligence features.
        
        Args:
            data (pd.DataFrame): Trend time-series data
            trend_name (str): Optional trend name
        
        Returns:
            dict: Enhanced unified analysis with all intelligence features
        """
        print(f"\n[{self.name}] Running enhanced analysis...")
        
        # STEP 1: Run base orchestrator analysis
        print(f"  → Running base analysis...")
        base_analysis = self.base_orchestrator.analyze_trend(data, trend_name)
        
        prediction = base_analysis.get('prediction', {})
        signal_details = base_analysis.get('signal_details', {})
        
        # STEP 2: Calculate prediction confidence
        print(f"  → Calculating confidence score...")
        confidence_analysis = self.intelligence_enhancer.calculate_prediction_confidence(
            prediction,
            signal_details
        )
        
        # STEP 3: Rank decline drivers
        print(f"  → Ranking decline drivers...")
        driver_ranking = self.intelligence_enhancer.rank_decline_drivers(prediction)
        
        # STEP 4: Classify risk
        print(f"  → Classifying risk level...")
        risk_classification = self.intelligence_enhancer.classify_risk(
            prediction.get('decline_probability', 0)
        )
        
        # STEP 5: Detect lifecycle stage details
        print(f"  → Detecting lifecycle visualization data...")
        lifecycle_visualization = self.intelligence_enhancer.detect_lifecycle_stage(prediction)
        
        # STEP 6: Compare platforms (if data available)
        print(f"  → Analyzing platform comparison...")
        platform_comparison = self.platform_analyzer.compare_platforms(data, trend_name)
        
        # STEP 7: Enhance early warning
        print(f"  → Enhancing early warning system...")
        enhanced_early_warning = self.executive_intelligence.enhance_early_warning(
            prediction.get('early_warning', {}),
            signal_details,
            prediction
        )
        
        # STEP 8: Build enhanced unified output
        print(f"  → Building enhanced unified output...")
        enhanced_output = self._build_enhanced_output(
            base_analysis,
            confidence_analysis,
            driver_ranking,
            risk_classification,
            lifecycle_visualization,
            platform_comparison,
            enhanced_early_warning
        )
        
        # STEP 9: Generate executive summary
        print(f"  → Generating executive summary...")
        executive_summary = self.executive_intelligence.generate_executive_summary(enhanced_output)
        enhanced_output['executive_summary'] = executive_summary
        
        print(f"[{self.name}] ✅ Enhanced analysis complete")
        
        return enhanced_output
    
    def _build_enhanced_output(
        self,
        base_analysis: Dict,
        confidence_analysis: Dict,
        driver_ranking: List,
        risk_classification: Dict,
        lifecycle_visualization: Dict,
        platform_comparison: Dict,
        enhanced_early_warning: Dict
    ) -> Dict:
        """
        Build enhanced unified output schema.
        """
        prediction = base_analysis.get('prediction', {})
        
        # Start with base structure
        enhanced = {
            # Core fields
            "trend_name": base_analysis.get('metadata', {}).get('trend_name', 'Unknown'),
            "decline_probability": prediction.get('decline_probability', 0),
            "lifecycle_stage": prediction.get('lifecycle_stage', 'Unknown'),
            "days_to_collapse": prediction.get('days_to_collapse', 'Unknown'),
            
            # Enhanced fields (NEW!)
            "confidence_analysis": confidence_analysis,
            "risk_classification": risk_classification,
            "driver_ranking": driver_ranking,
            "lifecycle_visualization": lifecycle_visualization,
            "platform_comparison": platform_comparison,
            
            # Enhanced early warning (UPGRADED)
            "early_warning": enhanced_early_warning,
            
            # Existing fields
            "decline_drivers": self._build_decline_drivers(base_analysis),
            "narrative_explanation": base_analysis.get('narrative', {}).get('narrative_explanation', ''),
            "strategy_recommendations": base_analysis.get('narrative', {}).get('strategy_recommendations', []),
            "simulation_results": {},
            
            # Prediction details
            "prediction": {
                "risk_level": prediction.get('risk_level', 'Unknown'),
                "confidence": confidence_analysis.get('confidence_score', 0),
                "confidence_level": confidence_analysis.get('confidence_level', 'Unknown'),
                "contributing_factors": prediction.get('contributing_factors', [])
            },
            
            # Metadata
            "metadata": base_analysis.get('metadata', {}),
            "alerts": base_analysis.get('alerts', [])
        }
        
        return enhanced
    
    def _build_decline_drivers(self, base_analysis: Dict) -> Dict:
        """
        Build decline drivers from base analysis.
        """
        signal_details = base_analysis.get('signal_details', {})
        drivers = {}
        
        if signal_details.get('engagement'):
            drivers['engagement'] = {
                "decline_percent": signal_details['engagement'].get('engagement_decline_percent', 0),
                "risk_level": signal_details['engagement'].get('risk_level', 'Unknown')
            }
        
        if signal_details.get('sentiment'):
            drivers['sentiment'] = {
                "shift": signal_details['sentiment'].get('sentiment_shift', 'Unknown'),
                "impact_level": signal_details['sentiment'].get('impact_level', 'Unknown')
            }
        
        if signal_details.get('influencer'):
            drivers['influencer'] = {
                "participation_drop": signal_details['influencer'].get('participation_drop_percent', 0),
                "disengagement": signal_details['influencer'].get('disengagement_status', 'Unknown')
            }
        
        if signal_details.get('saturation'):
            drivers['saturation'] = {
                "saturation_score": signal_details['saturation'].get('saturation_score', 0),
                "fatigue_detected": signal_details['saturation'].get('fatigue_detected', False)
            }
        
        return drivers


# Convenience function for direct use
def analyze_trend_enhanced(data: pd.DataFrame, trend_name: Optional[str] = None) -> Dict:
    """
    Analyze trend with all enhanced intelligence features.
    
    Args:
        data (pd.DataFrame): Trend time-series data
        trend_name (str): Optional trend name
    
    Returns:
        dict: Complete enhanced analysis
    """
    orchestrator = EnhancedOrchestrator()
    return orchestrator.analyze_trend_enhanced(data, trend_name)


# Test the enhanced orchestrator
if __name__ == "__main__":
    print("🧪 Testing Enhanced Orchestrator\n")
    
    from utils.data_generator import generate_trend_data
    
    # Generate sample data
    print("📊 Generating sample trend data...")
    trend_data = generate_trend_data("Enhanced Test Trend", total_days=60)
    
    # Run enhanced analysis
    print("\n🚀 Running enhanced analysis...")
    results = analyze_trend_enhanced(trend_data, "Enhanced Test Trend")
    
    # Display results
    print(f"\n{'='*70}")
    print("ENHANCED ANALYSIS RESULTS")
    print('='*70)
    
    print(f"\n📊 Core Metrics:")
    print(f"  • Trend: {results['trend_name']}")
    print(f"  • Decline Probability: {results['decline_probability']}%")
    print(f"  • Lifecycle Stage: {results['lifecycle_stage']}")
    
    print(f"\n🎯 Confidence Analysis:")
    conf = results['confidence_analysis']
    print(f"  • Confidence Score: {conf['confidence_score']}%")
    print(f"  • Confidence Level: {conf['confidence_level']}")
    print(f"  • Reliability: {conf['reliability']}")
    
    print(f"\n⚠️  Risk Classification:")
    risk = results['risk_classification']
    print(f"  • Risk Label: {risk['severity_indicator']} {risk['risk_label']}")
    print(f"  • Urgency: {risk['urgency']}")
    print(f"  • Action Timeline: {risk['action_timeline']}")
    
    print(f"\n📈 Driver Ranking:")
    for driver in results['driver_ranking']:
        print(f"  {driver['rank']}. {driver['driver']}: {driver['contribution_percentage']}%")
    
    print(f"\n🔔 Enhanced Early Warning:")
    ew = results['early_warning']
    print(f"  • Warning Level: {ew['warning_level']}")
    print(f"  • Active Warnings: {ew['warning_count']}")
    print(f"  • Severity Score: {ew.get('severity_score', 'N/A')}/100")
    if ew.get('collapse_window'):
        print(f"  • Collapse Window: {ew['collapse_window']['estimated_days']} days")
    
    print(f"\n🔄 Lifecycle Visualization:")
    lc = results['lifecycle_visualization']
    print(f"  • Current Stage: {lc['current_stage']}")
    print(f"  • Next Stage: {lc['next_stage']}")
    print(f"  • Stability: {lc['stage_stability']}")
    
    print(f"\n💼 Executive Summary:")
    exec_sum = results['executive_summary']
    print(f"  • Health Score: {exec_sum['health_icon']} {exec_sum['trend_health_score']}/100")
    print(f"  • Health Status: {exec_sum['health_status']}")
    print(f"  • Revenue Impact: {exec_sum['revenue_impact_proxy']['impact_level']}")
    print(f"  • Marketing Urgency: {exec_sum['marketing_action_urgency']['urgency_level']}")
    
    print(f"\n💡 Key Insights:")
    for insight in exec_sum['key_insights']:
        print(f"  • {insight}")
    
    print(f"\n✅ Enhanced Orchestrator test complete!")
