/**
 * 꿈해몽 페이지 스크립트
 */

// 꿈해몽 카테고리 데이터
const DREAM_CATEGORIES = {
    "동물": {
        "키워드": ["뱀", "개", "고양이", "호랑이", "사자", "말", "소", "돼지", "닭", "용", "봉황", "새", "물고기", "거북이", "곰", "원숭이", "쥐", "토끼", "양", "염소"],
        "아이콘": "🦁"
    },
    "자연": {
        "키워드": ["물", "바다", "불", "산", "하늘", "구름", "비", "눈", "태양", "달", "별", "번개", "천둥", "바람", "벼락", "폭풍", "지진"],
        "아이콘": "🌊"
    },
    "식물": {
        "키워드": ["나무", "꽃", "장미", "벚꽃", "소나무", "대나무", "과일", "사과", "복숭아", "포도", "수박", "버섯", "풀", "잎"],
        "아이콘": "🌺"
    },
    "건물/장소": {
        "키워드": ["집", "학교", "병원", "교회", "절", "무덤", "다리", "문", "창문", "계단", "지하", "옥상", "방", "부엌", "화장실"],
        "아이콘": "🏠"
    },
    "사람/관계": {
        "키워드": ["아기", "아이", "어머니", "아버지", "할머니", "할아버지", "형제", "자매", "친구", "선생님", "사장", "배우자", "이혼", "결혼", "장례"],
        "아이콘": "👥"
    },
    "음식": {
        "키워드": ["밥", "국", "고기", "생선", "치킨", "떡", "케이크", "쌀", "술", "차", "물", "과일", "채소"],
        "아이콘": "🍱"
    },
    "옷/장신구": {
        "키워드": ["옷", "신발", "가방", "반지", "목걸이", "귀걸이", "시계", "안경", "모자", "벨트", "손목시계"],
        "아이콘": "👔"
    },
    "교통수단": {
        "키워드": ["자동차", "버스", "지하철", "기차", "비행기", "배", "자전거", "오토바이", "택시"],
        "아이콘": "🚗"
    },
    "액체/물질": {
        "키워드": ["피", "오줌", "똥", "침", "눈물", "땀", "기름", "물", "술", "우유", "꿀"],
        "아이콘": "💧"
    },
    "도구/악기": {
        "키워드": ["칼", "가위", "망치", "톱", "톱니바퀴", "피아노", "기타", "북", "바이올린", "플루트"],
        "아이콘": "🔧"
    },
    "재물/금전": {
        "키워드": ["돈", "금", "은", "보석", "다이아몬드", "진주", "지갑", "은행", "계좌", "복권", "상금"],
        "아이콘": "💰"
    },
    "기타": {
        "키워드": ["시험", "시계", "거울", "사진", "책", "편지", "전화", "컴퓨터", "화면", "불", "등불", "촛불"],
        "아이콘": "✨"
    }
};

// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', function () {
    // 카테고리 표시
    renderCategories();

    // 쿼리 파라미터에서 키워드가 있으면 검색 (서버에서 전달된 설정 사용)
    if (window.DREAM_CONFIG && window.DREAM_CONFIG.initialKeyword) {
        searchDream(window.DREAM_CONFIG.initialKeyword);
    }

    // API Key 자동 저장 설정
    setupApiKeyAutoSave();

    // 검색 폼 제출 처리
    const searchForm = document.getElementById('dream-search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const searchInput = document.getElementById('dream-search-input');
            if (searchInput && searchInput.value.trim()) {
                searchDream(searchInput.value.trim());
            } else {
                alert('검색할 키워드를 입력해주세요.');
            }
        });
    }

    // 사주 데이터 업데이트 시 알림 (선택 사항)
    document.addEventListener('sajuUpdated', function (e) {
        if (e.detail.success) {
            console.log('사주 데이터가 업데이트되었습니다.');
        }
    });
});

