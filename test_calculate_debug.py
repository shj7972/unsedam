# -*- coding: utf-8 -*-
import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import json

url = "http://localhost:8001/api/calculate"
data = {
    'name': '테스트',
    'birth_date': '2000-01-01',
    'gender': '남성',
    'is_lunar': False
}

print("=" * 50)
print("API 테스트 시작")
print("=" * 50)

try:
    response = requests.post(url, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"\nResponse Text:")
    print(response.text)
    
    if response.status_code == 200:
        result = response.json()
        print("\n성공!")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("\n오류 발생")
        try:
            error_json = response.json()
            print(json.dumps(error_json, indent=2, ensure_ascii=False))
        except:
            print("JSON 파싱 실패")
            
except Exception as e:
    print(f"예외 발생: {e}")
    import traceback
    traceback.print_exc()

