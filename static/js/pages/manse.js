/**
 * manse.js
 * 만세력 페이지 전용 JavaScript
 */

let currentDate = new Date();

document.addEventListener('DOMContentLoaded', function () {
    // 초기 날짜 설정
    if (window.MANSE_CONFIG) {
        currentDate.setFullYear(window.MANSE_CONFIG.initialYear);
        currentDate.setMonth(window.MANSE_CONFIG.initialMonth - 1); // Month is 0-indexed in JS
        currentDate.setDate(1);
    }

    // 초기 달력 로드
    loadCalendar();

    // 이벤트 리스너 설정
    setupEventListeners();
});

function setupEventListeners() {
    // 이전 달 버튼
    document.getElementById('prev-month-btn')?.addEventListener('click', function () {
        currentDate.setMonth(currentDate.getMonth() - 1);
        loadCalendar();
    });

    // 다음 달 버튼
    document.getElementById('next-month-btn')?.addEventListener('click', function () {
        currentDate.setMonth(currentDate.getMonth() + 1);
        loadCalendar();
    });

    // 오늘 버튼
    document.getElementById('today-btn')?.addEventListener('click', function () {
        currentDate = new Date();
        loadCalendar();
    });

    // 옵션 체크박스
    document.getElementById('show-lunar')?.addEventListener('change', loadCalendar);
    document.getElementById('show-ganji')?.addEventListener('change', loadCalendar);
}

async function loadCalendar() {
    const calendarContainer = document.getElementById('calendar-container');
    const yearMonthDisplay = document.getElementById('year-month-display');

    if (!calendarContainer) return;

    // 로딩 표시
    calendarContainer.innerHTML = `
        <div style="text-align: center; padding: 3rem;">
            <div class="spinner" style="display: inline-block; width: 40px; height: 40px; border: 4px solid var(--border-gold); border-top-color: var(--gold-primary); border-radius: 50%; animation: spin 1s linear infinite;"></div>
            <p style="margin-top: 1rem; color: var(--text-muted);">만세력 데이터를 불러오는 중...</p>
        </div>
    `;

    const year = currentDate.getFullYear();
    const month = currentDate.getMonth() + 1;
    const showLunar = document.getElementById('show-lunar')?.checked ?? true;
    const showGanji = document.getElementById('show-ganji')?.checked ?? true;

    try {
        const response = await apiRequest('/api/manse', 'POST', {
            year: year,
            month: month,
            show_lunar: showLunar,
            show_ganji: showGanji
        });

        if (response.success) {
            renderCalendar(response.data);

            // 헤더 업데이트
            if (yearMonthDisplay) {
                yearMonthDisplay.textContent = `${year}.${String(month).padStart(2, '0')}`;
            }

            // 공유 버튼 표시 및 데이터 설정
            const shareDiv = document.getElementById('manse-share');
            if (shareDiv) shareDiv.style.display = 'block';

            const shareTitle = `${year}년 ${month}월 만세력 - 운세담`;
            const shareDesc = `음력, 간지 정보가 포함된 ${year}년 ${month}월 만세력을 확인해보세요.`;

            window.currentShareData = {
                title: shareTitle,
                description: shareDesc,
                url: window.location.href,
                text: `${shareTitle}\n${shareDesc}\n\n지금 바로 확인해보세요!`
            };
        } else {
            calendarContainer.innerHTML = `<div class="error-message">데이터를 불러오지 못했습니다.</div>`;
        }
    } catch (error) {
        console.error('만세력 로드 오류:', error);
        calendarContainer.innerHTML = `<div class="error-message">오류가 발생했습니다.</div>`;
    }
}

function renderCalendar(data) {
    const calendarContainer = document.getElementById('calendar-container');
    if (!calendarContainer) return;

    const { weekdays, calendar_data, year_month_display } = data;

    let html = `
        <div style="text-align: center; color: var(--gold-primary); margin-bottom: 1rem; font-size: 0.9em;">
            ${year_month_display}
        </div>
        <table style="width: 100%; border-collapse: collapse; table-layout: fixed;">
            <thead>
                <tr>
                    ${weekdays.map((day, index) => {
        let color = 'var(--text-primary)';
        if (index === 0) color = '#e74c3c'; // 일요일
        else if (index === 6) color = '#3498db'; // 토요일
        return `<th style="padding: 0.8rem 0.2rem; text-align: center; color: ${color}; border-bottom: 1px solid rgba(255,255,255,0.1); font-weight: bold;">${day}</th>`;
    }).join('')}
                </tr>
            </thead>
            <tbody>
    `;

    calendar_data.forEach(week => {
        html += '<tr>';
        week.forEach((day, index) => {
            if (!day) {
                html += '<td style="padding: 0.5rem; height: 100px;"></td>';
            } else {
                const dayColor = index === 0 ? '#e74c3c' : (index === 6 ? '#3498db' : 'var(--text-primary)');
                const bgColor = day.is_today ? 'rgba(212, 175, 55, 0.2)' : (day.is_secondary_month ? 'rgba(255, 255, 255, 0.03)' : 'transparent');
                const border = day.is_today ? '2px solid var(--gold-primary)' : '1px solid rgba(255, 255, 255, 0.05)';

                html += `
                    <td style="padding: 0.5rem; height: 100px; vertical-align: top; border: ${border}; background: ${bgColor}; border-radius: 6px;">
                        <div style="display: flex; flex-direction: column; height: 100%; justify-content: space-between;">
                            <div style="text-align: center; font-weight: bold; font-size: 1.1em; color: ${dayColor}; margin-bottom: 0.3rem;">
                                ${day.day}
                            </div>
                            <div style="font-size: 0.75em; color: #A0AEC0; text-align: center; line-height: 1.4;">
                                ${day.lunar_display ? `<div style="color: #95a5a6;">${day.lunar_display}</div>` : ''}
                                ${day.ganji_display ? `<div style="color: var(--gold-secondary); margin-top: 2px;">${day.ganji_display}</div>` : ''}
                            </div>
                        </div>
                    </td>
                `;
            }
        });
        html += '</tr>';
    });

    html += `
            </tbody>
        </table>
    `;

    calendarContainer.innerHTML = html;
}