// 카테고리 렌더링
function renderCategories() {
    const container = document.getElementById('dream-categories-container');
    if (!container) return;

    const categories = Object.entries(DREAM_CATEGORIES);
    let html = '';

    // 2개씩 그룹화
    for (let i = 0; i < categories.length; i += 2) {
        html += '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-bottom: 1rem;">';

        for (let j = 0; j < 2 && i + j < categories.length; j++) {
            const [categoryName, categoryData] = categories[i + j];
            const icon = categoryData.아이콘;
            const keywords = categoryData.키워드;

            // onclick 핸들러 대신 데이터 속성과 전역 검색 함수 사용 위임
            // 여기서는 간단하게 window.searchDream을 호출할 수 있도록 함
            const keywordLinks = keywords.map(keyword =>
                `<a href="#" onclick="searchDream('${keyword}'); return false;" style="color: #F9E79F; text-decoration: none; border-bottom: 1px solid rgba(249,231,159,0.6); cursor: pointer; margin-right: 0.5rem; display: inline-block;" onmouseover="this.style.color='#FFFFFF'; this.style.borderBottomColor='#FFFFFF'; this.style.textShadow='0 0 3px rgba(249,231,159,0.8)'" onmouseout="this.style.color='#F9E79F'; this.style.borderBottomColor='rgba(249,231,159,0.6)'; this.style.textShadow='none'">${keyword}</a>`
            ).join(' ');

            html += `
        <div style="padding: 1rem; background: rgba(212,175,55,0.1); border-radius: 8px; border: 1px solid rgba(212,175,55,0.3);">
            <div style="font-size: 1.1em; font-weight: bold; color: #D4AF37; margin-bottom: 0.5rem;">
                ${icon} ${categoryName}
            </div>
            <div style="color: #E2E8F0; font-size: 0.95em; line-height: 2.0; word-wrap: break-word;">
                ${keywordLinks}
            </div>
        </div>
    `;
        }

        html += '</div>';
    }

    container.innerHTML = html;
}

// 꿈해몽 검색 (전역 함수로 노출하여 HTML inline onclick에서 호출 가능하게 함)
window.searchDream = async function (keyword) {
    if (!keyword || !keyword.trim()) {
        alert('검색할 키워드를 입력해주세요.');
        return;
    }

    const resultContainer = document.getElementById('dream-result-container');
    const searchInput = document.getElementById('dream-search-input');

    if (searchInput) {
        searchInput.value = keyword;
    }

    if (!resultContainer) return;

    // 로딩 표시
    showSpinner('dream-result-container', '꿈해몽을 분석하고 있습니다...');
    resultContainer.style.display = 'block';

    try {
        // API Key는 입력 필드에서 직접 가져옴 (저장하지 않음)
        const apiKeyInput = document.getElementById('api-key-input');
        const currentApiKey = apiKeyInput ? apiKeyInput.value.trim() : '';

        const data = await apiRequest('/api/dream', 'POST', {
            keyword: keyword.trim(),
            api_key: currentApiKey  // API Key를 요청 본문에 포함
        });

        if (data.success) {
            renderDreamResult(data.data);
        } else {
            showError('dream-result-container', data.detail || '꿈해몽 검색 중 오류가 발생했습니다.');
        }
    } catch (error) {
        console.error('꿈해몽 검색 오류:', error);
        showError('dream-result-container', '네트워크 오류가 발생했습니다.');
    }
};

// 꿈해몽 길흉도 시각화 함수
function renderDreamFortuneBar(level) {
    let score = 5; // 보통
    let color = "#f39c12";
    let percentage = 50;

    if (level === "길몽") {
        score = 9;
        color = "#2ecc71";
        percentage = 90;
    } else if (level === "흉몽") {
        score = 3;
        color = "#e74c3c";
        percentage = 30;
    }

    return `
<div style="margin-top: 1rem;">
    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
        <span style="color: var(--text-primary); font-weight: 500;">길흉도</span>
        <span style="color: ${color}; font-weight: bold; font-size: 1.1em;">${score}/10</span>
    </div>
    <div style="width: 100%; height: 8px; background: rgba(255, 255, 255, 0.1); border-radius: 4px; overflow: hidden;">
        <div style="width: ${percentage}%; height: 100%; background: ${color}; transition: width 0.3s ease;"></div>
    </div>
</div>
`;
}

// 꿈해몽 키워드 추출 함수
function getDreamKeywords(keyword, category, fortuneLevel) {
    const keywords = [];

    // 카테고리 기반 키워드
    const categoryKeywords = {
        "동물": ["변화", "본능", "직관"],
        "자연": ["감정", "순환", "성장"],
        "인물": ["관계", "소통", "인연"],
        "장소": ["상태", "환경", "안정"],
        "물건": ["도구", "수단", "자원"],
        "행동": ["의지", "변화", "결정"]
    };

    if (category && categoryKeywords[category]) {
        keywords.push(...categoryKeywords[category].slice(0, 2));
    }

    // 길흉 기반 키워드
    if (fortuneLevel === "길몽") {
        keywords.push("기회");
    } else if (fortuneLevel === "흉몽") {
        keywords.push("주의");
    } else {
        keywords.push("균형");
    }

    // 키워드가 3개 미만이면 기본 키워드 추가
    const defaultKeywords = ["해석", "성찰", "조언", "인식", "반영"];
    while (keywords.length < 3) {
        const candidate = defaultKeywords[Math.floor(Math.random() * defaultKeywords.length)];
        if (!keywords.includes(candidate)) {
            keywords.push(candidate);
        }
    }

    return keywords.slice(0, 3);
}

