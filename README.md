# 🎯 Explainable AI for Social Media Trend Decline Prediction

> **Complete AI Intelligence Layer - Gen AI Hackathon 2026**

**Status**: ✅ **ALL 11 STEPS COMPLETE + DECISION INTELLIGENCE ENHANCEMENTS - PRODUCTION READY**

---

## 🚀 What This Project Does

This is a complete AI-powered system that:

1. **Predicts** when social media trends will decline (0-100% probability)
2. **Warns** you early before collapse happens (45% threshold)
3. **Explains** WHY trends are declining using AI (Featherless AI)
4. **Recommends** strategies to save dying trends  
5. **Simulates** what-if recovery scenarios
6. **Works** with both synthetic and real Kaggle datasets

---

## 📚 Documentation Hub

### 🎯 Start Here

| Document | Best For | Read Time |
|----------|----------|-----------|
| **[FINAL_SUMMARY.md](./FINAL_SUMMARY.md)** | Complete overview of all 11 steps | 10 min |
| **[QUICK_START.md](./QUICK_START.md)** | Get running in 5 minutes | 5 min |
| **[IMPLEMENTATION_COMPLETE.md](./IMPLEMENTATION_COMPLETE.md)** | Feature details (Steps 1-4) | 15 min |
| **[REAL_DATASET_GUIDE.md](./REAL_DATASET_GUIDE.md)** | Real data integration (Steps 5-11) | 15 min |
| **[AI_LAYER_README.md](./AI_LAYER_README.md)** | Technical architecture | 20 min |

---

## ⚡ Quick Demo

### Option 1: Synthetic Data (No Setup Required)

```bash
python demo_complete.py
```

### Option 2: Real Kaggle Data

```bash
# Install Kaggle dependencies
pip install kagglehub scikit-learn

# Run real data pipeline
python real_dataset_pipeline.py
```

### Option 3: API Usage

```python
from ai_api import analyze_trend
from utils.data_generator import generate_trend_data

# Generate sample trend
data = generate_trend_data("Viral Dance", total_days=60)

# Analyze
results = analyze_trend(data)

# View results
print(f"Decline Probability: {results['decline_probability']}%")
print(f"Lifecycle Stage: {results['lifecycle_stage']}")
print(f"Early Warning: {results['early_warning']['warning_level']}")
print(f"\nNarrative: {results['narrative_explanation']}")
print(f"\nRecommendations:")
for rec in results['strategy_recommendations'][:3]:
    print(f"  • {rec}")
```

---

## 🏗️ System Architecture

```
┌────────────────────────────────────────┐
│      DATA SOURCES                      │
│  • Synthetic (data_generator.py)      │
│  • Real Kaggle (kaggle_loader.py) NEW!│
└──────────────┬─────────────────────────┘
               │
┌──────────────▼─────────────────────────┐
│   DATA PROCESSING (NEW!)               │
│  • Clean (data_preprocessor.py)        │
│  • Engineer Features                   │
│  • Transform to Time-Series            │
└──────────────┬─────────────────────────┘
               │
┌──────────────▼─────────────────────────┐
│   SIGNAL AGENTS (4)                    │
│  • Engagement                          │
│  • Sentiment                           │
│  • Influencer                          │
│  • Saturation                          │
└──────────────┬─────────────────────────┘
               │
┌──────────────▼─────────────────────────┐
│   DECLINE PREDICTOR                    │
│  • Weighted Model (35/25/20/20)        │
│  • Early Warning System NEW!           │
└──────────────┬─────────────────────────┘
               │
       ┌───────┴───────┐
       │               │
┌──────▼──────┐ ┌─────▼───────┐
│  NARRATIVE  │ │ SIMULATION  │
│   AGENT     │ │   AGENT     │
│(Featherless)│ │ (What-If)   │
└──────┬──────┘ └─────┬───────┘
       │               │
       └───────┬───────┘
               │
┌──────────────▼─────────────────────────┐
│   UNIFIED API LAYER                    │
│  • analyze_trend()                     │
│  • predict_decline()                   │
│  • generate_trend_narrative()          │
│  • simulate_trend_recovery()           │
└────────────────────────────────────────┘
```

