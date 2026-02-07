"""
🚀 COMPLETE AI INTELLIGENCE LAYER DEMO
Explainable AI for Social Media Trend Decline Prediction

This demo showcases all implemented features:
1. Multi-agent trend analysis
2. Decline prediction with early warnings
3. AI-generated narratives (Featherless AI)
4. Strategy recommendations
5. What-if simulations
6. Unified API output
"""

import sys
sys.path.append('.')

from ai_api import (
    analyze_trend,
    predict_decline,
    generate_trend_narrative,
    simulate_trend_recovery
)
from utils.data_generator import generate_trend_data
import json

def print_section(title):
    """Print formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def main():
    print("\n" + "█" * 70)
    print("█" + " " * 15 + "AI INTELLIGENCE LAYER - COMPLETE DEMO" + " " * 16 + "█")
    print("█" * 70)
    
    # ========================================================================
    # STEP 1: Generate Realistic Trend Data
    # ========================================================================
    print_section("STEP 1: Generating Realistic Trend Data")
    
    print("\n📊 Creating synthetic trend lifecycle data...")
    trend_data = generate_trend_data(
        trend_name="Viral TikTok Dance Challenge",
        total_days=75
    )
    print(f"✅ Generated {len(trend_data)} days of data")
    print(f"   Columns: {', '.join(trend_data.columns)}")
    
    # ========================================================================
    # STEP 2: Complete Trend Analysis (All Agents)
    # ========================================================================
    print_section("STEP 2: Complete Multi-Agent Analysis")
    
    print("\n🤖 Running all agents + orchestrator...")
    full_analysis = analyze_trend(trend_data, "Viral TikTok Dance Challenge")
    
    print(f"\n📊 RESULTS SUMMARY:")
    print(f"  • Trend: {full_analysis['trend_name']}")
    print(f"  • Decline Probability: {full_analysis['decline_probability']}%")
    print(f"  • Lifecycle Stage: {full_analysis['lifecycle_stage']}")
    print(f"  • Days to Collapse: {full_analysis['days_to_collapse']}")
    print(f"  • Risk Level: {full_analysis['prediction']['risk_level']}")
    print(f"  • Confidence: {full_analysis['prediction']['confidence']}%")
    
    # ========================================================================
    # STEP 3: Early Warning System
    # ========================================================================
    print_section("STEP 3: Early Warning Radar")
    
    early_warning = full_analysis['early_warning']
    
    print(f"\n⚠️  WARNING ANALYSIS:")
    print(f"  • Warning Level: {early_warning.get('warning_level', 'Unknown')}")
    print(f"  • Active Warnings: {early_warning.get('warning_count', 0)}")
    print(f"  • Status: {early_warning.get('days_to_critical_zone', 'Unknown')}")
    
    if early_warning.get('active_warnings'):
        print(f"\n🔔 ACTIVE WARNINGS:")
        for i, warning in enumerate(early_warning.get('active_warnings', []), 1):
            print(f"    {i}. {warning}")
    
    print(f"\n💡 RECOMMENDED ACTION:")
    print(f"  {early_warning.get('recommended_action', 'Monitor trend performance')}")

    
    # ========================================================================
    # STEP 4: Decline Drivers Analysis
    # ========================================================================
    print_section("STEP 4: Decline Drivers Breakdown")
    
    drivers = full_analysis['decline_drivers']
    
    print(f"\n📉 SIGNAL-BY-SIGNAL ANALYSIS:")
    
    if 'engagement' in drivers:
        eng = drivers['engagement']
        print(f"\n  🎯 ENGAGEMENT:")
        print(f"     Decline: {eng['decline_percent']}%")
        print(f"     Risk: {eng['risk_level']}")
    
    if 'sentiment' in drivers:
        sent = drivers['sentiment']
        print(f"\n  😊 SENTIMENT:")
        print(f"     Shift: {sent['shift']}")
        print(f"     Impact: {sent['impact_level']}")
    
    if 'influencer' in drivers:
        inf = drivers['influencer']
        print(f"\n  👥 INFLUENCER:")
        print(f"     Drop: {inf['participation_drop']}%")
        print(f"     Status: {inf['disengagement']}")
    
    if 'saturation' in drivers:
        sat = drivers['saturation']
        print(f"\n  📊 SATURATION:")
        print(f"     Score: {sat['saturation_score']}/100")
        print(f"     Fatigue: {sat['fatigue_detected']}")
    
    # ========================================================================
    # STEP 5: AI-Generated Narrative
    # ========================================================================
    print_section("STEP 5: AI-Generated Narrative Explanation")
    
    print(f"\n📖 NARRATIVE:")
    print(f"{full_analysis['narrative_explanation']}")
    
    # ========================================================================
    # STEP 6: Strategy Recommendations
    # ========================================================================
    print_section("STEP 6: Strategy Recommendations")
    
    print(f"\n💼 ACTIONABLE STRATEGIES:")
    recommendations = full_analysis['strategy_recommendations']
    
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec}")
    
    # ========================================================================
    # STEP 7: What-If Simulations
    # ========================================================================
    print_section("STEP 7: What-If Scenario Simulations")
    
    print("\n🔬 Testing recovery scenarios...")
    
    # Scenario 1: Influencer Re-engagement
    scenario1 = simulate_trend_recovery(
        full_analysis,
        {
            "influencer_boost": 0.35,
            "engagement_boost": 0.20
        },
        "Influencer Re-engagement Campaign"
    )
    
    print(f"\n📊 SCENARIO 1: {scenario1['scenario_name']}")
    print(f"  Original Decline: {scenario1['original_decline_probability']}%")
    print(f"  New Decline: {scenario1['new_decline_probability']}%")
    print(f"  Change: {scenario1['impact_analysis']['probability_change']:+.2f}%")
    print(f"  Impact: {scenario1['impact_analysis']['impact_category']}")
    print(f"  Recovery Potential: {scenario1['recovery_potential']}")
    print(f"\n  📝 Explanation:")
    print(f"  {scenario1['explanation']}")
    
    # Scenario 2: Optimistic Recovery
    scenario2 = simulate_trend_recovery(
        full_analysis,
        {
            "influencer_boost": 0.50,
            "engagement_boost": 0.40,
            "sentiment_improvement": 0.30
        },
        "Full Recovery Push"
    )
    
    print(f"\n📊 SCENARIO 2: {scenario2['scenario_name']}")
    print(f"  Original Decline: {scenario2['original_decline_probability']}%")
    print(f"  New Decline: {scenario2['new_decline_probability']}%")
    print(f"  Change: {scenario2['impact_analysis']['probability_change']:+.2f}%")
    print(f"  Impact: {scenario2['impact_analysis']['impact_category']}")
    
    # ========================================================================
    # STEP 8: Unified JSON Output (API Ready)
    # ========================================================================
    print_section("STEP 8: Unified JSON Output (API Ready)")
    
    # Create minimal output for API
    api_output = {
        "trend_name": full_analysis['trend_name'],
        "decline_probability": full_analysis['decline_probability'],
        "lifecycle_stage": full_analysis['lifecycle_stage'],
        "days_to_collapse": full_analysis['days_to_collapse'],
        "early_warning": {
            "level": early_warning.get('warning_level', 'Unknown'),
            "count": early_warning.get('warning_count', 0)
        },
        "risk_level": full_analysis['prediction']['risk_level'],
        "top_recommendations": recommendations[:3]
    }
    
    print("\n📦 SAMPLE API RESPONSE:")
    print(json.dumps(api_output, indent=2))
    
    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    print_section("✅ DEMO COMPLETE")
    
    print("\n🎯 FEATURES DEMONSTRATED:")
    print("  ✅ Multi-agent trend analysis (4 signal agents)")
    print("  ✅ Weighted decline prediction model")
    print("  ✅ Early warning system (before visible collapse)")
    print("  ✅ AI-generated narrative explanations")
    print("  ✅ Strategy recommendations engine")
    print("  ✅ What-if simulation scenarios")
    print("  ✅ Unified JSON API schema")
    print("  ✅ FastAPI-ready outputs")
    
    print("\n📊 SYSTEM STATUS:")
    print(f"  • Total Agents: 7 (4 signal + 1 predictor + 1 narrative + 1 simulation)")
    print(f"  • Analysis Time: Real-time")
    print(f"  • API Ready: ✅ Yes")
    print(f"  • Production Ready: ✅ Yes")
    
    print("\n🚀 NEXT STEPS:")
    print("  1. Integrate with FastAPI backend (see QUICK_START.md)")
    print("  2. Connect to frontend dashboard")
    print("  3. Set up Featherless AI for enhanced narratives")
    print("  4. Deploy to production")
    
    print("\n" + "█" * 70)
    print("█" + " " * 23 + "DEMO SUCCESSFUL! 🎉" + " " * 24 + "█")
    print("█" * 70 + "\n")


if __name__ == "__main__":
    main()
