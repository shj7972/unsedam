"""
보안 유틸리티
입력 검증, XSS 방지, 에러 처리 등을 제공합니다.
"""
import re
import html
from typing import Any


def sanitize_input(text: str, max_length: int = 1000) -> str:
    """
    사용자 입력을 검증하고 정리합니다.
    
    Args:
        text: 검증할 텍스트
        max_length: 최대 길이
        
    Returns:
        str: 검증된 텍스트
    """
    if not isinstance(text, str):
        return ""
    
    # 길이 제한
    if len(text) > max_length:
        text = text[:max_length]
    
    # 앞뒤 공백 제거
    text = text.strip()
    
    # 제어 문자 제거 (탭, 개행 등은 허용)
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)
    
    return text


def sanitize_html(text: str) -> str:
    """
    HTML 특수 문자를 이스케이프하여 XSS를 방지합니다.
    
    Args:
        text: 이스케이프할 텍스트
        
    Returns:
        str: 이스케이프된 텍스트
    """
    if not isinstance(text, str):
        return ""
    
    return html.escape(text, quote=True)


def validate_name(name: str) -> tuple[bool, str]:
    """
    이름 입력을 검증합니다.
    
    Args:
        name: 검증할 이름
        
    Returns:
        tuple[bool, str]: (유효성, 에러 메시지)
    """
    if not name:
        return False, "이름을 입력해주세요."
    
    name = sanitize_input(name, max_length=50)
    
    if len(name) < 1:
        return False, "이름을 입력해주세요."
    
    if len(name) > 50:
        return False, "이름은 50자 이하여야 합니다."
    
    # 특수 문자 제한 (한글, 영문, 숫자, 공백, 일부 특수문자만 허용)
    if not re.match(r'^[가-힣a-zA-Z0-9\s\-\.]+$', name):
        return False, "이름은 한글, 영문, 숫자만 사용할 수 있습니다."
    
    return True, ""


def validate_api_key(api_key: str) -> tuple[bool, str]:
    """
    API 키 형식을 검증합니다.
    
    Args:
        api_key: 검증할 API 키
        
    Returns:
        tuple[bool, str]: (유효성, 에러 메시지)
    """
    if not api_key:
        return True, ""  # API 키는 선택사항
    
    api_key = sanitize_input(api_key, max_length=200)
    
    # OpenAI API 키 형식 검증 (sk-로 시작)
    if api_key.startswith('sk-'):
        if len(api_key) < 20 or len(api_key) > 200:
            return False, "API 키 형식이 올바르지 않습니다."
        return True, ""
    
    # Google API 키 형식 검증
    if len(api_key) < 20 or len(api_key) > 200:
        return False, "API 키 형식이 올바르지 않습니다."
    
    return True, ""


def safe_error_message(error: Exception, show_details: bool = False) -> str:
    """
    안전한 에러 메시지를 반환합니다.
    프로덕션 환경에서는 상세한 에러 정보를 숨깁니다.
    
    Args:
        error: 발생한 예외
        show_details: 상세 정보 표시 여부 (개발 환경용)
        
    Returns:
        str: 안전한 에러 메시지
    """
    if show_details:
        return f"오류가 발생했습니다: {str(error)}"
    
    # 프로덕션 환경에서는 일반적인 메시지만 반환
    error_type = type(error).__name__
    
    # 일반적인 에러 메시지 매핑
    generic_messages = {
        'ValueError': '입력값이 올바르지 않습니다.',
        'TypeError': '데이터 형식이 올바르지 않습니다.',
        'KeyError': '필요한 정보가 없습니다.',
        'AttributeError': '요청을 처리할 수 없습니다.',
        'ConnectionError': '연결에 실패했습니다. 잠시 후 다시 시도해주세요.',
        'TimeoutError': '요청 시간이 초과되었습니다. 잠시 후 다시 시도해주세요.',
    }
    
    return generic_messages.get(error_type, '오류가 발생했습니다. 잠시 후 다시 시도해주세요.')


def is_production() -> bool:
    """
    프로덕션 환경인지 확인합니다.
    
    Returns:
        bool: 프로덕션 환경 여부
    """
    import os
    # Heroku 환경 변수 확인
    return 'DYNO' in os.environ or os.environ.get('ENVIRONMENT') == 'production'

