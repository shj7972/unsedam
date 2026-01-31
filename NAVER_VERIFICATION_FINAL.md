# 네이버 웹마스터 도구 소유권 확인 최종 가이드

## 현재 상황

DNS 방식은 HTML 파일 업로드 또는 메타 태그 삽입으로 먼저 소유권 확인이 필요합니다.

## 적용된 개선 사항

### 1. 메타 태그 삽입 개선
- ✅ 메인 함수 시작 시 즉시 메타 태그 삽입
- ✅ head의 최상단에 삽입하여 네이버 봇이 빠르게 찾을 수 있도록
- ✅ DOMContentLoaded 이벤트 대비

### 2. HTML 파일 경로
- ✅ 파일 위치: `static/naverc30385e5fad1beddd1da6ba899dd964f.html`
- ✅ 접근 경로: `/?page=naverc30385e5fad1beddd1da6ba899dd964f.html`
- ⚠️ 루트 경로 직접 접근 불가 (Streamlit 제약)

## 소유권 확인 방법

### 방법 1: 메타 태그 방식 (개선됨) ⭐

**현재 상태:**
- 메타 태그가 페이지 로드 시 즉시 삽입됨
- head의 최상단에 위치하여 네이버 봇이 빠르게 찾을 수 있음

**확인 방법:**
1. `https://unsedam.kr` 접속
2. 개발자 도구(F12) → Elements 탭
3. `<head>` 섹션에서 다음 메타 태그 확인:
   ```html
   <meta name="naver-site-verification" content="43dc017823a9c46420c367e23e62c5a3f0e0d99c" />
   ```

**네이버 웹마스터 도구에서:**
1. "메타 태그 삽입" 방식 선택
2. "소유권 확인" 버튼 클릭
3. 몇 분~몇 시간 대기

### 방법 2: HTML 파일 업로드 방식 (제한적)

**접근 가능한 경로:**
- `https://unsedam.kr/?page=naverc30385e5fad1beddd1da6ba899dd964f.html`
- `https://unsedam.kr/app/static/naverc30385e5fad1beddd1da6ba899dd964f.html`

**문제:**
- 네이버는 루트 경로(`/naverc30385e5fad1beddd1da6ba899dd964f.html`)에서 파일을 찾음
- Streamlit의 제약으로 루트 경로 직접 접근 불가

**해결 시도:**
1. 네이버 웹마스터 도구에서 파일 경로를 쿼리 파라미터 형식으로 설정 시도
2. 또는 `/app/static/` 경로 사용 시도
3. 네이버 고객센터에 문의하여 쿼리 파라미터 형식 지원 여부 확인

## 권장 순서

### 1단계: 메타 태그 방식 재시도 (개선됨)
1. 배포 완료 후 `https://unsedam.kr` 접속
2. 개발자 도구에서 메타 태그 확인
3. 네이버 웹마스터 도구에서 "메타 태그 삽입" 방식 선택
4. "소유권 확인" 버튼 클릭
5. 몇 분~몇 시간 대기

### 2단계: HTML 파일 업로드 방식 (메타 태그 실패 시)
1. 네이버 웹마스터 도구에서 "HTML 파일 업로드" 방식 선택
2. 파일 경로를 다음 중 하나로 설정:
   - `/?page=naverc30385e5fad1beddd1da6ba899dd964f.html`
   - `/app/static/naverc30385e5fad1beddd1da6ba899dd964f.html`
3. 네이버 고객센터에 문의하여 지원 여부 확인

### 3단계: DNS 레코드 방식 (위 방법들 성공 후)
1. HTML 파일 업로드 또는 메타 태그로 소유권 확인 완료
2. 네이버 웹마스터 도구에서 "DNS 레코드 추가" 방식 선택
3. 제공된 TXT 레코드를 가비아 DNS 설정에 추가
4. DNS 전파 대기
5. 네이버에서 자동 확인

## 확인 체크리스트

### 메타 태그 확인
- [ ] `https://unsedam.kr` 접속
- [ ] 개발자 도구(F12) → Elements 탭
- [ ] `<head>` 섹션에서 메타 태그 확인
- [ ] 네이버 웹마스터 도구에서 "소유권 확인" 클릭

### HTML 파일 확인
- [ ] `https://unsedam.kr/?page=naverc30385e5fad1beddd1da6ba899dd964f.html` 접속
- [ ] 파일 내용 확인: `naver-site-verification: naverc30385e5fad1beddd1da6ba899dd964f.html`
- [ ] 네이버 웹마스터 도구에서 파일 경로 설정 시도

## 문제 해결

### 메타 태그를 찾을 수 없을 때
1. 브라우저 캐시 삭제 후 재시도
2. 시크릿 모드에서 접속 확인
3. 배포 후 몇 분 대기 (전파 시간)

### HTML 파일을 찾을 수 없을 때
1. 쿼리 파라미터 경로 사용: `/?page=naverc30385e5fad1beddd1da6ba899dd964f.html`
2. 정적 파일 서빙 경로 사용: `/app/static/naverc30385e5fad1beddd1da6ba899dd964f.html`
3. 네이버 고객센터에 문의

---

**현재 상태: 메타 태그 삽입 개선 완료, 배포 대기 중** ✅

