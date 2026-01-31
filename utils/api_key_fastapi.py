"""
API Key 관리 유틸리티 (FastAPI 버전)
OpenAI API Key를 안전하게 관리하고 가져오는 기능 제공
"""
import os
from typing import Optional


def get_api_key(session: Optional[dict] = None) -> Optional[str]:
    """
    API Key를 우선순위에 따라 가져옵니다.
    
    우선순위:
    1. 사용자가 입력한 API Key (session)
    2. 환경 변수
    
    Args:
        session: FastAPI 세션 딕셔너리 (선택사항)
    
    Returns:
        str or None: API Key 문자열 또는 None
    """
    api_key = None
    
    # Priority 1: User-provided key (from session)
    if session and 'user_api_key' in session and session['user_api_key']:
        api_key = session['user_api_key']
    
    # Priority 2: Environment variable
    if not api_key:
        if 'OPENAI_API_KEY' in os.environ:
            api_key = os.environ['OPENAI_API_KEY']
    
    return api_key


def validate_api_key(api_key: str) -> tuple[bool, str]:
    """
    API Key 형식을 검증합니다.
    
    Args:
        api_key: 검증할 API Key
    
    Returns:
        tuple[bool, str]: (유효 여부, 오류 메시지)
    """
    if not api_key:
        return False, "API Key를 입력해주세요."
    
    api_key = api_key.strip()
    
    if not api_key.startswith('sk-'):
        return False, "올바른 OpenAI API Key 형식이 아닙니다. (sk-로 시작해야 합니다)"
    
    if len(api_key) < 20:
        return False, "API Key가 너무 짧습니다."
    
    return True, ""

