# 검색엔진 등록 가이드

## 🎯 추천 검색엔진 등록 순서

### 1순위: 필수 등록
1. **Google Search Console** ✅ (이미 진행 중)
2. **Naver Webmaster Tools** ✅ (메타 태그 추가 완료)

### 2순위: 한국 시장 중요
3. **다음(Daum) 웹마스터 도구**
4. **줌(Zum) 웹마스터 도구**

### 3순위: 글로벌 검색엔진
5. **Bing Webmaster Tools** (Microsoft, Yahoo 포함)

---

## 📋 각 검색엔진 등록 방법

### 1. Google Search Console
**상태:** ✅ 준비 완료

**등록 방법:**
- URL: https://search.google.com/search-console
- 사이트맵 제출: `https://unsedam.kr/?page=sitemap`
- 소유권 확인: HTML 파일, 메타 태그, DNS 등

**메타 태그 (필요 시):**
```html
<meta name="google-site-verification" content="YOUR_VERIFICATION_CODE" />
```

---

### 2. Naver Webmaster Tools
**상태:** ✅ 메타 태그 추가 완료

**등록 방법:**
- URL: https://searchadvisor.naver.com/
- 소유권 확인: 메타 태그 방식 (이미 추가됨)
- 사이트맵 제출: `https://unsedam.kr/?page=sitemap`

**메타 태그:**
```html
<meta name="naver-site-verification" content="43dc017823a9c46420c367e23e62c5a3f0e0d99c" />
```

---

### 3. 다음(Daum) 웹마스터 도구
**상태:** ⏳ 등록 필요

**등록 방법:**
- URL: https://webmaster.daum.net/
- 카카오 계정으로 로그인
- 사이트 추가 후 소유권 확인
- 사이트맵 제출: `https://unsedam.kr/?page=sitemap`

**소유권 확인 방법:**
- 메타 태그 방식 (추천)
- HTML 파일 업로드
- DNS 레코드 추가

**메타 태그 (등록 후 발급):**
```html
<meta name="daum-site-verification" content="YOUR_VERIFICATION_CODE" />
```

---

### 4. 줌(Zum) 웹마스터 도구
**상태:** ⏳ 등록 필요

**등록 방법:**
- URL: https://webmaster.zum.com/
- 줌 계정으로 로그인
- 사이트 추가 후 소유권 확인
- 사이트맵 제출: `https://unsedam.kr/?page=sitemap`

**소유권 확인 방법:**
- 메타 태그 방식
- HTML 파일 업로드

**메타 태그 (등록 후 발급):**
```html
<meta name="zum-site-verification" content="YOUR_VERIFICATION_CODE" />
```

---

### 5. Bing Webmaster Tools
**상태:** ⏳ 등록 필요

**등록 방법:**
- URL: https://www.bing.com/webmasters/
- Microsoft 계정으로 로그인
- 사이트 추가 후 소유권 확인
- 사이트맵 제출: `https://unsedam.kr/?page=sitemap`

**소유권 확인 방법:**
- 메타 태그 방식 (추천)
- XML 파일 업로드
- DNS 레코드 추가

**메타 태그 (등록 후 발급):**
```html
<meta name="msvalidate.01" content="YOUR_VERIFICATION_CODE" />
```

**참고:** Bing은 Yahoo 검색 결과에도 포함됩니다.

---

## 🔧 메타 태그 추가 방법

각 검색엔진에서 소유권 확인 코드를 발급받은 후, `utils/seo.py` 파일의 `render_seo_meta_tags()` 함수에 메타 태그를 추가하면 됩니다.

**현재 추가된 메타 태그:**
- ✅ Naver: `naver-site-verification`

**추가 예정:**
- ⏳ Daum: `daum-site-verification` (등록 후)
- ⏳ Zum: `zum-site-verification` (등록 후)
- ⏳ Bing: `msvalidate.01` (등록 후)
- ⏳ Google: `google-site-verification` (필요 시)

---

## 📊 검색엔진별 시장 점유율 (한국)

1. **Naver**: 약 60-70% (한국 시장 1위)
2. **Google**: 약 20-30%
3. **다음(Daum)**: 약 5-10%
4. **줌(Zum)**: 약 2-5%
5. **Bing**: 약 1-2%

---

## ✅ 등록 체크리스트

### Google Search Console
- [ ] 사이트 추가
- [ ] 소유권 확인
- [ ] 사이트맵 제출: `https://unsedam.kr/?page=sitemap`
- [ ] robots.txt 확인: `https://unsedam.kr/?page=robots`

### Naver Webmaster Tools
- [x] 메타 태그 추가 완료
- [ ] 사이트 추가
- [ ] 소유권 확인 (메타 태그 방식)
- [ ] 사이트맵 제출: `https://unsedam.kr/?page=sitemap`

### 다음(Daum) 웹마스터 도구
- [ ] 사이트 추가
- [ ] 소유권 확인 코드 발급
- [ ] 메타 태그 추가
- [ ] 사이트맵 제출

### 줌(Zum) 웹마스터 도구
- [ ] 사이트 추가
- [ ] 소유권 확인 코드 발급
- [ ] 메타 태그 추가
- [ ] 사이트맵 제출

### Bing Webmaster Tools
- [ ] 사이트 추가
- [ ] 소유권 확인 코드 발급
- [ ] 메타 태그 추가
- [ ] 사이트맵 제출

---

## 🚀 빠른 시작 가이드

### 오늘 할 일
1. ✅ Naver 웹마스터 도구 등록 (메타 태그 추가 완료)
2. ⏳ Google Search Console 사이트맵 제출

### 이번 주 할 일
3. ⏳ 다음(Daum) 웹마스터 도구 등록
4. ⏳ 줌(Zum) 웹마스터 도구 등록

### 선택 사항
5. ⏳ Bing Webmaster Tools 등록 (글로벌 확장 시)

---

## 💡 팁

- 각 검색엔진에서 소유권 확인 코드를 발급받으면 알려주시면 메타 태그에 추가하겠습니다.
- 사이트맵은 모든 검색엔진에서 동일하게 `https://unsedam.kr/?page=sitemap`을 사용합니다.
- 정기적으로 각 웹마스터 도구에서 색인 상태를 확인하는 것이 좋습니다.

---

**현재 상태: Naver 메타 태그 추가 완료, 배포 대기 중** ✅

