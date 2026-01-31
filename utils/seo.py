"""
SEO 최적화 유틸리티
메타 태그, 구조화된 데이터, sitemap 등을 관리합니다.
"""
import streamlit as st
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
        "keywords": "AI 사주, 사주명리, 사주분석, 무료사주, 사주보기"
    },
    'tojeong': {
        "title": "토정비결 | 운세담",
        "description": "2026년 무료 토정비결 서비스. 토정 이지함의 토정비결을 바탕으로 한 정확한 운세 분석을 제공합니다.",
        "keywords": "토정비결, 토정비결 무료, 2026 토정비결, 토정 이지함, 운세"
    },
    'byeoljari': {
        "title": "별자리운세 | 운세담",
        "description": "12궁 별자리 운세 분석 서비스. 오늘의 운세, 주간 운세, 월간 운세를 확인하세요.",
        "keywords": "별자리운세, 12궁, 별자리, 운세, 별자리 오늘의 운세"
    },
    'gonghap': {
        "title": "궁합 | 운세담",
        "description": "사주 궁합 분석 서비스. 연인, 부부, 친구 간의 궁합을 정확하게 분석해드립니다.",
        "keywords": "궁합, 사주궁합, 연인궁합, 부부궁합, 궁합보기"
    },
    'dream': {
        "title": "꿈해몽 | 운세담",
        "description": "무료 꿈해몽 서비스. 꿈의 의미를 AI로 분석하고 상세한 해몽을 제공합니다.",
        "keywords": "꿈해몽, 꿈풀이, 꿈해석, 무료꿈해몽, 꿈의 의미"
    },
    'tarot': {
        "title": "타로 | 운세담",
        "description": "타로 카드 뽑기 및 해석 서비스. 원카드, 3장, 켈틱 크로스 등 다양한 스프레드로 운세를 확인하세요.",
        "keywords": "타로, 타로카드, 타로뽑기, 타로해석, 무료타로"
    },
    'lotto': {
        "title": "로또 | 운세담",
        "description": "로또 번호 생성 및 운세 분석 서비스. 사주를 기반으로 한 로또 번호 추천을 제공합니다.",
        "keywords": "로또, 로또번호, 로또번호생성, 로또번호추천, 사주로또"
    },
    'manse': {
        "title": "만세력 | 운세담",
        "description": "만세력 조회 서비스. 생년월일시를 입력하여 정확한 만세력을 확인하세요.",
        "keywords": "만세력, 만세력보기, 사주만세력, 무료만세력"
    }
}


def get_page_meta(page_key: str) -> dict:
    """
    페이지별 메타 정보를 반환합니다.
    
    Args:
        page_key: 페이지 키
        
    Returns:
        dict: 메타 정보 딕셔너리
    """
    default_meta = {
        "title": f"{SITE_INFO['name']} | AI 프리미엄 사주",
        "description": SITE_INFO['description'],
        "keywords": SITE_INFO['keywords']
    }
    
    return PAGE_META.get(page_key, default_meta)


