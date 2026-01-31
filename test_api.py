"""API 테스트 스크립트"""
import requests

# API 테스트
try:
    response = requests.post(
        'http://localhost:8001/api/calculate',
        data={
            'name': 'Test',
            'birth_date': '2000-01-01',
            'gender': 'Male'
        }
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:500]}")
except Exception as e:
    print(f"Error: {e}")

