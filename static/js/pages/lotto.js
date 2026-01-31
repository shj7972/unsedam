/**
 * 로또 번호 추천 페이지 스크립트
 */

// 생성 방식 설명
const methodDescriptions = {
    "완전 랜덤": "1~45번 중 완전히 무작위로 6개의 번호를 선택합니다.",
    "홀짝 균형형": "홀수와 짝수를 균형있게 배분하여 생성합니다. (예: 홀수 3개, 짝수 3개)",
    "고저 분포형": "낮은 번호(1-15), 중간 번호(16-30), 높은 번호(31-45)를 골고루 배분합니다.",
    "연속 번호 포함형": "연속된 번호 1쌍을 포함하여 생성합니다.",
    "합계 조절형": "번호 합계를 100-200 범위로 조절하여 생성합니다.",
    "시간 기반": "현재 시간과 날짜를 기반으로 번호를 생성합니다.",
    "생년월일 기반": "입력하신 생년월일의 숫자를 활용하여 생성합니다.",
    "사주 기반": "사주 정보의 간지를 숫자로 변환하여 생성합니다.",
    "행운 숫자 조합": "생일 합산으로 계산한 행운 숫자와 조합하여 생성합니다.",
    "생일 합산 기반": "생년월일의 각 자리수를 합산하여 생성합니다.",
    "사주 오행 기반": "사주의 오행(목화토금수)을 숫자 범위로 변환하여 생성합니다."
};

// 사용자 정보가 필요한 방식
const userInfoRequiredMethods = ["생년월일 기반", "사주 기반", "행운 숫자 조합", "생일 합산 기반", "사주 오행 기반"];

document.addEventListener('DOMContentLoaded', function () {
    // 초기 설명 표시
    const methodSelect = document.getElementById('lotto-method');
    if (methodSelect) {
        methodSelect.addEventListener('change', updateMethodDescription);

        // 초기 로드 시 설명 업데이트
        updateMethodDescription.call(methodSelect);
    }

    // 세트 수 슬라이더
    const numSetsSlider = document.getElementById('num-sets');
    const numSetsValue = document.getElementById('num-sets-value');
    if (numSetsSlider && numSetsValue) {
        numSetsSlider.addEventListener('input', function () {
            numSetsValue.textContent = this.value + '세트';
        });
    }

    // 로또 번호 생성 버튼
    const generateBtn = document.getElementById('generate-lotto-btn');
    if (generateBtn) {
        generateBtn.addEventListener('click', generateLottoNumbers);
    }

    // 다시 생성 버튼 위임 (동적 생성 요소)
    document.addEventListener('click', function (e) {
        if (e.target && e.target.id === 'regenerate-lotto-btn') {
            const resultContainer = document.getElementById('lotto-result-container');
            if (resultContainer) {
                resultContainer.style.display = 'none';
                resultContainer.innerHTML = '';
            }
        }
    });

    // 사주 데이터 업데이트 시 알림 처리
    document.addEventListener('sajuUpdated', function (e) {
        if (e.detail.success) {
            console.log('사주 데이터를 바탕으로 로또 번호를 생성할 준비가 되었습니다.');
            // 사용자 정보 필요 경고 업데이트 로직 실행
            if (methodSelect) {
                methodSelect.dispatchEvent(new Event('change'));
            }

            // 전역 설정 업데이트 (만약 있다면)
            if (window.LOTTO_CONFIG) {
                window.LOTTO_CONFIG.hasUserInfo = true;
            }
        }
    });
});

/**
 * 생성 방식 설명 및 경고 메시지 업데이트
 */
function updateMethodDescription() {
    const method = this.value;
    const descriptionDiv = document.getElementById('method-description');
    const warningDiv = document.getElementById('user-info-warning');

    if (descriptionDiv) {
        descriptionDiv.textContent = methodDescriptions[method] || '';
    }

    // 사용자 정보 필요 여부 확인
    // LOTTO_CONFIG는 HTML에서 정의됨
    const hasUserInfo = (window.LOTTO_CONFIG && window.LOTTO_CONFIG.hasUserInfo) || false;

    if (warningDiv) {
        if (userInfoRequiredMethods.includes(method) && !hasUserInfo) {
            warningDiv.style.display = 'block';
        } else {
            warningDiv.style.display = 'none';
        }
    }
}

