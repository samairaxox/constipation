"""
Narrative Agent
Generates human-readable narratives and explanations from agent outputs.
Integrates with Featherless AI for advanced narrative generation.
"""

import os
import json
import requests
from typing import Dict, List, Optional


class NarrativeAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.name = "Narrative Agent"
        self.description = "Generates natural language summaries and insights"
        
        # Featherless AI configuration
        self.api_key = api_key or os.getenv('FEATHERLESS_API_KEY')
        self.api_endpoint = "https://api.featherless.ai/v1/completions"
        self.model = "mistralai/Mistral-7B-Instruct-v0.2"
        
        # Fallback mode if no API key
        self.use_ai = bool(self.api_key)
        
        if not self.use_ai:
            print(f"[{self.name}] ⚠️  No API key found - using template-based generation")
    
    def generate(self, analysis_results: Dict) -> Dict:
        """
        Generates narrative summary from agent analysis results.
        
        Args:
            analysis_results (dict): Combined results from all agents
        
        Returns:
            dict: Human-readable narrative and executive summary
        """
        print(f"[{self.name}] Generating narrative summary...")
        
        # Generate narrative explanation
        narrative = self.generate_trend_narrative(analysis_results)
        
        # Generate strategy recommendations
        recommendations = self.generate_strategy_recommendations(analysis_results)
        
        # Extract key insights
        key_insights = self._extract_key_insights(analysis_results)
        
        return {
            "agent": self.name,
            "status": "success",
            "narrative_explanation": narrative,
            "strategy_recommendations": recommendations,
            "key_insights": key_insights,
            "tone": "informative",
            "confidence_level": "high"
        }
    
    def generate_trend_narrative(self, trend_analysis_output: Dict) -> str:
        """
        Generate comprehensive narrative explanation of trend decline.
        
        Args:
            trend_analysis_output (dict): Complete trend analysis data
        
        Returns:
            str: AI-generated narrative explanation
        """
        if self.use_ai:
            return self._generate_ai_narrative(trend_analysis_output)
        else:
            return self._generate_template_narrative(trend_analysis_output)
    
    def _generate_ai_narrative(self, data: Dict) -> str:
        """
        Generate narrative using Featherless AI.
        """
        try:
            # Extract key metrics
            prediction = data.get('decline_prediction', {})
            signals = data.get('signal_details', {})
            
            decline_prob = prediction.get('decline_probability', 0)
            stage = prediction.get('lifecycle_stage', 'Unknown')
            
            # Build prompt
            prompt = self._build_narrative_prompt(data)
            
            # Call Featherless AI API
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "prompt": prompt,
                "max_tokens": 400,
                "temperature": 0.7,
                "top_p": 0.9
            }
            
            response = requests.post(
                self.api_endpoint,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                narrative = result.get('choices', [{}])[0].get('text', '').strip()
                return narrative
            else:
                print(f"[{self.name}] API error {response.status_code} - using fallback")
                return self._generate_template_narrative(data)
                
        except Exception as e:
            print(f"[{self.name}] Error generating AI narrative: {e}")
            return self._generate_template_narrative(data)
    
    def _build_narrative_prompt(self, data: Dict) -> str:
        """
        Build prompt for AI narrative generation.
        """
        prediction = data.get('decline_prediction', {})
        factors = data.get('contributing_factors', [])
        
        decline_prob = prediction.get('decline_probability', 0)
        stage = prediction.get('lifecycle_stage', 'Unknown')
        risk = prediction.get('risk_level', 'Unknown')
        
        # Get top factors
        top_factors = [f['factor'] for f in factors[:3]] if factors else []
        
        prompt = f"""You are a social media trend analyst. Analyze this trend decline prediction and explain it clearly.

Trend Analysis:
- Decline Probability: {decline_prob}%
- Lifecycle Stage: {stage}
- Risk Level: {risk}
- Top Decline Drivers: {', '.join(top_factors)}

Provide a concise business explanation (3-4 sentences) covering:
1. Why the trend is declining
2. Key decline drivers
3. Business interpretation
4. Strategic outlook

Response:"""
        
        return prompt
    
    def _generate_template_narrative(self, data: Dict) -> str:
        """
        Generate narrative using templates (fallback).
        """
        prediction = data.get('decline_prediction', {})
        factors = data.get('contributing_factors', [])
        
        decline_prob = prediction.get('decline_probability', 0)
        stage = prediction.get('lifecycle_stage', 'Unknown')
        risk = prediction.get('risk_level', 'Unknown')
        days = prediction.get('days_to_collapse', 'Unknown')
        
        # Build narrative
        narrative = f"The trend is currently in the {stage} phase with a {decline_prob:.1f}% decline probability. "
        
        # Add risk context
        if risk == "Critical":
            narrative += "This represents a critical risk level requiring immediate intervention. "
        elif risk == "High":
            narrative += "This indicates high risk and warrants urgent attention. "
        elif risk == "Medium":
            narrative += "This shows moderate risk that should be monitored closely. "
        else:
            narrative += "The trend remains relatively healthy with manageable risk. "
        
        # Add key drivers
        if factors:
            top_factor = factors[0]['factor']
            narrative += f"The primary decline driver is {top_factor}, "
            
            if len(factors) > 1:
                second_factor = factors[1]['factor']
                narrative += f"followed by {second_factor}. "
        
        # Add timeline
        if days != "Unknown":
            narrative += f"Without intervention, the trend is estimated to collapse in {days}."
        
        return narrative
    
    def generate_strategy_recommendations(self, data: Dict) -> List[str]:
        """
        Generate actionable strategy recommendations.
        
        Args:
            data (dict): Trend analysis data
        
        Returns:
            list: Strategy recommendations
        """
        recommendations = []
        
        factors = data.get('contributing_factors', [])
        prediction = data.get('decline_prediction', {})
        signals = data.get('signal_details', {})
        
        # Extract top factor
        if factors:
            top_factor = factors[0]['factor']
            contribution = factors[0]['contribution']
            
            # Factor-specific recommendations
            if top_factor == 'engagement' and contribution > 15:
                recommendations.extend([
                    "Launch interactive challenges or contests to boost engagement",
                    "Increase posting frequency with high-quality, varied content",
                    "Create user-generated content campaigns to drive participation"
                ])
            
            if top_factor == 'influencer' and contribution > 10:
                recommendations.extend([
                    "Re-engage key influencers with exclusive partnership opportunities",
                    "Identify and activate emerging micro-influencers in the space",
                    "Create influencer incentive programs with performance rewards"
                ])
            
            if top_factor == 'sentiment' and contribution > 10:
                recommendations.extend([
                    "Address negative sentiment through transparent communication",
                    "Improve content quality based on user feedback",
                    "Launch positive PR campaign highlighting success stories"
                ])
            
            if top_factor == 'saturation' and contribution > 10:
                recommendations.extend([
                    "Introduce fresh variations and creative twists to combat fatigue",
                    "Pivot to adjacent niches or sub-trends",
                    "Create scarcity through limited-time or exclusive content"
                ])
        
        # Stage-specific recommendations
        stage = prediction.get('lifecycle_stage', '')
        
        if stage == "Early Decline":
            recommendations.append("Implement retention strategies and loyalty programs immediately")
        elif stage == "Rapid Collapse":
            recommendations.append("Consider strategic pivot or controlled wind-down to preserve brand equity")
        elif stage == "Peak":
            recommendations.append("Prepare sustainability plan and diversification strategy")
        
        # Revival strategies
        if prediction.get('decline_probability', 0) > 50:
            recommendations.extend(self._generate_revival_strategies(data))
        
        # Marketing recommendations
        recommendations.extend(self._generate_marketing_recommendations(data))
        
        # Deduplicate and limit
        seen = set()
        unique_recs = []
        for rec in recommendations:
            if rec not in seen:
                seen.add(rec)
                unique_recs.append(rec)
        
        return unique_recs[:8]  # Limit to top 8
    
    def _generate_revival_strategies(self, data: Dict) -> List[str]:
        """
        Generate revival strategies for declining trends.
        """
        strategies = [
            "Partner with major brands for co-branded revival campaign",
            "Create nostalgia-driven content to re-engage original audience",
            "Launch 2.0 version with improved features and benefits"
        ]
        return strategies[:2]
    
    def _generate_marketing_recommendations(self, data: Dict) -> List[str]:
        """
        Generate marketing-specific recommendations.
        """
        recs = [
            "Amplify top-performing content through paid promotion",
            "Target new audience segments with tailored messaging"
        ]
        return recs[:1]
    
    def generate_simulation_explanation(self, simulation_results: Dict) -> str:
        """
        Generate AI explanation of simulation results.
        
        Args:
            simulation_results (dict): Simulation output data
        
        Returns:
            str: Explanation of simulation outcomes
        """
        scenario = simulation_results.get('scenario_name', 'modified')
        original_prob = simulation_results.get('original_decline_probability', 0)
        new_prob = simulation_results.get('new_decline_probability', 0)
        changes = simulation_results.get('parameter_changes', {})
        
        change_delta = new_prob - original_prob
        
        # Build explanation
        explanation = f"In the '{scenario}' scenario, "
        
        # Describe parameter changes
        if changes:
            change_desc = []
            for param, value in changes.items():
                change_desc.append(f"{param} changes to {value}")
            explanation += f"with {', '.join(change_desc)}, "
        
        # Describe outcome
        if change_delta < -10:
            explanation += f"the decline risk significantly improves, dropping from {original_prob:.1f}% to {new_prob:.1f}%. "
            explanation += "This represents a favorable outcome with reduced collapse risk."
        elif change_delta < 0:
            explanation += f"the decline risk slightly improves from {original_prob:.1f}% to {new_prob:.1f}%. "
            explanation += "This shows modest positive impact."
        elif change_delta > 10:
            explanation += f"the decline risk significantly worsens, increasing from {original_prob:.1f}% to {new_prob:.1f}%. "
            explanation += "This scenario should be avoided."
        else:
            explanation += f"the decline risk remains relatively stable at {new_prob:.1f}%. "
            explanation += "The changes have minimal impact."
        
        return explanation
    
    def _extract_key_insights(self, data: Dict) -> List[str]:
        """
        Extract key insights from analysis.
        """
        insights = []
        
        prediction = data.get('decline_prediction', {})
        
        # Decline probability insight
        prob = prediction.get('decline_probability', 0)
        if prob > 70:
            insights.append(f"Critical decline risk detected at {prob:.1f}%")
        elif prob > 40:
            insights.append(f"Elevated decline risk at {prob:.1f}%")
        
        # Lifecycle insight
        stage = prediction.get('lifecycle_stage', '')
        if stage:
            insights.append(f"Trend is in {stage} phase")
        
        # Timeline insight
        days = prediction.get('days_to_collapse', '')
        if days and days != "Unknown":
            insights.append(f"Estimated collapse timeline: {days}")
        
        return insights


# Test the agent
if __name__ == "__main__":
    print("🧪 Testing Narrative Agent\n")
    
    # Sample analysis data
    sample_data = {
        'decline_prediction': {
            'decline_probability': 67.5,
            'lifecycle_stage': 'Early Decline',
            'risk_level': 'High',
            'days_to_collapse': '15-25 days'
        },
        'contributing_factors': [
            {'factor': 'engagement', 'contribution': 25.3},
            {'factor': 'influencer', 'contribution': 18.7},
            {'factor': 'sentiment', 'contribution': 12.5}
        ],
        'signal_details': {}
    }
    
    agent = NarrativeAgent()
    result = agent.generate(sample_data)
    
    print(f"✅ Status: {result['status']}\n")
    print(f"📖 NARRATIVE:")
    print(f"{result['narrative_explanation']}\n")
    print(f"📋 RECOMMENDATIONS:")
    for i, rec in enumerate(result['strategy_recommendations'], 1):
        print(f"  {i}. {rec}")
    
    print("\n✅ Narrative Agent test complete!")
