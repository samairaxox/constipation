# Quick Start Guide - AI Intelligence Layer

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Dependencies

```bash
pip install pandas numpy requests python-dotenv fastapi uvicorn
```

### Step 2: Set Up Environment (Optional - for AI narratives)

```bash
# Create .env file
echo "FEATHERLESS_API_KEY=your_api_key_here" > .env
```

### Step 3: Test the System

```python
# test_ai_system.py
from ai_api import analyze_trend
from utils.data_generator import generate_trend_data

# Generate sample data
trend_data = generate_trend_data("Viral Dance Challenge", total_days=60)

# Run complete analysis
results = analyze_trend(trend_data)

# View results
print(f"📊 Trend: {results['trend_name']}")
print(f"🎯 Decline Probability: {results['decline_probability']}%")
print(f"🔄 Lifecycle Stage: {results['lifecycle_stage']}")
print(f"⚠️  Early Warning: {results['early_warning']['warning_level']}")
print(f"\n📖 Narrative:")
print(results['narrative_explanation'])
print(f"\n💡 Recommendations:")
for rec in results['strategy_recommendations'][:3]:
    print(f"  • {rec}")
```

### Step 4: Run It

```bash
python test_ai_system.py
```

## 📊 Expected Output

```
📊 Trend: Viral Dance Challenge
🎯 Decline Probability: 67.5%
🔄 Lifecycle Stage: Early Decline
⚠️  Early Warning: High

📖 Narrative:
The trend is currently in the Early Decline phase with a 67.5% 
decline probability. This indicates high risk and warrants urgent 
attention. The primary decline driver is engagement, followed by 
influencer. Without intervention, the trend is estimated to 
collapse in 15-25 days.

💡 Recommendations:
  • Launch interactive challenges or contests to boost engagement
  • Re-engage key influencers with exclusive partnership opportunities
  • Monitor metrics daily and activate retention strategies
```

## 🎯 Use Cases

### Use Case 1: Real-Time Trend Monitoring

```python
from ai_api import predict_decline

# Quick decline check
prediction = predict_decline(trend_data)

if prediction['decline_probability'] > 60:
    print("⚠️ ALERT: High decline risk detected!")
    print(f"Action needed within: {prediction['days_to_collapse']}")
```

### Use Case 2: What-If Analysis

```python
from ai_api import simulate_trend_recovery

baseline = analyze_trend(trend_data)

# Test influencer campaign
campaign_result = simulate_trend_recovery(
    baseline,
    {
        "influencer_boost": 0.30,  # +30% influencers
        "engagement_boost": 0.20    # +20% engagement
    },
    "Influencer Reactivation Campaign"
)

print(f"Before: {campaign_result['original_decline_probability']}%")
print(f"After: {campaign_result['new_decline_probability']}%")
print(f"{campaign_result['explanation']}")
```

### Use Case 3: Early Warning Dashboard

```python
results = analyze_trend(trend_data)

early_warning = results['early_warning']

print(f"Warning Level: {early_warning['warning_level']}")
print(f"Active Warnings: {early_warning['warning_count']}")
print("\nWarnings:")
for warning in early_warning['active_warnings']:
    print(f"  ⚠️  {warning}")
print(f"\n🎯 Action: {early_warning['recommended_action']}")
```

## 🔌 FastAPI Integration Pattern

```python
# backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ai_api import analyze_trend, predict_decline, simulate_trend_recovery
import pandas as pd

app = FastAPI(title="Trend Decline Prediction API")

class TrendData(BaseModel):
    trend_data: list
    trend_name: str = "Unknown Trend"

class SimulationRequest(BaseModel):
    baseline_analysis: dict
    scenario_params: dict
    scenario_name: str = "Scenario"

@app.post("/analyze")
async def analyze(data: TrendData):
    """Complete trend analysis"""
    try:
        df = pd.DataFrame(data.trend_data)
        results = analyze_trend(df, data.trend_name)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict")
async def predict(data: TrendData):
    """Decline prediction only"""
    try:
        df = pd.DataFrame(data.trend_data)
        prediction = predict_decline(df)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/simulate")
async def simulate(data: SimulationRequest):
    """Run what-if simulation"""
    try:
        results = simulate_trend_recovery(
            data.baseline_analysis,
            data.scenario_params,
            data.scenario_name
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy", "service": "AI Intelligence Layer"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Start the API

```bash
python backend/main.py
```

### Test the API

```bash
# Visit http://localhost:8000/docs for interactive API documentation
```

## 🧪 More Examples

### Example: Batch Processing

```python
from ai_api import AIIntelligenceLayer
from utils.data_generator import generate_trend_data

