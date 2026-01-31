"""
만세력 계산 유틸리티
전통 한글 달력 (음력, 간지 포함) 표시
"""
import calendar
import saju_logic
from korean_lunar_calendar import KoreanLunarCalendar
import ephem
from datetime import datetime, timedelta, date


# 한글 발음 매핑
GANJI_PRONUNCIATION = {
    "甲": "갑", "乙": "을", "丙": "병", "丁": "정", "戊": "무",
    "己": "기", "庚": "경", "辛": "신", "壬": "임", "癸": "계",
    "子": "자", "丑": "축", "寅": "인", "卯": "묘", "辰": "진",
    "巳": "사", "午": "오", "未": "미", "申": "신", "酉": "유",
    "戌": "술", "亥": "해"
}


def find_ipchun_date(year):
    """
    해당 년도의 입춘 날짜를 찾습니다.
    입춘은 태양의 황경이 315도가 되는 날입니다.
    
    Args:
        year: 년도
        
    Returns:
        datetime: 입춘 날짜 (시간 포함, 한국시간 기준)
    """
    # 입춘은 보통 2월 4일경이므로 그 근처에서 검색
    target_longitude = 315  # 입춘
    
    obs = ephem.Observer()
    obs.lat = '37.5665'  # 서울 위도 (대략적)
    obs.lon = '126.9780'  # 서울 경도
    
    # 2월 1일부터 2월 10일까지 검색
    best_date = None
    min_diff = 360
    
    for day in range(1, 11):
        test_date = datetime(year, 2, day, 12, 0, 0)  # 정오에 검색
        utc_date = test_date - timedelta(hours=9)
        obs.date = ephem.Date(utc_date)
        s = ephem.Sun()
        s.compute(obs)
        ecl = ephem.Ecliptic(s.ra, s.dec)
        current_long = float(ecl.lon) * 180 / ephem.pi
        current_long = current_long % 360
        
        # 315도에 가장 가까운 날 찾기
        diff = abs(current_long - target_longitude)
        if diff > 180:
            diff = 360 - diff
        
        if diff < min_diff:
            min_diff = diff
            best_date = test_date
    
    # 더 정밀하게 검색 (시간 단위)
    if best_date:
        base_date = best_date
        for hour in range(0, 24):
            for minute in range(0, 60, 15):  # 15분 단위
                test_date = datetime(base_date.year, base_date.month, base_date.day, hour, minute, 0)
                utc_date = test_date - timedelta(hours=9)
                obs.date = ephem.Date(utc_date)
                s = ephem.Sun()
                s.compute(obs)
                ecl = ephem.Ecliptic(s.ra, s.dec)
                current_long = float(ecl.lon) * 180 / ephem.pi
                current_long = current_long % 360
                
                diff = abs(current_long - target_longitude)
                if diff > 180:
                    diff = 360 - diff
                
                if diff < min_diff:
                    min_diff = diff
                    best_date = test_date
                    
                    if diff < 0.5:  # 충분히 정확하면 중단
                        break
    
    return best_date if best_date else datetime(year, 2, 4, 0, 0, 0)


