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
        "title": "AI 사주 | 운세담",
        "description": "AI 기반 프리미엄 사주 분석 서비스. 정확한 사주명리 분석과 상세한 해석을 제공합니다.",
        "keywords": "AI 사주, 사주명리, 사주분석, 무료사주, 사주보기",
        "url": SITE_INFO['url']
    },
    'tojeong': {
        "title": "토정비결 | 운세담",
        "description": "2026년 무료 토정비결 서비스. 토정 이지함의 토정비결을 바탕으로 한 정확한 운세 분석을 제공합니다.",
        "keywords": "토정비결, 토정비결 무료, 2026 토정비결, 토정 이지함, 운세",
        "url": f"{SITE_INFO['url']}/tojeong"
    },
    'byeoljari': {
        "title": "별자리운세 | 운세담",
        "description": "12궁 별자리 운세 분석 서비스. 오늘의 운세, 주간 운세, 월간 운세를 확인하세요.",
        "keywords": "별자리운세, 12궁, 별자리, 운세, 별자리 오늘의 운세",
        "url": f"{SITE_INFO['url']}/byeoljari"
    },
    'gonghap': {
        "title": "궁합 | 운세담",
        "description": "사주 궁합 분석 서비스. 연인, 부부, 친구 간의 궁합을 정확하게 분석해드립니다.",
        "keywords": "궁합, 사주궁합, 연인궁합, 부부궁합, 궁합보기",
        "url": f"{SITE_INFO['url']}/gonghap"
    },
    'dream': {
        "title": "꿈해몽 | 운세담",
        "description": "무료 꿈해몽 서비스. 꿈의 의미를 AI로 분석하고 상세한 해몽을 제공합니다.",
        "keywords": "꿈해몽, 꿈풀이, 꿈해석, 무료꿈해몽, 꿈의 의미",
        "url": f"{SITE_INFO['url']}/dream"
    },
    'tarot': {
        "title": "타로 | 운세담",
        "description": "타로 카드 뽑기 및 해석 서비스. 원카드, 3장, 켈틱 크로스 등 다양한 스프레드로 운세를 확인하세요.",
        "keywords": "타로, 타로카드, 타로뽑기, 타로해석, 무료타로",
        "url": f"{SITE_INFO['url']}/tarot"
    },
    'lotto': {
        "title": "로또 | 운세담",
        "description": "로또 번호 생성 및 운세 분석 서비스. 사주를 기반으로 한 로또 번호 추천을 제공합니다.",
        "keywords": "로또, 로또번호, 로또번호생성, 로또번호추천, 사주로또",
        "url": f"{SITE_INFO['url']}/lotto"
    },
    'manse': {
        "title": "만세력 | 운세담",
        "description": "만세력 조회 서비스. 생년월일시를 입력하여 정확한 만세력을 확인하세요.",
        "keywords": "만세력, 만세력보기, 사주만세력, 무료만세력",
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
        # ai_saju는 메인 페이지이므로 이미 추가됨
        if page_key == 'ai_saju':
            continue
            
        # tarot 페이지는 실제 라우터에서 /tarot로 되어 있음
        if page_key == 'tarot':
            page_url = f"{site_url}/tarot"
        else:
            page_url = f"{site_url}/{page_key}"
            
        sitemap_lines.append('  <url>')
        sitemap_lines.append(f'    <loc>{page_url}</loc>')
        sitemap_lines.append(f'    <lastmod>{current_date}</lastmod>')
        sitemap_lines.append('    <changefreq>weekly</changefreq>')
        sitemap_lines.append('    <priority>0.8</priority>')
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

# 다음 웹마스터 도구 인증
#DaumWebMasterTool:42858a913fc55df5e2dc9371b659ac47ba48ec6bb332cb43322f947d6e1ac763:1hrba1lpzexyTL25MI8THg==
"""
    return robots_content