def render_seo_meta_tags(page_key: str = 'ai_saju'):
    """
    SEO 메타 태그를 렌더링합니다.
    
    Args:
        page_key: 현재 페이지 키
    """
    meta = get_page_meta(page_key)
    site_url = SITE_INFO['url']
    page_url = f"{site_url}/?page={page_key}" if page_key != 'ai_saju' else site_url
    
    # Open Graph 이미지 URL (실제 이미지가 있으면 추가)
    og_image = f"{site_url}/og-image.png"  # 나중에 추가 가능
    
    # JavaScript를 사용하여 head 섹션에 메타 태그 동적 삽입
    # Streamlit은 st.markdown으로 head에 직접 접근할 수 없으므로 JavaScript 사용
    # 네이버 봇이 JavaScript를 실행하지 않을 수 있으므로, 즉시 실행 함수로 최대한 빨리 삽입
    seo_script = f"""
    <script>
    (function() {{
        // 즉시 실행하여 검색엔진 봇이 가능한 한 빨리 메타 태그를 찾을 수 있도록
        // 기존 메타 태그 제거 (중복 방지)
        const existingNaverTags = document.querySelectorAll('meta[name="naver-site-verification"]');
        existingNaverTags.forEach(tag => tag.remove());
        const existingDaumTags = document.querySelectorAll('meta[name="daum-site-verification"]');
        existingDaumTags.forEach(tag => tag.remove());
        
        // Naver Webmaster Tools 메타 태그 추가 (최우선)
        const naverMeta = document.createElement('meta');
        naverMeta.name = 'naver-site-verification';
        naverMeta.content = '43dc017823a9c46420c367e23e62c5a3f0e0d99c';
        document.head.insertBefore(naverMeta, document.head.firstChild);
        
        // Daum Webmaster Tools 메타 태그 추가
        const daumMeta = document.createElement('meta');
        daumMeta.name = 'daum-site-verification';
        daumMeta.content = '42858a913fc55df5e2dc9371b659ac47ba48ec6bb332cb43322f947d6e1ac763:1hrba1lpzexyTL25MI8THg==';
        document.head.insertBefore(daumMeta, naverMeta.nextSibling);
        
        // Primary Meta Tags
        const metaTags = [
            {{name: 'title', content: '{meta['title']}'}},
            {{name: 'description', content: '{meta['description']}'}},
            {{name: 'keywords', content: '{meta['keywords']}'}},
            {{name: 'author', content: '{SITE_INFO['author']}'}},
            {{name: 'language', content: '{SITE_INFO['language']}'}},
            {{name: 'robots', content: 'index, follow'}},
            {{name: 'googlebot', content: 'index, follow'}}
        ];
        
        metaTags.forEach(tag => {{
            const existing = document.querySelector(`meta[name="${{tag.name}}"]`);
            if (!existing) {{
                const meta = document.createElement('meta');
                meta.name = tag.name;
                meta.content = tag.content;
                document.head.appendChild(meta);
            }}
        }});
        
        // Open Graph Tags
        const ogTags = [
            {{property: 'og:type', content: 'website'}},
            {{property: 'og:url', content: '{page_url}'}},
            {{property: 'og:title', content: '{meta['title']}'}},
            {{property: 'og:description', content: '{meta['description']}'}},
            {{property: 'og:site_name', content: '{SITE_INFO['name']}'}},
            {{property: 'og:locale', content: 'ko_KR'}}
        ];
        
        ogTags.forEach(tag => {{
            const existing = document.querySelector(`meta[property="${{tag.property}}"]`);
            if (!existing) {{
                const meta = document.createElement('meta');
                meta.setAttribute('property', tag.property);
                meta.content = tag.content;
                document.head.appendChild(meta);
            }}
        }});
        
        // Twitter Card Tags
        const twitterTags = [
            {{property: 'twitter:card', content: 'summary_large_image'}},
            {{property: 'twitter:url', content: '{page_url}'}},
            {{property: 'twitter:title', content: '{meta['title']}'}},
            {{property: 'twitter:description', content: '{meta['description']}'}}
        ];
        
        twitterTags.forEach(tag => {{
            const existing = document.querySelector(`meta[property="${{tag.property}}"]`);
            if (!existing) {{
                const meta = document.createElement('meta');
                meta.setAttribute('property', tag.property);
                meta.content = tag.content;
                document.head.appendChild(meta);
            }}
        }});
        
        // Canonical URL
        let canonical = document.querySelector('link[rel="canonical"]');
        if (!canonical) {{
            canonical = document.createElement('link');
            canonical.rel = 'canonical';
            canonical.href = '{page_url}';
            document.head.appendChild(canonical);
        }} else {{
            canonical.href = '{page_url}';
        }}
    }})();
    </script>
    """
    
    st.markdown(seo_script, unsafe_allow_html=True)


