import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    print("-" * 50)
    print("STEP 1: Health Check")
    try:
        start_time = time.time()
        r = requests.get(f"{BASE_URL}/", timeout=5)
        elapsed = time.time() - start_time
        print(f"Status: {r.status_code}")
        print(f"Time: {elapsed:.2f}s")
        if r.status_code == 200 and r.json() == {"status": "Backend running"}:
            print("SUCCESS: Backend is running.")
        else:
            print(f"FAIL: Unexpected response: {r.text}")
    except Exception as e:
        print(f"FAIL: {e}")

def test_narrative():
    print("-" * 50)
    print("STEP 2: Narrative Endpoint Test")
    payload = {
        "trend_data": {
            "trend_name": "Sustainable Fashion",
            "engagement_rate": 0.27,
            "sentiment_score": -0.42,
            "influencer_ratio": 0.18
        }
    }
    
    try:
        start_time = time.time()
        print("Sending request to /trend-narrative...")
        r = requests.post(f"{BASE_URL}/trend-narrative", json=payload, timeout=35)
        elapsed = time.time() - start_time
        
        print(f"Status: {r.status_code}")
        print(f"Time: {elapsed:.2f}s")
        
        if elapsed > 30:
            print("WARNING: Response time exceeded 30s limit.")
        
        if r.status_code == 200:
            data = r.json()
            print("Response Data:")
            print(json.dumps(data, indent=2))
            
            explanation = data.get("explanation")
            source = data.get("source")
            model = data.get("model")
            
            if explanation and len(explanation) > 20:
                print("SUCCESS: Valid explanation received.")
            else:
                print("FAIL: Explanation missing or too short.")
                
            if source in ["Featherless.ai", "Fallback Logic"]:
                print(f"SUCCESS: Valid source attribution: {source}")
            else:
                print(f"FAIL: Invalid source: {source}")
                
            if model:
                print(f"SUCCESS: Model reported: {model}")
        else:
            print(f"FAIL: HTTP {r.status_code}")
            print(r.text)

    except Exception as e:
        print(f"EXCEPTION: {e}")

if __name__ == "__main__":
    time.sleep(2) # Give server time to reload
    test_health()
    test_narrative()
