import requests
import json

url = "http://localhost:8001/api/calculate"

# FormData로 전송
data = {
    'name': '테스트',
    'birth_date': '2000-01-01',
    'gender': '남성',
    'is_lunar': False
}

try:
    print("API 요청 전송 중...")
    response = requests.post(url, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {response.headers}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Success: {json.dumps(result, indent=2, ensure_ascii=False)}")
    else:
        print(f"Error Response: {response.text}")
        try:
            error_json = response.json()
            print(f"Error JSON: {json.dumps(error_json, indent=2, ensure_ascii=False)}")
        except:
            pass
except requests.exceptions.ConnectionError as e:
    print(f"Connection Error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Request Error: {e}")
except Exception as e:
    print(f"Unexpected Error: {e}")
    import traceback
    traceback.print_exc()

