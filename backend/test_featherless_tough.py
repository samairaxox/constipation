import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"

def test_narrative_tough():
    print("Testing POST /trend-narrative with sample payload...", end=" ")
    payload = {
        "trend_data": {
            "trend_name": "Sustainable Fashion",
            "engagement_rate": 0.27,
            "sentiment_score": -0.42,
            "influencer_ratio": 0.18
        }
    }
    
    start_time = time.time()
    try:
        r = requests.post(f"{BASE_URL}/trend-narrative", json=payload, timeout=35)
        elapsed = time.time() - start_time
        
        print(f"Status: {r.status_code}")
        print(f"Time: {elapsed:.2f}s")
        
        if r.status_code == 200:
            data = r.json()
            print("Response Data:")
            print(json.dumps(data, indent=2))
            
            if data.get("explanation"):
                print("SUCCESS: Explanation received.")
                if data.get("source") == "Featherless.ai":
                    print("SOURCE: Proper AI source.")
                elif "Fallback" in data.get("source"):
                    print("SOURCE: Fallback logic triggered (Acceptable if API key invalid).")
                else:
                    print(f"SOURCE: {data.get('source')}")
            else:
                print("FAIL: No explanation in response.")
        else:
            print(f"FAIL: HTTP {r.status_code}")
            print(r.text)
            
    except Exception as e:
        print(f"EXCEPTION: {e}")

if __name__ == "__main__":
    time.sleep(3) # Wait for server to settle
    test_narrative_tough()
