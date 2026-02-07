"""
Trend Orchestrator
Coordinates multi-agent trend analysis workflow.
Executes all signal agents and aggregates results into unified predictions.
"""

import pandas as pd
from datetime import datetime

try:
    from agents.engagement_agent import EngagementAgent
    from agents.sentiment_agent import SentimentAgent
    from agents.influencer_agent import InfluencerAgent
    from agents.saturation_agent import SaturationAgent
    from agents.decline_predictor import DeclinePredictor
except ImportError:
    from engagement_agent import EngagementAgent
    from sentiment_agent import SentimentAgent
    from influencer_agent import InfluencerAgent
    from saturation_agent import SaturationAgent
    from decline_predictor import DeclinePredictor


class TrendOrchestrator:
    def __init__(self):
        self.name = "Trend Orchestrator"
        self.description = "Coordinates multi-agent trend analysis workflow"
        
        # Initialize all agents
        print(f"[{self.name}] Initializing agent ecosystem...")
        self.engagement_agent = EngagementAgent()
        self.sentiment_agent = SentimentAgent()
        self.influencer_agent = InfluencerAgent()
        self.saturation_agent = SaturationAgent()
        self.decline_predictor = DeclinePredictor()
        
        print(f"[{self.name}] ✅ All agents ready")
    
    def analyze_trend(self, trend_data, trend_name=None):
        """
        Executes complete trend analysis workflow across all agents.
        
        Args:
            trend_data (pd.DataFrame): Complete trend time-series data
            trend_name (str): Optional name of the trend
        
        Returns:
            dict: Comprehensive unified insight object
        """
        print(f"\n{'='*70}")
        print(f"[{self.name}] Starting comprehensive trend analysis...")
        print(f"{'='*70}\n")
        
        # Validate input
        if not isinstance(trend_data, pd.DataFrame):
            raise ValueError("trend_data must be a pandas DataFrame")
        
        # Extract trend metadata
        metadata = self._extract_metadata(trend_data, trend_name)
        
        # Execute signal agents in parallel (modular execution)
        signal_results = self._execute_signal_agents(trend_data)
        
        # Aggregate signals
        aggregated_signals = self._aggregate_signals(signal_results)
        
        # Run decline prediction
        prediction = self._run_prediction(aggregated_signals)
        
        # Generate unified insight object
        unified_insights = self._generate_unified_insights(
            metadata,
            signal_results,
            prediction
        )
        
        print(f"\n{'='*70}")
        print(f"[{self.name}] ✅ Analysis complete!")
        print(f"{'='*70}\n")
        
        return unified_insights
    
    def _extract_metadata(self, df, trend_name):
        """
        Extract metadata from trend dataset.
        
        Args:
            df (pd.DataFrame): Trend data
            trend_name (str): Trend name
        
        Returns:
            dict: Metadata information
        """
        print(f"[{self.name}] Extracting trend metadata...")
        
        # Get trend name from DataFrame if available
        if trend_name is None and 'trend_name' in df.columns:
            trend_name = df['trend_name'].iloc[0]
        elif trend_name is None:
            trend_name = "Unknown Trend"
        
        # Date range
        if 'date' in df.columns:
            start_date = df['date'].min()
            end_date = df['date'].max()
        else:
            start_date = "Unknown"
            end_date = "Unknown"
        
        metadata = {
            "trend_name": trend_name,
            "data_points": len(df),
            "start_date": str(start_date),
            "end_date": str(end_date),
            "analysis_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        print(f"  ✅ Trend: {metadata['trend_name']} ({metadata['data_points']} days)")
        
        return metadata
    
    def _execute_signal_agents(self, df):
        """
        Execute all signal agents in modular fashion.
        
        Args:
            df (pd.DataFrame): Trend data
        
        Returns:
            dict: Results from all signal agents
        """
        print(f"\n[{self.name}] Executing signal agents...")
        print("-" * 70)
        
        results = {}
        
        # Execute each agent with error handling
        try:
            print("  → Running Engagement Agent...")
            results['engagement'] = self.engagement_agent.analyze(df)
            print(f"    ✅ Complete: {results['engagement']['engagement_decline_percent']}% decline")
        except Exception as e:
            print(f"    ❌ Error: {str(e)}")
            results['engagement'] = None
        
        try:
            print("  → Running Sentiment Agent...")
            results['sentiment'] = self.sentiment_agent.analyze(df)
            print(f"    ✅ Complete: {results['sentiment']['sentiment_shift']}")
        except Exception as e:
            print(f"    ❌ Error: {str(e)}")
            results['sentiment'] = None
        
        try:
            print("  → Running Influencer Agent...")
            results['influencers'] = self.influencer_agent.analyze(df)
            print(f"    ✅ Complete: {results['influencers']['disengagement_status']}")
        except Exception as e:
            print(f"    ❌ Error: {str(e)}")
            results['influencers'] = None
        
        try:
            print("  → Running Saturation Agent...")
            results['saturation'] = self.saturation_agent.analyze(df)
            print(f"    ✅ Complete: {results['saturation']['saturation_score']}/100")
        except Exception as e:
            print(f"    ❌ Error: {str(e)}")
            results['saturation'] = None
        
        print("-" * 70)
        
        return results
    
    def _aggregate_signals(self, signal_results):
        """
        Aggregate signal results for prediction model.
        
        Args:
            signal_results (dict): Individual agent results
        
        Returns:
            dict: Aggregated signals
        """
        print(f"[{self.name}] Aggregating multi-agent signals...")
        
        # Filter out failed agents
        valid_signals = {k: v for k, v in signal_results.items() if v is not None}
        
        print(f"  ✅ {len(valid_signals)}/4 agents provided signals")
        
        return valid_signals
    
    def _run_prediction(self, aggregated_signals):
        """
        Run decline prediction model.
        
        Args:
            aggregated_signals (dict): Aggregated agent outputs
        
        Returns:
            dict: Prediction results
        """
        print(f"[{self.name}] Running decline prediction model...")
        
        if not aggregated_signals:
            print("  ⚠️  No valid signals - cannot generate prediction")
            return {
                "status": "failed",
                "error": "No valid agent signals available"
            }
        
        prediction = self.decline_predictor.predict(aggregated_signals)
        
        print(f"  ✅ Prediction: {prediction['decline_probability']}% decline risk")
        
        return prediction
    
    def _generate_unified_insights(self, metadata, signal_results, prediction):
        """
        Generate comprehensive unified insight object.
        
        Args:
            metadata (dict): Trend metadata
            signal_results (dict): Signal agent results
            prediction (dict): Prediction results
        
        Returns:
            dict: Unified insight object
        """
        print(f"[{self.name}] Generating unified insights...")
        
        # Build executive summary
        executive_summary = self._build_executive_summary(prediction, signal_results)
        
        # Extract key metrics
        key_metrics = self._extract_key_metrics(signal_results, prediction)
        
        # Compile alerts
        alerts = self._compile_alerts(signal_results, prediction)
        
        # Build unified object
        unified_insights = {
            "orchestrator": self.name,
            "status": "success",
            "metadata": metadata,
            "executive_summary": executive_summary,
            "prediction": {
                "decline_probability": prediction.get('decline_probability', 0),
                "lifecycle_stage": prediction.get('lifecycle_stage', 'Unknown'),
                "risk_level": prediction.get('risk_level', 'Unknown'),
                "days_to_collapse": prediction.get('days_to_collapse', 'Unknown'),
                "confidence": prediction.get('confidence', 0)
            },
            "key_metrics": key_metrics,
            "signal_details": {
                "engagement": signal_results.get('engagement'),
                "sentiment": signal_results.get('sentiment'),
                "influencer": signal_results.get('influencers'),
                "saturation": signal_results.get('saturation')
            },
            "alerts": alerts,
            "recommendations": prediction.get('recommendations', []),
            "contributing_factors": prediction.get('contributing_factors', [])
        }
        
        print(f"  ✅ Unified insights generated")
        
        return unified_insights
    
    def _build_executive_summary(self, prediction, signals):
        """
        Build executive summary text.
        """
        stage = prediction.get('lifecycle_stage', 'Unknown')
        probability = prediction.get('decline_probability', 0)
        risk = prediction.get('risk_level', 'Unknown')
        
        summary = f"The trend is currently in {stage} with a {probability:.1f}% decline probability. "
        summary += f"Risk level is {risk}. "
        
        if prediction.get('days_to_collapse') != 'Unknown':
            summary += f"Estimated time to collapse: {prediction.get('days_to_collapse')}. "
        
        return summary
    
    def _extract_key_metrics(self, signals, prediction):
        """
        Extract key metrics from all agents.
        """
        metrics = {}
        
        if signals.get('engagement'):
            metrics['engagement_decline'] = signals['engagement'].get('engagement_decline_percent', 0)
        
        if signals.get('sentiment'):
            metrics['sentiment_change'] = signals['sentiment'].get('metrics', {}).get('sentiment_change_percent', 0)
        
        if signals.get('influencers'):
            metrics['influencer_drop'] = signals['influencers'].get('participation_drop_percent', 0)
        
        if signals.get('saturation'):
            metrics['saturation_level'] = signals['saturation'].get('saturation_score', 0)
        
        metrics['overall_decline_probability'] = prediction.get('decline_probability', 0)
        
        return metrics
    
    def _compile_alerts(self, signals, prediction):
        """
        Compile critical alerts from all agents.
        """
        alerts = []
        
        # Prediction alerts
        if prediction.get('risk_level') == 'Critical':
            alerts.append({
                "severity": "Critical",
                "source": "Decline Predictor",
                "message": prediction.get('insights', 'Critical decline risk detected')
            })
        
        # Engagement alerts
        if signals.get('engagement') and signals['engagement'].get('risk_level') == 'High':
            alerts.append({
                "severity": "High",
                "source": "Engagement Agent",
                "message": f"Engagement declined {signals['engagement']['engagement_decline_percent']}%"
            })
        
        # Sentiment alerts
        if signals.get('sentiment') and signals['sentiment'].get('impact_level') in ['High', 'Critical']:
            alerts.append({
                "severity": signals['sentiment']['impact_level'],
                "source": "Sentiment Agent",
                "message": f"Sentiment shift: {signals['sentiment']['sentiment_shift']}"
            })
        
        # Influencer alerts
        if signals.get('influencers') and signals['influencers'].get('risk_level') in ['High', 'Critical']:
            alerts.append({
                "severity": signals['influencers']['risk_level'],
                "source": "Influencer Agent",
                "message": f"{signals['influencers']['disengagement_status']} detected"
            })
        
        # Saturation alerts
        if signals.get('saturation') and signals['saturation'].get('fatigue_detected'):
            alerts.append({
                "severity": "High",
                "source": "Saturation Agent",
                "message": f"Content fatigue at {signals['saturation']['saturation_score']}% saturation"
            })
        
        return alerts
    
    def get_agent_status(self):
        """
        Returns status of all agents.
        """
        return {
            "orchestrator": "active",
            "agents": {
                "engagement": self.engagement_agent.name,
                "sentiment": self.sentiment_agent.name,
                "influencer": self.influencer_agent.name,
                "saturation": self.saturation_agent.name,
                "decline_predictor": self.decline_predictor.name
            },
            "total_agents": 5
        }


# Test orchestrator
if __name__ == "__main__":
    print("🧪 Testing Trend Orchestrator\n")
    
    # Create sample trend data
    import numpy as np
    
    sample_data = pd.DataFrame({
        'trend_name': ['Test Trend'] * 45,
        'date': pd.date_range('2026-01-01', periods=45, freq='D'),
        'engagement_rate': np.concatenate([
            np.linspace(0.08, 0.12, 15),
            np.linspace(0.12, 0.10, 15),
            np.linspace(0.10, 0.04, 15)
        ]),
        'sentiment_score': np.concatenate([
            np.random.normal(0.75, 0.05, 15),
            np.random.normal(0.55, 0.08, 15),
            np.random.normal(0.35, 0.10, 15)
        ]),
        'influencer_ratio': np.concatenate([
            np.random.normal(0.25, 0.02, 15),
            np.random.normal(0.15, 0.03, 15),
            np.random.normal(0.08, 0.02, 15)
        ]),
        'saturation_score': np.concatenate([
            np.linspace(0, 40, 15),
            np.linspace(40, 70, 15),
            np.linspace(70, 90, 15)
        ])
    })
    
    # Initialize orchestrator
    orchestrator = TrendOrchestrator()
    
    # Run analysis
    results = orchestrator.analyze_trend(sample_data, "Test Viral Challenge")
    
    # Display results
    print("\n" + "="*70)
    print("ORCHESTRATOR RESULTS")
    print("="*70)
    print(f"\nTrend: {results['metadata']['trend_name']}")
    print(f"Status: {results['status']}")
    print(f"\nExecutive Summary:")
    print(f"  {results['executive_summary']}")
    print(f"\nPrediction:")
    print(f"  • Decline Probability: {results['prediction']['decline_probability']}%")
    print(f"  • Lifecycle Stage: {results['prediction']['lifecycle_stage']}")
    print(f"  • Risk Level: {results['prediction']['risk_level']}")
    print(f"\nAlerts: {len(results['alerts'])}")
    for alert in results['alerts']:
        print(f"  [{alert['severity']}] {alert['source']}: {alert['message']}")
    
    print("\n✅ Orchestrator test complete!")
