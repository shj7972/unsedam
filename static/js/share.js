/**
 * 공유 기능 유틸리티
 * Kakao, Twitter, Link Copy, Native Share 지원
 */

const ShareUtils = {
    kakaoInitialized: false,

    /**
     * 카카오 SDK 초기화
     * @param {string} apiKey - 카카오 JavaScript 키
     */
    initKakao: function (apiKey) {
        if (window.Kakao && !window.Kakao.isInitialized() && apiKey) {
            try {
                window.Kakao.init(apiKey);
                this.kakaoInitialized = true;
                console.log('Kakao SDK Initialized');
            } catch (error) {
                console.error('Kakao SDK Init Error:', error);
            }
        }
    },

    /**
     * 카카오톡 공유하기
     * @param {object} params - 공유 파라미터
     */
    shareKakao: function (params) {
        if (!this.kakaoInitialized) {
            alert('카카오톡 공유 기능을 사용할 수 없습니다. (API Key 미설정)');
            return;
        }

        const { title, description, imageUrl, linkUrl } = params;

        window.Kakao.Share.sendDefault({
            objectType: 'feed',
            content: {
                title: title,
                description: description,
                imageUrl: imageUrl || (window.location.origin + '/static/images/og-image.png'),
                link: {
                    mobileWebUrl: linkUrl,
                    webUrl: linkUrl,
                },
            },
            buttons: [
                {
                    title: '결과 확인하기',
                    link: {
                        mobileWebUrl: linkUrl,
                        webUrl: linkUrl,
                    },
                },
            ],
        });
    },

    /**
     * 트위터(X) 공유하기
     * @param {string} text - 공유할 텍스트
     * @param {string} url - 공유할 URL
     */
    shareTwitter: function (text, url) {
        const intentUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`;
        window.open(intentUrl, '_blank', 'width=550,height=420');
    },

    /**
     * 링크 복사하기
     * @param {string} url - 복사할 URL
     */
    copyLink: async function (url) {
        try {
            await navigator.clipboard.writeText(url);
            ShareUtils.showToast('🔗 링크가 복사되었습니다!', 'success');
        } catch (err) {
            console.error('링크 복사 실패:', err);
            // fallback: execCommand
            try {
                const ta = document.createElement('textarea');
                ta.value = url;
                ta.style.position = 'fixed';
                ta.style.opacity = '0';
                document.body.appendChild(ta);
                ta.select();
                document.execCommand('copy');
                document.body.removeChild(ta);
                ShareUtils.showToast('🔗 링크가 복사되었습니다!', 'success');
            } catch (e) {
                ShareUtils.showToast('링크 복사에 실패했습니다.', 'error');
            }
        }
    },

    /**
     * 토스트 메시지 표시
     * @param {string} message - 표시할 메시지
     * @param {string} type - 'success' | 'error'
     */
    showToast: function (message, type) {
        // 기존 토스트 제거
        const existing = document.getElementById('share-utils-toast');
        if (existing) existing.remove();

        const toast = document.createElement('div');
        toast.id = 'share-utils-toast';
        toast.textContent = message;
        const bg = type === 'error' ? 'rgba(231,76,60,0.9)' : 'rgba(39,174,96,0.9)';
        toast.style.cssText = [
            'position:fixed', 'bottom:2rem', 'left:50%', 'transform:translateX(-50%)',
            `background:${bg}`, 'color:#fff', 'padding:0.75rem 1.5rem',
            'border-radius:30px', 'font-size:0.95rem', 'font-weight:500',
            'z-index:9999', 'box-shadow:0 4px 20px rgba(0,0,0,0.3)',
            'pointer-events:none', 'transition:opacity 0.4s'
        ].join(';');
        document.body.appendChild(toast);

        // 2.5초 후 페이드아웃
        setTimeout(() => { toast.style.opacity = '0'; }, 2000);
        setTimeout(() => { if (toast.parentNode) toast.remove(); }, 2500);
    },

    /**
     * 네이티브 공유 (모바일)
     * @param {object} data - 공유 데이터 { title, text, url }
     */
    shareNative: async function (data) {
        if (navigator.share) {
            try {
                await navigator.share(data);
                console.log('공유 성공');
            } catch (err) {
                console.log('공유 취소 또는 실패:', err);
            }
        } else {
            // 네이티브 공유 미지원 시 링크 복사로 대체
            this.copyLink(data.url);
        }
    }
};

// 페이지 로드 시 카카오 키 초기화 (플레이스홀더)
// 페이지 로드 시 카카오 키 초기화 (플레이스홀더)
document.addEventListener('DOMContentLoaded', () => {
    const KAKAO_JS_KEY = 'ee2a88cbac8ba33e6ec6bcdd9cb57c14';

    // 키가 설정되어 있을 때만 초기화 수행
    if (KAKAO_JS_KEY) {
        ShareUtils.initKakao(KAKAO_JS_KEY);
    }

    // 초기화 실패 시 (키 미설정 등) 버튼 숨기기
    // 동적으로 추가되는 버튼도 처리하기 위해 함수로 분리하고 MutationObserver 사용
    function hideKakaoButtons() {
        if (!ShareUtils.kakaoInitialized) {
            const kakaoBtns = document.querySelectorAll('.share-btn.kakao');
            kakaoBtns.forEach(btn => {
                // 이미 숨겨진 경우는 건너뜀 (성능 최적화)
                if (btn.style.display !== 'none') {
                    btn.style.display = 'none';
                }
            });
        }
    }

    // 1. 초기 로드 시 실행
    hideKakaoButtons();

    // 2. 동적으로 추가되는 요소 감지 (MutationObserver)
    if (!ShareUtils.kakaoInitialized) {
        const observer = new MutationObserver((mutations) => {
            let shouldCheck = false;
            for (const mutation of mutations) {
                if (mutation.addedNodes.length > 0) {
                    shouldCheck = true;
                    break;
                }
            }
            if (shouldCheck) {
                hideKakaoButtons();
            }
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }
});
