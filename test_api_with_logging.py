# -*- coding: utf-8 -*-
import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import json

# 로깅 활성화
import logging
logging.basicConfig(level=logging.DEBUG)

url = "http://localhost:8001/api/calculate"

# 테스트 데이터
data = {
    'name': '테스트',
    'birth_date': '2000-01-01',
    'gender': '남성',
    'is_lunar': False
}

print("=" * 50)
print("API 테스트 (로깅 활성화)")
print("=" * 50)
print(f"Request data: {data}")

try:
    response = requests.post(url, data=data)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ 성공!")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("\n❌ 오류 발생")
        try:
            error_json = response.json()
            print(json.dumps(error_json, indent=2, ensure_ascii=False))
        except:
            print("JSON 파싱 실패")
            
except Exception as e:
    print(f"\n❌ 예외 발생: {e}")
    import traceback
    traceback.print_exc()

