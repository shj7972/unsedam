"""
SEO 최적화 유틸리티 (FastAPI 버전)
메타 태그, 구조화된 데이터, sitemap 등을 관리합니다.
Streamlit 의존성 제거 버전
"""
from utils.page_config import PAGE_NAMES


# 사이트 기본 정보
SITE_INFO = {
    "name": "운세담",
    "description": "AI 프리미엄 사주 명리 분석 서비스. 토정비결, AI 사주, 별자리운세, 궁합, 꿈해몽, 타로, 로또 등 다양한 운세 서비스를 제공합니다.",
    "url": "https://unsedam.kr",  # 커스텀 도메인
    "author": "운세담",
    "keywords": "사주, 운세, 토정비결, AI 사주, 별자리운세, 궁합, 꿈해몽, 타로, 로또, 명리학, 사주명리, 무료사주",
    "language": "ko-KR"
}

# 페이지별 메타 정보
PAGE_META = {
    'ai_saju': {
        "title": "[무료] 2026년 AI 사주 분석 ✨ 내 운명의 진짜 흐름 | 운세담",
        "description": "수천 년 명리학 데이터와 최신 AI 기술의 결합! 생년월일을 입력하고 나의 2026년 대운과 재물운, 직장운의 완벽한 흐름을 무료로 확인해 보세요.",
        "keywords": "AI사주, 사주명리, 사주분석, 무료사주, 사주보기, 내사주보기, 사주풀이, 무료운세, 2026사주, 사주팔자무료",
        "url": SITE_INFO['url']
    },
    'tojeong': {
        "title": "[무료] 2026년 토정비결 ✨ 소름돋는 정확도 | 운세담",
        "description": "올해 나의 재물운과 연애운은? 토정 이지함의 비결을 현대적으로 완벽 분석한 2026년 토정비결 무료 풀이로 대비책을 확인해 보세요.",
        "keywords": "토정비결, 토정비결무료, 2026토정비결, 토정비결보기, 올해토정비결, 무료토정비결, 토정이지함, 토정비결2026년",
        "url": f"{SITE_INFO['url']}/tojeong"
    },
    'byeoljari': {
        "title": "오늘의 별자리 운세 ✨ 나만의 럭키 컬러와 숫자 | 운세담",
        "description": "매일 아침 업데이트되는 12별자리 운세! 당신의 애정운, 금전운, 직장운을 완벽 가이드합니다. 오늘의 행운 팁을 지금 무료로 확인하세요.",
        "keywords": "별자리운세, 오늘의별자리운세, 별자리운세오늘, 12궁운세, 별자리보기, 내별자리운세, 오늘별자리, 무료별자리운세",
        "url": f"{SITE_INFO['url']}/byeoljari"
    },
    'gonghap': {
        "title": "소름돋는 사주 궁합 💑 우리는 찰떡궁합일까? | 운세담",
        "description": "나와 상대방의 생년월일만으로 완벽한 사주 궁합을 분석합니다. 연인, 썸남썸녀, 친구와의 속궁합부터 결혼운까지 지금 바로 테스트해보세요.",
        "keywords": "궁합보기, 사주궁합, 무료궁합, 연인궁합, 부부궁합, 궁합테스트, 속궁합, 사주궁합보기, 생년월일궁합",
        "url": f"{SITE_INFO['url']}/gonghap"
    },
    'dream': {
        "title": "이 꿈 로또 사야 할까? 💤 소름돋는 AI 꿈해몽 | 운세담",
        "description": "어젯밤 꾼 꿈, 혹시 대박 징조? 돼지꿈, 뱀꿈, 이빨 빠지는 꿈 등 모든 꿈의 진짜 의미를 AI가 즉시 해몽해 드립니다.",
        "keywords": "꿈해몽, 꿈풀이, 무료꿈해몽, 돼지꿈, 뱀꿈, 이빨빠지는꿈, 꿈해석, 꿈의미, 길몽흉몽, 꿈해몽사전",
        "url": f"{SITE_INFO['url']}/dream"
    },
    'tarot': {
        "title": "무료 타로점 보기 🃏 지금 바로 카드 한 장 뽑기 | 운세담",
        "description": "당신의 고민, 타로 카드는 답을 알고 있습니다. 금전운, 연애운, 속마음을 꿰뚫어 보는 소름돋는 무료 타로점 테스트를 시작해 보세요.",
        "keywords": "타로카드, 무료타로, 타로뽑기, 타로점, 연애타로, 오늘의타로, 타로보기, 원카드타로, 타로해석",
        "url": f"{SITE_INFO['url']}/tarot"
    },
    'lotto': {
        "title": "사주 로또 번호 추천 🍀 대박 터지는 행운의 숫자 | 운세담",
        "description": "나의 사주팔자 오행에 숨겨진 1등 당첨 행운의 숫자는? 타고난 재물운 기운을 분석하여 소름돋는 맞춤형 로또 번호를 무료로 추천해 드립니다.",
        "keywords": "로또번호추천, 이번주로또번호, 로또번호생성, 사주로또, 행운의번호, 로또번호, 로또당첨번호, 로또번호예측",
        "url": f"{SITE_INFO['url']}/lotto"
    },
    'manse': {
        "title": "내 사주팔자 직접 보기 📖 가장 정확한 만세력 | 운세담",
        "description": "전문가 수준의 가장 정확한 만세력 서비스. 태어난 시간만 알아도 나의 천간, 지지, 십이운성, 신살까지 완벽한 명식표를 즉시 제공합니다.",
        "keywords": "만세력, 무료만세력, 만세력보기, 사주만세력, 만세력조견표, 사주팔자보기, 내만세력, 만세력2026",
        "url": f"{SITE_INFO['url']}/manse"
    },
    'about': {
        "title": "운세담 소개 | AI 프리미엄 사주",
        "description": "운세담 서비스의 비전과 AI 명리학 분석 기술에 대해 소개합니다.",
        "keywords": "운세담 소개, AI 사주 비전, 명리학 기술, 운세 서비스",
        "url": f"{SITE_INFO['url']}/about"
    },
    'faq': {
        "title": "자주 묻는 질문(FAQ) | 운세담",
        "description": "운세담 서비스 이용과 관련된 주요 궁금증을 해결해 드립니다.",
        "keywords": "FAQ, 자주 묻는 질문, 고객지원, 운세담 도움말",
        "url": f"{SITE_INFO['url']}/faq"
    },
    'daily': {
        "title": "오늘의 운세 총정리 ✨ 나의 행운 포인트는? | 운세담",
        "description": "오늘 하루, 대박 날 타이밍은 언제일까? 별자리와 사주 일진을 결합한 가장 완벽한 일일 무료 운세로 완벽한 하루를 준비하세요.",
        "keywords": "오늘의운세, 오늘운세, 무료운세, 일일운세, 오늘의별자리, 별자리운세오늘, 오늘사주, 오늘의운세무료, 내일운세, 이번주운세",
        "url": f"{SITE_INFO['url']}/daily"
    },
    'namefortune': {
        "title": "내 이름에 숨겨진 진짜 운명 🔍 무료 81수리 이름풀이 | 운세담",
        "description": "내 이름은 재물운을 부를까? 전문가 수준의 81수리 성명학과 원형이정 4격 분석으로 이름의 좋고 나쁨을 소름돋게 풀이해 드립니다.",
        "keywords": "이름풀이, 무료이름풀이, 성명학, 이름획수, 81수리, 이름작명, 개명, 이름운세, 이름뜻, 성명학풀이",
        "url": f"{SITE_INFO['url']}/namefortune"
    },
    'blog': {
        "title": "운세 가이드 | 운세담",
        "description": "사주팔자, 별자리, 타로, 꿈해몽, 성명학 등 운세에 관한 깊이 있는 가이드 아티클 모음. 초보자부터 전문가까지 쉽게 이해할 수 있는 동양 철학 완전 정복.",
        "keywords": "사주가이드, 운세공부, 사주팔자기초, 별자리운세가이드, 타로가이드, 꿈해몽가이드, 성명학가이드",
        "url": f"{SITE_INFO['url']}/blog"
    }
}