---

## 📊 Complete Feature List

### ✅ Steps 1-4: AI Intelligence Layer
- ✅ Featherless AI integration for narratives
- ✅ Strategy recommendation engine
- ✅ What-if simulation agent
- ✅ Simulation explanations

### ✅ Steps 5-8: Data Integration
- ✅ Kaggle dataset loading
- ✅ Data cleaning (duplicates, missing values, normalization)
- ✅ Feature engineering (engagement_rate, influencer_ratio, etc.)
- ✅ Time-series transformation (lifecycle format)

### ✅ Steps 9-11: Complete Integration
- ✅ Agent integration with real data
- ✅ AI narratives from real insights
- ✅ Unified JSON output schema

---

## 🎯 Key Capabilities

| Capability | Details |
|------------|---------|
| **Multi-Signal Analysis** | 4 specialized agents analyzing different trend aspects |
| **Decline Prediction** | 0-100% probability with weighted model |
| **Early Warning** | Detects problems at 45% threshold (before visible collapse) |
| **Lifecycle Detection** | 5 stages: Growth → Peak → Early Decline → Rapid Collapse → Dead |
| **AI Narratives** | Featherless AI generates human-readable explanations |
| **Strategy Recommendations** | 8+ actionable business strategies |
| **What-If Simulations** | Test recovery scenarios with modified parameters |
| **Real Data Support** | Works with Kaggle social media datasets |
| **Unified API** | 4 FastAPI-ready functions |

---

## 📦 Installation

### Core System
```bash
pip install -r requirements.txt
```

### Real Dataset Support
```bash
pip install -r requirements_kaggle.txt
```

### Optional: Featherless AI
```bash
# Create .env file
echo "FEATHERLESS_API_KEY=your_key_here" > .env
```

---

## 🧪 Testing

### Test Individual Components
```bash
# Test agents
python agents/engagement_agent.py
python agents/narrative_agent.py
python agents/simulation_agent.py

# Test data processing
python  utils/kaggle_loader.py
python utils/data_preprocessor.py
python utils/timeseries_transformer.py

# Test API layer
python ai_api.py
```

### Test Complete System
```bash
# Synthetic data demo
python demo_complete.py

# Real data pipeline
python real_dataset_pipeline.py
```

---

## 📈 Sample Output

```json
{
  "trend_name": "Viral Dance Challenge",
  "decline_probability": 67.5,
  "lifecycle_stage": "Early Decline",
  "days_to_collapse": "15-25 days",
  "early_warning": {
    "warning_level": "High",
    "active_warnings": [
      "Engagement showing early decline signs",
      "Market saturation approaching critical levels"
    ],
    "recommended_action": "Urgent attention needed - activate mitigation measures within 48 hours"
  },
  "narrative_explanation": "The trend is currently in the Early Decline phase with a 67.5% decline probability. This indicates high risk and warrants urgent attention. The primary decline driver is engagement, showing a 55% drop from peak levels...",
  "strategy_recommendations": [
    "Launch interactive challenges or contests to boost engagement",
    "Re-engage key influencers with exclusive partnership opportunities",
    "Create user-generated content campaigns to drive participation"
  ]
}
```

---

## 🔧 API Functions

```python
# 1. Complete Analysis
analyze_trend(data, trend_name, api_key)
# Returns: Full analysis with all insights

# 2. Quick Decline Check
predict_decline(data, api_key)
# Returns: Decline probability + early warning

# 3. AI Narrative Only
generate_trend_narrative(analysis_data, api_key)
# Returns: Explanation text

# 4. What-If Simulation
simulate_trend_recovery(baseline, params, scenario_name, api_key)
# Returns: Simulation results + impact
```

---

