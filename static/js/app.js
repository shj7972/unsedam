/**
 * 운세담 JavaScript 유틸리티
 * 전역 함수 및 헬퍼 함수들
 */

// AJAX 요청 헬퍼
async function apiRequest(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'same-origin' // 세션 쿠키 포함
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(url, options);
        return await response.json();
    } catch (error) {
        console.error('API Request Error:', error);
        throw error;
    }
}

// 로딩 인디케이터 표시
function showSpinner(elementId, message = '처리 중...') {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `
            <div style="text-align: center; padding: 2rem;">
                <div class="spinner" style="display: inline-block; width: 40px; height: 40px; border: 4px solid var(--border-gold); border-top-color: var(--gold-primary); border-radius: 50%; animation: spin 1s linear infinite;"></div>
                <p style="margin-top: 1rem; color: var(--text-muted);">${message}</p>
            </div>
        `;
    }
}

// 에러 메시지 표시
function showError(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `
            <div style="padding: 1rem; background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 8px; color: #FCA5A5;">
                ⚠️ ${message}
            </div>
        `;
        element.style.display = 'block';
    }
}

// 성공 메시지 표시
function showSuccess(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `
            <div style="padding: 1rem; background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 8px; color: #86EFAC;">
                ✅ ${message}
            </div>
        `;
        element.style.display = 'block';
    }
}

// 스피너 애니메이션 CSS 추가
if (!document.getElementById('spinner-style')) {
    const style = document.createElement('style');
    style.id = 'spinner-style';
    style.textContent = `
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    `;
    document.head.appendChild(style);
}

// 세션 데이터를 localStorage에 저장
function saveSessionDataToLocalStorage(data) {
    if (data && data.session_data) {
        const sessionDataWithTimestamp = {
            ...data.session_data,
            _timestamp: Date.now() // 타임스탬프 추가
        };
        localStorage.setItem('user_session_data', JSON.stringify(sessionDataWithTimestamp));
    }
}

// localStorage에서 세션 데이터 읽기
function getSessionDataFromLocalStorage() {
    const storedData = localStorage.getItem('user_session_data');
    if (storedData) {
        try {
            return JSON.parse(storedData);
        } catch (e) {
            console.error('localStorage 데이터 파싱 오류:', e);
            return null;
        }
    }
    return null;
}

// 폼에 세션 데이터 채우기 (localStorage 값이 있으면 항상 사용)
function fillFormFromLocalStorage(formId, hasSessionData = false) {
    const form = document.getElementById(formId);
    if (!form) return;

    const sessionData = getSessionDataFromLocalStorage();
    if (!sessionData) return;

    const nameInput = form.querySelector('[name="name"]');
    const birthDateInput = form.querySelector('[name="birth_date"]');
    const birthTimeInput = form.querySelector('[name="birth_time"]');
    const genderSelect = form.querySelector('[name="gender"]');
    const isLunarCheckbox = form.querySelector('[name="is_lunar"]');

    // localStorage 값이 있으면 항상 사용 (세션 값보다 우선)
    // 폼 값이 비어있거나, localStorage 값이 다르면 localStorage 값으로 업데이트
    if (nameInput && sessionData.user_name) {
        if (!nameInput.value || nameInput.value !== sessionData.user_name) {
            nameInput.value = sessionData.user_name;
        }
    }
    if (birthDateInput && sessionData.birth_date) {
        if (!birthDateInput.value || birthDateInput.value !== sessionData.birth_date) {
            birthDateInput.value = sessionData.birth_date;
        }
    }
    if (birthTimeInput && sessionData.birth_time) {
        if (!birthTimeInput.value || birthTimeInput.value !== sessionData.birth_time) {
            birthTimeInput.value = sessionData.birth_time;
        }
    }
    if (genderSelect && sessionData.user_gender) {
        if (!genderSelect.value || genderSelect.value !== sessionData.user_gender) {
            genderSelect.value = sessionData.user_gender;
        }
    }
    if (isLunarCheckbox && sessionData.is_lunar !== undefined) {
        if (isLunarCheckbox.checked !== sessionData.is_lunar) {
            isLunarCheckbox.checked = sessionData.is_lunar;
        }
    }
}

// 사주 입력 폼 설정 (공통 로직)
function setupInputForm(formId = 'input-form') {
    const form = document.getElementById(formId);
    if (!form) return;

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const submitBtn = this.querySelector('button[type="submit"]');
        if (submitBtn && submitBtn.disabled) return;

        const formData = new FormData(this);
        const errorDiv = document.getElementById('form-error');

        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.textContent = '처리 중...';
        }
        if (errorDiv) {
            errorDiv.style.display = 'none';
        }

        try {
            const response = await fetch('/api/calculate', {
                method: 'POST',
                body: formData,
                credentials: 'same-origin'
            });

            const data = await response.json();

            if (response.ok && data.success) {
                // 세션 데이터를 localStorage에 저장
                if (data.data && data.data.session_data) {
                    saveSessionDataToLocalStorage(data.data);
                } else {
                    const sessionData = {
                        user_name: formData.get('name') || '',
                        user_gender: formData.get('gender') || '',
                        birth_date: formData.get('birth_date') || '',
                        birth_time: formData.get('birth_time') || '',
                        is_lunar: formData.get('is_lunar') === 'on' || formData.get('is_lunar') === 'true',
                        _timestamp: Date.now()
                    };
                    localStorage.setItem('user_session_data', JSON.stringify(sessionData));
                }

                // 성공 이벤트 발생
                const event = new CustomEvent('sajuUpdated', {
                    detail: { success: true, data: data.data }
                });
                document.dispatchEvent(event);

                // 버튼만 복원하고 알림은 생략 (각 페이지에서 처리)
            } else {
                if (errorDiv) {
                    errorDiv.textContent = data.detail || '오류가 발생했습니다.';
                    errorDiv.style.display = 'block';
                }
            }
        } catch (error) {
            console.error('Error:', error);
            if (errorDiv) {
                errorDiv.textContent = '네트워크 오류가 발생했습니다.';
                errorDiv.style.display = 'block';
            }
        } finally {
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.textContent = '결과보기';
            }
        }
    });

    // 초기 로드 시 값 채우기
    fillFormFromLocalStorage(formId);
}

// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', function () {
    console.log('운세담 앱이 로드되었습니다.');
    setupInputForm('input-form');
});

