# AI Intelligence Layer - Complete Documentation

## Overview

This is the complete AI intelligence layer for **Explainable AI for Social Media Trend Decline Prediction** hackathon project.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  AI Intelligence Layer                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌───────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Engagement   │  │  Sentiment   │  │  Influencer  │ │
│  │    Agent      │  │    Agent     │  │    Agent     │ │
│  └───────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│          │                 │                  │          │
│          └─────────────────┼──────────────────┘          │
│                            │                             │
│                  ┌─────────▼─────────┐                  │
│                  │  Saturation Agent │                  │
│                  └─────────┬─────────┘                  │
│                            │                             │
│                  ┌─────────▼──────────┐                 │
│                  │  Decline Predictor │                 │
│                  │  (Weighted Model)  │                 │
│                  └─────────┬──────────┘                 │
│                            │                             │
│          ┌─────────────────┴─────────────────┐          │
│          │                                   │          │
│   ┌──────▼────────┐               ┌─────────▼────────┐ │
│   │   Narrative   │               │    Simulation    │ │
│   │     Agent     │               │      Agent       │ │
│   │ (Featherless) │               │  (What-If Tests) │ │
│   └───────────────┘               └──────────────────┘ │
│                                                          │
│                  ┌────────────────┐                     │
│                  │  Orchestrator  │                     │
│                  │  (Coordinator) │                     │
│                  └────────┬───────┘                     │
│                           │                              │
│                  ┌────────▼────────┐                    │
│                  │   AI API Layer  │                    │
│                  │  (FastAPI Ready)│                    │
│                  └─────────────────┘                    │
└─────────────────────────────────────────────────────────┘
```

## 📁 File Structure

```
constipation/
├── agents/
│   ├── engagement_agent.py      # Engagement decline detection
│   ├── sentiment_agent.py       # Sentiment shift analysis
│   ├── influencer_agent.py      # Influencer disengagement tracking
│   ├── saturation_agent.py      # Market saturation detection
│   ├── decline_predictor.py     # Multi-signal prediction + Early Warning
│   ├── narrative_agent.py       # AI narrative generation (Featherless)
│   ├── simulation_agent.py      # What-if scenario testing
│   └── orchestrator.py          # Multi-agent coordinator
├── utils/
│   └── data_generator.py        # Synthetic trend data generator
├── ai_api.py                    # Unified API layer (FastAPI ready)
└── backend/
    └── main.py                  # FastAPI backend (integration point)
```

## 🚀 Features Implemented

### ✅ STEP 1: Featherless AI Integration
- **File**: `agents/narrative_agent.py`
- **Function**: `generate_trend_narrative(trend_analysis_output)`
- **Features**:
  - Integrates Featherless AI via Python requests
  - Accepts API key via `FEATHERLESS_API_KEY` environment variable
  - Uses `/v1/completions` endpoint
  - Explains decline reasons with business interpretation
  - Provides high-level strategy recommendations
  - Fallback to template-based generation if API unavailable

### ✅ STEP 2: Strategy Recommendation Engine
- **File**: `agents/narrative_agent.py`
- **Method**: `generate_strategy_recommendations()`
- **Includes**:
  - Revival strategies
  - Marketing recommendations
  - Influencer re-engagement ideas
  - Content refresh suggestions
  - Factor-specific recommendations
  - Stage-specific strategies

### ✅ STEP 3: What-If Simulation Agent
- **File**: `agents/simulation_agent.py`
- **Class**: `TrendSimulationAgent`
- **Capabilities**:
  - Accepts modified parameters (influencer_ratio, engagement_rate, sentiment_score, saturation_score)
  - Recalculates decline probability using predictor logic
  - Predicts new lifecycle stage
  - Estimates recovery or collapse timeline
  - Supports multiple scenario testing

### ✅ STEP 4: Simulation Explanation
- **Integration**: Simulation outputs → Narrative Agent
- **Method**: `generate_simulation_explanation()`
- **Output Example**: 
  ```
  "If influencer participation increases 30%, decline risk drops to 42%..."
  ```

### ✅ STEP 5: Early Warning Signal Generator
- **File**: `agents/decline_predictor.py`
- **Method**: `_detect_early_warnings()`
- **Features**:
  - Detects early decline signals before visible collapse
  - Calculates warning threshold (45% default)
  - Predicts estimated days to collapse
  - Provides warning levels: Critical, High, Moderate, Low
  - Returns actionable recommended actions

### ✅ STEP 6: Unified AI Output Schema
- **Implementation**: `ai_api.py` → `_build_unified_output()`
- **Schema**:
  ```json
  {
    "trend_name": "",
    "decline_probability": 0,
    "lifecycle_stage": "",
    "days_to_collapse": "",
    "early_warning": {
      "warning_level": "",
      "active_warnings": [],
      "recommended_action": ""
    },
    "decline_drivers": {
      "engagement": {},
      "sentiment": {},
      "influencer": {},
      "saturation": {}
    },
    "narrative_explanation": "",
    "strategy_recommendations": [],
    "simulation_results": {},
    "prediction": {
      "risk_level": "",
      "confidence": 0,
      "contributing_factors": []
    }
  }
  ```

### ✅ STEP 7: Backend Integration Functions
- **File**: `ai_api.py`
- **Functions**:
  1. `analyze_trend(data)` - Complete trend analysis
  2. `predict_decline(data)` - Decline prediction
  3. `generate_trend_narrative(data)` - AI narrative generation
  4. `simulate_trend_recovery(data)` - What-if simulations
- **All return structured JSON for FastAPI consumption**

### ✅ STEP 8: Code Quality
- ✅ Modular agent architecture
- ✅ Clean docstrings on all functions
- ✅ Comprehensive error handling
- ✅ API-ready outputs with standardized schemas

## 📊 API Usage Examples

### Example 1: Analyze Trend

```python
from ai_api import analyze_trend
from utils.data_generator import generate_trend_data

