"""
Executive Intelligence Module
Generates executive summaries and enhanced early warning insights.
"""

import numpy as np
from typing import Dict, List, Optional


class ExecutiveIntelligence:
    """
    Generates executive-level insights and enhanced early warnings.
    """
    
    def __init__(self):
        self.name = "Executive Intelligence"
    
    def generate_executive_summary(self, analysis_data: Dict) -> Dict:
        """
        Generate high-level executive summary for dashboard display.
        
        Args:
            analysis_data (dict): Complete trend analysis
        
        Returns:
            dict: Executive summary
        """
        print(f"[{self.name}] Generating executive summary...")
        
        # Extract key metrics
        decline_prob = analysis_data.get('decline_probability', 0)
        lifecycle_stage = analysis_data.get('lifecycle_stage', 'Unknown')
        risk_label = analysis_data.get('risk_classification', {}).get('risk_label', 'Unknown')
        confidence = analysis_data.get('confidence_analysis', {}).get('confidence_score', 0)
        
        # Calculate trend health score (0-100, inverse of decline)
        trend_health_score = 100 - decline_prob
        
        # Determine health status
        if trend_health_score >= 70:
            health_status = "Excellent"
            health_icon = "🟢"
        elif trend_health_score >= 50:
            health_status = "Good"
            health_icon = "🟡"
        elif trend_health_score >= 30:
            health_status = "At Risk"
            health_icon = "🟠"
        else:
            health_status = "Critical"
            health_icon = "🔴"
        
        # Revenue impact proxy (based on decline risk and lifecycle stage)
        revenue_impact = self._calculate_revenue_impact(decline_prob, lifecycle_stage)
        
        # Marketing action urgency
        action_urgency = self._determine_action_urgency(decline_prob, lifecycle_stage)
        
        # Key insights summary
        key_insights = self._generate_key_insights(analysis_data)
        
        # Strategic recommendations (top 3)
        top_recommendations = analysis_data.get('strategy_recommendations', [])[:3]
        
        return {
            "trend_health_score": round(trend_health_score, 1),
            "health_status": health_status,
            "health_icon": health_icon,
            "decline_risk": risk_label,
            "confidence_level": analysis_data.get('confidence_analysis', {}).get('confidence_level', 'Unknown'),
            "lifecycle_stage": lifecycle_stage,
            "revenue_impact_proxy": revenue_impact,
            "marketing_action_urgency": action_urgency,
            "key_insights": key_insights,
            "top_strategic_actions": top_recommendations,
            "dashboard_metrics": {
                "health_score": round(trend_health_score, 1),
                "decline_probability": round(decline_prob, 1),
                "confidence": round(confidence, 1),
                "days_to_action": action_urgency.get('days_to_action', 'N/A')
            }
        }
    
    def _calculate_revenue_impact(self, decline_prob: float, lifecycle_stage: str) -> Dict:
        """
        Calculate revenue impact proxy.
        """
        # Revenue multiplier based on lifecycle stage
        stage_multipliers = {
            'Growth': 1.5,
            'Peak': 2.0,
            'Early Decline': 1.2,
            'Rapid Collapse': 0.5,
            'Dead Trend': 0.1
        }
        
        base_multiplier = stage_multipliers.get(lifecycle_stage, 1.0)
        
        # Calculate potential revenue loss
        if decline_prob < 30:
            impact_level = "Minimal"
            estimated_loss_pct = decline_prob * 0.3
        elif decline_prob < 60:
            impact_level = "Moderate"
            estimated_loss_pct = decline_prob * 0.5
        elif decline_prob < 80:
            impact_level = "Significant"
            estimated_loss_pct = decline_prob * 0.7
        else:
            impact_level = "Severe"
            estimated_loss_pct = decline_prob * 0.9
        
        # Adjust by lifecycle multiplier
        estimated_loss_pct *= base_multiplier
        estimated_loss_pct = min(100, estimated_loss_pct)
        
        return {
            "impact_level": impact_level,
            "estimated_revenue_loss_pct": round(estimated_loss_pct, 1),
            "stage_multiplier": base_multiplier,
            "mitigation_potential": round(100 - decline_prob, 1)
        }
    
    def _determine_action_urgency(self, decline_prob: float, lifecycle_stage: str) -> Dict:
        """
        Determine marketing action urgency.
        """
        if decline_prob >= 80 or lifecycle_stage == "Rapid Collapse":
            urgency_level = "Critical - Immediate"
            days_to_action = "0-2 days"
            color_code = "#FF0000"
        elif decline_prob >= 60 or lifecycle_stage == "Early Decline":
            urgency_level = "High - Urgent"
            days_to_action = "3-7 days"
            color_code = "#FF6600"
        elif decline_prob >= 40:
            urgency_level = "Medium - Plan"
            days_to_action = "1-2 weeks"
            color_code = "#FFAA00"
        else:
            urgency_level = "Low - Monitor"
            days_to_action = "Routine"
            color_code = "#00AA00"
        
        return {
            "urgency_level": urgency_level,
            "days_to_action": days_to_action,
            "color_code": color_code,
            "immediate_actions_required": decline_prob >= 60
        }
    
    def _generate_key_insights(self, analysis_data: Dict) -> List[str]:
        """
        Generate key executive insights.
        """
        insights = []
        
        decline_prob = analysis_data.get('decline_probability', 0)
        lifecycle_stage = analysis_data.get('lifecycle_stage', '')
        
        # Primary insight
        insights.append(f"Trend is in {lifecycle_stage} stage with {decline_prob:.1f}% decline risk")
        
        # Driver insights
        driver_ranking = analysis_data.get('driver_ranking', [])
        if driver_ranking:
            top_driver = driver_ranking[0]
            insights.append(f"Primary risk factor: {top_driver['driver']} ({top_driver['contribution_percentage']:.1f}% contribution)")
        
        # Early warning insights
        early_warning = analysis_data.get('early_warning', {})
        if early_warning.get('warning_level') in ['High', 'Critical']:
            insights.append(f"Early warning: {early_warning.get('warning_level')} - {len(early_warning.get('active_warnings', []))} risk signals detected")
        
        # Platform insights (if available)
        platform_comparison = analysis_data.get('platform_comparison', {})
        if platform_comparison.get('status') == 'success':
            best_platform = platform_comparison.get('recommended_focus_platform')
            if best_platform:
                insights.append(f"Best performing platform: {best_platform}")
        
        return insights
    
    def enhance_early_warning(self, early_warning_data: Dict, signal_data: Dict, prediction_data: Dict) -> Dict:
        """
        Enhance early warning system with advanced detection.
        
        Args:
            early_warning_data (dict): Existing early warning
            signal_data (dict): Signal agent outputs
            prediction_data (dict): Prediction results
        
        Returns:
            dict: Enhanced early warning
        """
        print(f"[{self.name}] Enhancing early warning system...")
        
        # Start with existing warnings
        enhanced = dict(early_warning_data)
        
        # Detect multi-signal convergence
        convergence_detected = self._detect_signal_convergence(signal_data)
        
        # Detect sudden drops
        sudden_drops = self._detect_sudden_drops(signal_data)
        
        # Detect influencer withdrawal
        influencer_withdrawal = self._detect_influencer_withdrawal(signal_data)
        
        # Predict collapse window
        collapse_window = self._predict_collapse_window(prediction_data, signal_data)
        
        # Add enhanced warnings
        additional_warnings = []
        
        if convergence_detected:
            additional_warnings.append("⚠️ Multi-signal decline convergence detected - cascading failure risk")
        
        if sudden_drops:
            additional_warnings.extend(sudden_drops)
        
        if influencer_withdrawal:
            additional_warnings.append(influencer_withdrawal)
        
        # Combine warnings
        enhanced['active_warnings'] = enhanced.get('active_warnings', []) + additional_warnings
        enhanced['warning_count'] = len(enhanced['active_warnings'])
        
        # Update warning level if needed
        if len(additional_warnings) >= 2:
            if enhanced.get('warning_level') == 'Moderate':
                enhanced['warning_level'] = 'High'
            elif enhanced.get('warning_level') == 'High':
                enhanced['warning_level'] = 'Critical'
        
        # Add collapse window prediction
        enhanced['collapse_window'] = collapse_window
        
        # Add severity score
        enhanced['severity_score'] = self._calculate_severity_score(enhanced)
        
        return enhanced
    
    def _detect_signal_convergence(self, signal_data: Dict) -> bool:
        """
        Detect if multiple signals are converging on decline.
        """
        declining_signals = 0
        
        if signal_data.get('engagement', {}).get('risk_level') in ['High', 'Critical']:
            declining_signals += 1
        
        if signal_data.get('sentiment', {}).get('impact_level') in ['High', 'Critical']:
            declining_signals += 1
        
        if signal_data.get('influencers', {}).get('disengagement_status') != 'Stable':
            declining_signals += 1
        
        if signal_data.get('saturation', {}).get('saturation_score', 0) > 70:
            declining_signals += 1
        
        return declining_signals >= 3
    
    def _detect_sudden_drops(self, signal_data: Dict) -> List[str]:
        """
        Detect sudden engagement drops.
        """
        warnings = []
        
        # Check engagement decay speed
        if signal_data.get('engagement', {}).get('decay_speed') == 'rapid':
            decline_pct = signal_data.get('engagement', {}).get('engagement_decline_percent', 0)
            if decline_pct > 50:
                warnings.append(f"🚨 Sudden engagement drop: {decline_pct:.1f}% decline detected")
        
        return warnings
    
    def _detect_influencer_withdrawal(self, signal_data: Dict) -> Optional[str]:
        """
        Detect influencer withdrawal spikes.
        """
        influencer_drop = signal_data.get('influencers', {}).get('participation_drop_percent', 0)
        
        if influencer_drop > 40:
            return f"👥 Influencer withdrawal spike: {influencer_drop:.1f}% drop in participation"
        
        return None
    
    def _predict_collapse_window(self, prediction_data: Dict, signal_data: Dict) -> Dict:
        """
        Predict collapse window in days.
        """
        days_to_collapse = prediction_data.get('days_to_collapse', 'Unknown')
        decline_prob = prediction_data.get('decline_probability', 0)
        decay_speed = signal_data.get('engagement', {}).get('decay_speed', 'moderate')
        
        # Parse days to collapse if it's a string range
        if isinstance(days_to_collapse, str) and '-' in days_to_collapse:
            try:
                parts = days_to_collapse.split('-')
                min_days = int(parts[0].strip().split()[0])
                max_days = int(parts[1].strip().split()[0])
                avg_days = (min_days + max_days) / 2
            except:
                avg_days = 30
        elif days_to_collapse == "Already Collapsed":
            avg_days = 0
        else:
            avg_days = 30
        
        # Adjust based on decay speed
        speed_multipliers = {
            'slow': 1.5,
            'moderate': 1.0,
            'rapid': 0.5
        }
        
        adjusted_days = avg_days * speed_multipliers.get(decay_speed, 1.0)
        
        return {
            "estimated_days": int(adjusted_days),
            "window_range": days_to_collapse,
            "confidence": "High" if decline_prob > 60 else "Moderate",
            "decay_velocity": decay_speed
        }
    
    def _calculate_severity_score(self, enhanced_warning: Dict) -> int:
        """
        Calculate overall severity score (0-100).
        """
        warning_count = enhanced_warning.get('warning_count', 0)
        warning_level = enhanced_warning.get('warning_level', 'Low')
        
        level_scores = {
            'Low': 20,
            'Moderate': 40,
            'High': 70,
            'Critical': 95
        }
        
        base_score = level_scores.get(warning_level, 20)
        
        # Add points for each warning (max 30 points)
        warning_points = min(30, warning_count * 5)
        
        severity = base_score + warning_points
        
        return min(100, severity)