ai = AIIntelligenceLayer()

trends = ["Dance Challenge", "Fashion Trend", "Meme Wave"]

for trend_name in trends:
    print(f"\n{'='*50}")
    print(f"Analyzing: {trend_name}")
    print('='*50)
    
    data = generate_trend_data(trend_name, total_days=45)
    results = ai.analyze_trend(data, trend_name)
    
    print(f"Decline: {results['decline_probability']}%")
    print(f"Stage: {results['lifecycle_stage']}")
    print(f"Warning: {results['early_warning']['warning_level']}")
```

### Example: Custom Signal Weights

```python
from agents.decline_predictor import DeclinePredictor

predictor = DeclinePredictor()

# Customize weights (must sum to 1.0)
predictor.WEIGHTS = {
    'engagement': 0.40,     # Increase engagement importance
    'influencer': 0.30,     # Increase influencer importance
    'sentiment': 0.15,      # Decrease sentiment
    'saturation': 0.15      # Decrease saturation
}

# Now use predictor with custom weights
```

## 🎓 Key Functions Summary

| Function | Purpose | Returns |
|----------|---------|---------|
| `analyze_trend()` | Complete analysis | Unified schema with all insights |
| `predict_decline()` | Quick decline check | Decline probability + early warning |
| `generate_trend_narrative()` | AI explanation only | Narrative text + insights |
| `simulate_trend_recovery()` | What-if testing | Simulation results + explanation |

## 📦 Required Data Format

### Input DataFrame Structure

```python
required_columns = [
    'date',               # Date (YYYY-MM-DD)
    'engagement_rate',    # Float (0.0-1.0)
    'sentiment_score',    # Float (0.0-1.0)
    'influencer_ratio',   # Float (0.0-1.0)
    'saturation_score'    # Float (0-100)
]

# Optional columns
optional_columns = [
    'trend_name',         # String
    'post_count',         # Integer
    'algorithm_boost'     # Float
]
```

### Example Data

```python
import pandas as pd

data = pd.DataFrame({
    'date': ['2026-01-01', '2026-01-02', '2026-01-03'],
    'engagement_rate': [0.12, 0.11, 0.10],
    'sentiment_score': [0.75, 0.72, 0.68],
    'influencer_ratio': [0.20, 0.18, 0.15],
    'saturation_score': [45.0, 50.0, 55.0]
})
```

## 🔥 Pro Tips

1. **Use Early Warnings**: Check `early_warning.warning_level` before decline reaches 65%
2. **Test Scenarios**: Run simulations to find optimal recovery strategies
3. **Monitor Velocity**: Check `decay_speed` for rapid decline detection
4. **Batch Analysis**: Process multiple trends to find common patterns
5. **Custom Weights**: Adjust predictor weights based on your domain

## 🐛 Troubleshooting

**Issue**: No API key for Featherless AI
**Solution**: System uses template-based narratives automatically. Set `FEATHERLESS_API_KEY` for AI-generated narratives.

**Issue**: Missing DataFrame columns
**Solution**: Use `generate_trend_data()` or ensure your data has required columns.

**Issue**: Low confidence scores
**Solution**: Provide more complete time-series data (60+ days recommended).

## 🎯 Next Steps

1. ✅ Test with your own trend data
2. ✅ Integrate with FastAPI backend
3. ✅ Set up Featherless AI for advanced narratives
4. ✅ Build frontend dashboard to visualize results
5. ✅ Deploy to production

---

**You're ready to predict trend declines with AI! 🚀**
