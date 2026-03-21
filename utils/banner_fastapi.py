"""
배너 광고 유틸리티 (FastAPI 버전)
프로젝트 메뉴 홍보 및 광고 배너를 생성합니다.
"""
import random
from utils.page_config import PAGE_NAMES


# 프로젝트 메뉴별 배너 광고 문구
BANNER_ADS = {
    'ai_saju': {
        'text': '2026년 무료 AI 운세',
        'icon': '🤖',
        'link': '/'
    },
    'tojeong': {
        'text': '2026년 무료 토정비결',
        'icon': '📜',
        'link': '/tojeong'
    },
    'byeoljari': {
        'text': '2026년 무료 별자리운세',
        'icon': '⭐',
        'link': '/byeoljari'
    },
    'gonghap': {
        'text': '2026년 무료 궁합',
        'icon': '💕',
        'link': '/gonghap'
    },
    'dream': {
        'text': '2026년 무료 꿈해몽',
        'icon': '💭',
        'link': '/dream'
    },
    'tarot': {
        'text': '2026년 무료 타로',
        'icon': '🃏',
        'link': '/taro'
    },
    'lotto': {
        'text': '2026년 무료 로또번호',
        'icon': '🎱',
        'link': '/lotto'
    },
    'manse': {
        'text': '2026년 무료 만세력',
        'icon': '📅',
        'link': '/manse'
    }
}


def get_random_banner(current_page: str = None):
    """
    현재 페이지를 제외한 랜덤 배너를 선택합니다.
    
    Args:
        current_page: 현재 페이지 키 (제외할 페이지)
        
    Returns:
        dict: 배너 정보 (text, icon, link)
    """
    # 현재 페이지를 제외한 배너 목록
    available_ads = {k: v for k, v in BANNER_ADS.items() if k != current_page}
    
    if not available_ads:
        # 모든 페이지가 현재 페이지인 경우 (이론적으로 불가능하지만 안전장치)
        available_ads = BANNER_ADS
    
    # 랜덤 선택
    selected_key = random.choice(list(available_ads.keys()))
    return available_ads[selected_key]


def get_banner_html(
    text: str = None,
    link: str = None,
    link_text: str = "지금 확인하기",
    style: str = "promotion",  # "promotion" or "ad"
    current_page: str = None,
    random_rotation: bool = True,
    is_sidebar: bool = False
):
    """
    배너 HTML을 생성합니다.
    
    Args:
        text: 배너에 표시할 텍스트 (None이면 랜덤 선택)
        link: 클릭 시 이동할 링크 (None이면 랜덤 선택)
        link_text: 링크 버튼 텍스트
        style: 배너 스타일 ("promotion" 또는 "ad")
        current_page: 현재 페이지 키 (랜덤 선택 시 제외할 페이지)
        random_rotation: 랜덤 로테이션 사용 여부
        is_sidebar: 사이드바용 배너 여부
    
    Returns:
        str: 배너 HTML 문자열
    """
    # 랜덤 로테이션이 활성화되고 text/link가 지정되지 않은 경우
    if random_rotation and (text is None or link is None):
        banner_info = get_random_banner(current_page)
        text = text or banner_info['text']
        link = link or banner_info['link']
        icon = banner_info.get('icon', '🎯')
    else:
        icon = '🎯'
    
    # text와 link가 여전히 None인 경우 기본값 사용
    if text is None:
        text = "2026년 무료 토정비결"
    if link is None:
        link = "/tojeong"
    
    if is_sidebar:
        # 사이드바용 배너 스타일
        banner_html = f"""
        <div class="sidebar-banner-promotion" style="margin-top: 1.5rem; padding: 1rem; background: linear-gradient(rgba(26, 35, 62, 0.5), rgba(26, 35, 62, 0.5)), url('/static/images/sidebar_banner_bg.webp') no-repeat center center; background-size: cover; border: 1px solid rgba(212,175,55,0.3); border-radius: 8px; position: relative; overflow: hidden;">
            <div style="display: flex; flex-direction: column; gap: 0.75rem; position: relative; z-index: 1;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="font-size: 1.2em;">{icon}</span>
                    <span style="color: var(--text-primary); font-weight: 500; font-size: 0.9em;">{text}</span>
                </div>
                <a href="{link}" style="display: inline-block; padding: 0.5rem 1rem; background: var(--gold-gradient); color: var(--bg-dark); text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 0.85em; text-align: center; transition: transform 0.2s;">
                    {link_text} →
                </a>
            </div>
        </div>
        """
    else:
        # 컨텐츠 상단용 배너 스타일 (결과 영역에만 위치, 모바일 대응)
        banner_html = f"""
        <div class="banner-promotion" style="margin-top: 0; margin-bottom: 2rem; padding: 1rem 1.25rem; background: linear-gradient(rgba(26, 35, 62, 0.4), rgba(26, 35, 62, 0.4)), url('/static/images/main_banner_bg.webp') no-repeat center center; background-size: cover; border: 2px solid rgba(212,175,55,0.4); border-radius: 12px; box-shadow: 0 4px 15px rgba(212,175,55,0.2); width: 100%; max-width: 100%; position: relative; overflow: hidden;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; position: relative; z-index: 1;">
                <div style="display: flex; align-items: center; gap: 0.75rem; flex: 1; min-width: 200px;">
                    <span style="font-size: 1.3em;">{icon}</span>
                    <span style="color: var(--text-primary); font-weight: 600; font-size: 1em;">{text}</span>
                </div>
                <a href="{link}" style="display: inline-block; padding: 0.6rem 1.2rem; background: var(--gold-gradient); color: var(--bg-dark); text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 0.9em; transition: transform 0.2s; white-space: nowrap; flex-shrink: 0;">
                    {link_text} →
                </a>
            </div>
        </div>
        """
    
    return banner_html

