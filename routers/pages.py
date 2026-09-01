"""
페이지 라우터
각 페이지의 라우트를 정의합니다.
"""
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from utils.page_config import PAGE_NAMES
from utils.seo_fastapi import get_page_meta, SITE_INFO
from utils.banner_fastapi import get_banner_html

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

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
        request,
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
        request,
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
        request,
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
        request,
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
        request,
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
        request,
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
        request,
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
        request,
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
        request,
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
        request,
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
        request,
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


@router.get("/namefortune", response_class=HTMLResponse)
async def namefortune_page(request: Request):
    """이름 풀이 (성명학) 페이지"""
    from utils.namefortune import analyze_name, TYPE_COLORS

    page = "namefortune"
    meta = {
        "title": "이름 풀이 성명학 | 운세담",
        "description": "이름의 획수를 분석하는 무료 성명학 서비스. 81수리 기반 이름 풀이, 원형이정 4격 분석으로 내 이름에 담긴 기운을 확인하세요.",
        "keywords": "이름풀이, 성명학, 이름획수, 81수리, 작명, 개명, 이름분석, 무료이름풀이",
        "url": f"{SITE_INFO['url']}/namefortune",
        "author": SITE_INFO['author']
    }

    name = request.query_params.get('name', '').strip()
    result = None
    if name:
        result = analyze_name(name)

    sidebar_banner_html = get_banner_html(current_page=page, is_sidebar=True)

    return templates.TemplateResponse(
        request,
        "namefortune.html",
        {
            "request": request,
            "page": page,
            "page_names": PAGE_NAMES,
            "meta": meta,
            "site_info": SITE_INFO,
            "result": result,
            "name": name,
            "TYPE_COLORS": TYPE_COLORS,
            "sidebar_banner_html": sidebar_banner_html,
        }
    )


@router.get("/daily", response_class=HTMLResponse)
async def daily_page(request: Request):
    """오늘의 운세 페이지"""
    from datetime import datetime
    from utils.constellation import get_constellation, get_daily_fortune, get_lucky_elements, get_life_aspects_fortune
    import saju_logic

    page = "daily"

    # 세션에서 사용자 데이터 가져오기
    user_name = request.session.get('user_name', '')
    birth_date = request.session.get('birth_date', '')
    processed = request.session.get('processed', False)

    today = datetime.now()
    today_str = today.strftime('%Y년 %m월 %d일')

    # 오늘 날짜를 메타 title/description에 동적 반영 (네이버 "오늘의운세 날짜" 검색 타겟)
    meta = {
        "title": f"{today.strftime('%Y년 %m월 %d일')} 오늘의 운세 ✨ 별자리·사주 일진 총정리 | 운세담",
        "description": f"{today.strftime('%Y년 %#m월 %#d일')} 오늘의 운세! 내 별자리 운세와 사주 일진을 결합한 {today.strftime('%Y')}년 가장 정확한 오늘의 무료 운세를 확인하세요.",
        "keywords": f"오늘의운세, 오늘운세, {today.strftime('%m')}월운세, 별자리운세오늘, 오늘사주, 무료운세, 일일운세, {today.strftime('%Y년%m월%d일')}운세",
        "url": f"{SITE_INFO['url']}/daily",
        "author": SITE_INFO['author'],
    }
    weekdays = ['월', '화', '수', '목', '금', '토', '일']
    today_weekday = weekdays[today.weekday()]
    today_full = f"{today_str} ({today_weekday}요일)"

    # 오늘의 일진 계산
    from datetime import date as date_type
    today_date_obj = today.date()
    day_stem, day_branch = saju_logic.get_day_ganji(today)
    day_ganji = f"{day_stem} {day_branch}"

    daily_fortune = None
    lucky = None
    constellation_name = None
    constellation_emoji = None
    life_aspects = None

    if birth_date:
        try:
            birth_dt = datetime.strptime(birth_date, "%Y-%m-%d").date()
            constellation_name, constellation_emoji, _ = get_constellation(birth_dt)
            daily_fortune = get_daily_fortune(constellation_name, today.date())
            lucky = get_lucky_elements(constellation_name)
            life_aspects = get_life_aspects_fortune(constellation_name, today.date())
        except Exception:
            pass

    sidebar_banner_html = get_banner_html(current_page=page, is_sidebar=True)

    return templates.TemplateResponse(
        request,
        "daily.html",
        {
            "request": request,
            "page": page,
            "page_names": PAGE_NAMES,
            "meta": meta,
            "site_info": SITE_INFO,
            "user_name": user_name,
            "birth_date": birth_date,
            "processed": processed,
            "today_full": today_full,
            "day_ganji": day_ganji,
            "today": today,
            "daily_fortune": daily_fortune,
            "lucky": lucky,
            "constellation_name": constellation_name,
            "constellation_emoji": constellation_emoji,
            "life_aspects": life_aspects,
            "sidebar_banner_html": sidebar_banner_html,
        }
    )


