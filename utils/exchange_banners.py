"""
Exchange Banner Utility
Manages banner data and randomization logic for banner exchange partners.
"""
import random

# List of all exchange banners
EXCHANGE_BANNERS = [
    {
        "id": "stock_insight",
        "href": "https://stock-insight.app",
        "title": "내 주식, 살까 팔까? Stock Insight AI 분석 결과 보기",
        "img_src": "https://stock-insight.app/static/banner_link_234x60.png",
        "alt": "Stock Insight AI 배너",
        "width": 234,
        "height": 60,
        "style": "border:0;"
    },
    {
        "id": "vibecheck",
        "href": "https://vibecheck.page",
        "title": "VibeCheck - 나를 찾는 트렌디한 심리테스트",
        "img_src": "https://vibecheck.page/images/vibecheck_banner_234x60.png",
        "alt": "VibeCheck 배너",
        "width": 234,
        "height": 60,
        "style": "border-radius: 4px; border: 1px solid #eee;"
    },
    {
        "id": "promptgenie",
        "href": "https://promptgenie.kr",
        "title": "PromptGenie - AI Prompt Library",
        "img_src": "https://promptgenie.kr/images/banner_link_new_234x60.png",
        "alt": "PromptGenie - AI Prompt Library",
        "width": 234,
        "height": 60,
        "style": "border:0;"
    },
    {
        "id": "irumlab",
        "href": "https://irumlab.com",
        "title": "이룸랩 - 무료 셀프 작명, 영어 닉네임, 브랜드 네이밍",
        "img_src": "https://irumlab.com/banner_link_234x60.png",
        "alt": "이룸랩 배너",
        "width": 234,
        "height": 60,
        "style": "border:0;"
    },
    {
        "id": "nutrimatch",
        "href": "https://nutrimatch.kr",
        "title": "Nutri-Match - 나만의 영양제 궁합 & 저속노화 분석기",
        "img_src": "https://nutrimatch.kr/banner_link_234x60.png",
        "alt": "내 몸이 진짜 원하는 영양제는? Nutri-Match 분석 결과 보기",
        "width": 234,
        "height": 60,
        "style": "border:0; border-radius:4px;"
    },
    {
        "id": "moneymatch",
        "href": "https://moneymatch.kr",
        "title": "Money Match - AI 실시간 금융 뉴스 & 지원금 매칭",
        "img_src": "https://moneymatch.kr/banner_link_234x60.png",
        "alt": "놓치면 손해 보는 정부지원금, 3초 만에 찾기 - Money Match",
        "width": 234,
        "height": 60,
        "style": "border:0; border-radius:4px;"
    }
]

def get_random_banners(count: int = 3):
    """
    Selects a random subset of banners efficiently.
    If count is greater than total banners, returns all banners shuffled.
    
    Args:
        count: Number of banners to select
        
    Returns:
        list: List of selected banner dictionaries
    """
    if count >= len(EXCHANGE_BANNERS):
        shuffled = EXCHANGE_BANNERS.copy()
        random.shuffle(shuffled)
        return shuffled
    
    return random.sample(EXCHANGE_BANNERS, count)