def find_solar_term_date(year, target_longitude):
    """
    해당 년도의 특정 절기 날짜를 찾습니다.
    
    Args:
        year: 년도
        target_longitude: 목표 황경 (예: 315=입춘, 345=경칩)
        
    Returns:
        datetime: 절기 날짜 (시간 포함, 한국시간 기준)
    """
    obs = ephem.Observer()
    obs.lat = '37.5665'
    obs.lon = '126.9780'
    
    # 대략적인 날짜 범위 결정
    term_ranges = {
        315: (2, 1, 10),   # 입춘
        345: (1, 18, 25),  # 경칩
        0: (3, 18, 23),    # 춘분
        15: (4, 3, 6),     # 청명
        30: (4, 18, 21),   # 곡우
        45: (5, 4, 7),     # 입하
        60: (5, 19, 22),   # 소만
        75: (6, 4, 7),     # 망종
        90: (6, 19, 23), # 하지
        105: (7, 5, 8),    # 소서
        120: (7, 20, 23), # 대서
        135: (8, 6, 9),    # 입추
        150: (8, 21, 24), # 처서
        165: (9, 6, 9),    # 백로
        180: (9, 21, 24), # 추분
        195: (10, 7, 9),  # 한로
        210: (10, 22, 24), # 상강
        225: (11, 6, 9),  # 입동
        240: (11, 21, 24), # 소설
        255: (12, 6, 9),  # 대설
        270: (12, 20, 24), # 동지
        285: (1, 4, 7),   # 소한
        300: (1, 19, 22)  # 대한
    }
    
    start_month, start_day, end_day = term_ranges.get(target_longitude, (1, 1, 31))
    
    best_date = None
    min_diff = 360
    
    for day in range(start_day, end_day + 1):
        for hour in range(0, 24):
            for minute in range(0, 60, 15):  # 15분 단위
                try:
                    test_date = datetime(year, start_month, day, hour, minute, 0)
                    utc_date = test_date - timedelta(hours=9)
                    obs.date = ephem.Date(utc_date)
                    s = ephem.Sun()
                    s.compute(obs)
                    ecl = ephem.Ecliptic(s.ra, s.dec)
                    current_long = float(ecl.lon) * 180 / ephem.pi
                    current_long = current_long % 360
                    
                    diff = abs(current_long - target_longitude)
                    if diff > 180:
                        diff = 360 - diff
                    
                    if diff < min_diff:
                        min_diff = diff
                        best_date = test_date
                        
                        if diff < 0.1:  # 매우 정확하면 중단
                            return best_date
                except ValueError:
                    continue
    
    return best_date if best_date else datetime(year, start_month, start_day, 12, 0, 0)


def get_month_ganji_for_date(date_obj):
    """
    날짜의 월간지를 계산합니다.
    절기 기준으로 정확한 월간지를 결정합니다.
    
    Args:
        date_obj: datetime 객체
        
    Returns:
        tuple: (월간지 문자열, 한글발음)
    """
    year = date_obj.year
    month = date_obj.month
    day = date_obj.day
    
    # 입춘 기준으로 년도 결정
    ipchun_date = find_ipchun_date(year)
    if date_obj < ipchun_date:
        saju_year = year - 1
        prev_ipchun = find_ipchun_date(year - 1)
    else:
        saju_year = year
        prev_ipchun = ipchun_date
    
    # 현재 날짜의 태양 황경 계산
    obs = ephem.Observer()
    utc_datetime = date_obj - timedelta(hours=9)
    obs.date = ephem.Date(utc_datetime)
    s = ephem.Sun()
    s.compute(obs)
    ecl = ephem.Ecliptic(s.ra, s.dec)
    long_deg = float(ecl.lon) * 180 / ephem.pi
    long_deg = long_deg % 360
    
    # 월간지 인덱스 계산 (절기 기준)
    if date_obj < ipchun_date:
        # 입춘 이전: 전년도 기준으로 경칩 확인
        gyeongchip_date = find_solar_term_date(year - 1, 345)
        if gyeongchip_date.year >= year:
            gyeongchip_date = find_solar_term_date(year, 345)
    else:
        # 입춘 이후: 올해 기준으로 경칩 확인
        gyeongchip_date = find_solar_term_date(year, 345)
    
    # 월간지 구간 결정 (경칩 기준)
    if date_obj < gyeongchip_date:
        month_idx = 0  # 무자월 (인월)
    else:
        # 경칩 이후의 다른 월간지도 고려
        if long_deg >= 345 or long_deg < 15:
            month_idx = 1  # 묘월 (기축월)
        elif long_deg >= 15 and long_deg < 45:
            month_idx = 2  # 진월
        elif long_deg >= 45 and long_deg < 75:
            month_idx = 3  # 사월
        elif long_deg >= 75 and long_deg < 105:
            month_idx = 4  # 오월
        elif long_deg >= 105 and long_deg < 135:
            month_idx = 5  # 미월
        elif long_deg >= 135 and long_deg < 165:
            month_idx = 6  # 신월
        elif long_deg >= 165 and long_deg < 195:
            month_idx = 7  # 유월
        elif long_deg >= 195 and long_deg < 225:
            month_idx = 8  # 술월
        elif long_deg >= 225 and long_deg < 255:
            month_idx = 9  # 해월
        elif long_deg >= 255 and long_deg < 285:
            month_idx = 10  # 자월
        elif long_deg >= 285 and long_deg < 315:
            month_idx = 11  # 축월
        elif long_deg >= 315 and long_deg < 345:
            month_idx = 0  # 인월 (무자월, 다음 해 입춘 이후)
        else:
            month_idx = 1  # 기본값
    
    # 년간지에서 년천간 인덱스
    year_stem, year_branch = saju_logic.get_year_ganji(saju_year)
    year_stem_char = year_stem.split()[0] if isinstance(year_stem, str) and "(" in year_stem else year_stem
    try:
        year_stem_idx = saju_logic.HEAVENLY_STEMS.index(year_stem)
    except ValueError:
        # 문자열 매칭으로 찾기
        year_stem_idx = 0
        for idx, stem in enumerate(saju_logic.HEAVENLY_STEMS):
            stem_char = stem.split()[0] if isinstance(stem, str) and "(" in stem else stem
            if stem_char == year_stem_char:
                year_stem_idx = idx
                break
    
    # 월간지 계산
    month_stem, month_branch = saju_logic.get_month_ganji(year_stem_idx, month_idx)
    
    month_stem_char = month_stem.split()[0] if isinstance(month_stem, str) and "(" in month_stem else month_stem
    month_branch_char = month_branch.split()[0] if isinstance(month_branch, str) and "(" in month_branch else month_branch
    
    month_pronunciation = GANJI_PRONUNCIATION.get(month_stem_char, "") + GANJI_PRONUNCIATION.get(month_branch_char, "")
    month_ganji_display = f"{month_pronunciation}({month_stem_char}{month_branch_char})"
    
    return month_ganji_display, month_pronunciation


