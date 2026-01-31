# Streamlit → 전통적 웹 프레임워크 마이그레이션 분석

## 📊 프로젝트 현황 분석

### 현재 기술 스택
- **프레임워크**: Streamlit
- **언어**: Python 3.11
- **배포**: Heroku
- **주요 의존성**: 
  - streamlit
  - pandas, ephem, korean-lunar-calendar
  - google-generativeai, openai
  - flask, gunicorn (현재 미사용)

### 프로젝트 규모
- **총 Streamlit 호출**: 약 470개 (`st.` 사용)
- **페이지 수**: 8개 주요 페이지 + 특수 페이지 (sitemap, robots, naver verification)
- **컴포넌트**: 3개 (input_form, banner, navigation)
- **유틸리티**: 5개 모듈

### 주요 기능
1. **AI 사주 분석** - Google Generative AI 기반
2. **사주 계산** - 전통 명리학 로직 (saju_logic.py)
3. **다양한 운세 서비스**:
   - 토정비결 (tojeong)
   - 별자리 (byeoljari)
   - 궁합 (gonghap)
   - 꿈해몽 (dream)
   - 만세력 (manse)
   - 타로 (taro)
   - 로또 (lotto)
4. **SEO 최적화** - 메타 태그, 구조화된 데이터, sitemap, robots.txt
5. **사용자 입력 폼** - 이름, 생년월일, 시간, 성별 등

---

## ✅ 마이그레이션 가능성 평가

### 🟢 **매우 가능함 (High Feasibility)**

#### 1. 비즈니스 로직
- ✅ **saju_logic.py**: Streamlit과 완전히 독립적
- ✅ **ai_analyst.py**: API 호출만 포함, 프레임워크 독립적
- ✅ **계산 로직**: 순수 Python 함수들

#### 2. 데이터 처리
- ✅ **pandas**: 모든 프레임워크에서 사용 가능
- ✅ **ephem, korean-lunar-calendar**: 프레임워크 독립적

#### 3. SEO 기능
- ✅ **메타 태그, 구조화된 데이터**: HTML 템플릿으로 쉽게 구현
- ✅ **robots.txt, sitemap.xml**: 정적 파일 또는 동적 생성 모두 가능

---

### 🟡 **주의 필요 (Medium Complexity)**

#### 1. UI 컴포넌트 변환
- **현재**: Streamlit 위젯 (`st.text_input`, `st.date_input`, `st.button` 등)
- **변환 필요**: HTML 폼 + JavaScript
- **복잡도**: 중간 (약 10-15개 주요 컴포넌트)

#### 2. 상태 관리
- **현재**: `st.session_state` (자동 관리)
- **변환 필요**: 세션/쿠키 또는 서버 사이드 세션
- **복잡도**: 중간

#### 3. 레이아웃
- **현재**: `st.columns`, `st.container`
- **변환 필요**: CSS Grid/Flexbox
- **복잡도**: 낮음 (CSS로 해결)

---

### 🔴 **주의 깊게 처리 필요 (Higher Complexity)**

#### 1. 실시간 상호작용
- **현재**: Streamlit의 자동 rerun 메커니즘
- **변환 필요**: AJAX/Fetch API 또는 WebSocket
- **복잡도**: 중간-높음

#### 2. AI 분석 로딩 상태
- **현재**: `st.spinner("AI 분석 중...")`
- **변환 필요**: JavaScript 로딩 인디케이터
- **복잡도**: 낮음

---

## 🎯 추천 마이그레이션 전략

### 옵션 1: **Flask + Jinja2** (추천 ⭐)

#### 장점
- ✅ **가벼움**: 최소한의 오버헤드
- ✅ **유연성**: 완전한 HTML/CSS/JS 제어
- ✅ **SEO 친화적**: 정적 라우팅, 메타 태그 완벽 지원
- ✅ **학습 곡선**: 낮음 (Python 개발자에게 친숙)
- ✅ **배포**: Heroku에서 이미 사용 중 (gunicorn)

#### 단점
- ⚠️ **템플릿 작성 필요**: Jinja2 템플릿 작성
- ⚠️ **JavaScript 필요**: 프론트엔드 상호작용 구현

#### 예상 작업량
- **비즈니스 로직**: 0% (재사용)
- **백엔드 API**: 20% (Flask 라우트 작성)
- **프론트엔드**: 60% (HTML/CSS/JS 작성)
- **테스트 및 디버깅**: 20%

**총 예상 시간**: 2-3주 (1인 개발 기준)

---

### 옵션 2: **FastAPI + Jinja2**

#### 장점
- ✅ **성능**: 비동기 지원, 높은 처리량
- ✅ **API 중심**: RESTful API 설계 용이
- ✅ **자동 문서화**: Swagger UI 자동 생성
- ✅ **타입 힌팅**: Python 타입 힌팅 지원

#### 단점
- ⚠️ **복잡도**: Flask보다 약간 복잡
- ⚠️ **템플릿**: Jinja2 별도 설정 필요

#### 예상 작업량
- **비즈니스 로직**: 0% (재사용)
- **백엔드 API**: 25% (FastAPI 라우트 작성)
- **프론트엔드**: 60% (HTML/CSS/JS 작성)
- **테스트 및 디버깅**: 15%

**총 예상 시간**: 2-3주 (1인 개발 기준)

---

### 옵션 3: **Django**

#### 장점
- ✅ **풀스택**: ORM, 관리자 페이지, 인증 등 내장
- ✅ **SEO**: URL 라우팅, 사이트맵 자동 생성
- ✅ **확장성**: 대규모 프로젝트에 적합