// 관련 조언 확장 함수
function expandDreamAdvice(dreamMeaning, category) {
    let advice = dreamMeaning.조언 || "꿈의 전체적인 맥락과 자신의 현재 상황을 종합적으로 고려하여 해석하세요.";

    // 카테고리별 추가 조언
    const categoryAdvice = {
        "동물": "동물 꿈은 본능과 직관을 나타냅니다. 내면의 목소리에 귀 기울이고, 직관을 신뢰하세요.",
        "자연": "자연 요소는 감정과 순환을 상징합니다. 감정의 흐름을 잘 관리하고, 자연스러운 변화를 받아들이세요.",
        "인물": "인물 꿈은 관계와 소통을 의미합니다. 주변 사람들과의 관계를 점검하고, 소통을 늘려보세요.",
        "장소": "장소 꿈은 현재 상태나 환경을 반영합니다. 자신의 환경을 객관적으로 살펴보고, 필요시 개선을 고려하세요.",
        "물건": "물건 꿈은 수단이나 도구를 나타냅니다. 현재 소유하거나 필요로 하는 것에 대해 생각해보세요.",
        "행동": "행동 꿈은 의지나 변화를 의미합니다. 적극적인 의지를 가지고, 필요한 변화를 추진하세요."
    };

    if (category && categoryAdvice[category]) {
        advice += ` ${categoryAdvice[category]}`;
    }

    return advice;
}

// 행동 체크리스트 생성 함수
function getDreamChecklist(keyword, fortuneLevel, category) {
    const checklist = {
        reflection: [],
        action: [],
        attention: []
    };

    if (fortuneLevel === "길몽") {
        checklist.reflection = [
            "이 꿈이 나타내는 기회를 현실에서 찾아보기",
            "긍정적인 변화를 위해 준비하기",
            "주변 환경에서 긍정적인 신호 찾기"
        ];
        checklist.action = [
            "새로운 시작을 위한 계획 세우기",
            "기회를 활용할 수 있는 능력 개발하기",
            "긍정적인 사람들과의 관계 강화하기"
        ];
        checklist.attention = [
            "기회를 놓치지 않도록 주의 깊게 관찰하기",
            "과도한 낙관보다는 신중한 판단하기",
            "현재 상황을 객관적으로 평가하기"
        ];
    } else if (fortuneLevel === "흉몽") {
        checklist.reflection = [
            "꿈이 경고하는 위험 요소 파악하기",
            "현재 상황에서 문제점 찾아보기",
            "과거 경험을 통해 해결책 모색하기"
        ];
        checklist.action = [
            "예방 조치를 취하고 신중하게 행동하기",
            "주변 사람들에게 조언 구하기",
            "필요한 경우 전문가의 도움 받기"
        ];
        checklist.attention = [
            "건강과 안전에 특히 주의하기",
            "중요한 결정은 신중하게 내리기",
            "감정적으로 대응하지 않고 차근차근 처리하기"
        ];
    } else {
        checklist.reflection = [
            "꿈의 의미를 깊이 있게 성찰하기",
            "현재 상황을 객관적으로 평가하기",
            "자신의 감정과 생각 정리하기"
        ];
        checklist.action = [
            "꾸준한 노력과 계획으로 목표 달성하기",
            "현재 상황에서 개선할 수 있는 부분 찾기",
            "균형 잡힌 생활 습관 유지하기"
        ];
        checklist.attention = [
            "무리한 변화보다는 점진적 발전 추구하기",
            "긍정적인 마음가짐 유지하기",
            "주변 환경의 변화를 주의 깊게 관찰하기"
        ];
    }

    return checklist;
}

