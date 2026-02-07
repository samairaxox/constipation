# 🚀 Explainable AI for Social Media Trend Decline Prediction

> Complete AI Intelligence Layer for Gen AI Hackathon

**Status**: ✅ **PRODUCTION READY**

---

## 📚 Documentation Index

Start here to understand and use the system:

| Document | Purpose | Start Here If... |
|----------|---------|------------------|
| **[IMPLEMENTATION_COMPLETE.md](./IMPLEMENTATION_COMPLETE.md)** | Complete feature overview | You want to see what's implemented |
| **[QUICK_START.md](./QUICK_START.md)** | Quick start guide | You want to test the system in 5 minutes |
| **[AI_LAYER_README.md](./AI_LAYER_README.md)** | Technical documentation | You need API details and architecture |

---

## ⚡ Quick Links

### Want to...

- **Run a demo?** → `python demo_complete.py`
- **Test the API?** → `python ai_api.py`
- **See individual agents?** → `python agents/orchestrator.py`
- **Generate synthetic data?** → `python utils/data_generator.py`

### Need to...

- **Integrate with backend?** → See [QUICK_START.md](./QUICK_START.md) Section "FastAPI Integration"
- **Understand the architecture?** → See [AI_LAYER_README.md](./AI_LAYER_README.md) Section "Architecture"
- **Set up Featherless AI?** → Add `FEATHERLESS_API_KEY` to `.env` file

---

## 🎯 What This System Does

1. **Analyzes social media trends** using 4 specialized AI agents
2. **Predicts decline probability** with 0-100% accuracy score
3. **Detects early warnings** before visible collapse (45% threshold)
4. **Generates AI narratives** explaining WHY trends decline
5. **Recommends strategies** for revival and mitigation
6. **Simulates what-if scenarios** to test recovery plans
7. **Returns unified JSON** ready for FastAPI consumption

---

## 🏗️ System Components

```
📦 AI Intelligence Layer
│
├── 🤖 Signal Agents (4)
│   ├── Engagement Analysis
│   ├── Sentiment Tracking
│   ├── Influencer Monitoring
│   └── Saturation Detection
│
├── 🧠 Prediction Engine
│   ├── Weighted Decline Model
│   └── Early Warning Radar
│
├── 💬 AI Layer
│   ├── Narrative Generation (Featherless AI)
│   └── What-If Simulations
│
└── 🔌 API Layer
    └── FastAPI-Ready Functions
```

---

## ✅ Features Checklist

### Core Signal Analysis
- ✅ Engagement decline detection
- ✅ Sentiment shift tracking
- ✅ Influencer disengagement monitoring
- ✅ Market saturation analysis

### Prediction & Intelligence
- ✅ Weighted decline prediction (35/25/20/20 model)
- ✅ Lifecycle stage detection (5 stages)
- ✅ Early warning system (before 45% threshold)
- ✅ Days-to-collapse estimation

### AI-Powered Features
- ✅ Featherless AI narrative generation
- ✅ Business strategy recommendations
- ✅ What-if simulation scenarios
- ✅ Simulation explanations

### API & Integration
- ✅ Unified JSON output schema
- ✅ 4 backend integration functions
- ✅ FastAPI-compatible responses
- ✅ Complete error handling

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Complete Demo
```bash
python demo_complete.py
```

### 3. Test Individual Components
```bash
python ai_api.py
```

### 4. (Optional) Set Featherless AI Key
```bash
echo "FEATHERLESS_API_KEY=your_key" > .env
```

---

## 📊 Sample Usage

```python
from ai_api import analyze_trend
from utils.data_generator import generate_trend_data

# Generate data
trend_data = generate_trend_data("Viral Dance", total_days=60)

# Analyze
results = analyze_trend(trend_data)

# View results
print(f"Decline: {results['decline_probability']}%")
print(f"Stage: {results['lifecycle_stage']}")
print(f"Early Warning: {results['early_warning']['warning_level']}")
print(f"Narrative: {results['narrative_explanation']}")
```

---

