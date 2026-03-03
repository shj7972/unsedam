"""
페이지 설정 및 네비게이션 관련 유틸리티
"""

# Page names mapping (헤더 nav에 표시되는 페이지)
PAGE_NAMES = {
    'ai_saju': 'AI 사주',
    'daily': '오늘의 운세',
    'tojeong': '토정비결',
    'byeoljari': '별자리운세',
    'gonghap': '궁합',
    'dream': '꿈해몽',
    'tarot': '타로',
    'lotto': '로또',
    'manse': '만세력',
    'namefortune': '이름풀이',
    'blog': '운세가이드',
}

# 하단 footer 전용 페이지 (헤더 nav에 미포함)
FOOTER_PAGES = {
    'about': '사이트 소개',
    'faq': '자주 묻는 질문',
}

# NOTE: Legacy Streamlit functions removed for FastAPI migration.
# If you need to run Streamlit app, please revert this file or install streamlit.