function renderDreamResult(data) {
    const resultContainer = document.getElementById('dream-result-container');
    if (!resultContainer) return;

    const keyword = data.keyword;
    const category = data.category || '';
    const dreamMeaning = data.dream_meaning;
    const fortuneLevel = dreamMeaning.길흉 || '보통';

    // 키워드 생성
    const keywords = getDreamKeywords(keyword, category, fortuneLevel);

    // 조언 확장
    const expandedAdvice = expandDreamAdvice(dreamMeaning, category);

    // 체크리스트 생성
    const checklist = getDreamChecklist(keyword, fortuneLevel, category);

    // 공유 버튼 표시
    const shareDiv = document.getElementById('dream-share');
    if (shareDiv) shareDiv.style.display = 'block';

    // 공유 데이터 설정
    const shareTitle = `"${keyword}" 꿈해몽 결과 - 운세담`;
    const shareDesc = `꿈의 의미: ${dreamMeaning.기본의미.substring(0, 50)}... 결과: ${fortuneLevel}`;

    window.currentShareData = {
        title: shareTitle,
        description: shareDesc,
        url: window.location.href,
        text: `${shareTitle}\n${shareDesc}\n\n지금 바로 확인해보세요!`
    };

    let html = `
<div class="section-header" style="margin-top: 0;">
    <span>🔮</span> "${keyword}" 꿈해몽
</div>

<!-- 카테고리 및 키워드 -->
${category ? `
<div style="padding: 1rem; background: rgba(212,175,55,0.05); border-radius: 8px; margin-top: 1.5rem; margin-bottom: 1rem;">
    <div style="display: flex; align-items: center; gap: 1rem; flex-wrap: wrap;">
        ${category ? `<span style="padding: 0.4rem 0.8rem; background: rgba(212,175,55,0.2); color: var(--gold-primary); border-radius: 12px; font-size: 0.9em; font-weight: 500;">📂 ${category}</span>` : ''}
        ${keywords.map((kw, idx) => {
        const colors = ['#3498db', '#2ecc71', '#f1c40f'];
        return `<span style="padding: 0.4rem 0.8rem; background: ${colors[idx % colors.length]}; color: white; border-radius: 12px; font-size: 0.9em; font-weight: bold;">${kw}</span>`;
    }).join('')}
    </div>
</div>
` : ''}

<!-- 기본 해몽 -->
<h3 style="color: var(--gold-primary); margin-top: 1.5rem; margin-bottom: 1rem;">📖 기본 해몽</h3>
<div style="padding: 1.5rem; background: linear-gradient(135deg, rgba(212,175,55,0.15) 0%, rgba(212,175,55,0.05) 100%); border-radius: 12px; border-left: 5px solid #D4AF37; margin-bottom: 1.5rem;">
    <div style="color: #E2E8F0; line-height: 1.9; font-size: 1.05em; margin-bottom: 1rem;">
        ${dreamMeaning.기본의미 || '해몽 정보를 생성하는 중입니다.'}
    </div>
`;

    // 상세 해몽이 있는 경우 추가 표시
    if (dreamMeaning.상세해몽) {
        html += `
    <div style="padding: 1rem; background: rgba(212,175,55,0.08); border-radius: 8px; margin-top: 1rem;">
        <div style="color: #D4AF37; font-weight: 600; font-size: 0.95em; margin-bottom: 0.5rem;">✨ 상세 해석</div>
        <div style="color: #E2E8F0; line-height: 1.8; font-size: 0.98em;">${dreamMeaning.상세해몽}</div>
    </div>
`;
    }

    // 상징의미가 있는 경우 추가
    if (dreamMeaning.상징의미) {
        html += `
    <div style="padding: 1rem; background: rgba(212,175,55,0.08); border-radius: 8px; margin-top: 1rem;">
        <div style="color: #D4AF37; font-weight: 600; font-size: 0.95em; margin-bottom: 0.5rem;">🎭 상징적 의미</div>
        <div style="color: #E2E8F0; line-height: 1.8; font-size: 0.98em;">${dreamMeaning.상징의미}</div>
    </div>
`;
    }

    // 심리 해석이 있는 경우 추가
    if (dreamMeaning.심리해석) {
        html += `
    <div style="padding: 1rem; background: rgba(212,175,55,0.08); border-radius: 8px; margin-top: 1rem;">
        <div style="color: #D4AF37; font-weight: 600; font-size: 0.95em; margin-bottom: 0.5rem;">🧠 심리적 해석</div>
        <div style="color: #E2E8F0; line-height: 1.8; font-size: 0.98em;">${dreamMeaning.심리해석}</div>
    </div>
`;
    } else {
        // 기본 심리 해석 추가
        html += `
    <div style="padding: 1rem; background: rgba(212,175,55,0.08); border-radius: 8px; margin-top: 1rem;">
        <div style="color: #D4AF37; font-weight: 600; font-size: 0.95em; margin-bottom: 0.5rem;">🧠 심리적 해석</div>
        <div style="color: #E2E8F0; line-height: 1.8; font-size: 0.98em;">이 꿈은 현재 당신의 무의식이나 감정 상태를 반영할 수 있습니다. 꿈 속에서 느낀 감정과 상황을 기억하고, 일상생활에서 유사한 패턴이나 감정을 찾아보세요.</div>
    </div>
`;
    }

    html += '</div>';

    // 길흉 판단 (시각화 강화)
    if (dreamMeaning.길흉) {
        const fortuneLevel = dreamMeaning.길흉;
        const fortuneColor = fortuneLevel === "길몽" ? "#2ecc71" : fortuneLevel === "흉몽" ? "#e74c3c" : "#f39c12";
        const fortuneEmoji = fortuneLevel === '길몽' ? '✅' : fortuneLevel === '흉몽' ? '⚠️' : 'ℹ️';

        html += `
    <h3 style="color: var(--gold-primary); margin-top: 2rem; margin-bottom: 1rem;">🎯 길흉 판단</h3>
    <div style="padding: 1.5rem; background: linear-gradient(135deg, ${fortuneLevel === "길몽" ? "rgba(46, 204, 113, 0.1)" : fortuneLevel === "흉몽" ? "rgba(231, 76, 60, 0.1)" : "rgba(243, 156, 18, 0.1)"} 0%, rgba(212,175,55,0.05) 100%); border-radius: 12px; border-left: 5px solid ${fortuneColor}; margin-bottom: 1.5rem; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.8rem;">
            <span style="font-size: 1.5em;">${fortuneEmoji}</span>
            <div style="font-weight: bold; color: ${fortuneColor}; font-size: 1.2em;">
                ${fortuneLevel}
            </div>
        </div>
        ${renderDreamFortuneBar(fortuneLevel)}
        <div style="color: #E2E8F0; line-height: 1.8; margin-top: 1rem;">${dreamMeaning.길흉설명 || '상황과 감정에 따라 의미가 달라질 수 있습니다.'}</div>
    </div>
`;
    }

    // 상황별 해몽 (강화)
    if (dreamMeaning.상황별해몽 && Object.keys(dreamMeaning.상황별해몽).length > 0) {
        html += `
    <h3 style="color: var(--gold-primary); margin-top: 2rem; margin-bottom: 1rem;">🔍 상황별 해몽</h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
`;

        for (const [situation, meaning] of Object.entries(dreamMeaning.상황별해몽)) {
            html += `
        <div style="padding: 1rem; background: rgba(212,175,55,0.05); border-left: 3px solid var(--gold-primary); border-radius: 6px;">
            <strong style="color: #D4AF37; display: block; margin-bottom: 0.5rem;">${situation}</strong>
            <span style="color: #E2E8F0; line-height: 1.6; font-size: 0.95em;">${meaning}</span>
        </div>
    `;
        }

        html += '</div>';
    } else {
        // 기본 상황별 해몽 추가
        html += `
    <h3 style="color: var(--gold-primary); margin-top: 2rem; margin-bottom: 1rem;">🔍 상황별 해몽</h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
        <div style="padding: 1rem; background: rgba(212,175,55,0.05); border-left: 3px solid var(--gold-primary); border-radius: 6px;">
            <strong style="color: #D4AF37; display: block; margin-bottom: 0.5rem;">명확하고 선명한 꿈</strong>
            <span style="color: #E2E8F0; line-height: 1.6; font-size: 0.95em;">꿈의 내용이 선명하면 무의식의 강한 메시지일 수 있습니다. 특히 주의 깊게 살펴보세요.</span>
        </div>
        <div style="padding: 1rem; background: rgba(212,175,55,0.05); border-left: 3px solid var(--gold-primary); border-radius: 6px;">
            <strong style="color: #D4AF37; display: block; margin-bottom: 0.5rem;">반복되는 꿈</strong>
            <span style="color: #E2E8F0; line-height: 1.6; font-size: 0.95em;">같은 꿈을 반복해서 꾸면 중요한 메시지이거나 해결해야 할 문제가 있다는 신호일 수 있습니다.</span>
        </div>
        <div style="padding: 1rem; background: rgba(212,175,55,0.05); border-left: 3px solid var(--gold-primary); border-radius: 6px;">
            <strong style="color: #D4AF37; display: block; margin-bottom: 0.5rem;">강한 감정을 느낀 꿈</strong>
            <span style="color: #E2E8F0; line-height: 1.6; font-size: 0.95em;">꿈 속에서 느낀 감정(기쁨, 두려움, 슬픔 등)이 실제 상황을 반영할 수 있습니다.</span>
        </div>
    </div>
`;
    }

    // 관련 조언 (강화)
    html += `
<h3 style="color: var(--gold-primary); margin-top: 2rem; margin-bottom: 1rem;">💡 실용적 조언</h3>
<div style="padding: 1.5rem; background: linear-gradient(135deg, rgba(52,152,219,0.1) 0%, rgba(52,152,219,0.05) 100%); border-radius: 12px; border-left: 5px solid #3498db; margin-bottom: 2rem;">
    <div style="color: #E2E8F0; line-height: 1.9; font-size: 1.05em;">
        ${expandedAdvice}
    </div>
</div>
`;

    // 행동 체크리스트
    html += `
<h3 style="color: var(--gold-primary); margin-top: 2rem; margin-bottom: 1rem;">✅ 실천 체크리스트</h3>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
    <div style="padding: 1rem; background: rgba(212,175,55,0.03); border-radius: 6px;">
        <h5 style="color: var(--gold-primary); margin-bottom: 0.8rem; font-size: 1em;">
            🤔 성찰
        </h5>
        <ul style="list-style: none; padding: 0; margin: 0;">
            ${checklist.reflection.map(item => `
                <li style="padding: 0.5rem 0; color: var(--text-primary); font-size: 0.9em; line-height: 1.6; border-bottom: 1px solid rgba(255, 255, 255, 0.1);">
                    <span style="color: var(--gold-primary); margin-right: 0.5rem;">☐</span> ${item}
                </li>
            `).join('')}
        </ul>
    </div>
    <div style="padding: 1rem; background: rgba(212,175,55,0.03); border-radius: 6px;">
        <h5 style="color: var(--gold-primary); margin-bottom: 0.8rem; font-size: 1em;">
            🎯 실행
        </h5>
        <ul style="list-style: none; padding: 0; margin: 0;">
            ${checklist.action.map(item => `
                <li style="padding: 0.5rem 0; color: var(--text-primary); font-size: 0.9em; line-height: 1.6; border-bottom: 1px solid rgba(255, 255, 255, 0.1);">
                    <span style="color: var(--gold-primary); margin-right: 0.5rem;">☐</span> ${item}
                </li>
            `).join('')}
        </ul>
    </div>
    <div style="padding: 1rem; background: rgba(212,175,55,0.03); border-radius: 6px;">
        <h5 style="color: var(--gold-primary); margin-bottom: 0.8rem; font-size: 1em;">
            ⚠️ 주의사항
        </h5>
        <ul style="list-style: none; padding: 0; margin: 0;">
            ${checklist.attention.map(item => `
                <li style="padding: 0.5rem 0; color: var(--text-primary); font-size: 0.9em; line-height: 1.6; border-bottom: 1px solid rgba(255, 255, 255, 0.1);">
                    <span style="color: var(--gold-primary); margin-right: 0.5rem;">☐</span> ${item}
                </li>
            `).join('')}
        </ul>
    </div>
</div>
`;

    resultContainer.innerHTML = html;
}