@router.get("/blog", response_class=HTMLResponse)
async def blog_page(request: Request):
    """블로그/아티클 목록 페이지"""
    from utils.blog_articles import get_all_articles, get_articles_by_category, CATEGORIES
    page = "blog"
    meta = get_page_meta(page)

    category = request.query_params.get('category', '').strip()
    if category:
        articles = get_articles_by_category(category)
    else:
        articles = get_all_articles()

    sidebar_banner_html = get_banner_html(current_page=page, is_sidebar=True)
    return templates.TemplateResponse(request, "blog.html", {
        "request": request, "page": page, "page_names": PAGE_NAMES,
        "meta": meta, "site_info": SITE_INFO,
        "articles": articles,
        "categories": sorted(CATEGORIES),
        "current_category": category,
        "sidebar_banner_html": sidebar_banner_html,
    })


@router.get("/blog/{slug}", response_class=HTMLResponse)
async def blog_detail_page(request: Request, slug: str):
    """블로그 아티클 상세 페이지"""
    from utils.blog_articles import get_article_by_slug, get_related_articles
    article = get_article_by_slug(slug)
    if not article:
        raise HTTPException(status_code=404, detail="아티클을 찾을 수 없습니다.")

    related = get_related_articles(slug, limit=3)
    page = "blog"
    meta = {
        "title": f"{article['title']} | 운세담",
        "description": article['description'],
        "keywords": ", ".join(article['tags']),
        "url": f"{SITE_INFO['url']}/blog/{slug}",
        "author": SITE_INFO['author']
    }
    sidebar_banner_html = get_banner_html(current_page=page, is_sidebar=True)
    return templates.TemplateResponse(request, "blog_detail.html", {
        "request": request, "page": page, "page_names": PAGE_NAMES,
        "meta": meta, "site_info": SITE_INFO,
        "article": article,
        "related": related,
        "sidebar_banner_html": sidebar_banner_html,
    })


@router.get("/zodiac", response_class=HTMLResponse)
async def zodiac_hub_page(request: Request):
    """12띠 운세 허브 페이지"""
    from utils.zodiac_fortune import get_all_zodiacs
    page = "zodiac"
    meta = {
        "title": "12띠 운세 | 운세담",
        "description": "2026년 12띠별 운세를 확인하세요. 쥐띠, 소띠, 호랑이띠, 토끼띠, 용띠, 뱀띠, 말띠, 양띠, 원숭이띠, 닭띠, 개띠, 돼지띠 운세 및 궁합 정보.",
        "keywords": "12띠 운세, 2026 띠별 운세, 호랑이띠 운세, 말띠 운세, 용띠 운세, 띠 궁합",
        "url": f"{SITE_INFO['url']}/zodiac",
        "author": SITE_INFO['author']
    }
    zodiacs = get_all_zodiacs()
    sidebar_banner_html = get_banner_html(current_page=page, is_sidebar=True)
    return templates.TemplateResponse(request, "zodiac.html", {
        "request": request, "page": page, "page_names": PAGE_NAMES,
        "meta": meta, "site_info": SITE_INFO,
        "zodiacs": zodiacs, "sidebar_banner_html": sidebar_banner_html,
    })


@router.get("/zodiac/{animal}", response_class=HTMLResponse)
async def zodiac_detail_page(request: Request, animal: str):
    """특정 띠 상세 운세 페이지"""
    from utils.zodiac_fortune import get_zodiac_by_key
    zodiac = get_zodiac_by_key(animal)
    if not zodiac:
        raise HTTPException(status_code=404, detail="Not found")
    page = "zodiac"
    meta = {
        "title": f"{zodiac['korean']} 운세 2026 | 운세담",
        "description": f"2026년 {zodiac['korean']} 운세를 확인하세요. {zodiac['korean']} 성격, 특징, 2026년 운세, 궁합 정보를 제공합니다.",
        "keywords": f"{zodiac['korean']}, {zodiac['korean']} 운세, {zodiac['korean']} 2026, {zodiac['korean']} 궁합",
        "url": f"{SITE_INFO['url']}/zodiac/{animal}",
        "author": SITE_INFO['author']
    }
    sidebar_banner_html = get_banner_html(current_page=page, is_sidebar=True)
    return templates.TemplateResponse(request, "zodiac_detail.html", {
        "request": request, "page": page, "page_names": PAGE_NAMES,
        "meta": meta, "site_info": SITE_INFO,
        "zodiac": zodiac, "sidebar_banner_html": sidebar_banner_html,
    })