def get_page_meta(page_key: str) -> dict:
    """
    페이지별 메타 정보를 반환합니다.
    
    Args:
        page_key: 페이지 키
        
    Returns:
        dict: 메타 정보 딕셔너리 (title, description, keywords, url, author 포함)
    """
    default_meta = {
        "title": f"{SITE_INFO['name']} | AI 프리미엄 사주",
        "description": SITE_INFO['description'],
        "keywords": SITE_INFO['keywords'],
        "url": SITE_INFO['url'],
        "author": SITE_INFO['author']
    }
    
    meta = PAGE_META.get(page_key, default_meta)
    # author는 항상 추가
    meta['author'] = SITE_INFO['author']
    return meta


def generate_sitemap() -> str:
    """
    sitemap.xml을 생성합니다.
    
    Returns:
        str: sitemap.xml 내용
    """
    from datetime import datetime
    
    site_url = SITE_INFO['url']
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    sitemap_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    sitemap_lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    # 메인 페이지 (AI 사주)
    sitemap_lines.append('  <url>')
    sitemap_lines.append(f'    <loc>{site_url}/</loc>')
    sitemap_lines.append(f'    <lastmod>{current_date}</lastmod>')
    sitemap_lines.append('    <changefreq>daily</changefreq>')
    sitemap_lines.append('    <priority>1.0</priority>')
    sitemap_lines.append('  </url>')
    
    # 각 페이지
    # tarot 페이지는 실제 라우터에서 /tarot로 되어 있으므로 확인 필요
    for page_key, page_name in PAGE_NAMES.items():
        # ai_saju는 메인 페이지, blog는 별도 처리
        if page_key in ('ai_saju', 'blog'):
            continue

        # tarot 페이지는 실제 라우터에서 /tarot로 되어 있음
        if page_key == 'tarot':
            page_url = f"{site_url}/tarot"
        else:
            page_url = f"{site_url}/{page_key}"

        # daily 페이지는 매일 업데이트되므로 changefreq=daily, priority 높게
        if page_key == 'daily':
            changefreq = 'daily'
            priority = '0.9'
        else:
            changefreq = 'weekly'
            priority = '0.8'

        sitemap_lines.append('  <url>')
        sitemap_lines.append(f'    <loc>{page_url}</loc>')
        sitemap_lines.append(f'    <lastmod>{current_date}</lastmod>')
        sitemap_lines.append(f'    <changefreq>{changefreq}</changefreq>')
        sitemap_lines.append(f'    <priority>{priority}</priority>')
        sitemap_lines.append('  </url>')
    
    # 12띠 및 연도별 페이지 (대표 페이지만 추가)
    for zodiac_key in ['rat', 'ox', 'tiger', 'rabbit', 'dragon', 'snake', 'horse', 'sheep', 'monkey', 'rooster', 'dog', 'pig']:
        sitemap_lines.append('  <url>')
        sitemap_lines.append(f'    <loc>{site_url}/zodiac/{zodiac_key}</loc>')
        sitemap_lines.append(f'    <lastmod>{current_date}</lastmod>')
        sitemap_lines.append('    <changefreq>monthly</changefreq>')
        sitemap_lines.append('    <priority>0.7</priority>')
        sitemap_lines.append('  </url>')

    # 띠궁합 (compat) 페이지 — 66쌍 전체
    zodiac_keys = ['rat', 'ox', 'tiger', 'rabbit', 'dragon', 'snake', 'horse', 'sheep', 'monkey', 'rooster', 'dog', 'pig']
    sitemap_lines.append('  <url>')
    sitemap_lines.append(f'    <loc>{site_url}/compat</loc>')
    sitemap_lines.append(f'    <lastmod>{current_date}</lastmod>')
    sitemap_lines.append('    <changefreq>weekly</changefreq>')
    sitemap_lines.append('    <priority>0.8</priority>')
    sitemap_lines.append('  </url>')
    for a_idx, a_key in enumerate(zodiac_keys):
        for b_key in zodiac_keys[a_idx+1:]:
            sitemap_lines.append('  <url>')
            sitemap_lines.append(f'    <loc>{site_url}/compat/{a_key}-vs-{b_key}</loc>')
            sitemap_lines.append(f'    <lastmod>{current_date}</lastmod>')
            sitemap_lines.append('    <changefreq>monthly</changefreq>')
            sitemap_lines.append('    <priority>0.7</priority>')
            sitemap_lines.append('  </url>')

    # 주요 출생연도 페이지 (1970~2010년대 대표 연도)
    for yr in range(1970, 2011, 3):
        sitemap_lines.append('  <url>')
        sitemap_lines.append(f'    <loc>{site_url}/fortune/{yr}</loc>')
        sitemap_lines.append(f'    <lastmod>{current_date}</lastmod>')
        sitemap_lines.append('    <changefreq>monthly</changefreq>')
        sitemap_lines.append('    <priority>0.7</priority>')
        sitemap_lines.append('  </url>')

    # 블로그/가이드 아티클 페이지
    from utils.blog_articles import get_all_articles
    sitemap_lines.append('  <url>')
    sitemap_lines.append(f'    <loc>{site_url}/blog</loc>')
    sitemap_lines.append(f'    <lastmod>{current_date}</lastmod>')
    sitemap_lines.append('    <changefreq>weekly</changefreq>')
    sitemap_lines.append('    <priority>0.8</priority>')
    sitemap_lines.append('  </url>')
    for article in get_all_articles():
        sitemap_lines.append('  <url>')
        sitemap_lines.append(f'    <loc>{site_url}/blog/{article["slug"]}</loc>')
        sitemap_lines.append(f'    <lastmod>{article["date"].strftime("%Y-%m-%d")}</lastmod>')
        sitemap_lines.append('    <changefreq>monthly</changefreq>')
        sitemap_lines.append('    <priority>0.75</priority>')
        sitemap_lines.append('  </url>')

    # 추가 정책/정보 페이지
    for extra_page in ['about', 'faq', 'privacy', 'terms']:
        sitemap_lines.append('  <url>')
        sitemap_lines.append(f'    <loc>{site_url}/{extra_page}</loc>')
        sitemap_lines.append(f'    <lastmod>{current_date}</lastmod>')
        sitemap_lines.append('    <changefreq>monthly</changefreq>')
        sitemap_lines.append('    <priority>0.5</priority>')
        sitemap_lines.append('  </url>')
    
    sitemap_lines.append('</urlset>')
    
    return '\n'.join(sitemap_lines)


