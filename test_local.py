"""
로컬 Flask 래퍼 테스트 스크립트
"""
import requests
import sys
import time

BASE_URL = "http://localhost:8000"

def test_robots_txt():
    """robots.txt 테스트"""
    try:
        response = requests.get(f"{BASE_URL}/robots.txt", timeout=5)
        print(f"✅ robots.txt: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('Content-Type')}")
        print(f"   Content Length: {len(response.text)} bytes")
        print(f"   First 100 chars: {response.text[:100]}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ robots.txt: {e}")
        return False

def test_sitemap():
    """sitemap.xml 테스트"""
    try:
        response = requests.get(f"{BASE_URL}/sitemap.xml", timeout=5)
        print(f"✅ sitemap.xml: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('Content-Type')}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ sitemap.xml: {e}")
        return False

def test_index():
    """메인 페이지 테스트"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        print(f"✅ Main Page: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Main Page: {e}")
        return False

if __name__ == "__main__":
    print("🧪 로컬 테스트 시작...\n")
    
    # 잠시 대기 (서버 시작 시간)
    print("⏳ 서버 시작 대기 중... (2초)")
    time.sleep(2)
    
    results = []
    print("=" * 50)
    results.append(test_robots_txt())
    print()
    results.append(test_sitemap())
    print()
    results.append(test_index())
    print("=" * 50)
    
    if all(results):
        print("\n✅ 모든 테스트 통과!")
        sys.exit(0)
    else:
        print("\n❌ 일부 테스트 실패")
        sys.exit(1)

