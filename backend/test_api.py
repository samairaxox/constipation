import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    print("Testing GET / ...", end=" ")
    try:
        r = requests.get(f"{BASE_URL}/")
        assert r.status_code == 200
        assert r.json() == {"status": "Backend running"}
        print("OK")
    except Exception as e:
        print(f"FAIL: {e}")

def test_trend_analysis():
    print("Testing POST /trend-analysis ...", end=" ")
    payload = {"trend_data": {"id": 123, "name": "Test Trend"}}
    try:
        r = requests.post(f"{BASE_URL}/trend-analysis", json=payload)
        assert r.status_code == 200
        data = r.json()
        assert "decline_probability" in data
        assert "lifecycle_stage" in data
        print("OK")
    except Exception as e:
        print(f"FAIL: {e}")
        print(r.text)

def test_early_warning():
    print("Testing POST /early-warning ...", end=" ")
    payload = {"trend_data": {"id": 123, "name": "Disappearing Trend", "engagement_rate": 0.1, "sentiment_score": -0.5}}
    try:
        r = requests.post(f"{BASE_URL}/early-warning", json=payload)
        assert r.status_code == 200
        data = r.json()
        assert "risk_level" in data
        print("OK")
    except Exception as e:
        print(f"FAIL: {e}")
        print(r.text)

def test_narrative():
    print("Testing POST /trend-narrative ...", end=" ")
    payload = {"trend_data": {"id": 123, "text": "Viral decline observed"}}
    try:
        r = requests.post(f"{BASE_URL}/trend-narrative", json=payload)
        assert r.status_code == 200
        data = r.json()
        assert "explanation" in data
        assert "source" in data
        assert "model" in data
        # Check if it handled the missing key gracefully or if key is provided
        if data["source"] == "Featherless.ai":
            print(f"OK (Featherless response received)")
        else:
            print(f"OK (Mock/Error response: {data['source']})")
    except Exception as e:
        print(f"FAIL: {e}")
        print(r.text)

def test_simulation():
    print("Testing POST /simulate-recovery ...", end=" ")
    payload = {
        "influencer_ratio": 0.5,
        "engagement_rate": 0.8,
        "sentiment_score": 0.9
    }
    try:
        r = requests.post(f"{BASE_URL}/simulate-recovery", json=payload)
        assert r.status_code == 200
        data = r.json()
        assert "new_decline_probability" in data
        print("OK")
    except Exception as e:
        print(f"FAIL: {e}")
        print(r.text)

def test_chat():
    print("Testing POST /chat-analysis ...", end=" ")
    payload = {"user_query": "What's happening?", "trend_context": {"id": 1}}
    try:
        r = requests.post(f"{BASE_URL}/chat-analysis", json=payload)
        assert r.status_code == 200
        data = r.json()
        assert "response" in data
        print("OK")
    except Exception as e:
        print(f"FAIL: {e}")
        print(r.text)

def test_available_trends():
    print("Testing GET /available-trends ...", end=" ")
    try:
        r = requests.get(f"{BASE_URL}/available-trends")
        assert r.status_code == 200
        data = r.json()
        assert "trends" in data
        assert len(data["trends"]) > 0
        print("OK")
    except Exception as e:
        print(f"FAIL: {e}")
        print(r.text)

def test_full_insight():
    print("Testing POST /full-trend-insight ...", end=" ")
    payload = {"trend_id": "t1"}
    try:
        r = requests.post(f"{BASE_URL}/full-trend-insight", json=payload)
        assert r.status_code == 200
        data = r.json()
        assert "trend_id" in data
        assert "analysis" in data
        assert "prediction" in data
        assert "narrative" in data
        assert "simulation_baseline" in data
        print("OK")
    except Exception as e:
        print(f"FAIL: {e}")
        print(r.text)

def test_filtered_analysis():
    print("Testing POST /trend-analysis-filtered ...", end=" ")
    payload = {"trend_name": "Sustainable Fashion", "platform": "Instagram"}
    try:
        r = requests.post(f"{BASE_URL}/trend-analysis-filtered", json=payload)
        assert r.status_code == 200
        data = r.json()
        assert "decline_probability" in data
        print("OK")
    except Exception as e:
        print(f"FAIL: {e}")
        print(r.text)

if __name__ == "__main__":
    time.sleep(2)
    test_health()
    test_trend_analysis()
    test_early_warning()
    test_narrative()
    test_simulation()
    test_chat()
    test_available_trends()
    test_full_insight()
    test_filtered_analysis()