/**
 * 로또 번호 생성 요청
 */
async function generateLottoNumbers() {
    const methodSelect = document.getElementById('lotto-method');
    const numSetsSlider = document.getElementById('num-sets');
    const resultContainer = document.getElementById('lotto-result-container');

    if (!resultContainer || !methodSelect || !numSetsSlider) return;

    const method = methodSelect.value;
    const numSets = parseInt(numSetsSlider.value);

    // 로딩 표시
    showSpinner('lotto-result-container', '로또 번호를 생성하고 있습니다...');
    resultContainer.style.display = 'block';

    try {
        const data = await apiRequest('/api/lotto', 'POST', {
            method: method,
            num_sets: numSets
        });

        if (data.success) {
            renderLottoResult(data.data);
        } else {
            showError('lotto-result-container', data.detail || '로또 번호 생성 중 오류가 발생했습니다.');
        }
    } catch (error) {
        console.error('로또 번호 생성 오류:', error);
        showError('lotto-result-container', '네트워크 오류가 발생했습니다.');
    }
}

/**
 * 로또 결과 렌더링
 */
function renderLottoResult(result) {
    const resultContainer = document.getElementById('lotto-result-container');
    if (!resultContainer) return;

    const method = result.method;
    const sets = result.sets;
    const generatedAt = new Date(result.generated_at);
    const statistics = result.statistics;



    // 공유 버튼 표시
    const shareDiv = document.getElementById('lotto-share');
    if (shareDiv) shareDiv.style.display = 'block';

    // 공유 데이터 설정
    const shareTitle = `이번 주 로또 행운 번호 추천 - 운세담`;
    const shareDesc = `생성 방식: ${method}. ${sets.length}세트의 행운 번호를 확인해보세요!`;

    window.currentShareData = {
        title: shareTitle,
        description: shareDesc,
        url: window.location.href,
        text: `${shareTitle}\n${shareDesc}\n\n지금 바로 확인해보세요!`
    };

    let html = `
    <div class="section-header" style="margin-top: 0;">
        <span>🎱</span> 추천 번호 (총 ${sets.length}세트)
    </div>
    <p style="color: #A0AEC0; margin-bottom: 1.5rem;">
        생성 방식: <strong style="color: #D4AF37;">${method}</strong> | 
        생성 시간: ${generatedAt.toLocaleString('ko-KR')}
    </p>
`;

    // 각 세트 표시
    for (let i = 0; i < sets.length; i++) {
        const lottoSet = sets[i];
        const numbers = lottoSet.numbers;
        const explanation = lottoSet.explanation || '';
        const setNum = lottoSet.set_index || (i + 1);

        html += `<h3 style="color: var(--gold-primary); margin-top: 2rem; margin-bottom: 1rem;">📋 ${setNum}번 세트</h3>`;

        // 번호 표시
        const numberDivs = numbers.map(num => {
            const colorInfo = getNumberColor(num);
            return `<div style="display: inline-block; width: 60px; height: 60px; line-height: 60px; text-align: center; background: ${colorInfo.bg}; color: ${colorInfo.color}; font-weight: bold; font-size: 1.3em; border-radius: 50%; margin: 0.3rem; box-shadow: 0 4px 6px ${colorInfo.shadow};">${num}</div>`;
        }).join('');

        html += `
        <div style="text-align: center; margin: 1.5rem 0; padding: 1.5rem; background: rgba(212,175,55,0.1); border-radius: 12px;">
            ${numberDivs}
        </div>
    `;

        if (explanation) {
            html += `<p style="color: #A0AEC0; font-size: 0.9em; text-align: center; margin-bottom: 2rem;">${explanation}</p>`;
        }

        if (i < sets.length - 1) {
            html += '<hr style="margin: 2rem 0; border: none; border-top: 1px solid rgba(212,175,55,0.3);">';
        }
    }

    // 통계 정보
    html += '<hr style="margin: 2rem 0; border: none; border-top: 1px solid rgba(212,175,55,0.3);">';
    html += '<h3 style="color: var(--gold-primary); margin-top: 2rem; margin-bottom: 1rem;">📊 번호 통계</h3>';

    html += '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem;">';

    // 가장 많이 나온 번호
    html += '<div>';
    html += '<strong style="color: #D4AF37;">가장 많이 나온 번호 TOP 6:</strong>';
    for (const [num, count] of statistics.most_common) {
        html += `<div style="padding: 0.5rem; margin: 0.3rem 0; background: rgba(212,175,55,0.2); border-radius: 6px;"><strong>${num}번</strong> (${count}회)</div>`;
    }
    html += '</div>';

    // 번호 분포
    html += '<div>';
    html += '<strong style="color: #D4AF37;">번호 분포:</strong>';
    for (const [rangeName, count] of Object.entries(statistics.ranges)) {
        const percentage = (count / statistics.total_numbers) * 100;
        html += `<div style="padding: 0.5rem; margin: 0.3rem 0; background: rgba(212,175,55,0.2); border-radius: 6px;"><strong>${rangeName}</strong>: ${count}개 (${percentage.toFixed(1)}%)</div>`;
    }
    html += '</div>';

    html += '</div>';

    // 안내 메시지
    html += `
    <hr style="margin: 2rem 0; border: none; border-top: 1px solid rgba(212,175,55,0.3);">
    <div style="padding: 1rem; background: rgba(212,175,55,0.1); border-radius: 8px; margin-top: 1rem;">
        <p style="color: #E2E8F0; line-height: 1.8; font-size: 0.9em;">
            ⚠️ <strong>면책 고지:</strong> 본 서비스는 오락 목적으로 제공되는 참고용 번호 추천 기능입니다. 
            실제 로또 당첨 확률은 모든 번호 조합에 대해 동일하며, 본 서비스가 제공하는 번호가 더 높은 당첨 확률을 보장하지 않습니다. 
            과도한 투자는 금지되며, 책임 있는 게임을 권장합니다.
        </p>
    </div>
`;

    // 다시 생성 버튼
    html += `
    <button id="regenerate-lotto-btn" style="width: 100%; padding: 1rem; background: var(--gold-gradient); border: none; border-radius: 8px; color: var(--bg-dark); font-weight: bold; cursor: pointer; font-size: 1rem; margin-top: 1.5rem;">
        🔄 다시 생성
    </button>
`;

    resultContainer.innerHTML = html;
}

