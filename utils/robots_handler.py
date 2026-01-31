"""
robots.txt를 루트 경로에서 직접 제공하는 커스텀 핸들러
Streamlit 서버에 Tornado 핸들러를 추가합니다.
"""
import os
from tornado.web import RequestHandler
from utils.seo import generate_robots_txt


class RobotsTxtHandler(RequestHandler):
    """robots.txt를 직접 제공하는 Tornado 핸들러"""
    
    def get(self):
        """GET 요청 처리 - robots.txt 내용 직접 제공"""
        # 정적 파일을 우선적으로 읽기 시도
        static_robots_path = "static/robots.txt"
        robots_content = None
        
        if os.path.exists(static_robots_path):
            try:
                with open(static_robots_path, 'r', encoding='utf-8') as f:
                    robots_content = f.read().strip()
            except Exception:
                pass
        
        # 정적 파일이 없거나 읽기 실패 시 동적으로 생성
        if not robots_content:
            robots_content = generate_robots_txt()
        
        # Content-Type 설정
        self.set_header("Content-Type", "text/plain; charset=utf-8")
        self.set_header("Cache-Control", "public, max-age=3600")
        self.write(robots_content)


def add_robots_txt_handler():
    """
    Streamlit 서버에 robots.txt 핸들러를 추가합니다.
    Streamlit의 Runtime이 초기화된 후 호출해야 합니다.
    여러 번 호출해도 안전합니다 (중복 체크 포함).
    """
    try:
        # Streamlit Runtime에서 서버 인스턴스 가져오기
        from streamlit.runtime import Runtime
        runtime = Runtime.instance()
        
        if not runtime:
            return False
        
        # 서버 인스턴스 가져오기
        server = getattr(runtime, '_server', None)
        if not server:
            return False
        
        # Tornado 앱 가져오기
        app = getattr(server, '_app', None)
        if not app:
            return False
        
        # 이미 핸들러가 추가되었는지 확인
        robots_handler_exists = False
        for host_pattern, handler_list in app.handlers:
            for handler_tuple in handler_list:
                if len(handler_tuple) >= 2:
                    pattern = handler_tuple[0]
                    handler_class = handler_tuple[1]
                    # 패턴이나 핸들러 클래스로 확인
                    if (isinstance(pattern, str) and 'robots' in pattern) or \
                       (handler_class == RobotsTxtHandler):
                        robots_handler_exists = True
                        break
            if robots_handler_exists:
                break
        
        # 핸들러가 없으면 추가
        if not robots_handler_exists:
            # base URL path 가져오기
            from streamlit import config
            base = config.get_option("server.baseUrlPath") or ""
            
            # base path를 고려한 패턴 생성
            import re
            if base and base != "/":
                # base path가 있으면 escape하고 robots.txt 추가
                base_escaped = re.escape(base.rstrip('/'))
                pattern = rf"{base_escaped}/robots\.txt"
            else:
                pattern = r"/robots\.txt"
            
            # 핸들러를 맨 앞에 추가 (최우선 순위)
            # handlers는 (host_pattern, [(pattern, handler, kwargs), ...]) 형태
            app.handlers.insert(0, (r".*", [(pattern, RobotsTxtHandler)]))
            return True
        
        return True  # 이미 존재하면 성공으로 간주
    except Exception as e:
        # 에러 발생 시 무시 (로깅만)
        import logging
        logging.warning(f"Failed to add robots.txt handler: {e}")
        return False