# Test the module
if __name__ == "__main__":
    print("🧪 Testing Executive Intelligence\n")
    
    # Sample analysis data
    sample_analysis = {
        'decline_probability': 67.5,
        'lifecycle_stage': 'Early Decline',
        'risk_classification': {'risk_label': 'High Risk'},
        'confidence_analysis': {'confidence_score': 78, 'confidence_level': 'High'},
        'strategy_recommendations': [
            'Launch interactive challenges',
            'Re-engage key influencers',
            'Create user-generated content campaigns'
        ],
        'driver_ranking': [
            {'driver': 'Engagement Decline', 'contribution_percentage': 35.0}
        ],
        'early_warning': {
            'warning_level': 'High',
            'active_warnings': ['Engagement showing early decline signs'],
            'warning_count': 1
        }
    }
    
    sample_signals = {
        'engagement': {'risk_level': 'High', 'decay_speed': 'rapid', 'engagement_decline_percent': 55},
        'sentiment': {'impact_level': 'High'},
        'influencers': {'disengagement_status': 'Moderate', 'participation_drop_percent': 45},
        'saturation': {'saturation_score': 75}
    }
    
    sample_prediction = {
        'decline_probability': 67.5,
        'days_to_collapse': '15-25 days'
    }
    
    exec_intel = ExecutiveIntelligence()
    
    # Test executive summary
    summary = exec_intel.generate_executive_summary(sample_analysis)
    print(f"✅ Executive Summary Generated:")
    print(f"   {summary['health_icon']} Health Score: {summary['trend_health_score']}")
    print(f"   Risk: {summary['decline_risk']}")
    print(f"   Urgency: {summary['marketing_action_urgency']['urgency_level']}")
    print(f"   Revenue Impact: {summary['revenue_impact_proxy']['impact_level']}")
    
    # Test enhanced early warning
    enhanced_warning = exec_intel.enhance_early_warning(
        sample_analysis['early_warning'],
        sample_signals,
        sample_prediction
    )
    print(f"\n✅ Enhanced Early Warning:")
    print(f"   Warning Level: {enhanced_warning['warning_level']}")
    print(f"   Active Warnings: {enhanced_warning['warning_count']}")
    print(f"   Severity Score: {enhanced_warning['severity_score']}/100")
    print(f"   Collapse Window: {enhanced_warning['collapse_window']['estimated_days']} days")
    
    print("\n✅ Executive Intelligence test complete!")
