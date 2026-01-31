# 로컬 테스트 가이드

## Flask 래퍼를 사용한 robots.txt 로컬 테스트

### 방법 1: Flask 앱 직접 실행 (권장)

1. **터미널에서 Flask 앱 실행:**
   ```bash
   python flask_app.py
   ```

2. **브라우저에서 확인:**
   - Flask 서버: `http://localhost:5000`
   - robots.txt: `http://localhost:5000/robots.txt`
   - Streamlit 앱: `http://localhost:5000/` (자동으로 Streamlit으로 프록시)

3. **curl로 테스트:**
   ```bash
   curl http://localhost:5000/robots.txt
   ```

### 방법 2: 환경 변수 설정 후 실행

1. **PORT 환경 변수 설정 (선택사항):**
   ```bash
   # Windows (PowerShell)
   $env:PORT=5000
   python flask_app.py
   
   # Windows (CMD)
   set PORT=5000
   python flask_app.py
   
   # Linux/Mac
   export PORT=5000
   python flask_app.py
   ```

2. **STREAMLIT_INTERNAL_PORT 설정 (선택사항):**
   ```bash
   # Windows (PowerShell)
   $env:STREAMLIT_INTERNAL_PORT=8501
   python flask_app.py
   
   # Linux/Mac
   export STREAMLIT_INTERNAL_PORT=8501
   python flask_app.py
   ```

### 방법 3: Flask 개발 서버로 실행

Flask 앱을 수정하여 개발 모드로 실행:

```python
if __name__ == '__main__':
    # Streamlit 시작 (백그라운드)
    threading.Thread(target=start_streamlit, daemon=True).start()
    
    # Flask 서버 시작 (개발 모드)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)  # debug=True 추가
```

### 테스트 체크리스트

1. **robots.txt 확인:**
   - ✅ `http://localhost:5000/robots.txt` 접속
   - ✅ Content-Type이 `text/plain`인지 확인
   - ✅ 내용이 올바른지 확인

2. **sitemap.xml 확인:**
   - ✅ `http://localhost:5000/sitemap.xml` 접속
   - ✅ Content-Type이 `application/xml`인지 확인

3. **Streamlit 앱 확인:**
   - ✅ `http://localhost:5000/` 접속
   - ✅ Streamlit 앱이 정상적으로 로드되는지 확인
   - ✅ 메뉴 네비게이션이 작동하는지 확인

4. **프록시 확인:**
   - ✅ `http://localhost:5000/?page=robots` 접속
   - ✅ Streamlit 페이지가 정상적으로 표시되는지 확인

### 문제 해결

#### Streamlit이 시작되지 않는 경우

1. **포트 충돌 확인:**
   ```bash
   # Windows
   netstat -ano | findstr :8501
   
   # Linux/Mac
   lsof -i :8501
   ```

2. **Streamlit 로그 확인:**
   - Flask 앱 실행 시 콘솔에 Streamlit 시작 메시지 확인
   - "Streamlit server started successfully" 메시지 확인

3. **수동으로 Streamlit 실행 테스트:**
   ```bash
   streamlit run app.py --server.port=8501 --server.address=127.0.0.1
   ```

#### robots.txt가 표시되지 않는 경우

1. **Flask 라우트 확인:**
   - `@app.route('/robots.txt')` 데코레이터 확인
   - 함수가 올바르게 정의되어 있는지 확인

2. **정적 파일 경로 확인:**
   - `static/robots.txt` 파일이 존재하는지 확인
   - 파일 경로가 올바른지 확인

3. **에러 로그 확인:**
   - Flask 콘솔에서 에러 메시지 확인
   - Python 예외가 발생했는지 확인

### 빠른 테스트 스크립트

`test_local.py` 파일 생성:

```python
import requests
import sys

BASE_URL = "http://localhost:5000"

def test_robots_txt():
    """robots.txt 테스트"""
    try:
        response = requests.get(f"{BASE_URL}/robots.txt")
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
        response = requests.get(f"{BASE_URL}/sitemap.xml")
        print(f"✅ sitemap.xml: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('Content-Type')}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ sitemap.xml: {e}")
        return False

def test_streamlit():
    """Streamlit 앱 테스트"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Streamlit app: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Streamlit app: {e}")
        return False

if __name__ == "__main__":
    print("🧪 로컬 테스트 시작...\n")
    
    # 잠시 대기 (Streamlit 시작 시간)
    import time
    print("⏳ Streamlit 시작 대기 중... (5초)")
    time.sleep(5)
    
    results = []
    results.append(test_robots_txt())
    print()
    results.append(test_sitemap())
    print()
    results.append(test_streamlit())
    print()
    
    if all(results):
        print("✅ 모든 테스트 통과!")
        sys.exit(0)
    else:
        print("❌ 일부 테스트 실패")
        sys.exit(1)
```

실행:
```bash
python test_local.py
```

