from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import (
    TrendAnalysisRequest, TrendAnalysisResponse,
    EarlyWarningResponse,
    NarrativeRequest, NarrativeResponse,
    SimulationRequest, SimulationResponse,
    ChatRequest, ChatResponse
)
from .services import (
    analyze_trend_stub,
    get_early_warning_stub,
    featherless_narrative_agent,
    run_simulation_stub,
    chat_stub
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "Backend running"}

@app.post("/trend-analysis", response_model=TrendAnalysisResponse)
def trend_analysis(request: TrendAnalysisRequest):
    return analyze_trend_stub(request.trend_data)

@app.post("/early-warning", response_model=EarlyWarningResponse)
def early_warning(request: TrendAnalysisRequest):
    return get_early_warning_stub(request.trend_data)

@app.post("/trend-narrative", response_model=NarrativeResponse)
def trend_narrative(request: NarrativeRequest):
    return featherless_narrative_agent(request.trend_data)

@app.post("/simulate-recovery", response_model=SimulationResponse)
def simulate_recovery(request: SimulationRequest):
    return run_simulation_stub(request)

@app.post("/chat-analysis", response_model=ChatResponse)
def chat_analysis(request: ChatRequest):
    return chat_stub(request.user_query, request.trend_context)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