def generate_robots_txt() -> str:
    """
    robots.txt를 생성합니다.
    네이버, 구글, 다음 검색로봇을 명시적으로 허용합니다.
    
    Returns:
        str: robots.txt 내용
    """
    site_url = SITE_INFO['url']
    
    robots_content = f"""# 네이버 검색로봇 명시적 허용
User-agent: Yeti
Allow: /
Disallow: /api/
Disallow: /health

User-agent: NaverBot
Allow: /
Disallow: /api/
Disallow: /health

# 구글 검색로봇
User-agent: Googlebot
Allow: /
Disallow: /api/
Disallow: /health

# 다음 검색로봇
User-agent: Daumoa
Allow: /
Disallow: /api/
Disallow: /health

# 기타 모든 봇
User-agent: *
Allow: /
Disallow: /api/
Disallow: /health

# Sitemap 위치
Sitemap: {site_url}/sitemap.xml

# RSS 피드 (네이버 웹마스터 도구 RSS 등록용)
# RSS: {site_url}/rss.xml

# 다음 웹마스터 도구 인증
#DaumWebMasterTool:42858a913fc55df5e2dc9371b659ac47ba48ec6bb332cb43322f947d6e1ac763:1hrba1lpzexyTL25MI8THg==
"""
    return robots_content