## 🎓 Use Cases

### Use Case 1: Marketing Team
```python
# Check if campaign is declining
results = predict_decline(campaign_data)

if results['early_warning']['warning_level'] in ['High', 'Critical']:
    print("🚨 Campaign needs intervention!")
    print(f"Time left: {results['days_to_collapse']}")
```

### Use Case 2: Content Strategy
```python
# Analyze trend and get recommendations
analysis = analyze_trend(trend_data, "Hashtag Challenge")

print(f"Strategies to try:")
for strategy in analysis['strategy_recommendations']:
    print(f"  • {strategy}")
```

### Use Case 3: Executive Dashboard
```python
# Test recovery scenarios
scenario = simulate_trend_recovery(
    baseline_analysis,
    {"influencer_boost": 0.30, "engagement_boost": 0.25},
    "Influencer Campaign"
)

print(f"Expected decline reduction: {scenario['impact_analysis']['probability_change']}%")
```

---

## 📁 Project Structure

```
constipation/
├── agents/                  # AI agents
│   ├── engagement_agent.py
│   ├── sentiment_agent.py
│   ├── influencer_agent.py
│   ├── saturation_agent.py
│   ├── decline_predictor.py
│   ├── narrative_agent.py   # Steps 1-2
│   ├── simulation_agent.py  # Steps 3-4
│   └── orchestrator.py
│
├── utils/                   # Data utilities
│   ├── data_generator.py    # Synthetic data
│   ├── kaggle_loader.py     # Step 5 NEW!
│   ├── data_preprocessor.py # Steps 6-7 NEW!
│   └── timeseries_transformer.py # Step 8 NEW!
│
├── ai_api.py               # Steps 11 - Unified API
├── real_dataset_pipeline.py # Steps 9-10 NEW!
└── demo_complete.py        # Full demo
```

---

## 🏆 Hackathon Highlights

**What Makes This Special**:

1. 🧠 **Explainable AI** - Not just predictions, full narratives
2. ⚠️ **Early Detection** - Warns before problems are visible
3. 🎯 **Actionable** - Specific strategies, not just analytics
4. 🔬 **Interactive** - What-if simulations for planning
5. 📊 **Real Data** - Works with actual Kaggle datasets
6. 🚀 **Production-Ready** - FastAPI compatible, fully documented

---

## 🎉 Status Summary

**ALL FEATURES COMPLETE ✅**

- ✅ 11/11 Steps implemented
- ✅ 7 AI agents operational
- ✅ Real + Synthetic data support
- ✅ Complete documentation
- ✅ FastAPI-ready
- ✅ Demo scripts ready
- ✅ **Production-ready for hackathon**

---

## 💡 Next Steps

1. **Test the system**: Run `python demo_complete.py`
2. **Try real data**: Run `python real_dataset_pipeline.py`
3. **Integrate backend**: Use functions from `ai_api.py`
4. **Build frontend**: Display results from unified JSON
5. **Set up Featherless AI**: Add API key for enhanced narratives
6. **Demo preparation**: Use complete demo script

---

## 📞 Quick Links

- **Main Documentation**: [FINAL_SUMMARY.md](./FINAL_SUMMARY.md)
- **Quick Start**: [QUICK_START.md](./QUICK_START.md)
- **Real Data Guide**: [REAL_DATASET_GUIDE.md](./REAL_DATASET_GUIDE.md)
- **Technical Docs**: [AI_LAYER_README.md](./AI_LAYER_README.md)

---

## 🎯 YOU ARE READY TO WIN THE HACKATHON! 🏆

Your AI Intelligence Layer is:
- ✅ Fully implemented (all 11 steps)
- ✅ Thoroughly tested
- ✅ Completely documented
- ✅ Production-ready
- ✅ Demo-ready

**Time to present and WIN! 🎉**

---

*Last Updated: February 7, 2026*  
*Gen AI Hackathon - Explainable AI for Social Media Trend Decline Prediction*
