# 네이버 HTML 파일 경로 문제 해결

## 문제
`https://unsedam.kr/naverc30385e5fad1beddd1da6ba899dd964f.html` 경로에서 "Page Not Found" 오류 발생

## 원인
Streamlit은 URL 경로를 직접 처리하지 않습니다. Streamlit은 쿼리 파라미터(`?page=...`)만 처리합니다.

## 해결 방법

### 방법 1: 쿼리 파라미터로 접근 (현재 설정)
```
https://unsedam.kr/?page=naverc30385e5fad1beddd1da6ba899dd964f.html
```

이 경로는 현재 설정으로 접근 가능합니다.

### 방법 2: 네이버 웹마스터 도구에서 경로 설정
네이버 웹마스터 도구에서 파일 경로를 쿼리 파라미터 형식으로 설정:
- 파일 경로: `/?page=naverc30385e5fad1beddd1da6ba899dd964f.html`

### 방법 3: Streamlit 정적 파일 서빙 (제한적)
Streamlit의 정적 파일 서빙은 `/app/static/` 경로를 통해 제공되므로:
- 접근 경로: `https://unsedam.kr/app/static/naverc30385e5fad1beddd1da6ba899dd964f.html`

하지만 네이버는 루트 경로에서 파일을 찾으므로 이 방법도 완벽하지 않습니다.

## 현재 설정 상태

✅ 쿼리 파라미터로 접근 가능:
- `https://unsedam.kr/?page=naverc30385e5fad1beddd1da6ba899dd964f.html`
- `.html` 확장자 포함 처리 완료

## 권장 사항

네이버 웹마스터 도구에서:
1. "HTML 파일 업로드" 방식 선택
2. 파일 경로를 `/?page=naverc30385e5fad1beddd1da6ba899dd964f.html`로 설정
3. 또는 네이버 고객센터에 문의하여 쿼리 파라미터 형식 경로 사용 가능 여부 확인

## 확인 방법

배포 후 다음 경로에서 확인:
```
https://unsedam.kr/?page=naverc30385e5fad1beddd1da6ba899dd964f.html
```

이 경로에서 다음 내용이 표시되어야 합니다:
```
naver-site-verification: naverc30385e5fad1beddd1da6ba899dd964f.html
```

