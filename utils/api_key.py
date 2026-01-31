"""
API Key 관리 유틸리티
OpenAI API Key를 안전하게 관리하고 가져오는 기능 제공
"""
import os
import streamlit as st


def get_api_key():
    """
    API Key를 우선순위에 따라 가져옵니다.
    
    우선순위:
    1. 사용자가 입력한 API Key (session_state)
    2. Streamlit secrets.toml
    3. 환경 변수
    
    Returns:
        str or None: API Key 문자열 또는 None
    """
    api_key = None
    
    # Priority 1: User-provided key (from input field)
    if 'user_api_key' in st.session_state and st.session_state['user_api_key']:
        api_key = st.session_state['user_api_key']
    
    # Priority 2: Server secrets (for deployment with shared key)
    if not api_key:
        try:
            # Check if secrets.toml exists and load it
            if hasattr(st, 'secrets'):
                # Try to load secrets.toml if it exists (returns False if no secrets file)
                secrets_loaded = False
                if hasattr(st.secrets, 'load_if_toml_exists'):
                    secrets_loaded = st.secrets.load_if_toml_exists()
                
                # Only access secrets if they were successfully loaded
                if secrets_loaded:
                    if hasattr(st.secrets, 'openai') and 'api_key' in st.secrets.openai:
                        secrets_key = st.secrets.openai.api_key
                        if secrets_key and secrets_key != "your-api-key-here":
                            api_key = secrets_key
        except Exception:
            # If secrets.toml doesn't exist or can't be loaded, just skip
            # This is expected in Heroku if secrets are not configured
            pass
    
    # Priority 3: Environment variable
    if not api_key:
        if 'OPENAI_API_KEY' in os.environ:
            api_key = os.environ['OPENAI_API_KEY']
    
    return api_key


def render_api_key_input():
    """
    API Key 입력 필드를 렌더링합니다.
    """
    st.markdown("<hr style='margin: 1rem 0; border: none; border-top: 1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 0.85em; color: #A0AEC0; margin-bottom: 0.5rem;'>OpenAI API Key (선택사항)</div>", unsafe_allow_html=True)
    
    # Check if API key exists in secrets first
    has_secrets_key = False
    try:
        if hasattr(st, 'secrets'):
            # Try to load secrets.toml if it exists (returns False if no secrets file)
            secrets_loaded = False
            if hasattr(st.secrets, 'load_if_toml_exists'):
                secrets_loaded = st.secrets.load_if_toml_exists()
            
            # Only access secrets if they were successfully loaded
            if secrets_loaded:
                if hasattr(st.secrets, 'openai') and 'api_key' in st.secrets.openai:
                    has_secrets_key = bool(st.secrets.openai.api_key and st.secrets.openai.api_key != "your-api-key-here")
    except Exception:
        # If secrets.toml doesn't exist or can't be loaded, just skip
        # This is expected in Heroku if secrets are not configured
        pass
    
    if has_secrets_key:
        st.info("ℹ️ 서버에 API Key가 설정되어 있습니다. 아래에서 다른 Key를 입력할 수 있습니다.")
        use_custom_key = st.checkbox("직접 입력한 API Key 사용", key="use_custom_api_key")
    else:
        use_custom_key = True
    
    user_api_key = None
    if use_custom_key:
        api_key_placeholder = "sk-proj-..." if not has_secrets_key else "비워두면 서버 설정 사용"
        user_api_key_input = st.text_input(
            "API Key",
            value=st.session_state.get('user_api_key', ''),
            type="password",
            placeholder=api_key_placeholder,
            key="api_key_input",
            help="OpenAI API Key를 입력하세요. https://platform.openai.com/api-keys 에서 발급받을 수 있습니다."
        )
        if user_api_key_input:
            # API 키 검증 및 정리
            user_api_key = sanitize_input(user_api_key_input.strip(), max_length=200)
            api_key_valid, api_key_error = validate_api_key(user_api_key)
            if api_key_valid:
                st.session_state['user_api_key'] = user_api_key
            else:
                st.warning(api_key_error)
                if 'user_api_key' in st.session_state:
                    del st.session_state['user_api_key']
        elif 'user_api_key' in st.session_state:
            # Clear if user removed the key
            del st.session_state['user_api_key']
    elif 'user_api_key' in st.session_state:
        del st.session_state['user_api_key']

