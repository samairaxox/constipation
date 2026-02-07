"""
Test Influencer Agent with Synthetic Trend Data
"""

import sys
sys.path.append('.')

from utils.data_generator import generate_trend_data
from agents.influencer_agent import InfluencerAgent

print("🚀 Testing Influencer Agent with Synthetic Data\n")

# Generate realistic trend data
print("📊 Generating synthetic trend data...")
trend_df = generate_trend_data("Celebrity Fashion Challenge", total_days=60, export_json=False)

print(f"\n👥 Analyzing {len(trend_df)} days of influencer participation data...\n")

# Initialize agent
agent = InfluencerAgent()

# Analyze influencer trends
result = agent.analyze(trend_df)

# Display results
print("=" * 60)
print("INFLUENCER ANALYSIS RESULTS")
print("=" * 60)
print(f"\n👥 Agent: {result['agent']}")
print(f"✅ Status: {result['status']}\n")

print("🔍 INFLUENCER PARTICIPATION ANALYSIS:")
print(f"  • Participation Drop: {result['participation_drop_percent']:.2f}%")
print(f"  • Influence Impact Score: {result['influence_impact_score']:.2f}/100")
print(f"  • Disengagement Status: {result['disengagement_status']}")
print(f"  • Risk Level: {result['risk_level']}")
print(f"  • Trend Direction: {result['trend_direction']}\n")

print("📊 DETAILED METRICS:")
print(f"  • Initial Ratio: {result['metrics']['initial_ratio']}")
print(f"  • Current Ratio: {result['metrics']['current_ratio']}")
print(f"  • Peak Ratio: {result['metrics']['peak_ratio']}")
print(f"  • Overall Average: {result['metrics']['overall_average']}")
print(f"  • Activity Level: {result['influencer_activity']}\n")

print("💡 INSIGHTS:")
print(f"  {result['insights']}\n")

print("=" * 60)

# Output structured JSON format
import json
print("\n📦 STRUCTURED OUTPUT:")
output = {
    "participation_drop_percent": result['participation_drop_percent'],
    "influence_impact_score": result['influence_impact_score'],
    "disengagement_status": result['disengagement_status'],
    "risk_level": result['risk_level']
}
print(json.dumps(output, indent=2))

print("\n✅ Test complete!")
