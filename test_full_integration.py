"""
Full Integration Test: All Agents + Decline Predictor
"""

import sys
sys.path.append('.')

from utils.data_generator import generate_trend_data
from agents.engagement_agent import EngagementAgent
from agents.sentiment_agent import SentimentAgent
from agents.influencer_agent import InfluencerAgent
from agents.saturation_agent import SaturationAgent
from agents.decline_predictor import DeclinePredictor

print("🚀 FULL AGENT INTEGRATION TEST\n")
print("=" * 70)

# Generate realistic trend data
print("\n📊 Step 1: Generating synthetic trend data...")
trend_df = generate_trend_data("Viral TikTok Challenge", total_days=60, export_json=False)
print(f"✅ Generated {len(trend_df)} days of data\n")

# Initialize all agents
print("🤖 Step 2: Initializing all agents...")
engagement_agent = EngagementAgent()
sentiment_agent = SentimentAgent()
influencer_agent = InfluencerAgent()
saturation_agent = SaturationAgent()
decline_predictor = DeclinePredictor()
print("✅ All agents initialized\n")

# Run individual agent analyses
print("🔍 Step 3: Running individual agent analyses...")
print("-" * 70)

engagement_result = engagement_agent.analyze(trend_df)
print(f"✅ Engagement: {engagement_result['engagement_decline_percent']}% decline, Risk: {engagement_result['risk_level']}")

sentiment_result = sentiment_agent.analyze(trend_df)
print(f"✅ Sentiment: {sentiment_result['sentiment_shift']}, Impact: {sentiment_result['impact_level']}")

influencer_result = influencer_agent.analyze(trend_df)
print(f"✅ Influencer: {influencer_result['participation_drop_percent']}% drop, Score: {influencer_result['influence_impact_score']}")

saturation_result = saturation_agent.analyze(trend_df)
print(f"✅ Saturation: {saturation_result['saturation_score']}/100, Impact: {saturation_result['saturation_impact_level']}")

# Aggregate results for decline predictor
print(f"\n🧠 Step 4: Running decline prediction model...")
print("-" * 70)

aggregated_data = {
    'engagement': engagement_result,
    'sentiment': sentiment_result,
    'influencers': influencer_result,
    'saturation': saturation_result
}

prediction = decline_predictor.predict(aggregated_data)

# Display comprehensive results
print("\n" + "=" * 70)
print("DECLINE PREDICTION RESULTS")
print("=" * 70)

print(f"\n🎯 PREDICTION SUMMARY:")
print(f"  • Decline Probability: {prediction['decline_probability']}%")
print(f"  • Lifecycle Stage: {prediction['lifecycle_stage']}")
print(f"  • Risk Level: {prediction['risk_level']}")
print(f"  • Days to Collapse: {prediction['days_to_collapse']}")
print(f"  • Confidence: {prediction['confidence']}%")

print(f"\n📊 SIGNAL SCORES (Normalized to 0-100):")
print(f"  • Engagement:  {prediction['signal_scores']['engagement_score']}")
print(f"  • Influencer:  {prediction['signal_scores']['influencer_score']}")
print(f"  • Sentiment:   {prediction['signal_scores']['sentiment_score']}")
print(f"  • Saturation:  {prediction['signal_scores']['saturation_score']}")

print(f"\n⚖️  WEIGHTED CONTRIBUTIONS:")
print(f"  • Engagement (35%):  {prediction['weighted_contributions']['engagement_weight']}")
print(f"  • Influencer (25%):  {prediction['weighted_contributions']['influencer_weight']}")
print(f"  • Sentiment (20%):   {prediction['weighted_contributions']['sentiment_weight']}")
print(f"  • Saturation (20%):  {prediction['weighted_contributions']['saturation_weight']}")

print(f"\n🔝 TOP CONTRIBUTING FACTORS:")
for i, factor in enumerate(prediction['contributing_factors'], 1):
    print(f"  {i}. {factor['factor'].upper()}: {factor['contribution']} pts (raw: {factor['raw_score']})")

print(f"\n💡 KEY INSIGHTS:")
print(f"  {prediction['insights']}")

print(f"\n📋 RECOMMENDATIONS:")
for i, rec in enumerate(prediction['recommendations'], 1):
    print(f"  {i}. {rec}")

# Output final prediction JSON
import json
print("\n" + "=" * 70)
print("STRUCTURED PREDICTION OUTPUT (JSON)")
print("=" * 70)

final_output = {
    "decline_probability": prediction['decline_probability'],
    "lifecycle_stage": prediction['lifecycle_stage'],
    "days_to_collapse": prediction['days_to_collapse'],
    "risk_level": prediction['risk_level'],
    "confidence": prediction['confidence'],
    "top_factor": prediction['contributing_factors'][0]['factor']
}

print(json.dumps(final_output, indent=2))

print("\n" + "=" * 70)
print("✅ FULL INTEGRATION TEST COMPLETE!")
print("=" * 70)
