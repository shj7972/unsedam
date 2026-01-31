"""
페이지 라우터
각 페이지의 라우트를 정의합니다.
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from utils.page_config import PAGE_NAMES
from utils.seo_fastapi import get_page_meta, SITE_INFO
from utils.banner_fastapi import get_banner_html

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# 전역 함수 등록 (배너 로테이션)
from utils.exchange_banners import get_random_banners
templates.env.globals["get_random_banners"] = get_random_banners


@router.get("/tojeong", response_class=HTMLResponse)
async def tojeong_page(request: Request):
    """토정비결 페이지"""
    from datetime import datetime
    
    page = "tojeong"
    meta = get_page_meta(page)
    
    pillars_data = request.session.get('pillars_data')
    pillars_info = request.session.get('pillars_info')
    user_name = request.session.get('user_name', '')
    user_gender = request.session.get('user_gender', '')
    birth_date = request.session.get('birth_date', '')
    birth_time = request.session.get('birth_time', '')
    # is_lunar는 boolean 또는 문자열로 저장될 수 있으므로 변환
    is_lunar_session = request.session.get('is_lunar', False)
    if isinstance(is_lunar_session, str):
        is_lunar = is_lunar_session.lower() in ('true', '1', 'yes', 'on')
    else:
        is_lunar = bool(is_lunar_session)
    processed = request.session.get('processed', False)
    current_year = datetime.now().year
    
    # 배너 생성
    sidebar_banner_html = get_banner_html(current_page=page, is_sidebar=True)
    
    return templates.TemplateResponse(
        "tojeong.html",
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
            "current_year": current_year,
            "sidebar_banner_html": sidebar_banner_html,
        }
    )


@router.get("/byeoljari", response_class=HTMLResponse)
async def byeoljari_page(request: Request):
    """별자리운세 페이지"""
    from datetime import datetime
    
    page = "byeoljari"
    meta = get_page_meta(page)
    
    # 세션에서 사용자 데이터 가져오기
    pillars_data = request.session.get('pillars_data')
    pillars_info = request.session.get('pillars_info')
    user_name = request.session.get('user_name', '')
    user_gender = request.session.get('user_gender', '')
    birth_date = request.session.get('birth_date', '')
    birth_time = request.session.get('birth_time', '')
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
    sidebar_banner_html = get_banner_html(current_page=page, is_sidebar=True)
    
    return templates.TemplateResponse(
        "byeoljari.html",
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
            "sidebar_banner_html": sidebar_banner_html,
        }
    )


@router.get("/gonghap", response_class=HTMLResponse)
async def gonghap_page(request: Request):
    """궁합 페이지"""
    page = "gonghap"
    meta = get_page_meta(page)
    
    # 세션에서 사용자 데이터 가져오기 (첫 번째 사람 기본값)
    pillars_data = request.session.get('pillars_data')
    pillars_info = request.session.get('pillars_info')
    user_name = request.session.get('user_name', '')
    user_gender = request.session.get('user_gender', '')
    birth_date = request.session.get('birth_date', '')
    birth_time = request.session.get('birth_time', '')
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
    sidebar_banner_html = get_banner_html(current_page=page, is_sidebar=True)
    
    return templates.TemplateResponse(
        "gonghap.html",
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
            "sidebar_banner_html": sidebar_banner_html,
        }
    )


@router.get("/dream", response_class=HTMLResponse)
async def dream_page(request: Request):
    """꿈해몽 페이지"""
    from datetime import datetime
    
    page = "dream"
    meta = get_page_meta(page)
    
    # 세션에서 사용자 데이터 가져오기
    pillars_data = request.session.get('pillars_data')
    pillars_info = request.session.get('pillars_info')
    user_name = request.session.get('user_name', '')
    user_gender = request.session.get('user_gender', '')
    birth_date = request.session.get('birth_date', '')
    birth_time = request.session.get('birth_time', '')
    # is_lunar는 boolean 또는 문자열로 저장될 수 있으므로 변환
    is_lunar_session = request.session.get('is_lunar', False)
    if isinstance(is_lunar_session, str):
        is_lunar = is_lunar_session.lower() in ('true', '1', 'yes', 'on')
    elif isinstance(is_lunar_session, bool):
        is_lunar = is_lunar_session
    else:
        is_lunar = bool(is_lunar_session)
    processed = request.session.get('processed', False)
    
    # 쿼리 파라미터에서 키워드 확인
    keyword = request.query_params.get('keyword', '')
    
    # 배너 생성
    sidebar_banner_html = get_banner_html(current_page=page, is_sidebar=True)
    
    return templates.TemplateResponse(
        "dream.html",
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
            "keyword": keyword,
            "sidebar_banner_html": sidebar_banner_html,
        }
    )


@router.get("/manse", response_class=HTMLResponse)
async def manse_page(request: Request):
    """만세력 페이지"""
    from datetime import datetime
    
    page = "manse"
    meta = get_page_meta(page)
    
    # 세션에서 사용자 데이터 가져오기
    pillars_data = request.session.get('pillars_data')
    pillars_info = request.session.get('pillars_info')
    user_name = request.session.get('user_name', '')
    user_gender = request.session.get('user_gender', '')
    birth_date = request.session.get('birth_date', '')
    birth_time = request.session.get('birth_time', '')
    # is_lunar는 boolean 또는 문자열로 저장될 수 있으므로 변환
    is_lunar_session = request.session.get('is_lunar', False)
    if isinstance(is_lunar_session, str):
        is_lunar = is_lunar_session.lower() in ('true', '1', 'yes', 'on')
    elif isinstance(is_lunar_session, bool):
        is_lunar = is_lunar_session
    else:
        is_lunar = bool(is_lunar_session)
    processed = request.session.get('processed', False)
    
    # 쿼리 파라미터에서 년월 가져오기 (기본값: 현재 년월)
    now = datetime.now()
    try:
        year = int(request.query_params.get('year', now.year))
        month = int(request.query_params.get('month', now.month))
    except (ValueError, TypeError):
        year = now.year
        month = now.month
    
    # 년월 유효성 검증
    if year < 1900 or year > 2100:
        year = now.year
    if month < 1 or month > 12:
        month = now.month
    
    # 배너 생성
    sidebar_banner_html = get_banner_html(current_page=page, is_sidebar=True)
    
    return templates.TemplateResponse(
        "manse.html",
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
            "year": year,
            "month": month,
            "sidebar_banner_html": sidebar_banner_html,
        }
    )


@router.get("/tarot", response_class=HTMLResponse)
async def taro_page(request: Request):
    """타로 페이지"""
    from datetime import datetime
    
    page = "tarot"
    meta = get_page_meta(page)
    
    # 세션에서 사용자 데이터 가져오기
    pillars_data = request.session.get('pillars_data')
    pillars_info = request.session.get('pillars_info')
    user_name = request.session.get('user_name', '')
    user_gender = request.session.get('user_gender', '')
    birth_date = request.session.get('birth_date', '')
    birth_time = request.session.get('birth_time', '')
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
    sidebar_banner_html = get_banner_html(current_page=page, is_sidebar=True)
    
    return templates.TemplateResponse(
        "taro.html",
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
            "sidebar_banner_html": sidebar_banner_html,
        }
    )


@router.get("/lotto", response_class=HTMLResponse)
async def lotto_page(request: Request):
    """로또 페이지"""
    from datetime import datetime
    
    page = "lotto"
    meta = get_page_meta(page)
    
    # 세션에서 사용자 데이터 가져오기
    pillars_data = request.session.get('pillars_data')
    pillars_info = request.session.get('pillars_info')
    user_name = request.session.get('user_name', '')
    user_gender = request.session.get('user_gender', '')
    birth_date = request.session.get('birth_date', '')
    birth_time = request.session.get('birth_time', '')
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
    sidebar_banner_html = get_banner_html(current_page=page, is_sidebar=True)
    
    return templates.TemplateResponse(
        "lotto.html",
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
            "sidebar_banner_html": sidebar_banner_html,
        }
    )


@router.get("/privacy", response_class=HTMLResponse)
async def privacy_page(request: Request):
    """개인정보처리방침 페이지"""
    page = "privacy"
    meta = {
        "title": "개인정보처리방침 | 운세담",
        "description": "운세담 서비스의 개인정보처리방침입니다.",
        "keywords": "개인정보처리방침, 개인정보, 운세담",
        "url": f"{SITE_INFO['url']}/privacy",
        "author": SITE_INFO['author']
    }
    
    # 배너 생성
    sidebar_banner_html = get_banner_html(current_page=page, is_sidebar=True)
    
    return templates.TemplateResponse(
        "privacy.html",
        {
            "request": request,
            "page": page,
            "page_names": PAGE_NAMES,
            "meta": meta,
            "site_info": SITE_INFO,
            "sidebar_banner_html": sidebar_banner_html,
        }
    )


@router.get("/terms", response_class=HTMLResponse)
async def terms_page(request: Request):
    """이용약관 페이지"""
    page = "terms"
    meta = {
        "title": "이용약관 | 운세담",
        "description": "운세담 서비스 이용약관입니다.",
        "keywords": "이용약관, 약관, 운세담",
        "url": f"{SITE_INFO['url']}/terms",
        "author": SITE_INFO['author']
    }
    
    # 배너 생성
    sidebar_banner_html = get_banner_html(current_page=page, is_sidebar=True)
    
    return templates.TemplateResponse(
        "terms.html",
        {
            "request": request,
            "page": page,
            "page_names": PAGE_NAMES,
            "meta": meta,
            "site_info": SITE_INFO,
            "sidebar_banner_html": sidebar_banner_html,
        }
    )


@router.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    """사이트 소개 페이지"""
    page = "about"
    meta = get_page_meta(page)
    
    # 배너 생성
    sidebar_banner_html = get_banner_html(current_page=page, is_sidebar=True)
    
    return templates.TemplateResponse(
        "about.html",
        {
            "request": request,
            "page": page,
            "page_names": PAGE_NAMES,
            "meta": meta,
            "site_info": SITE_INFO,
            "sidebar_banner_html": sidebar_banner_html,
        }
    )


@router.get("/faq", response_class=HTMLResponse)
async def faq_page(request: Request):
    """자주 묻는 질문 페이지"""
    page = "faq"
    meta = get_page_meta(page)
    
    # 배너 생성
    sidebar_banner_html = get_banner_html(current_page=page, is_sidebar=True)
    
    return templates.TemplateResponse(
        "contact.html",  # 파일명은 그대로 유지하거나 faq.html로 변경 가능 (여기선 유지)
        {
            "request": request,
            "page": page,
            "page_names": PAGE_NAMES,
            "meta": meta,
            "site_info": SITE_INFO,
            "sidebar_banner_html": sidebar_banner_html,
        }
    )