// API Key 입력 처리 (저장하지 않고 입력값만 사용)
function setupApiKeyAutoSave() {
    let apiKeyDebounceTimer;
    const apiKeyInput = document.getElementById('api-key-input');
    const statusDiv = document.getElementById('api-key-status');

    apiKeyInput?.addEventListener('input', function () {
        clearTimeout(apiKeyDebounceTimer);
        const apiKey = this.value.trim();

        apiKeyDebounceTimer = setTimeout(() => {
            if (apiKey) {
                if (statusDiv) {
                    statusDiv.textContent = '✅ API Key가 입력되었습니다. 꿈해몽을 다시 검색하면 AI 분석이 실행됩니다.';
                    statusDiv.style.color = '#86EFAC';
                    statusDiv.style.display = 'block';
                }

                // API Key 입력 후, 검색 결과가 이미 표시되어 있으면 다시 검색
                const resultContainer = document.getElementById('dream-result-container');
                const searchInput = document.getElementById('dream-search-input');
                if (resultContainer && resultContainer.style.display !== 'none' && searchInput && searchInput.value.trim()) {
                    setTimeout(() => {
                        searchDream(searchInput.value.trim());
                    }, 500);
                }
            } else {
                if (statusDiv) {
                    statusDiv.style.display = 'none';
                }
            }
        }, 1000);
    });
}
