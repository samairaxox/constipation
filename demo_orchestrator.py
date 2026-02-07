"""
Comprehensive Orchestrator Demo with Real Synthetic Data
"""

import sys
sys.path.append('.')

from utils.data_generator import generate_trend_data
from agents.orchestrator import TrendOrchestrator
import json

print("🚀 TREND DECLINE PREDICTION SYSTEM - FULL DEMO")
print("="*70)
print()

# Generate realistic trend data
print("📊 Generating realistic trend lifecycle data...")
trend_data = generate_trend_data("Viral TikTok Dance Challenge", total_days=75)
print()

# Initialize orchestrator
orchestrator = TrendOrchestrator()
print()

# Run comprehensive analysis
results = orchestrator.analyze_trend(trend_data)

# Display comprehensive results
print("\n" + "█"*70)
print("█" + " "*20 + "COMPREHENSIVE ANALYSIS RESULTS" + " "*19 + "█")
print("█"*70)

print(f"\n📋 TREND INFORMATION:")
print(f"  • Name: {results['metadata']['trend_name']}")
print(f"  • Data Points: {results['metadata']['data_points']} days")
print(f"  • Period: {results['metadata']['start_date']} to {results['metadata']['end_date']}")
print(f"  • Analyzed: {results['metadata']['analysis_timestamp']}")

print(f"\n📊 EXECUTIVE SUMMARY:")
print(f"  {results['executive_summary']}")

print(f"\n🎯 DECLINE PREDICTION:")
print(f"  • Probability: {results['prediction']['decline_probability']}%")
print(f"  • Stage: {results['prediction']['lifecycle_stage']}")
print(f"  • Risk: {results['prediction']['risk_level']}")
print(f"  • Days to Collapse: {results['prediction']['days_to_collapse']}")
print(f"  • Confidence: {results['prediction']['confidence']}%")

print(f"\n📈 KEY METRICS:")
for metric, value in results['key_metrics'].items():
    metric_name = metric.replace('_', ' ').title()
    print(f"  • {metric_name}: {value:.2f}")

print(f"\n🔔 ALERTS ({len(results['alerts'])}):")
if results['alerts']:
    for alert in results['alerts']:
        icon = "🚨" if alert['severity'] == "Critical" else "⚠️" if alert['severity'] == "High" else "ℹ️"
        print(f"  {icon} [{alert['severity']}] {alert['source']}")
        print(f"     → {alert['message']}")
else:
    print("  ✅ No critical alerts")

print(f"\n🔝 TOP CONTRIBUTING FACTORS:")
for i, factor in enumerate(results['contributing_factors'][:3], 1):
    print(f"  {i}. {factor['factor'].upper()}: {factor['contribution']} points")

print(f"\n💡 RECOMMENDATIONS:")
for i, rec in enumerate(results['recommendations'], 1):
    print(f"  {i}. {rec}")

print(f"\n📦 SIGNAL AGENT DETAILS:")
print(f"  • Engagement: {results['signal_details']['engagement']['risk_level']} risk")
print(f"  • Sentiment: {results['signal_details']['sentiment']['impact_level']} impact")
print(f"  • Influencer: {results['signal_details']['influencer']['disengagement_status']}")
print(f"  • Saturation: {results['signal_details']['saturation']['saturation_stage']}")

# Output JSON summary
print("\n" + "="*70)
print("STRUCTURED JSON OUTPUT")
print("="*70)

summary_output = {
    "trend": results['metadata']['trend_name'],
    "prediction": {
        "decline_probability": results['prediction']['decline_probability'],
        "lifecycle_stage": results['prediction']['lifecycle_stage'],
        "risk_level": results['prediction']['risk_level'],
        "days_to_collapse": results['prediction']['days_to_collapse']
    },
    "key_metrics": results['key_metrics'],
    "alert_count": len(results['alerts']),
    "top_factor": results['contributing_factors'][0]['factor'] if results['contributing_factors'] else None
}

print(json.dumps(summary_output, indent=2))

print("\n" + "="*70)
print("✅ COMPREHENSIVE DEMO COMPLETE!")
print("="*70)

print("\n📊 System Summary:")
print(f"  • Total Agents: 5 (4 signal + 1 predictor)")
print(f"  • Analysis Status: {results['status'].upper()}")
print(f"  • Overall Health: {'🟢 HEALTHY' if results['prediction']['risk_level'] in ['Low', 'Medium'] else '🔴 AT RISK'}")
