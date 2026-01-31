# 보안 가이드

## 보안 점검 완료 사항

### ✅ 완료된 보안 개선

1. **API 키 보안**
   - 하드코딩된 API 키 제거 (`test_ai_analyst.py`)
   - 환경 변수 또는 secrets.toml 사용 강제
   - API 키 입력 검증 추가

2. **입력 검증**
   - 사용자 입력 검증 (`utils/security.py`)
   - 이름 입력 검증 (길이, 특수문자 제한)
   - API 키 형식 검증
   - XSS 방지 (HTML 이스케이프)

3. **에러 처리**
   - 프로덕션 환경에서 상세한 에러 메시지 숨김
   - 일반적인 에러 메시지로 대체
   - 민감한 정보 노출 방지

4. **파일 보안**
   - `.gitignore`에 민감한 파일 추가 확인
   - `.env`, `.streamlit/secrets.toml` 제외 확인

## 보안 체크리스트

### 배포 전 확인 사항

- [x] 하드코딩된 API 키 제거
- [x] 입력 검증 구현
- [x] 에러 메시지 일반화
- [x] .gitignore 확인
- [ ] 환경 변수 설정 확인 (Heroku Config Vars)
- [ ] HTTPS 강제 (Heroku 자동 적용)
- [ ] 의존성 보안 업데이트 확인

### 지속적인 보안 관리

1. **의존성 업데이트**
   ```bash
   pip list --outdated
   pip install --upgrade <package>
   ```

2. **환경 변수 관리**
   - Heroku Config Vars 사용
   - 절대 코드에 하드코딩하지 않기
   - secrets.toml은 로컬 개발용으로만 사용

3. **입력 검증**
   - 모든 사용자 입력 검증
   - SQL Injection 방지 (현재 SQL 사용 없음)
   - XSS 방지 (HTML 이스케이프)

4. **에러 처리**
   - 프로덕션에서는 상세한 에러 숨김
   - 로깅은 서버 측에서만 수행

## 보안 모범 사례

### API 키 관리

1. **환경 변수 사용 (권장)**
   ```bash
   heroku config:set OPENAI_API_KEY=your-key
   ```

2. **Streamlit Secrets (로컬 개발용)**
   - `.streamlit/secrets.toml`에 저장
   - `.gitignore`에 포함 확인

3. **절대 하드코딩하지 않기**
   - 코드에 직접 API 키 작성 금지
   - 테스트 파일에도 환경 변수 사용

### 입력 검증

- 모든 사용자 입력 검증
- 길이 제한 설정
- 특수 문자 필터링
- HTML 이스케이프

### 에러 처리

- 프로덕션에서는 일반적인 메시지만 표시
- 상세한 스택 트레이스는 로그에만 기록
- 민감한 정보(파일 경로, 내부 구조 등) 노출 방지

## 알려진 보안 고려사항

1. **Streamlit의 제한사항**
   - Streamlit은 클라이언트-서버 아키텍처
   - 서버 측에서 모든 처리가 이루어짐
   - API 키는 서버 측에서만 사용됨

2. **세션 관리**
   - Streamlit이 자동으로 세션 관리
   - session_state는 서버 측에만 저장됨

3. **HTTPS**
   - Heroku는 자동으로 HTTPS 제공
   - HTTP는 자동으로 HTTPS로 리다이렉트

## 보안 취약점 신고

보안 취약점을 발견하신 경우, 즉시 프로젝트 관리자에게 연락해주세요.
