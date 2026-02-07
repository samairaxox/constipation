import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    try:
        r = requests.get(f"{BASE_URL}/")
        print(f"GET /: {r.status_code}")
        assert r.status_code == 200
        print(r.json())
        return True
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_available_brands():
    try:
        r = requests.get(f"{BASE_URL}/available-brands")
        print(f"GET /available-brands: {r.status_code}")
        assert r.status_code == 200
        data = r.json()
        print(json.dumps(data, indent=2))
        return [b["id"] for b in data["brands"]]
    except Exception as e:
        print(f"Available brands check failed: {e}")
        return []

def test_analyze_brand(brand_id):
    try:
        r = requests.post(f"{BASE_URL}/analyze-brand/{brand_id}")
        print(f"POST /analyze-brand/{brand_id}: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"Brand: {data['brand_name']}")
            print(f"Decline Probability: {data['decline_probability']}")
            print(f"Insight: {data['explainable_insights']}")
        else:
            print(r.text)
        assert r.status_code == 200
    except Exception as e:
        print(f"Analysis failed for {brand_id}: {e}")

if __name__ == "__main__":
    print("Waiting for server...")
    time.sleep(2)
    if test_health():
        brands = test_available_brands()
        for b in brands:
            test_analyze_brand(b)
