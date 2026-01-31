# 로컬 테스트 가이드

## 현재 상황

FastAPI 서버가 포트 8001에서 실행 중입니다.

## 접속 URL

- **메인 페이지**: http://localhost:8001/
- **API 문서**: http://localhost:8001/docs
- **API 엔드포인트**: http://localhost:8001/api/calculate

## 문제 해결

### 404 Not Found 오류

라우터는 정상적으로 등록되어 있습니다:
- `/api/calculate` (POST)
- `/api/ai-analysis` (POST)

하지만 404 오류가 발생하는 경우:

1. **서버 재시작**
   ```bash
   # 모든 Python 프로세스 종료
   Get-Process python | Stop-Process -Force
   
   # 서버 재시작
   python -m uvicorn main:app --reload --port 8001
   ```

2. **브라우저에서 직접 테스트**
   - http://localhost:8001/ 에 접속
   - 입력 폼에 데이터 입력 후 "결과보기" 버튼 클릭
   - 브라우저 개발자 도구(F12)에서 Network 탭 확인

3. **API 문서에서 테스트**
   - http://localhost:8001/docs 에 접속
   - `/api/calculate` 엔드포인트 찾기
   - "Try it out" 버튼 클릭하여 직접 테스트

## 확인 사항

- [ ] 서버가 포트 8001에서 실행 중인지 확인
- [ ] http://localhost:8001/health 에서 {"status":"ok"} 응답 확인
- [ ] http://localhost:8001/docs 에서 API 엔드포인트 확인
- [ ] 브라우저 콘솔에서 JavaScript 오류 확인