## 📁 Key Files

### Agents
- `agents/engagement_agent.py` - Engagement analysis
- `agents/sentiment_agent.py` - Sentiment tracking
- `agents/influencer_agent.py` - Influencer monitoring
- `agents/saturation_agent.py` - Saturation detection
- `agents/decline_predictor.py` - Prediction + Early warnings
- `agents/narrative_agent.py` - AI narratives + Strategies
- `agents/simulation_agent.py` - What-if scenarios
- `agents/orchestrator.py` - Multi-agent coordinator

### API & Integration
- `ai_api.py` - **Main API layer** (FastAPI ready)
- `utils/data_generator.py` - Synthetic data generation

### Demos & Tests
- `demo_complete.py` - **Full system demo**
- `test_*.py` - Individual component tests

---

## 🎓 Architecture Highlights

### Weighted Prediction Model
```
Decline Probability = (
    Engagement × 35% +
    Influencer × 25% +
    Sentiment × 20% +
    Saturation × 20%
)
```

### Lifecycle Stages
1. **Growth** (0-25%): Healthy expansion
2. **Peak** (25-45%): Maximum momentum
3. **Early Decline** (45-65%): Warning signs
4. **Rapid Collapse** (65-85%): Critical decline
5. **Dead Trend** (85-100%): Trend ended

### Early Warning Thresholds
- **Threshold**: 45% decline probability
- **Levels**: Critical, High, Moderate, Low
- **Prediction**: 5-60 days to collapse

---

## 🔧 API Functions (FastAPI Ready)

```python
# 1. Complete Analysis
analyze_trend(data, trend_name, api_key)

# 2. Decline Prediction Only
predict_decline(data, api_key)

# 3. AI Narrative Generation
generate_trend_narrative(analysis_data, api_key)

# 4. What-If Simulation
simulate_trend_recovery(baseline, params, scenario_name, api_key)
```

All functions return **structured JSON** compatible with FastAPI!

---

## 🏆 Hackathon Demo Points

1. ✨ **Explainable AI**: Full narrative explanations, not just numbers
2. ⚠️ **Early Detection**: Warns before problems are visible
3. 🎯 **Actionable**: Specific strategy recommendations
4. 🔬 **Interactive**: What-if simulations with real predictions
5. 🤖 **AI-Powered**: Featherless AI for natural language
6. 🚀 **Production-Ready**: Modular, documented, tested

---

## 📈 Performance Metrics

- **Agents**: 7 specialized AI agents
- **Code Lines**: ~3,200 lines
- **Analysis Time**: Real-time (<5 seconds)
- **Confidence**: Signal coverage-based (0-100%)
- **Accuracy**: Weighted multi-signal ensemble

---

## 🎯 Integration Path

### Backend (FastAPI)
```python
from fastapi import FastAPI
from ai_api import analyze_trend, predict_decline

app = FastAPI()

@app.post("/analyze")
async def analyze(data: dict):
    return analyze_trend(pd.DataFrame(data['trend_data']))
```

### Frontend (React)
```javascript
// Call backend
const response = await fetch('/analyze', {
    method: 'POST',
    body: JSON.stringify({ trend_data: data })
});

const results = await response.json();

// Display results
setDeclineProbability(results.decline_probability);
setNarrative(results.narrative_explanation);
```

---

## 📞 Support & Resources

- **Full Docs**: [AI_LAYER_README.md](./AI_LAYER_README.md)
- **Quick Start**: [QUICK_START.md](./QUICK_START.md)
- **Implementation**: [IMPLEMENTATION_COMPLETE.md](./IMPLEMENTATION_COMPLETE.md)

---

## 🎉 Ready for Hackathon!

Your AI Intelligence Layer is:
- ✅ Fully implemented
- ✅ Thoroughly tested
- ✅ Completely documented
- ✅ Production-ready
- ✅ FastAPI-compatible

**Time to demo and win! 🏆**

---

*Built for Gen AI Hackathon 2026*
*Explainable AI for Social Media Trend Decline Prediction*
