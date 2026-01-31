# FastAPI + Jinja2 마이그레이션 가이드

## ✅ FastAPI + Jinja2 마이그레이션 가능성: **100% 가능**

FastAPI는 Jinja2 템플릿을 완벽하게 지원하며, SEO 최적화에 매우 적합합니다.

---

## 🎯 FastAPI + Jinja2의 장점

### 1. SEO 완벽 지원
- ✅ 정적 라우팅 (`/robots.txt`, `/sitemap.xml`)
- ✅ 메타 태그 완전 제어
- ✅ 구조화된 데이터 (JSON-LD) 직접 삽입
- ✅ 깔끔한 URL 구조

### 2. 성능
- ✅ 비동기 지원 (async/await)
- ✅ 높은 처리량
- ✅ 낮은 지연시간

### 3. 개발 경험
- ✅ 자동 API 문서화 (Swagger UI)
- ✅ 타입 힌팅 지원
- ✅ Pythonic 코드

### 4. 배포
- ✅ Heroku 호환 (gunicorn + uvicorn)
- ✅ 기존 requirements.txt 재사용 가능

---

## 📁 프로젝트 구조 (FastAPI 버전)

```
fortune_guide/
├── main.py                 # FastAPI 앱 진입점
├── requirements.txt         # 의존성 (fastapi, jinja2, uvicorn 추가)
├── Procfile                # Heroku 배포 설정
├── templates/              # Jinja2 템플릿
│   ├── base.html           # 기본 레이아웃
│   ├── index.html          # 메인 페이지 (AI 사주)
│   ├── tojeong.html        # 토정비결
│   ├── byeoljari.html      # 별자리
│   ├── gonghap.html        # 궁합
│   ├── dream.html          # 꿈해몽
│   ├── manse.html          # 만세력
│   ├── taro.html           # 타로
│   └── lotto.html          # 로또
├── static/                 # 정적 파일
│   ├── css/
│   │   └── styles.css      # 기존 CSS 재사용
│   ├── js/
│   │   └── app.js          # JavaScript
│   ├── images/
│   ├── robots.txt
│   └── sitemap.xml
├── routers/                # 라우터 모듈
│   ├── __init__.py
│   ├── pages.py            # 페이지 라우트
│   └── api.py              # API 엔드포인트
├── services/               # 비즈니스 로직 (기존 코드 재사용)
│   ├── saju_logic.py       # 기존 파일 그대로 사용
│   └── ai_analyst.py       # 기존 파일 그대로 사용
├── utils/                  # 유틸리티 (일부 수정)
│   ├── page_config.py      # 페이지 설정 (Streamlit 제거)
│   ├── seo.py              # SEO 메타 태그 (수정)
│   └── security.py         # 보안 (기존 유지)
└── components/             # 컴포넌트 로직 (템플릿으로 변환)
    └── (템플릿으로 이동)
```

---

## 🔧 핵심 구현 예시

### 1. main.py (FastAPI 앱 진입점)

```python
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import os
from datetime import datetime

# 기존 로직 임포트 (그대로 사용)
import saju_logic
from utils.seo import get_page_meta, generate_sitemap, generate_robots_txt
from utils.page_config import PAGE_NAMES

app = FastAPI(title="운세담 | AI 프리미엄 사주")

# 세션 미들웨어 (st.session_state 대체)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "your-secret-key"))

# 정적 파일 서빙
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 템플릿
templates = Jinja2Templates(directory="templates")

# 기존 pages 라우터 임포트
from routers import pages, api

app.include_router(pages.router)
app.include_router(api.router, prefix="/api")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """메인 페이지 (AI 사주)"""
    page = "ai_saju"
    meta = get_page_meta(page)
    
    # 세션에서 사용자 데이터 가져오기
    pillars_data = request.session.get('pillars_data')
    pillars_info = request.session.get('pillars_info')
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "page": page,
            "page_names": PAGE_NAMES,
            "meta": meta,
            "pillars_data": pillars_data,
            "pillars_info": pillars_info,
            "user_name": request.session.get('user_name'),
            "user_gender": request.session.get('user_gender'),
        }
    )


@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots_txt():
    """robots.txt 제공"""
    robots_content = generate_robots_txt()
    return robots_content


@app.get("/sitemap.xml", response_class=PlainTextResponse)
async def sitemap_xml():
    """sitemap.xml 제공"""
    sitemap_content = generate_sitemap()
    return PlainTextResponse(
        content=sitemap_content,
        media_type="application/xml"
    )


@app.get("/naverc30385e5fad1beddd1da6ba899dd964f.html", response_class=PlainTextResponse)
async def naver_verification():
    """네이버 소유권 확인 파일"""
    verification_content = "naver-site-verification: naverc30385e5fad1beddd1da6ba899dd964f.html"
    file_path = "static/naverc30385e5fad1beddd1da6ba899dd964f.html"
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            verification_content = f.read().strip()
    return verification_content


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

### 2. routers/pages.py (페이지 라우터)

```python
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import saju_logic
from utils.page_config import PAGE_NAMES
from utils.seo import get_page_meta

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/tojeong", response_class=HTMLResponse)
async def tojeong_page(request: Request):
    """토정비결 페이지"""
    page = "tojeong"
    meta = get_page_meta(page)
    
    return templates.TemplateResponse(
        "tojeong.html",
        {
            "request": request,
            "page": page,
            "page_names": PAGE_NAMES,
            "meta": meta,
            "pillars_data": request.session.get('pillars_data'),
            "pillars_info": request.session.get('pillars_info'),
        }
    )


