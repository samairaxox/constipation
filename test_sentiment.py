"""
Test Sentiment Agent with Synthetic Trend Data
"""

import sys
sys.path.append('.')

from utils.data_generator import generate_trend_data
from agents.sentiment_agent import SentimentAgent

print("🚀 Testing Sentiment Agent with Synthetic Data\n")

# Generate realistic trend data
print("📊 Generating synthetic trend data...")
trend_df = generate_trend_data("Viral Fashion Trend", total_days=60, export_json=False)

print(f"\n🎭 Analyzing {len(trend_df)} days of sentiment data...\n")

# Initialize agent
agent = SentimentAgent()

# Analyze sentiment over time
result = agent.analyze(trend_df)

# Display results
print("=" * 60)
print("SENTIMENT ANALYSIS RESULTS")
print("=" * 60)
print(f"\n🎭 Agent: {result['agent']}")
print(f"✅ Status: {result['status']}\n")

print("🔍 SENTIMENT SHIFT ANALYSIS:")
print(f"  • Pattern: {result['sentiment_shift']}")
print(f"  • Description: {result['shift_description']}")
print(f"  • Impact Level: {result['impact_level']}")
print(f"  • Trend Direction: {result['trend_direction']}\n")

print("📊 SENTIMENT METRICS:")
print(f"  • Initial Sentiment: {result['metrics']['initial_sentiment']} ({result['sentiment_categories']['initial']})")
print(f"  • Current Sentiment: {result['metrics']['current_sentiment']} ({result['sentiment_categories']['current']})")
print(f"  • Overall Average: {result['metrics']['overall_sentiment']}")
print(f"  • Change: {result['metrics']['sentiment_change_percent']:+.2f}%")
print(f"  • Volatility: {result['metrics']['volatility']}\n")

print("💡 INSIGHTS:")
print(f"  {result['insights']}\n")

print("=" * 60)

# Output structured JSON format
import json
print("\n📦 STRUCTURED OUTPUT:")
output = {
    "sentiment_shift": result['sentiment_shift'],
    "shift_description": result['shift_description'],
    "impact_level": result['impact_level'],
    "sentiment_change_percent": result['metrics']['sentiment_change_percent'],
    "volatility": result['metrics']['volatility']
}
print(json.dumps(output, indent=2))

print("\n✅ Test complete!")