def get_day_ganji_display(date_obj):
    """
    날짜의 간지를 계산하여 표시 형식으로 반환합니다.
    
    Args:
        date_obj: datetime 객체
        
    Returns:
        str: 간지 문자열 (예: "을해(乙亥)")
    """
    try:
        # saju_logic.get_day_ganji 사용
        day_stem, day_branch = saju_logic.get_day_ganji(date_obj)
        
        # 문자 추출
        stem_char = day_stem.split()[0] if isinstance(day_stem, str) and "(" in day_stem else day_stem
        branch_char = day_branch.split()[0] if isinstance(day_branch, str) and "(" in day_branch else day_branch
        
        # 한글 발음
        stem_pron = GANJI_PRONUNCIATION.get(stem_char, "")
        branch_pron = GANJI_PRONUNCIATION.get(branch_char, "")
        
        if stem_pron and branch_pron:
            return f"{stem_pron}{branch_pron}({stem_char}{branch_char})"
        else:
            return f"{stem_char}{branch_char}"
            
    except Exception:
        # 간단한 계산 방식 (60갑자 순환)
        base_date = date(2000, 1, 1)  # 기준일 (임시)
        days_diff = (date_obj.date() - base_date).days
        
        # 60갑자 순환
        ganji_index = days_diff % 60
        
        # 간지 리스트 (60갑자)
        stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        
        stem_char = stems[ganji_index % 10]
        branch_char = branches[ganji_index % 12]
        
        stem_pron = GANJI_PRONUNCIATION.get(stem_char, "")
        branch_pron = GANJI_PRONUNCIATION.get(branch_char, "")
        
        if stem_pron and branch_pron:
            return f"{stem_pron}{branch_pron}({stem_char}{branch_char})"
        else:
            return f"{stem_char}{branch_char}"