@router.get("/fortune/{year}", response_class=HTMLResponse)
async def fortune_year_page(request: Request, year: int):
    """출생연도별 운세 페이지"""
    from utils.zodiac_fortune import get_year_fortune
    from datetime import datetime
    current_year = datetime.now().year
    if year < 1900 or year > current_year:
        raise HTTPException(status_code=404, detail="Not found")
    data = get_year_fortune(year)
    page = "fortune_year"
    meta = {
        "title": f"{year}년생 운세 | {data['zodiac']['korean']} | 운세담",
        "description": f"{year}년생({data['zodiac']['korean']}) 2026년 운세를 확인하세요. 한국 나이 {data['age_korean']}세, 2026년 {year}년생 운세 분석.",
        "keywords": f"{year}년생 운세, {year}년생 {data['zodiac']['korean']}, {year}년생 2026 운세, {data['age_korean']}세 운세",
        "url": f"{SITE_INFO['url']}/fortune/{year}",
        "author": SITE_INFO['author']
    }
    sidebar_banner_html = get_banner_html(current_page=page, is_sidebar=True)
    return templates.TemplateResponse(request, "fortune_year.html", {
        "request": request, "page": page, "page_names": PAGE_NAMES,
        "meta": meta, "site_info": SITE_INFO,
        "data": data, "year": year, "sidebar_banner_html": sidebar_banner_html,
    })


# =============================================================================
# 띠궁합 (compat) 페이지 — 2026-09-01 롱테일 1차
# =============================================================================

@router.get("/compat", response_class=HTMLResponse)
async def compat_hub_page(request: Request):
    """12띠 궁합 허브 페이지 (66쌍 전체)"""
    from utils.zodiac_fortune import get_all_zodiacs
    from utils.zodiac_compat import get_all_pairs

    page = "compat"
    meta = {
        "title": "12띠 궁합 총정리 | 육합·삼합·육충 명리 해석 | 운세담",
        "description": "띠별 궁합 66가지 조합을 명리학 육합·삼합·육충 원리로 해석합니다. 쥐띠부터 돼지띠까지 연애·결혼·동업 궁합 무료 확인.",
        "keywords": "띠궁합, 12띠 궁합, 띠별 궁합, 쥐띠 궁합, 소띠 궁합, 용띠 궁합, 말띠 궁합, 띠 궁합표, 명리 궁합",
        "url": f"{SITE_INFO['url']}/compat",
        "author": SITE_INFO['author']
    }
    zodiacs = get_all_zodiacs()
    compat_map = get_all_pairs()
    sidebar_banner_html = get_banner_html(current_page=page, is_sidebar=True)
    return templates.TemplateResponse(request, "compat.html", {
        "request": request, "page": page, "page_names": PAGE_NAMES,
        "meta": meta, "site_info": SITE_INFO,
        "zodiacs": zodiacs, "compat_map": compat_map,
        "sidebar_banner_html": sidebar_banner_html,
    })


@router.get("/compat/{pair}", response_class=HTMLResponse)
async def compat_detail_page(request: Request, pair: str):
    """띠×띠 궁합 상세 페이지 (예: rat-vs-ox)"""
    from utils.zodiac_fortune import get_all_zodiacs
    from utils.zodiac_compat import get_pair_fortune

    if "-vs-" not in pair:
        raise HTTPException(status_code=404, detail="Not found")
    a_key, b_key = pair.split("-vs-", 1)
    try:
        compat = get_pair_fortune(a_key, b_key)
    except KeyError:
        raise HTTPException(status_code=404, detail="Not found")

    page = "compat"
    za_name = compat['zodiac_a']['korean']
    zb_name = compat['zodiac_b']['korean']
    meta = {
        "title": f"{za_name} {zb_name} 궁합 — {compat['relation_label']} {compat['score']}점 | 운세담",
        "description": f"{za_name}와 {zb_name}의 궁합을 명리학 {compat['relation_label']} 원리로 분석. 연애 {compat['area']['love']}점, 결혼 {compat['area']['marriage']}점. 2026년 두 띠의 운세까지 한 번에 확인하세요.",
        "keywords": f"{za_name} {zb_name} 궁합, {za_name} 궁합, {zb_name} 궁합, 띠궁합, {compat['relation_label']}",
        "url": f"{SITE_INFO['url']}/compat/{pair}",
        "author": SITE_INFO['author']
    }
    zodiacs = get_all_zodiacs()
    sidebar_banner_html = get_banner_html(current_page=page, is_sidebar=True)
    return templates.TemplateResponse(request, "compat_detail.html", {
        "request": request, "page": page, "page_names": PAGE_NAMES,
        "meta": meta, "site_info": SITE_INFO,
        "compat": compat, "all_zodiacs": zodiacs,
        "sidebar_banner_html": sidebar_banner_html,
    })