#### 단점
- ⚠️ **무거움**: 현재 프로젝트에는 과할 수 있음
- ⚠️ **학습 곡선**: Django 특유의 개념 학습 필요
- ⚠️ **오버헤드**: 불필요한 기능들

#### 예상 작업량
- **비즈니스 로직**: 0% (재사용)
- **백엔드**: 30% (Django 설정 및 뷰 작성)
- **프론트엔드**: 60% (템플릿 작성)
- **테스트 및 디버깅**: 10%

**총 예상 시간**: 3-4주 (1인 개발 기준)

---

## 📋 마이그레이션 체크리스트

### Phase 1: 준비 단계
- [ ] 현재 기능 목록 정리
- [ ] Streamlit 의존성 매핑 (어떤 `st.` 호출이 어떤 기능인지)
- [ ] 테스트 케이스 작성 (현재 동작 확인용)

### Phase 2: 백엔드 구축
- [ ] Flask/FastAPI 프로젝트 구조 생성
- [ ] 라우트 정의 (각 페이지별)
- [ ] 비즈니스 로직 통합 (saju_logic.py, ai_analyst.py)
- [ ] 세션 관리 구현
- [ ] API 엔드포인트 작성 (AJAX용)

### Phase 3: 프론트엔드 구축
- [ ] HTML 템플릿 작성 (Jinja2)
- [ ] CSS 스타일 마이그레이션 (styles.css 재사용)
- [ ] JavaScript 작성 (폼 처리, AJAX 요청)
- [ ] 반응형 디자인 확인

### Phase 4: SEO 최적화
- [ ] 메타 태그 구현
- [ ] 구조화된 데이터 (JSON-LD) 구현
- [ ] robots.txt, sitemap.xml 라우팅
- [ ] 네이버/Daum 검증 파일 처리

### Phase 5: 테스트 및 배포
- [ ] 기능 테스트
- [ ] SEO 검증 (Google Search Console, Naver Webmaster)
- [ ] 성능 테스트
- [ ] Heroku 배포 설정

---

## 🔄 Streamlit → Flask 변환 예시

### Before (Streamlit)
```python
# components/input_form.py
name = st.text_input("성함", placeholder="성함을 입력해주세요", key="input_name")
birth_date = st.date_input("생년월일", min_value=datetime(1900, 1, 1), key="input_birth_date")
if st.button("결과보기"):
    result = saju_logic.calculate_pillars(birth_date, birth_time, is_lunar)
    st.session_state['pillars_data'] = result[0]
    st.rerun()
```

### After (Flask)
```python
# app.py
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        birth_date = request.form.get('birth_date')
        birth_time = request.form.get('birth_time')
        is_lunar = request.form.get('is_lunar') == 'on'
        
        result = saju_logic.calculate_pillars(birth_date, birth_time, is_lunar)
        session['pillars_data'] = result[0]
        return redirect(url_for('ai_saju'))
    
    return render_template('index.html')

# templates/index.html
<form method="POST" action="/">
    <input type="text" name="name" placeholder="성함을 입력해주세요" required>
    <input type="date" name="birth_date" min="1900-01-01" required>
    <input type="time" name="birth_time">
    <input type="checkbox" name="is_lunar"> 음력
    <button type="submit">결과보기</button>
</form>
```

---

## 💰 비용 및 리소스

### 개발 시간
- **옵션 1 (Flask)**: 2-3주
- **옵션 2 (FastAPI)**: 2-3주
- **옵션 3 (Django)**: 3-4주

### 추가 리소스
- **프론트엔드 개발자**: 선택사항 (JavaScript 지식 있으면 가능)
- **디자인**: 현재 CSS 재사용 가능
- **호스팅**: Heroku 유지 (변경 없음)

---

## 🎯 최종 권장사항

### **Flask + Jinja2 + JavaScript** (옵션 1) 추천

#### 이유:
1. ✅ **최소한의 변경**: 현재 프로젝트 구조와 가장 유사
2. ✅ **SEO 완벽 지원**: 정적 라우팅, 메타 태그 완벽 제어
3. ✅ **빠른 개발**: 학습 곡선 낮음
4. ✅ **유지보수 용이**: Python 중심, 간단한 구조
5. ✅ **배포 간편**: Heroku에서 이미 검증됨

#### 다음 단계:
1. 프로토타입 작성 (1개 페이지로 개념 검증)
2. 점진적 마이그레이션 (페이지별로 하나씩)
3. 병렬 운영 (Streamlit과 Flask 동시 운영 후 전환)

---

## ⚠️ 주의사항

1. **세션 관리**: Streamlit의 자동 세션 관리 → Flask 세션/쿠키로 수동 구현
2. **상태 유지**: `st.session_state` → 서버 사이드 세션 또는 클라이언트 사이드 저장
3. **실시간 업데이트**: Streamlit rerun → AJAX/Fetch API로 구현
4. **CSS 호환성**: 현재 `styles.css` 대부분 재사용 가능하나 일부 조정 필요

---

## 📞 추가 검토 필요 사항

1. **사용자 인증**: 현재 없음 → 필요 시 추가
2. **데이터베이스**: 현재 없음 → 필요 시 추가
3. **캐싱**: AI 분석 결과 캐싱 고려
4. **모바일 최적화**: 현재 반응형 → 유지 필요

---

**작성일**: 2025-01-XX  
**분석자**: AI Assistant  
**프로젝트**: 운세담 (fortune_guide)

