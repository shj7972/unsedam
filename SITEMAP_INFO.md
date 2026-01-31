# 사이트맵(Sitemap) 정보

## 📍 사이트맵 주소

### 현재 설정된 사이트맵 URL

**메인 사이트맵:**
```
https://unsedam.kr/?page=sitemap
```

**또는 직접 접근:**
```
https://unsedam.kr/?page=sitemap
```

---

## 🔍 사이트맵 내용

사이트맵에는 다음 페이지들이 포함됩니다:

1. **메인 페이지** (`/`)
   - Priority: 1.0
   - Change Frequency: daily

2. **AI 사주** (`/?page=ai_saju`)
   - Priority: 0.8
   - Change Frequency: weekly

3. **토정비결** (`/?page=tojeong`)
   - Priority: 0.8
   - Change Frequency: weekly

4. **별자리운세** (`/?page=byeoljari`)
   - Priority: 0.8
   - Change Frequency: weekly

5. **궁합** (`/?page=gonghap`)
   - Priority: 0.8
   - Change Frequency: weekly

6. **꿈해몽** (`/?page=dream`)
   - Priority: 0.8
   - Change Frequency: weekly

7. **타로** (`/?page=tarot`)
   - Priority: 0.8
   - Change Frequency: weekly

8. **로또** (`/?page=lotto`)
   - Priority: 0.8
   - Change Frequency: weekly

9. **만세력** (`/?page=manse`)
   - Priority: 0.8
   - Change Frequency: weekly

---

## 🤖 Robots.txt

**Robots.txt 주소:**
```
https://unsedam.kr/?page=robots
```

**Robots.txt 내용:**
```
User-agent: *
Allow: /
Disallow: /static/

Sitemap: https://unsedam.kr/?page=sitemap
```

---

## 📊 Google Search Console 등록

### 1. Google Search Console 접속
- https://search.google.com/search-console 접속
- Google 계정으로 로그인

### 2. 속성 추가
- **속성 추가** 클릭
- **URL 접두어** 선택
- `https://unsedam.kr` 입력

### 3. 소유권 확인
- HTML 파일 업로드 또는 메타 태그 추가
- 또는 DNS 레코드 추가

### 4. 사이트맵 제출
- **색인 생성** → **Sitemaps** 메뉴
- 사이트맵 URL 입력: `https://unsedam.kr/?page=sitemap`
- **제출** 클릭

---

## 🔄 사이트맵 업데이트

사이트맵은 자동으로 생성되며, 다음 경우에 업데이트됩니다:
- 새로운 페이지 추가 시
- 페이지 구조 변경 시

**수동 업데이트:**
- `utils/seo.py`의 `generate_sitemap()` 함수 수정
- `lastmod` 날짜 업데이트 (현재: 2025-01-01)

---

## ✅ 확인 방법

### 브라우저에서 확인
1. `https://unsedam.kr/?page=sitemap` 접속
2. XML 형식의 사이트맵 확인

### 명령줄에서 확인
```bash
curl https://unsedam.kr/?page=sitemap
```

### 온라인 도구로 검증
- https://www.xml-sitemaps.com/validate-xml-sitemap.html
- 사이트맵 URL 입력하여 검증

---

## 📝 참고사항

- 사이트맵은 XML 형식으로 제공됩니다
- Google, Naver 등 검색 엔진에 제출 가능합니다
- 사이트맵 제출 후 검색 엔진이 사이트를 크롤링하는 데 도움이 됩니다
- 정기적으로 사이트맵을 업데이트하는 것이 좋습니다

---

## 🆘 문제 해결

### 사이트맵이 표시되지 않을 때
1. DNS 전파 확인: `nslookup unsedam.kr`
2. SSL 인증서 확인: `heroku certs:info`
3. Heroku 로그 확인: `heroku logs --tail`

### Google Search Console에서 오류 발생 시
1. 사이트맵 형식 검증
2. robots.txt 확인
3. 사이트 접근 가능 여부 확인

---

**사이트맵 주소: `https://unsedam.kr/?page=sitemap`** ✅

