"""
Test Saturation Agent with Synthetic Trend Data
"""

import sys
sys.path.append('.')

from utils.data_generator import generate_trend_data
from agents.saturation_agent import SaturationAgent

print("🚀 Testing Saturation Agent with Synthetic Data\n")

# Generate realistic trend data
print("📊 Generating synthetic trend data...")
trend_df = generate_trend_data("Meme Challenge", total_days=60, export_json=False)

print(f"\n📈 Analyzing {len(trend_df)} days of saturation data...\n")

# Initialize agent
agent = SaturationAgent()

# Analyze saturation trends
result = agent.analyze(trend_df)

# Display results
print("=" * 60)
print("SATURATION ANALYSIS RESULTS")
print("=" * 60)
print(f"\n📊 Agent: {result['agent']}")
print(f"✅ Status: {result['status']}\n")

print("🔍 SATURATION ANALYSIS:")
print(f"  • Saturation Score: {result['saturation_score']}/100")
print(f"  • Impact Level: {result['saturation_impact_level']}")
print(f"  • Market Penetration: {result['market_penetration']}%")
print(f"  • Repetition Risk: {result['repetition_risk']}")
print(f"  • Saturation Stage: {result['saturation_stage']}")
print(f"  • Fatigue Detected: {result['fatigue_detected']}\n")

print("📊 DETAILED METRICS:")
print(f"  • Current Saturation: {result['metrics']['current_saturation']}")
print(f"  • Peak Saturation: {result['metrics']['peak_saturation']}")
print(f"  • Average Saturation: {result['metrics']['average_saturation']}")
print(f"  • Saturation Velocity: {result['metrics']['saturation_velocity']} pts/day\n")

print("⏰ TIMELINE:")
print(f"  • Time to Peak: {result['time_to_peak']}")
print(f"  • Threshold Breaches: {len(result['threshold_breaches'])}")

if result['threshold_breaches']:
    print("\n🔔 BREACHED THRESHOLDS:")
    for breach in result['threshold_breaches']:
        print(f"    - {breach['threshold']}: Day {breach['day']} (>{breach['value']})")

print(f"\n💡 INSIGHTS:")
print(f"  {result['insights']}\n")

print("=" * 60)

# Output structured JSON format
import json
print("\n📦 STRUCTURED OUTPUT:")
output = {
    "saturation_score": result['saturation_score'],
    "saturation_impact_level": result['saturation_impact_level'],
    "market_penetration": result['market_penetration'],
    "repetition_risk": result['repetition_risk'],
    "fatigue_detected": str(result['fatigue_detected'])
}
print(json.dumps(output, indent=2))

print("\n✅ Test complete!")