# Generate or load trend data
trend_data = generate_trend_data("Viral Dance", total_days=60)

# Analyze
results = analyze_trend(trend_data, api_key="your_featherless_key")

print(f"Decline: {results['decline_probability']}%")
print(f"Stage: {results['lifecycle_stage']}")
print(f"Narrative: {results['narrative_explanation']}")
```

### Example 2: Predict Decline

```python
from ai_api import predict_decline

prediction = predict_decline(trend_data)

print(f"Probability: {prediction['decline_probability']}%")
print(f"Days to Collapse: {prediction['days_to_collapse']}")
print(f"Early Warning: {prediction['early_warning']['warning_level']}")
```

### Example 3: Simulate Recovery

```python
from ai_api import simulate_trend_recovery

baseline = analyze_trend(trend_data)

scenario = simulate_trend_recovery(
    baseline,
    {"influencer_boost": 0.30, "engagement_boost": 0.25},
    "Influencer Campaign"
)

print(f"Original: {scenario['original_decline_probability']}%")
print(f"New: {scenario['new_decline_probability']}%")
print(f"Explanation: {scenario['explanation']}")
```

## 🔧 FastAPI Integration

```python
# backend/main.py

from fastapi import FastAPI
from ai_api import analyze_trend, predict_decline, simulate_trend_recovery
import pandas as pd

app = FastAPI()

@app.post("/api/analyze-trend")
async def api_analyze_trend(data: dict):
    """Analyze trend endpoint"""
    df = pd.DataFrame(data['trend_data'])
    results = analyze_trend(df, data.get('trend_name'))
    return results

@app.post("/api/predict-decline")
async def api_predict_decline(data: dict):
    """Predict decline endpoint"""
    df = pd.DataFrame(data['trend_data'])
    prediction = predict_decline(df)
    return prediction

@app.post("/api/simulate-recovery")
async def api_simulate_recovery(data: dict):
    """Simulate recovery endpoint"""
    baseline = data['baseline_analysis']
    params = data['scenario_params']
    name = data.get('scenario_name', 'Scenario')
    
    results = simulate_trend_recovery(baseline, params, name)
    return results
```

## 🎯 Key Capabilities

1. **Multi-Signal Analysis**: 4 specialized agents (Engagement, Sentiment, Influencer, Saturation)
2. **Weighted Prediction**: 35% Engagement, 25% Influencer, 20% Sentiment, 20% Saturation
3. **Lifecycle Detection**: Growth → Peak → Early Decline → Rapid Collapse → Dead Trend
4. **Early Warning Radar**: Detects decline signals before visible collapse
5. **AI Narratives**: Featherless AI-powered explanations
6. **What-If Simulations**: Test recovery scenarios with modified parameters
7. **Strategy Recommendations**: Actionable business strategies
8. **Unified JSON Schema**: FastAPI-ready standardized outputs

## 🔐 Environment Variables

```bash
# .env file
FEATHERLESS_API_KEY=your_api_key_here
```

## 📈 Testing

Run individual tests:
```bash
python agents/engagement_agent.py
python agents/sentiment_agent.py
python agents/influencer_agent.py
python agents/saturation_agent.py
python agents/decline_predictor.py
python agents/narrative_agent.py
python agents/simulation_agent.py
python agents/orchestrator.py
```

Run complete integration test:
```bash
python ai_api.py
```

## 🎓 Model Details

### Decline Prediction Model
- **Type**: Weighted ensemble model
- **Inputs**: 4 normalized signal scores (0-100)
- **Output**: Decline probability (0-100%)
- **Weights**: Configurable per signal type
- **Confidence**: Signal coverage-based (0-100%)

### Early Warning System
- **Threshold**: 45% probability
- **Warning Levels**: Critical, High, Moderate, Low
- **Signals**: 6+ early indicators
- **Prediction Horizon**: 5-60 days

## 📝 Output Schema Fields

| Field | Type | Description |
|-------|------|-------------|
| `trend_name` | string | Trend identifier |
| `decline_probability` | float | 0-100% decline risk |
| `lifecycle_stage` | string | Growth/Peak/Early Decline/Rapid Collapse/Dead |
| `days_to_collapse` | string | Estimated timeline |
| `early_warning` | object | Early warning signals |
| `decline_drivers` | object | Per-signal breakdown |
| `narrative_explanation` | string | AI-generated explanation |
| `strategy_recommendations` | array | Actionable strategies |
| `simulation_results` | object | What-if scenario outputs |

## ✨ Production Ready

This AI intelligence layer is fully production-ready with:
- ✅ Modular architecture
- ✅ Error handling
- ✅ API documentation
- ✅ Test coverage
- ✅ Standardized outputs
- ✅ FastAPI compatibility
- ✅ Environment configuration
- ✅ Scalable design

## 🎉 Complete Feature Matrix

| Feature | Status | File |
|---------|--------|------|
| Engagement Analysis | ✅ | `engagement_agent.py` |
| Sentiment Analysis | ✅ | `sentiment_agent.py` |
| Influencer Analysis | ✅ | `influencer_agent.py` |
| Saturation Analysis | ✅ | `saturation_agent.py` |
| Decline Prediction | ✅ | `decline_predictor.py` |
| Early Warning | ✅ | `decline_predictor.py` |
| AI Narratives | ✅ | `narrative_agent.py` |
| What-If Simulations | ✅ | `simulation_agent.py` |
| Orchestration | ✅ | `orchestrator.py` |
| API Layer | ✅ | `ai_api.py` |
| Data Generation | ✅ | `data_generator.py` |

---

**Ready for hackathon demo and backend integration!** 🚀
