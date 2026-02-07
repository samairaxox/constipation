"""
Test Engagement Agent with Synthetic Trend Data
"""

import sys
sys.path.append('.')

from utils.data_generator import generate_trend_data
from agents.engagement_agent import EngagementAgent

print("🚀 Testing Engagement Agent with Synthetic Data\n")

# Generate realistic trend data
print("📊 Generating synthetic trend data...")
trend_df = generate_trend_data("Viral Dance Challenge", total_days=60, export_json=False)

print(f"\n📈 Analyzing {len(trend_df)} days of engagement data...\n")

# Initialize agent
agent = EngagementAgent()

# Analyze full trend lifecycle
result = agent.analyze(trend_df)

# Display results
print("=" * 60)
print("ENGAGEMENT ANALYSIS RESULTS")
print("=" * 60)
print(f"\n📊 Agent: {result['agent']}")
print(f"✅ Status: {result['status']}\n")

print("🔍 KEY METRICS:")
print(f"  • Engagement Decline: {result['engagement_decline_percent']}%")
print(f"  • Risk Level: {result['risk_level']}")
print(f"  • Decay Speed: {result['decay_speed']}")
print(f"  • Trend Direction: {result['trend_direction']}\n")

print("📈 DETAILED METRICS:")
print(f"  • Peak Engagement Rate: {result['metrics']['peak_engagement']}")
print(f"  • Current Engagement Rate: {result['metrics']['current_engagement']}")
print(f"  • Average Engagement Rate: {result['metrics']['average_engagement']}")
print(f"  • Volatility: {result['metrics']['volatility']}\n")

print("💡 INSIGHTS:")
print(f"  {result['insights']}\n")

print("=" * 60)

# Output JSON format
import json
print("\n📦 JSON OUTPUT:")
output = {
    "engagement_decline_percent": result['engagement_decline_percent'],
    "risk_level": result['risk_level']
}
print(json.dumps(output, indent=2))

print("\n✅ Test complete!")