/**
 * 번호 색상 반환
 */
function getNumberColor(num) {
    if (1 <= num && num <= 10) {
        return {
            bg: 'linear-gradient(135deg, #FBC02D 0%, #FDD835 100%)',
            shadow: 'rgba(251, 192, 45, 0.4)',
            color: '#1A202C'
        };
    } else if (11 <= num && num <= 20) {
        return {
            bg: 'linear-gradient(135deg, #1976D2 0%, #2196F3 100%)',
            shadow: 'rgba(25, 118, 210, 0.4)',
            color: '#FFFFFF'
        };
    } else if (21 <= num && num <= 30) {
        return {
            bg: 'linear-gradient(135deg, #D32F2F 0%, #F44336 100%)',
            shadow: 'rgba(211, 47, 47, 0.4)',
            color: '#FFFFFF'
        };
    } else if (31 <= num && num <= 40) {
        return {
            bg: 'linear-gradient(135deg, #616161 0%, #757575 100%)',
            shadow: 'rgba(97, 97, 97, 0.4)',
            color: '#FFFFFF'
        };
    } else {
        return {
            bg: 'linear-gradient(135deg, #388E3C 0%, #4CAF50 100%)',
            shadow: 'rgba(56, 142, 60, 0.4)',
            color: '#FFFFFF'
        };
    }
}
