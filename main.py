"""
FastAPI 메인 애플리케이션
운세담 AI 프리미엄 사주 서비스
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_404_NOT_FOUND
import os
from datetime import datetime
from pathlib import Path

# 기본 디렉토리 설정 (절대 경로)
BASE_DIR = Path(__file__).resolve().parent

# 기존 로직 임포트 (그대로 사용)
import saju_logic
from utils.seo_fastapi import get_page_meta, generate_sitemap, generate_robots_txt, SITE_INFO
from utils.page_config import PAGE_NAMES
from utils.banner_fastapi import get_banner_html

app = FastAPI(
    title="운세담 | AI 프리미엄 사주",
    description="AI 기반 프리미엄 사주 명리 분석 서비스",
    version="2.0.0"
)

# 세션 미들웨어 (st.session_state 대체)
# 세션 쿠키 설정: same_site='lax'로 설정하여 메뉴 이동 시에도 쿠키가 전달되도록 함
SECRET_KEY = os.getenv("SECRET_KEY", "unsedam-secret-key-change-in-production")
app.add_middleware(
    SessionMiddleware, 
    secret_key=SECRET_KEY,
    max_age=86400,  # 24시간
    same_site='lax'  # 메뉴 이동 시에도 쿠키 전달
)

# 정적 파일 서빙 (절대 경로 사용)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Jinja2 템플릿 (절대 경로 사용)
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# 전역 함수 등록 (배너 로테이션)
from utils.exchange_banners import get_random_banners
templates.env.globals["get_random_banners"] = get_random_banners

# 라우터 임포트
from routers import pages, api

app.include_router(pages.router)
app.include_router(api.router, prefix="/api")

# 제거된 이전 디버그 라우트 위치


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """메인 페이지 (AI 사주)"""
    page = "ai_saju"
    meta = get_page_meta(page)
    
    # 세션에서 사용자 데이터 가져오기 (기본값 설정)
    pillars_data = request.session.get('pillars_data')
    pillars_info = request.session.get('pillars_info')
    user_name = str(request.session.get('user_name', '')) if request.session.get('user_name') else ''
    user_gender = str(request.session.get('user_gender', '')) if request.session.get('user_gender') else ''
    birth_date = str(request.session.get('birth_date', '')) if request.session.get('birth_date') else ''
    birth_time = str(request.session.get('birth_time', '')) if request.session.get('birth_time') else ''
    # is_lunar는 boolean 또는 문자열로 저장될 수 있으므로 변환
    is_lunar_session = request.session.get('is_lunar', False)
    if isinstance(is_lunar_session, str):
        is_lunar = is_lunar_session.lower() in ('true', '1', 'yes', 'on')
    elif isinstance(is_lunar_session, bool):
        is_lunar = is_lunar_session
    else:
        is_lunar = bool(is_lunar_session)
    processed = request.session.get('processed', False)
    
    # 배너 생성
    top_banner_html = get_banner_html(current_page=page, is_sidebar=False)
    sidebar_banner_html = get_banner_html(current_page=page, is_sidebar=True)
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "page": page,
            "page_names": PAGE_NAMES,
            "meta": meta,
            "site_info": SITE_INFO,
            "pillars_data": pillars_data,
            "pillars_info": pillars_info,
            "user_name": user_name,
            "user_gender": user_gender,
            "birth_date": birth_date,
            "birth_time": birth_time,
            "is_lunar": is_lunar,
            "processed": processed,
            "top_banner_html": top_banner_html,
            "sidebar_banner_html": sidebar_banner_html,
        }
    )


@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots_txt():
    """robots.txt 제공"""
    robots_content = generate_robots_txt()
    return PlainTextResponse(
        content=robots_content,
        media_type="text/plain; charset=utf-8",
        headers={"Cache-Control": "public, max-age=3600"}
    )


@app.get("/sitemap.xml", response_class=PlainTextResponse)
async def sitemap_xml():
    """sitemap.xml 제공"""
    sitemap_content = generate_sitemap()
    return PlainTextResponse(
        content=sitemap_content,
        media_type="application/xml; charset=utf-8",
        headers={"Cache-Control": "public, max-age=3600"}
    )


@app.get("/naverc30385e5fad1beddd1da6ba899dd964f.html", response_class=PlainTextResponse)
async def naver_verification():
    """네이버 소유권 확인 파일"""
    verification_content = "naver-site-verification: naverc30385e5fad1beddd1da6ba899dd964f.html"
    file_path = "static/naverc30385e5fad1beddd1da6ba899dd964f.html"
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                verification_content = f.read().strip()
        except Exception:
            pass
    return PlainTextResponse(
        content=verification_content,
        media_type="text/html; charset=utf-8"
    )


@app.get("/ads.txt", response_class=PlainTextResponse)
async def ads_txt():
    """Google AdSense ads.txt 제공"""
    ads_content = "google.com, pub-2947913248390883, DIRECT, f08c47fec0942fa0"
    file_path = "ads.txt"
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                ads_content = f.read().strip()
        except Exception:
            pass
    return PlainTextResponse(
        content=ads_content,
        media_type="text/plain; charset=utf-8"
    )


@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "ok", "service": "운세담", "version": "2.0.0"}


@app.get("/.well-known/appspecific/com.chrome.devtools.json")
async def chrome_devtools():
    """Chrome DevTools 자동 요청 처리"""
    return JSONResponse(content={"message": "Chrome DevTools endpoint"})


@app.get("/favicon.ico")
async def favicon():
    """Favicon 요청 처리 - redirect to static/images/favicon.png"""
    return RedirectResponse(url="/static/images/favicon.png", status_code=301)


# 404 에러 핸들러
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """404 및 기타 HTTP 예외 처리"""
    if exc.status_code == HTTP_404_NOT_FOUND:
        # 404 페이지 렌더링
        page = "404"
        meta = {
            "title": "404 - 페이지를 찾을 수 없습니다 | 운세담",
            "description": "요청하신 페이지를 찾을 수 없습니다.",
            "keywords": "404, 페이지 없음",
            "url": f"{SITE_INFO['url']}{request.url.path}",
            "author": SITE_INFO['author']
        }
        
        return templates.TemplateResponse(
            "404.html",
            {
                "request": request,
                "page": page,
                "page_names": PAGE_NAMES,
                "meta": meta,
                "site_info": SITE_INFO,
            },
            status_code=HTTP_404_NOT_FOUND
        )
    
    # 기타 HTTP 예외는 기본 처리
    return HTMLResponse(
        content=f"<h1>{exc.status_code} Error</h1><p>{exc.detail}</p>",
        status_code=exc.status_code
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