@router.get("/byeoljari", response_class=HTMLResponse)
async def byeoljari_page(request: Request):
    """별자리 페이지"""
    page = "byeoljari"
    meta = get_page_meta(page)
    
    return templates.TemplateResponse(
        "byeoljari.html",
        {
            "request": request,
            "page": page,
            "page_names": PAGE_NAMES,
            "meta": meta,
        }
    )


# 다른 페이지들도 동일한 패턴으로...
```

---

### 3. routers/api.py (API 엔드포인트)

```python
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import saju_logic
import ai_analyst
from utils.api_key import get_api_key

router = APIRouter(prefix="/api")


@router.post("/calculate")
async def calculate_pillars(
    request: Request,
    name: str = Form(...),
    birth_date: str = Form(...),
    birth_time: str = Form(None),
    gender: str = Form(...),
    is_lunar: bool = Form(False)
):
    """사주 계산 API"""
    try:
        # 날짜 파싱
        birth_dt = datetime.strptime(birth_date, "%Y-%m-%d")
        birth_tm = datetime.strptime(birth_time, "%H:%M").time() if birth_time else None
        
        # 사주 계산 (기존 로직 그대로 사용)
        result = saju_logic.calculate_pillars(birth_dt, birth_tm, is_lunar)
        
        # 세션에 저장 (st.session_state 대체)
        request.session['pillars_data'] = result[0]
        request.session['pillars_info'] = result[1]
        request.session['user_name'] = name
        request.session['user_gender'] = gender
        request.session['processed'] = True
        
        return JSONResponse({
            "success": True,
            "data": {
                "pillars_data": result[0],
                "pillars_info": result[1]
            }
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/ai-analysis")
async def ai_analysis(request: Request):
    """AI 사주 분석 API"""
    if 'pillars_data' not in request.session:
        raise HTTPException(status_code=400, detail="사주 데이터가 없습니다.")
    
    API_KEY = get_api_key()
    if not API_KEY:
        raise HTTPException(status_code=400, detail="API 키가 설정되지 않았습니다.")
    
    # AI 분석 (기존 로직 그대로 사용)
    ai_input_data = request.session.get('ai_input_data')
    result = ai_analyst.generate_saju_analysis(API_KEY, ai_input_data)
    
    request.session['ai_analysis_result'] = result
    
    return JSONResponse({
        "success": True,
        "data": result
    })
```

---

### 4. templates/base.html (기본 레이아웃)

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- SEO 메타 태그 -->
    <title>{{ meta.title }}</title>
    <meta name="description" content="{{ meta.description }}">
    <meta name="keywords" content="{{ meta.keywords }}">
    <meta name="author" content="{{ meta.author }}">
    <meta name="robots" content="index, follow">
    
    <!-- 네이버 웹마스터 도구 -->
    <meta name="naver-site-verification" content="43dc017823a9c46420c367e23e62c5a3f0e0d99c" />
    
    <!-- 다음 웹마스터 도구 -->
    <meta name="daum-site-verification" content="42858a913fc55df5e2dc9371b659ac47ba48ec6bb332cb43322f947d6e1ac763:1hrba1lpzexyTL25MI8THg==" />
    
    <!-- Open Graph -->
    <meta property="og:title" content="{{ meta.title }}">
    <meta property="og:description" content="{{ meta.description }}">
    <meta property="og:url" content="{{ meta.url }}">
    <meta property="og:type" content="website">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{{ meta.title }}">
    <meta name="twitter:description" content="{{ meta.description }}">
    
    <!-- Canonical URL -->
    <link rel="canonical" href="{{ meta.url }}">
    
    <!-- CSS -->
    <link rel="stylesheet" href="/static/css/styles.css">
    
    <!-- 구조화된 데이터 (JSON-LD) -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "운세담",
        "url": "https://unsedam.kr",
        "description": "AI 프리미엄 사주 명리 분석 서비스"
    }
    </script>
</head>
<body>
    <!-- 네비게이션 -->
    <div class="header-wrapper">
        <div class="logo-circle">
            <svg width="60" height="60" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 40 L50 20 L80 40 M30 40 L30 55 M70 40 L70 55 M40 40 L40 55 M60 40 L60 55" stroke="#D4AF37" stroke-width="4" stroke-linecap="round"/>
                <path d="M50 45 C30 55, 70 65, 50 85" stroke="#D4AF37" stroke-width="6" stroke-linecap="round" fill="none"/>
                <circle cx="65" cy="45" r="3" fill="#D4AF37"/>
            </svg>
            <div class="logo-text">운세담</div>
        </div>
        <div class="nav-menu">
            {% for page_key, page_name in page_names.items() %}
                <a href="/{{ page_key if page_key != 'ai_saju' else '' }}" 
                   class="nav-item {% if page == page_key %}active{% endif %}">
                    {{ page_name }}
                </a>
            {% endfor %}
        </div>
    </div>
    
    <!-- 메인 컨텐츠 -->
    <div class="main-container">
        {% block content %}{% endblock %}
    </div>
    
    <!-- 푸터 -->
    <div class="footer">
        © 2025 운세담 | AI 프리미엄 사주 명리 분석 서비스
    </div>
    
    <!-- JavaScript -->
    <script src="/static/js/app.js"></script>
</body>
</html>
```

---

### 5. templates/index.html (AI 사주 페이지)

```html
{% extends "base.html" %}

{% block content %}
<div class="container">
    <div class="row">
        <!-- 좌측: 입력 폼 -->
        <div class="col-md-4">
            <div class="glass-card">
                <div class="section-header">
                    <span>📋</span> 정보 입력
                </div>
                
                <form id="input-form" method="POST" action="/api/calculate">
                    <input type="text" name="name" placeholder="성함을 입력해주세요" required>
                    <input type="date" name="birth_date" min="1900-01-01" required>
                    <input type="time" name="birth_time">
                    <select name="gender" required>
                        <option value="">선택해주세요</option>
                        <option value="남성">남성</option>
                        <option value="여성">여성</option>
                        <option value="기타">기타</option>
                    </select>
                    <label>
                        <input type="checkbox" name="is_lunar"> 음력 (Lunar Calendar)
                    </label>
                    <button type="submit">결과보기</button>
                </form>
            </div>
        </div>
        
        <!-- 우측: 결과 표시 -->
        <div class="col-md-8">
            {% if pillars_data %}
                <div class="glass-card">
                    <div class="section-header">
                        <span>🔮</span> AI 사주 분석
                    </div>
                    
                    <!-- 사주 결과 표시 -->
                    <div id="saju-result">
                        <!-- 기존 pages/ai_saju.py의 렌더링 로직을 여기에 구현 -->
                    </div>
                    
                    <!-- AI 분석 버튼 -->
                    <button id="ai-analysis-btn" onclick="runAIAnalysis()">
                        AI 분석 시작
                    </button>
                    
                    <!-- AI 분석 결과 -->
                    <div id="ai-result" style="display: none;">
                        <div class="spinner">AI 분석 중...</div>
                    </div>
                </div>
            {% else %}
                <div class="empty-state">
                    <h2>당신의 운명 차트를 펼쳐보세요</h2>
                    <p>성함과 생년월일을 입력하시면 프리미엄 AI 사주 분석이 시작됩니다.</p>
                </div>
            {% endif %}
        </div>
    </div>
</div>

<script>
// AJAX 폼 제출
document.getElementById('input-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    const response = await fetch('/api/calculate', {
        method: 'POST',
        body: formData
    });
    
    if (response.ok) {
        window.location.reload();
    } else {
        alert('오류가 발생했습니다.');
    }
});

// AI 분석 실행
async function runAIAnalysis() {
    const resultDiv = document.getElementById('ai-result');
    resultDiv.style.display = 'block';
    resultDiv.innerHTML = '<div class="spinner">AI 분석 중...</div>';
    
    const response = await fetch('/api/ai-analysis', {
        method: 'POST'
    });
    
    if (response.ok) {
        const data = await response.json();
        resultDiv.innerHTML = formatAIResult(data.data);
    } else {
        resultDiv.innerHTML = '<div class="error">AI 분석 중 오류가 발생했습니다.</div>';
    }
}
</script>
{% endblock %}
```

---

### 6. static/js/app.js (JavaScript)

```javascript
// 전역 유틸리티 함수들

// AJAX 요청 헬퍼
async function apiRequest(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    const response = await fetch(url, options);
    return await response.json();
}

// AI 분석 결과 포맷팅
function formatAIResult(data) {
    // 기존 pages/ai_saju.py의 렌더링 로직을 JavaScript로 변환
    return `
        <div class="ai-analysis-result">
            <h3>${data.title || 'AI 사주 분석'}</h3>
            <div class="content">${data.content || ''}</div>
        </div>
    `;
}

// 로딩 인디케이터
function showSpinner(elementId) {
    document.getElementById(elementId).innerHTML = '<div class="spinner">처리 중...</div>';
}

// 에러 메시지 표시
function showError(elementId, message) {
    document.getElementById(elementId).innerHTML = `<div class="error">${message}</div>`;
}
```

---

## 📦 requirements.txt (업데이트)

```txt
# 웹 프레임워크
fastapi
uvicorn[standard]
jinja2
python-multipart  # Form 데이터 처리용

# 기존 의존성 (그대로 유지)
pandas
ephem
korean-lunar-calendar
google-generativeai
openai
requests

# 배포용
gunicorn
```

---

## 🚀 Procfile (업데이트)

```txt
web: gunicorn main:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120
```

---

## 🔄 마이그레이션 단계별 가이드

### Phase 1: 기본 구조 설정 (1-2일)
1. FastAPI 프로젝트 구조 생성
2. `main.py` 작성
3. 기본 템플릿 (`base.html`) 작성
4. 정적 파일 서빙 설정

### Phase 2: 메인 페이지 구현 (2-3일)
1. `templates/index.html` 작성
2. 입력 폼 구현 (HTML + JavaScript)
3. API 엔드포인트 작성 (`/api/calculate`)
4. 세션 관리 구현

### Phase 3: AI 분석 기능 (2-3일)
1. AI 분석 API 구현 (`/api/ai-analysis`)
2. JavaScript로 비동기 처리
3. 결과 렌더링

### Phase 4: 나머지 페이지들 (3-5일)
1. 각 페이지 템플릿 작성
2. 라우터 구현
3. 기능 테스트

### Phase 5: SEO 최적화 (1-2일)
1. 메타 태그 구현
2. 구조화된 데이터
3. robots.txt, sitemap.xml 라우팅

### Phase 6: 테스트 및 배포 (2-3일)
1. 기능 테스트
2. SEO 검증
3. Heroku 배포

**총 예상 시간**: 2-3주 (1인 개발 기준)

---

## ✅ FastAPI + Jinja2의 SEO 장점

### 1. 정적 라우팅
```python
@app.get("/robots.txt")
@app.get("/sitemap.xml")
@app.get("/naverc30385e5fad1beddd1da6ba899dd964f.html")
```
→ 검색엔진이 직접 접근 가능

### 2. 메타 태그 완전 제어
```html
<!-- templates/base.html에서 직접 제어 -->
<meta name="naver-site-verification" content="..." />
<meta name="daum-site-verification" content="..." />
```
→ Streamlit의 제약 없음

### 3. 구조화된 데이터
```html
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "WebSite",
    ...
}
</script>
```
→ 템플릿에서 직접 삽입

### 4. 깔끔한 URL
```
https://unsedam.kr/tojeong
https://unsedam.kr/byeoljari
```
→ SEO 친화적

---

## 🎯 결론

**FastAPI + Jinja2는 완벽하게 가능하며, SEO 최적화에 매우 적합합니다!**

### 주요 장점:
1. ✅ SEO 완벽 지원 (정적 라우팅, 메타 태그 제어)
2. ✅ 비즈니스 로직 100% 재사용 가능
3. ✅ 비동기 지원으로 높은 성능
4. ✅ 자동 API 문서화
5. ✅ Heroku 배포 간편

### 다음 단계:
1. 프로토타입 작성 (메인 페이지 1개)
2. 점진적 마이그레이션
3. 테스트 및 배포

**마이그레이션을 시작하시겠습니까?**

