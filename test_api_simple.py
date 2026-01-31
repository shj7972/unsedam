# -*- coding: utf-8 -*-
import requests
import json
import sys

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 간단한 테스트: 시간 없이
print("=" * 50)
print("테스트 1: 시간 없이 (birth_time=None)")
print("=" * 50)

url = "http://localhost:8001/api/calculate"
data = {
    'name': '테스트',
    'birth_date': '2000-01-01',
    'gender': '남성',
    'is_lunar': False
}

try:
    response = requests.post(url, data=data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("성공!")
        print(f"Success: {result.get('success', False)}")
    else:
        print(f"오류 발생")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"예외 발생: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("테스트 2: 시간 포함")
print("=" * 50)

data2 = {
    'name': '테스트2',
    'birth_date': '2000-01-01',
    'birth_time': '14:30',
    'gender': '여성',
    'is_lunar': False
}

try:
    response = requests.post(url, data=data2)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("성공!")
        print(f"Success: {result.get('success', False)}")
    else:
        print(f"오류 발생")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"예외 발생: {e}")
    import traceback
    traceback.print_exc()