def get_lunar_date(year, month, day):
    """
    양력 날짜를 음력으로 변환합니다.
    
    Args:
        year: 년도
        month: 월
        day: 일
        
    Returns:
        tuple: (음력월, 음력일) 또는 (None, None) (오류 시)
    """
    try:
        lunar_cal = KoreanLunarCalendar()
        lunar_cal.setSolarDate(year, month, day)
        return lunar_cal.lunarMonth, lunar_cal.lunarDay
    except Exception:
        return None, None


def generate_calendar_data(year, month, show_lunar=True, show_ganji=True):
    """
    달력 데이터를 생성합니다.
    
    Args:
        year: 년도
        month: 월
        show_lunar: 음력 표시 여부
        show_ganji: 간지 표시 여부
        
    Returns:
        dict: 달력 데이터
    """
    # 달력 정보 가져오기 (일요일을 첫 요일로 설정)
    calendar.setfirstweekday(calendar.SUNDAY)
    cal = calendar.monthcalendar(year, month)
    
    # 요일 헤더
    weekdays = ["일", "월", "화", "수", "목", "금", "토"]
    
    today = datetime.now()
    is_current_month = (year == today.year and month == today.month)
    
    # 첫 날과 마지막 날의 월간지 계산
    first_day = datetime(year, month, 1)
    last_day_num = calendar.monthrange(year, month)[1]
    last_day = datetime(year, month, last_day_num)
    
    first_month_ganji, first_month_pron = get_month_ganji_for_date(first_day)
    last_month_ganji, last_month_pron = get_month_ganji_for_date(last_day)
    
    # 년간지 계산 (입춘 기준)
    ipchun_date = find_ipchun_date(year)
    if first_day < ipchun_date:
        saju_year = year - 1
    else:
        saju_year = year
    
    year_stem, year_branch = saju_logic.get_year_ganji(saju_year)
    year_stem_char = year_stem.split()[0] if isinstance(year_stem, str) and "(" in year_stem else year_stem
    year_branch_char = year_branch.split()[0] if isinstance(year_branch, str) and "(" in year_branch else year_branch
    
    year_pronunciation = GANJI_PRONUNCIATION.get(year_stem_char, "") + GANJI_PRONUNCIATION.get(year_branch_char, "")
    
    # 년/월 표시
    first_month_ganji_chars = first_month_ganji.split('(')[1].rstrip(')') if '(' in first_month_ganji else first_month_ganji
    year_month_display = f"{year_pronunciation}({year_stem_char}{year_branch_char})년 {first_month_pron}({first_month_ganji_chars})월"
    if first_month_pron != last_month_pron:
        last_month_ganji_chars = last_month_ganji.split('(')[1].rstrip(')') if '(' in last_month_ganji else last_month_ganji
        year_month_display += f", {last_month_pron}({last_month_ganji_chars})월"
    
    # 달력 데이터 생성
    calendar_data = []
    for week in cal:
        week_data = []
        for day in week:
            if day == 0:
                week_data.append(None)  # 빈 셀
            else:
                date_obj = datetime(year, month, day)
                is_today = is_current_month and day == today.day
                
                # 음력 날짜
                lunar_month, lunar_day = get_lunar_date(year, month, day) if show_lunar else (None, None)
                lunar_display = f"{lunar_month}.{lunar_day:02d}" if lunar_month and lunar_day else ""
                
                # 간지 (일간지)
                ganji_display = get_day_ganji_display(date_obj) if show_ganji else ""
                
                # 월간지
                month_ganji_display, month_pron = get_month_ganji_for_date(date_obj)
                is_secondary_month = (month_pron != first_month_pron)
                
                week_data.append({
                    'day': day,
                    'is_today': is_today,
                    'lunar_display': lunar_display,
                    'ganji_display': ganji_display,
                    'month_ganji': month_pron,
                    'is_secondary_month': is_secondary_month
                })
        calendar_data.append(week_data)
    
    return {
        'weekdays': weekdays,
        'calendar_data': calendar_data,
        'year_month_display': year_month_display,
        'year': year,
        'month': month
    }