def render_structured_data(page_key: str = 'ai_saju', enabled: bool = True):
    """
    구조화된 데이터 (JSON-LD)를 렌더링합니다.
    
    Args:
        page_key: 현재 페이지 키
        enabled: 구조화된 데이터 활성화 여부 (기본값: True)
    """
    # 구조화된 데이터가 비활성화된 경우 아무것도 렌더링하지 않음
    if not enabled:
        return
    meta = get_page_meta(page_key)
    site_url = SITE_INFO['url']
    page_url = f"{site_url}/?page={page_key}" if page_key != 'ai_saju' else site_url
    
    # WebSite 구조화된 데이터
    website_schema = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE_INFO['name'],
        "url": site_url,
        "description": SITE_INFO['description'],
        "inLanguage": "ko-KR",
        "potentialAction": {
            "@type": "SearchAction",
            "target": {
                "@type": "EntryPoint",
                "urlTemplate": f"{site_url}/?page={{search_term_string}}"
            },
            "query-input": "required name=search_term_string"
        }
    }
    
    # Organization 구조화된 데이터
    organization_schema = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": SITE_INFO['name'],
        "url": site_url,
        "description": SITE_INFO['description'],
        "logo": f"{site_url}/logo.png"  # 나중에 추가 가능
    }
    
    # WebPage 구조화된 데이터
    webpage_schema = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": meta['title'],
        "description": meta['description'],
        "url": page_url,
        "inLanguage": "ko-KR",
        "isPartOf": {
            "@type": "WebSite",
            "name": SITE_INFO['name'],
            "url": site_url
        }
    }
    
    # Service 구조화된 데이터 (운세 서비스)
    service_schema = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": meta['title'],
        "description": meta['description'],
        "provider": {
            "@type": "Organization",
            "name": SITE_INFO['name']
        },
        "serviceType": "운세 분석 서비스",
        "areaServed": "KR"
    }
    
    import json
    
    # JSON 데이터를 문자열로 변환
    website_json = json.dumps(website_schema, ensure_ascii=False)
    organization_json = json.dumps(organization_schema, ensure_ascii=False)
    webpage_json = json.dumps(webpage_schema, ensure_ascii=False)
    service_json = json.dumps(service_schema, ensure_ascii=False)
    
    # JavaScript를 사용하여 동적으로 스크립트 태그를 head에 삽입
    # Streamlit의 제한으로 인해 body에 스크립트를 넣고 head로 이동시킴
    structured_data_script = f"""
    <div style="display: none;">
    <script>
    (function() {{
        if (document.head) {{
            // WebSite 스키마
            var script1 = document.createElement('script');
            script1.type = 'application/ld+json';
            script1.textContent = {json.dumps(website_json)};
            document.head.appendChild(script1);
            
            // Organization 스키마
            var script2 = document.createElement('script');
            script2.type = 'application/ld+json';
            script2.textContent = {json.dumps(organization_json)};
            document.head.appendChild(script2);
            
            // WebPage 스키마
            var script3 = document.createElement('script');
            script3.type = 'application/ld+json';
            script3.textContent = {json.dumps(webpage_json)};
            document.head.appendChild(script3);
            
            // Service 스키마
            var script4 = document.createElement('script');
            script4.type = 'application/ld+json';
            script4.textContent = {json.dumps(service_json)};
            document.head.appendChild(script4);
        }}
    }})();
    </script>
    </div>
    """
    
    st.markdown(structured_data_script, unsafe_allow_html=True)


def generate_sitemap() -> str:
    """
    sitemap.xml을 생성합니다.
    
    Returns:
        str: sitemap.xml 내용
    """
    site_url = SITE_INFO['url']
    
    sitemap_lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    sitemap_lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    # 메인 페이지
    sitemap_lines.append('  <url>')
    sitemap_lines.append(f'    <loc>{site_url}/</loc>')
    sitemap_lines.append('    <lastmod>2025-01-01</lastmod>')
    sitemap_lines.append('    <changefreq>daily</changefreq>')
    sitemap_lines.append('    <priority>1.0</priority>')
    sitemap_lines.append('  </url>')
    
    # 각 페이지
    for page_key, page_name in PAGE_NAMES.items():
        page_url = f"{site_url}/?page={page_key}" if page_key != 'ai_saju' else site_url
        sitemap_lines.append('  <url>')
        sitemap_lines.append(f'    <loc>{page_url}</loc>')
        sitemap_lines.append('    <lastmod>2025-01-01</lastmod>')
        sitemap_lines.append('    <changefreq>weekly</changefreq>')
        sitemap_lines.append('    <priority>0.8</priority>')
        sitemap_lines.append('  </url>')
    
    sitemap_lines.append('</urlset>')
    
    return '\n'.join(sitemap_lines)


def generate_robots_txt() -> str:
    """
    robots.txt를 생성합니다.
    네이버 검색로봇을 명시적으로 허용합니다.
    
    Returns:
        str: robots.txt 내용
    """
    site_url = SITE_INFO['url']
    
    robots_content = f"""# 네이버 검색로봇 명시적 허용
User-agent: Yeti
Allow: /
Disallow: /static/

User-agent: NaverBot
Allow: /
Disallow: /static/

# 기타 모든 봇
User-agent: *
Allow: /
Disallow: /static/

Sitemap: {site_url}/?page=sitemap

#DaumWebMasterTool:42858a913fc55df5e2dc9371b659ac47ba48ec6bb332cb43322f947d6e1ac763:1hrba1lpzexyTL25MI8THg==
"""
    return robots_content

