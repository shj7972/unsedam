import ephem
from datetime import datetime, timedelta
from korean_lunar_calendar import KoreanLunarCalendar

# Gan-Ji Data
HEAVENLY_STEMS = ["甲 (갑)", "乙 (을)", "丙 (병)", "丁 (정)", "戊 (무)", "己 (기)", "庚 (경)", "辛 (신)", "壬 (임)", "癸 (계)"]
EARTHLY_BRANCHES = ["子 (자)", "丑 (축)", "寅 (인)", "卯 (묘)", "辰 (진)", "巳 (사)", "午 (오)", "未 (미)", "申 (신)", "酉 (유)", "戌 (술)", "亥 (해)"]

ZODIAC_ANIMALS = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Sheep", "Monkey", "Rooster", "Dog", "Pig"]

# 지장간 (地支藏干) - 각 지지에 숨어있는 천간
# Format: [본기(本氣), 중기(中氣), 여기(餘氣)]
HIDDEN_STEMS = {
    "子 (자)": ["壬 (임)", "癸 (계)"],
    "丑 (축)": ["己 (기)", "辛 (신)", "癸 (계)"],
    "寅 (인)": ["甲 (갑)", "丙 (병)", "戊 (무)"],
    "卯 (묘)": ["乙 (을)"],
    "辰 (진)": ["戊 (무)", "乙 (을)", "癸 (계)"],
    "巳 (사)": ["丙 (병)", "戊 (무)", "庚 (경)"],
    "午 (오)": ["丙 (병)", "己 (기)", "丁 (정)"],  # 병(본기), 기(중기), 정(여기)
    "未 (미)": ["己 (기)", "丁 (정)", "乙 (을)"],
    "申 (신)": ["庚 (경)", "壬 (임)", "戊 (무)"],
    "酉 (유)": ["辛 (신)"],
    "戌 (술)": ["戊 (무)", "辛 (신)", "丁 (정)"],
    "亥 (해)": ["壬 (임)", "甲 (갑)"]
}

# 오행 (五行)
FIVE_ELEMENTS = {
    "甲 (갑)": "木", "乙 (을)": "木",
    "丙 (병)": "火", "丁 (정)": "火",
    "戊 (무)": "土", "己 (기)": "土",
    "庚 (경)": "金", "辛 (신)": "金",
    "壬 (임)": "水", "癸 (계)": "水"
}

BRANCH_ELEMENTS = {
    "寅 (인)": "木", "卯 (묘)": "木",
    "巳 (사)": "火", "午 (오)": "火",
    "辰 (진)": "土", "戌 (술)": "土", "丑 (축)": "土", "未 (미)": "土",
    "申 (신)": "金", "酉 (유)": "金",
    "亥 (해)": "水", "子 (자)": "水"
}

# 십성 (十神) 이름
TEN_GODS = {
    "比肩": "比肩", "劫財": "劫財",
    "食神": "食神", "傷官": "傷官",
    "偏財": "偏財", "正財": "正財",
    "偏官": "偏官", "正官": "正官",
    "偏印": "偏印", "正印": "正印"
}

# 십이운성 (十二運星) - 일간별 지지에 대한 운성
# 순서: 장생(長生), 목욕(沐浴), 관대(冠帶), 건록(建祿), 제왕(帝旺), 쇠(衰), 병(病), 사(死), 묘(墓), 절(絶), 태(胎), 양(養)
TWELVE_FORTUNES = {
    "甲 (갑)": ["亥 (해)", "子 (자)", "丑 (축)", "寅 (인)", "卯 (묘)", "辰 (진)", "巳 (사)", "午 (오)", "未 (미)", "申 (신)", "酉 (유)", "戌 (술)"],
    "乙 (을)": ["午 (오)", "巳 (사)", "辰 (진)", "卯 (묘)", "寅 (인)", "丑 (축)", "子 (자)", "亥 (해)", "戌 (술)", "酉 (유)", "申 (신)", "未 (미)"],
    "丙 (병)": ["寅 (인)", "卯 (묘)", "辰 (진)", "巳 (사)", "午 (오)", "未 (미)", "申 (신)", "酉 (유)", "戌 (술)", "亥 (해)", "子 (자)", "丑 (축)"],
    "丁 (정)": ["酉 (유)", "申 (신)", "未 (미)", "午 (오)", "巳 (사)", "辰 (진)", "卯 (묘)", "寅 (인)", "丑 (축)", "子 (자)", "亥 (해)", "戌 (술)"],
    "戊 (무)": ["寅 (인)", "卯 (묘)", "辰 (진)", "巳 (사)", "午 (오)", "未 (미)", "申 (신)", "酉 (유)", "戌 (술)", "亥 (해)", "子 (자)", "丑 (축)"],
    "己 (기)": ["酉 (유)", "申 (신)", "未 (미)", "午 (오)", "巳 (사)", "辰 (진)", "卯 (묘)", "寅 (인)", "丑 (축)", "子 (자)", "亥 (해)", "戌 (술)"],
    "庚 (경)": ["巳 (사)", "午 (오)", "未 (미)", "申 (신)", "酉 (유)", "戌 (술)", "亥 (해)", "子 (자)", "丑 (축)", "寅 (인)", "卯 (묘)", "辰 (진)"],
    "辛 (신)": ["子 (자)", "亥 (해)", "戌 (술)", "酉 (유)", "申 (신)", "未 (미)", "午 (오)", "巳 (사)", "辰 (진)", "卯 (묘)", "寅 (인)", "丑 (축)"],
    "壬 (임)": ["申 (신)", "酉 (유)", "戌 (술)", "亥 (해)", "子 (자)", "丑 (축)", "寅 (인)", "卯 (묘)", "辰 (진)", "巳 (사)", "午 (오)", "未 (미)"],
    "癸 (계)": ["卯 (묘)", "寅 (인)", "丑 (축)", "子 (자)", "亥 (해)", "戌 (술)", "酉 (유)", "申 (신)", "未 (미)", "午 (오)", "巳 (사)", "辰 (진)"]
}

# 십이운성 한글 이름
TWELVE_FORTUNE_NAMES = ["장생", "목욕", "관대", "건록", "제왕", "쇠", "병", "사", "묘", "절", "태", "양"]

# 신살 (神煞) 계산용 데이터
# 천을귀인 (天乙貴人) - 일간별 해당 지지
TIANYI_GUIREN = {
    "甲 (갑)": ["丑 (축)", "未 (미)"],
    "乙 (을)": ["子 (자)", "申 (신)"],
    "丙 (병)": ["亥 (해)", "酉 (유)"],
    "丁 (정)": ["亥 (해)", "酉 (유)"],
    "戊 (무)": ["丑 (축)", "未 (미)"],
    "己 (기)": ["子 (자)", "申 (신)"],
    "庚 (경)": ["丑 (축)", "未 (미)"],
    "辛 (신)": ["午 (오)", "寅 (인)"],
    "壬 (임)": ["卯 (묘)", "巳 (사)"],
    "癸 (계)": ["卯 (묘)", "巳 (사)"]
}

# 도화 (桃花) - 년지/일지 기준
TAOHUA = {
    "子 (자)": "酉 (유)", "丑 (축)": "午 (오)", "寅 (인)": "卯 (묘)", "卯 (묘)": "子 (자)",
    "辰 (진)": "酉 (유)", "巳 (사)": "午 (오)", "午 (오)": "卯 (묘)", "未 (미)": "子 (자)",
    "申 (신)": "酉 (유)", "酉 (유)": "午 (오)", "戌 (술)": "卯 (묘)", "亥 (해)": "子 (자)"
}

# 화개 (華蓋) - 년지/일지 기준
HUAGAI = {
    "子 (자)": "辰 (진)", "丑 (축)": "丑 (축)", "寅 (인)": "戌 (술)", "卯 (묘)": "未 (미)",
    "辰 (진)": "辰 (진)", "巳 (사)": "丑 (축)", "午 (오)": "戌 (술)", "未 (미)": "未 (미)",
    "申 (신)": "辰 (진)", "酉 (유)": "丑 (축)", "戌 (술)": "戌 (술)", "亥 (해)": "未 (미)"
}

# 양인 (羊刃) - 일간별 해당 지지
YANGREN = {
    "甲 (갑)": "卯 (묘)", "乙 (을)": "寅 (인)", "丙 (병)": "午 (오)", "丁 (정)": "巳 (사)",
    "戊 (무)": "午 (오)", "己 (기)": "巳 (사)", "庚 (경)": "酉 (유)", "辛 (신)": "申 (신)",
    "壬 (임)": "子 (자)", "癸 (계)": "亥 (해)"
}

# 역마 (驛馬) - 년지/일지 기준
YIMA = {
    "子 (자)": "寅 (인)", "丑 (축)": "亥 (해)", "寅 (인)": "申 (신)", "卯 (묘)": "巳 (사)",
    "辰 (진)": "寅 (인)", "巳 (사)": "亥 (해)", "午 (오)": "申 (신)", "未 (미)": "巳 (사)",
    "申 (신)": "寅 (인)", "酉 (유)": "亥 (해)", "戌 (술)": "申 (신)", "亥 (해)": "巳 (사)"
}

# 공망 (空亡) - 일간과 일지 기준 (60갑자 순서)
KONGWANG = {
    "甲 (갑)": ["戌 (술)", "亥 (해)"],
    "乙 (을)": ["申 (신)", "酉 (유)"],
    "丙 (병)": ["午 (오)", "未 (미)"],
    "丁 (정)": ["辰 (진)", "巳 (사)"],
    "戊 (무)": ["寅 (인)", "卯 (묘)"],
    "己 (기)": ["子 (자)", "丑 (축)"],
    "庚 (경)": ["戌 (술)", "亥 (해)"],
    "辛 (신)": ["申 (신)", "酉 (유)"],
    "壬 (임)": ["午 (오)", "未 (미)"],
    "癸 (계)": ["辰 (진)", "巳 (사)"]
}

# 장성 (將星) - 년지/일지 기준
JIANGXING = {
    "子 (자)": "子 (자)", "丑 (축)": "酉 (유)", "寅 (인)": "午 (오)", "卯 (묘)": "卯 (묘)",
    "辰 (진)": "子 (자)", "巳 (사)": "酉 (유)", "午 (오)": "午 (오)", "未 (미)": "卯 (묘)",
    "申 (신)": "子 (자)", "酉 (유)": "酉 (유)", "戌 (술)": "午 (오)", "亥 (해)": "卯 (묘)"
}

# Gan-Ji for reference dates (Simplified)
# Ref: 1900-01-01 was ... actually we need a robust algorithm.
# We will use the standard modulo math for Year/Day.

def get_ganji(idx):
    """Returns (Stem, Branch) based on 0-59 index"""
    stem = HEAVENLY_STEMS[idx % 10]
    branch = EARTHLY_BRANCHES[idx % 12]
    return stem, branch

def get_year_ganji(year):
    """
    Calculate Year Gan-Ji using standard formula.
    Base year 1924 (Gap-Ja) -> 4
    (year - 4) % 60
    But note: Year starts at Ipchun (approx Feb 4).
    This function returns the Gan-Ji assuming the year HAS started.
    Adjust for pre-Ipchun dates in the main logic.
    """
    idx = (year - 4) % 60
    return get_ganji(idx)

def get_month_ganji(year_stem_idx, month_branch_idx):
    """
    Calculate Month Gan-Ji.
    Month Branch is fixed to the solar term (Tiger=In, Rabbit=Myo...).
    Tiger (In) starts at Ipchun.
    
    Formula for Month Stem:
    Year Stem 甲/己 (0/5) -> Start 丙 (2)
    Year Stem 乙/庚 (1/6) -> Start 戊 (4)
    Year Stem 丙/辛 (2/7) -> Start 庚 (6)
    Year Stem 丁/壬 (3/8) -> Start 壬 (8)
    Year Stem 戊/癸 (4/9) -> Start 甲 (0)
    
    (Year Stem Index % 5) * 2 + 2 = Start Month Stem Index (for Tiger Month)
    
    month_branch_idx: 0=Tiger(인/2), 1=Rabbit(묘/3), 2=Dragon(진/4), ..., 6=Monkey(신/8), ...
    """
    start_stem_idx = (year_stem_idx % 5) * 2 + 2
    
    # month_branch_idx: 0=Tiger, 1=Rabbit, ..., 6=Monkey, ...
    # Real branch index: Tiger=2, Rabbit=3, ..., Monkey=8, ...
    real_branch_idx = (month_branch_idx + 2) % 12
    
    # Month stem: start from Tiger month (month_branch_idx=0)
    current_stem_idx = (start_stem_idx + month_branch_idx) % 10
    
    # Return stem and branch directly
    return HEAVENLY_STEMS[current_stem_idx], EARTHLY_BRANCHES[real_branch_idx]

def get_day_ganji(date):
    """
    Calculate Day Gan-Ji.
    Base date: 1900-01-01 was 甲戌 (Gap-Sul, 10).
    Days passed since 1900-01-01.
    """
    base_date = datetime(1900, 1, 1)
    diff = (date - base_date).days
    # 1900-01-01 was Gap-Sul (idx 10).
    # Wait, need to verify 1900-01-01 Gan-Ji. 
    # Actually simpler: 1899-12-31 was ...
    # Let's perform a known check: 2024-01-01 was 甲子 (Gap-Ja).
    # 2024-01-01 -> Gap-Ja (0)? No.
    # 2024-01-01 was Gabjin Year... wait Day Ganji.
    # Let's use a known anchor. 2023-12-31.
    # Safe bet: Python's ordinal date or similar.
    # Anchor: 1901-01-01?
    # Let's use a standard algorithm:
    # (Total Days - Offset) % 60
    # Anchor: 1900-01-08 was 甲戌 (10)? No.
    # Anchor: 2000-01-01 was 戊午 (Mu-O, 54).
    anchor_date = datetime(2000, 1, 1)
    anchor_idx = 54 # Mu-O
    
    days_diff = (date - anchor_date).days
    current_idx = (anchor_idx + days_diff) % 60
    return get_ganji(current_idx)

def get_ten_god(day_stem_idx, other_stem_idx):
    """
    Calculate Ten God (十神) based on Day Stem and other Stem.
    
    Rules:
    - Same element, same yin-yang: 比肩 (比肩)
    - Same element, different yin-yang: 劫財 (劫財)
    - Day generates other (same yin-yang): 食神 (食神)
    - Day generates other (different yin-yang): 傷官 (傷官)
    - Day overcomes other (same yin-yang): 偏財 (偏財)
    - Day overcomes other (different yin-yang): 正財 (正財)
    - Other overcomes day (same yin-yang): 偏官 (偏官)
    - Other overcomes day (different yin-yang): 正官 (正官)
    - Other generates day (same yin-yang): 偏印 (偏印)
    - Other generates day (different yin-yang): 正印 (正印)
    
    Five Elements cycle:
    木(목) -> 火(화) -> 土(토) -> 金(금) -> 水(수) -> 木(목)
    """
    # Get elements
    day_element = FIVE_ELEMENTS[HEAVENLY_STEMS[day_stem_idx]]
    other_element = FIVE_ELEMENTS[HEAVENLY_STEMS[other_stem_idx]]
    
    # Get yin-yang
    day_yang = (day_stem_idx % 2 == 0)
    other_yang = (other_stem_idx % 2 == 0)
    same_yin_yang = (day_yang == other_yang)
    
    # Element mapping
    element_order = {"木": 0, "火": 1, "土": 2, "金": 3, "水": 4}
    day_elem_idx = element_order[day_element]
    other_elem_idx = element_order[other_element]
    
    # Calculate relationship
    if day_element == other_element:
        # Same element
        if same_yin_yang:
            return "比肩"
        else:
            return "劫財"
    elif (day_elem_idx + 1) % 5 == other_elem_idx:
        # Day generates other (木->火, 火->土, 土->金, 金->水, 水->木)
        if same_yin_yang:
            return "食神"
        else:
            return "傷官"
    elif (other_elem_idx + 1) % 5 == day_elem_idx:
        # Other generates day
        if same_yin_yang:
            return "偏印"
        else:
            return "正印"
    elif (day_elem_idx + 2) % 5 == other_elem_idx:
        # Day overcomes other (木->土, 火->金, 土->水, 金->木, 水->火)
        if same_yin_yang:
            return "偏財"
        else:
            return "正財"
    elif (other_elem_idx + 2) % 5 == day_elem_idx:
        # Other overcomes day
        if same_yin_yang:
            return "偏官"
        else:
            return "正官"
    else:
        # Should not happen, but return default
        return "比肩"

def get_hour_ganji(day_stem_idx, hour):
    """
    Calculate Hour Gan-Ji.
    Based on Day Stem.
    Hour Branch is determined by time (23-1: Ja, 1-3: Chuk...).
    Branch Index: ((hour + 1) // 2) % 12
    
    Formula for Hour Stem:
    Day Stem 甲/己 -> Start 甲 (0)
    Day Stem 乙/庚 -> Start 丙 (2)
    Day Stem 丙/辛 -> Start 戊 (4)
    Day Stem 丁/壬 -> Start 庚 (6)
    Day Stem 戊/癸 -> Start 壬 (8)
    
    (Day Stem Index % 5) * 2 = Start Hour Stem Index (for Ja hour)
    """
    branch_idx = ((hour + 1) // 2) % 12
    start_stem_idx = (day_stem_idx % 5) * 2
    current_stem_idx = (start_stem_idx + branch_idx) % 10
    
    # Return stem and branch directly
    return HEAVENLY_STEMS[current_stem_idx], EARTHLY_BRANCHES[branch_idx]

def find_next_solar_term(birth_datetime, direction):
    """
    Find the next (or previous) solar term from birth date.
    direction: 1 for forward (next), -1 for backward (previous)
    Returns: datetime of the solar term
    """
    # Solar terms are at: 315, 330, 345, 0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 240, 255, 270, 285, 300
    # Each term is 15 degrees apart
    term_angles = [315, 330, 345, 0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 240, 255, 270, 285, 300]
    
    # Get current solar longitude
    obs = ephem.Observer()
    utc_datetime = birth_datetime - timedelta(hours=9)
    obs.date = ephem.Date(utc_datetime)
    s = ephem.Sun()
    s.compute(obs)
    ecl = ephem.Ecliptic(s.ra, s.dec)
    current_long = float(ecl.lon) * 180 / ephem.pi
    current_long = current_long % 360
    
    # Find the target term angle
    if direction == 1:  # Forward - find next term
        # Find the next term angle that is greater than current
        target_angle = None
        for angle in term_angles:
            if angle > current_long:
                target_angle = angle
                break
        
        # If no next angle found, wrap to next cycle (315)
        if target_angle is None:
            target_angle = 315
    else:  # Backward - find previous term
        # Find the previous term angle that is less than current
        target_angle = None
        for angle in reversed(term_angles):
            if angle < current_long:
                target_angle = angle
                break
        
        # If no previous angle found, wrap to previous cycle (300)
        if target_angle is None:
            target_angle = 300
    
    # Search for the exact datetime by checking each day
    best_date = None
    min_diff = float('inf')
    
    # Search forward or backward up to 60 days
    for day_offset in range(60):
        if direction == 1:
            check_date = birth_datetime + timedelta(days=day_offset)
        else:
            check_date = birth_datetime - timedelta(days=day_offset)
        
        obs.date = ephem.Date(check_date - timedelta(hours=9))
        s.compute(obs)
        ecl = ephem.Ecliptic(s.ra, s.dec)
        check_long = float(ecl.lon) * 180 / ephem.pi
        check_long = check_long % 360
        
        # Calculate difference from target (considering wrap-around)
        diff = None
        if direction == 1:
            # For forward, find when we reach or pass target
            if target_angle < current_long:  # Wrap around case (e.g., 300 -> 315)
                # Target is in next cycle
                if check_long >= target_angle:
                    diff = abs(check_long - target_angle)
                elif check_long < current_long:
                    diff = abs(check_long + 360 - target_angle)
            else:
                # Normal case: target_angle > current_long
                if check_long >= target_angle:
                    diff = abs(check_long - target_angle)
        else:  # Backward
            if target_angle > current_long:  # Wrap around case (e.g., 15 -> 300)
                # Target is in previous cycle
                if check_long <= target_angle:
                    diff = abs(check_long - target_angle)
                elif check_long > current_long:
                    diff = abs(check_long - 360 - target_angle)
            else:
                # Normal case: target_angle < current_long
                if check_long <= target_angle:
                    diff = abs(check_long - target_angle)
        
        # Update best date if we found a valid difference
        if diff is not None and diff < min_diff:
            min_diff = diff
            best_date = check_date
            # If we're very close, we can stop
            if diff < 0.5:
                break
    
    # Refine with hourly search around the best date
    if best_date:
        for hour_offset in range(-24, 25):  # ±24 hours
            refined_date = best_date + timedelta(hours=hour_offset)
            obs.date = ephem.Date(refined_date - timedelta(hours=9))
            s.compute(obs)
            ecl = ephem.Ecliptic(s.ra, s.dec)
            refined_long = float(ecl.lon) * 180 / ephem.pi
            refined_long = refined_long % 360
            
            if direction == 1:
                if target_angle < current_long:
                    if refined_long >= target_angle:
                        diff = abs(refined_long - target_angle)
                    elif refined_long < current_long:
                        diff = abs(refined_long + 360 - target_angle)
                    else:
                        continue
                else:
                    if refined_long >= target_angle:
                        diff = abs(refined_long - target_angle)
                    else:
                        continue
            else:
                if target_angle > current_long:
                    if refined_long <= target_angle:
                        diff = abs(refined_long - target_angle)
                    elif refined_long > current_long:
                        diff = abs(refined_long - 360 - target_angle)
                    else:
                        continue
                else:
                    if refined_long <= target_angle:
                        diff = abs(refined_long - target_angle)
                    else:
                        continue
            
            if diff < min_diff:
                min_diff = diff
                best_date = refined_date
    
    return best_date if best_date else birth_datetime

def calculate_daeun(pillars_info, gender, birth_datetime):
    """
    Calculate Daeun (大運, Great Fortune Period).
    
    Daeun calculation rules:
    - Based on Year Stem (陽/陰) and Gender
    - 陽年 (Yang Year): 甲, 丙, 戊, 庚, 壬 (indices 0, 2, 4, 6, 8)
    - 陰年 (Yin Year): 乙, 丁, 己, 辛, 癸 (indices 1, 3, 5, 7, 9)
    
    Direction:
    - Male + 陽年: Forward (順行)
    - Male + 陰年: Backward (逆行)
    - Female + 陽年: Backward (逆行)
    - Female + 陰年: Forward (順行)
    
    Starting age calculation:
    - Days from birth to next/previous solar term divided by 3
    - 3 days = 1 year (1 day = 4 months = 1/3 year)
    """
    # birth_datetime이 None이면 pillars_info에서 가져오거나 기본값 사용
    if birth_datetime is None:
        if 'birth_datetime' in pillars_info and pillars_info['birth_datetime'] is not None:
            birth_datetime = pillars_info['birth_datetime']
        else:
            # 기본값: 현재 날짜의 정오
            from datetime import datetime, time
            birth_datetime = datetime.combine(datetime.now().date(), time(12, 0))
    
    year_stem_idx = pillars_info["year_stem_idx"]
    month_stem_idx = pillars_info["month_stem_idx"]
    month_branch_idx = pillars_info["month_branch_idx"]
    
    # Determine if year is Yang (陽) or Yin (陰)
    is_yang_year = (year_stem_idx % 2 == 0)
    
    # Determine direction based on gender and year type
    is_male = (gender == "남성")
    
    if (is_male and is_yang_year) or (not is_male and not is_yang_year):
        direction = 1  # Forward (順行)
    else:
        direction = -1  # Backward (逆行)
    
    # Calculate starting age based on solar longitude (more reliable than finding exact term date)
    # Get current solar longitude
    obs = ephem.Observer()
    utc_datetime = birth_datetime - timedelta(hours=9)
    obs.date = ephem.Date(utc_datetime)
    s = ephem.Sun()
    s.compute(obs)
    ecl = ephem.Ecliptic(s.ra, s.dec)
    current_long = float(ecl.lon) * 180 / ephem.pi
    current_long = current_long % 360
    
    # Find target angle
    term_angles = [315, 330, 345, 0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 240, 255, 270, 285, 300]
    if direction == 1:
        target_angle = None
        for angle in term_angles:
            if angle > current_long:
                target_angle = angle
                break
        if target_angle is None:
            target_angle = 315
    else:
        target_angle = None
        for angle in reversed(term_angles):
            if angle < current_long:
                target_angle = angle
                break
        if target_angle is None:
            target_angle = 300
    
    # Find the actual date when sun reaches target angle
    # Simple approach: find first date that reaches or passes target
    best_date = None
    
    # Search forward or backward up to 60 days
    for day_offset in range(60):
        if direction == 1:
            check_date = birth_datetime + timedelta(days=day_offset)
        else:
            check_date = birth_datetime - timedelta(days=day_offset)
        
        # Create new observer and sun for each date to avoid state issues
        check_obs = ephem.Observer()
        check_obs.date = ephem.Date(check_date - timedelta(hours=9))
        check_s = ephem.Sun()
        check_s.compute(check_obs)
        check_ecl = ephem.Ecliptic(check_s.ra, check_s.dec)
        check_long = float(check_ecl.lon) * 180 / ephem.pi
        check_long = check_long % 360
        
        # Check if we've reached or passed the target
        if direction == 1:
            # Forward: check if we've reached or passed target
            if target_angle < current_long:  # Wrap around case (e.g., 300 -> 315)
                # We need to check if we've passed into next cycle
                if check_long >= target_angle or (check_long < current_long and check_long < 50):
                    best_date = check_date
                    break
            else:
                # Normal case: target_angle > current_long (e.g., 154.92 -> 165)
                if check_long >= target_angle:
                    best_date = check_date
                    break
        else:  # Backward
            # Backward: check if we've reached or passed target
            if target_angle > current_long:  # Wrap around case (e.g., 15 -> 300)
                # We need to check if we've passed into previous cycle
                if check_long <= target_angle or (check_long > current_long and check_long > 300):
                    best_date = check_date
                    break
            else:
                # Normal case: target_angle < current_long
                if check_long <= target_angle:
                    best_date = check_date
                    break
    
    # Calculate days from birth to term
    if best_date and best_date != birth_datetime:
        days_diff = abs((best_date - birth_datetime).total_seconds() / 86400)
    else:
        # Fallback: use angle-based calculation (should not happen in normal cases)
        # This means we couldn't find the term date, so use approximate calculation
        if direction == 1:
            if target_angle < current_long:
                angle_diff = (target_angle + 360) - current_long
            else:
                angle_diff = target_angle - current_long
        else:
            if target_angle > current_long:
                angle_diff = current_long - (target_angle - 360)
            else:
                angle_diff = current_long - target_angle
        # Use slightly adjusted solar speed for better accuracy
        days_diff = angle_diff / 0.9856
    
    # Convert days to years: 3 days = 1 year (1 day = 4 months = 1/3 year)
    start_age_years = days_diff / 3
    
    # NEW RULE: Discard the tens digit (modulo 10)
    # Most schools use integer Daeun numbers. We'll use the integer part modulo 10.
    start_age = int(round(start_age_years, 0)) % 10
    if start_age == 0 and round(start_age_years, 0) >= 10:
        # Some might want 0, some might want 10. Modulo 10 gives 0.
        pass
    
    # Calculate Daeun periods (typically 8 periods, 10 years each)
    # Daeun starts from the NEXT ganji after month pillar
    daeun_periods = []
    current_stem_idx = month_stem_idx
    current_branch_idx = month_branch_idx
    
    for i in range(8):  # 8 periods of 10 years each = 80 years
        # Calculate next ganji (first daeun is after month pillar)
        next_stem_idx = (current_stem_idx + direction) % 10
        next_branch_idx = (current_branch_idx + direction) % 12
        
        stem = HEAVENLY_STEMS[next_stem_idx]
        branch = EARTHLY_BRANCHES[next_branch_idx]
        
        # Calculate age range
        age_start = start_age + i * 10
        age_end = age_start + 10 - 0.1  # End just before next period starts
        
        daeun_periods.append({
            "period": i + 1,
            "age_start": round(age_start, 1),
            "age_end": round(age_end, 1),
            "stem": stem,
            "branch": branch,
            "ganji": f"{stem} {branch}"
        })
        
        # Move to next ganji for next period
        current_stem_idx = next_stem_idx
        current_branch_idx = next_branch_idx
    
    return {
        "direction": "順行" if direction == 1 else "逆行",
        "periods": daeun_periods,
        "start_age": start_age
    }

def calculate_twelve_fortunes(pillars_data, day_stem):
    """
    Calculate Twelve Fortunes (十二運星) for each pillar based on day stem.
    
    Args:
        pillars_data: List of pillar dictionaries
        day_stem: Day stem string (e.g., "甲 (갑)")
    
    Returns:
        List of fortune names for each pillar
    """
    if day_stem not in TWELVE_FORTUNES:
        return []
    
    fortune_table = TWELVE_FORTUNES[day_stem]
    fortunes = []
    
    for pillar in pillars_data:
        branch = pillar["Earthly Branch (지지)"]
        # Branch might be just Chinese char (e.g., "子") or full format (e.g., "子 (자)")
        # Convert to full format for lookup
        branch_full = branch
        if "(" not in branch:
            # Find the full format
            for full_branch in EARTHLY_BRANCHES:
                if full_branch.split()[0] == branch:
                    branch_full = full_branch
                    break
        
        # Find the index of this branch in the fortune table
        try:
            branch_idx = fortune_table.index(branch_full)
            fortune_name = TWELVE_FORTUNE_NAMES[branch_idx]
            fortunes.append(fortune_name)
        except ValueError:
            fortunes.append("")
    
    return fortunes

def calculate_sinsal(pillars_data, day_stem, year_branch, day_branch):
    """
    Calculate Sinsal (神煞) for each pillar.
    
    Args:
        pillars_data: List of pillar dictionaries
        day_stem: Day stem string (e.g., "甲 (갑)" or "甲")
        year_branch: Year branch string (e.g., "子 (자)" or "子")
        day_branch: Day branch string (e.g., "子 (자)" or "子")
    
    Returns:
        List of sinsal names for each pillar
    """
    sinsal_list = []
    
    # Convert branches to full format if needed
    def get_full_branch(branch):
        if "(" in branch:
            return branch
        for full_branch in EARTHLY_BRANCHES:
            if full_branch.split()[0] == branch:
                return full_branch
        return branch
    
    # Convert stem to full format if needed
    def get_full_stem(stem):
        if "(" in stem:
            return stem
        for full_stem in HEAVENLY_STEMS:
            if full_stem.split()[0] == stem:
                return full_stem
        return stem
    
    # Ensure day_stem is in full format for dictionary lookup
    day_stem_full = get_full_stem(day_stem)
    year_branch_full = get_full_branch(year_branch)
    day_branch_full = get_full_branch(day_branch)
    
    for pillar in pillars_data:
        branch = pillar["Earthly Branch (지지)"]
        branch_full = get_full_branch(branch)
        sinsals = []
        
        # 천을귀인 (天乙貴人) - 일간(日干) 기준으로 해당 지지 확인
        if day_stem_full in TIANYI_GUIREN and branch_full in TIANYI_GUIREN[day_stem_full]:
            sinsals.append("천을귀인")
        
        # 도화 (桃花) - 년지나 일지 기준으로 삼합의 끝에서 3위
        # 각 기둥의 지지가 년지나 일지 기준 도화에 해당하는지 확인
        if branch_full == TAOHUA.get(year_branch_full) or branch_full == TAOHUA.get(day_branch_full):
            sinsals.append("도화")
        
        # 화개 (華蓋) - 년지나 일지 기준으로 삼합의 중간
        # 각 기둥의 지지가 년지나 일지 기준 화개에 해당하는지 확인
        if branch_full == HUAGAI.get(year_branch_full) or branch_full == HUAGAI.get(day_branch_full):
            sinsals.append("화개")
        
        # 양인 (羊刃) - 일간(日干) 기준으로 해당 지지 확인
        if day_stem_full in YANGREN and branch_full == YANGREN[day_stem_full]:
            sinsals.append("양인")
        
        # 역마 (驛馬) - 년지나 일지 기준으로 대충(對沖)의 양쪽
        # 각 기둥의 지지가 년지나 일지 기준 역마에 해당하는지 확인
        if branch_full == YIMA.get(year_branch_full) or branch_full == YIMA.get(day_branch_full):
            sinsals.append("역마")
        
        # 공망 (空亡) - 일간과 일지 기준 (60갑자 순서)
        # 일간의 갑자 순서에 따라 공망이 되는 지지 확인
        if day_stem_full in KONGWANG and branch_full in KONGWANG[day_stem_full]:
            sinsals.append("공망")
        
        # 장성 (將星) - 년지나 일지 기준으로 삼합의 첫 번째
        # 각 기둥의 지지가 년지나 일지 기준 장성에 해당하는지 확인
        if branch_full == JIANGXING.get(year_branch_full) or branch_full == JIANGXING.get(day_branch_full):
            sinsals.append("장성")
        
        if sinsals:
            sinsal_list.append(" ".join(sinsals))
        else:
            sinsal_list.append("")
    
    return sinsal_list

def generate_fortune_analysis(pillars_data, pillars_info, daeun, fortunes, sinsals, hidden_lists):
    """
    Generate comprehensive fortune analysis based on all available data.
    
    Args:
        pillars_data: List of pillar dictionaries
        pillars_info: Dictionary with pillar information
        daeun: Daeun calculation result
        fortunes: List of twelve fortunes for each pillar
        sinsals: List of sinsals for each pillar
        hidden_lists: List of hidden stems for each pillar
    
    Returns:
        String containing comprehensive analysis
    """
    analysis_parts = []
    
    # Get day stem element
    day_stem = pillars_info.get('day_stem', '')
    day_stem_char = day_stem.split()[0] if day_stem else ""
    day_element = FIVE_ELEMENTS.get(day_stem, "") if day_stem else ""
    
    # Count elements in pillars
    element_count = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
    for pillar in pillars_data:
        stem = pillar.get("Heavenly Stem (천간)", "")
        if stem:
            stem_full = stem if "(" in stem else None
            if not stem_full:
                for s in HEAVENLY_STEMS:
                    if s.split()[0] == stem:
                        stem_full = s
                        break
            if stem_full:
                elem = FIVE_ELEMENTS.get(stem_full, "")
                if elem:
                    element_count[elem] += 1
        
        branch = pillar.get("Earthly Branch (지지)", "")
        if branch:
            branch_full = branch if "(" in branch else None
            if not branch_full:
                for b in EARTHLY_BRANCHES:
                    if b.split()[0] == branch:
                        branch_full = b
                        break
            if branch_full and branch_full in HIDDEN_STEMS:
                for hidden_stem in HIDDEN_STEMS[branch_full]:
                    elem = FIVE_ELEMENTS.get(hidden_stem, "")
                    if elem:
                        element_count[elem] += 0.3  # Hidden stems have less weight
    
    # Find dominant element
    dominant_element = max(element_count, key=element_count.get)
    element_names = {"木": "목(木)", "火": "화(火)", "土": "토(土)", "金": "금(金)", "水": "수(水)"}
    
    # Start analysis
    name = "회원"  # Will be replaced in app.py
    analysis_parts.append(f"<strong>{name}</strong>님의 사주를 종합 분석한 결과입니다.")
    analysis_parts.append("")
    
    # Day element analysis
    if day_element:
        analysis_parts.append(f"<strong>일간(日干) 분석:</strong>")
        analysis_parts.append(f"일간은 {day_stem_char}으로, {element_names.get(day_element, day_element)}의 기운을 가지고 있습니다.")
        analysis_parts.append("")
    
    # Element balance analysis
    analysis_parts.append(f"<strong>오행(五行) 균형:</strong>")
    total_count = sum(element_count.values())
    if total_count > 0:
        for elem, count in element_count.items():
            if count > 0:
                percentage = (count / total_count) * 100
                analysis_parts.append(f"- {element_names.get(elem, elem)}: {percentage:.1f}%")
    
    if dominant_element:
        analysis_parts.append(f"전체적으로 <strong>{element_names.get(dominant_element, dominant_element)}</strong>의 기운이 가장 강하게 나타납니다.")
    analysis_parts.append("")
    
    # Twelve fortunes analysis
    if fortunes:
        analysis_parts.append(f"<strong>십이운성(十二運星) 분석:</strong>")
        fortune_meaning = {
            "장생": "새로운 시작과 성장의 기운",
            "목욕": "변화와 적응의 시기",
            "관대": "사회적 인정과 성장",
            "건록": "자신감과 독립성",
            "제왕": "최고의 기운과 성공",
            "쇠": "안정과 성숙",
            "병": "주의와 휴식 필요",
            "사": "변화와 전환점",
            "묘": "은둔과 내면 성찰",
            "절": "새로운 시작의 준비",
            "태": "잠재력과 가능성",
            "양": "성장과 발전"
        }
        
        day_fortune = fortunes[2] if len(fortunes) > 2 else ""
        if day_fortune and day_fortune in fortune_meaning:
            analysis_parts.append(f"일주(日柱)의 운성은 <strong>{day_fortune}</strong>으로, {fortune_meaning.get(day_fortune, '')}을 의미합니다.")
    analysis_parts.append("")
    
    # Sinsal analysis
    if sinsals:
        analysis_parts.append(f"<strong>신살(神煞) 분석:</strong>")
        sinsal_meaning = {
            "천을귀인": "귀인의 도움과 인복",
            "도화": "예술적 재능과 매력",
            "화개": "학문과 지식에 대한 열정",
            "양인": "강한 의지력과 추진력",
            "역마": "변화와 이동이 많은 삶",
            "공망": "허무와 공허함을 느낄 수 있음",
            "장성": "리더십과 지휘 능력"
        }
        
        found_sinsals = []
        for sinsal_str in sinsals:
            if sinsal_str:
                for s in sinsal_str.split():
                    if s not in found_sinsals:
                        found_sinsals.append(s)
        
        if found_sinsals:
            for s in found_sinsals[:3]:  # 최대 3개만 표시
                if s in sinsal_meaning:
                    analysis_parts.append(f"- <strong>{s}</strong>: {sinsal_meaning.get(s, '')}")
    analysis_parts.append("")
    
    # Daeun analysis
    if daeun and 'periods' in daeun:
        analysis_parts.append(f"<strong>대운(大運) 분석:</strong>")
        analysis_parts.append(f"대운 방향은 <strong>{daeun.get('direction', '')}</strong>입니다.")
        if daeun['periods']:
            first_daeun = daeun['periods'][0]
            first_age = int(first_daeun.get('age_start', 0)) % 10
            analysis_parts.append(f"첫 번째 대운은 {first_age}세부터 시작되며, 인생의 큰 흐름이 변화하는 중요한 시기입니다.")
    analysis_parts.append("")
    
    # Overall conclusion
    analysis_parts.append(f"<strong>종합 해석:</strong>")
    if day_element == dominant_element:
        analysis_parts.append(f"일간과 전체 오행이 조화를 이루고 있어, 타고난 성향을 발휘하기에 유리한 사주입니다.")
    else:
        analysis_parts.append(f"일간과 전체 오행의 균형을 맞추는 것이 중요합니다.")
    
    if day_fortune in ["제왕", "건록", "장생"]:
        analysis_parts.append("강한 기운을 가지고 있어 목표를 달성하기에 유리한 시기입니다.")
    elif day_fortune in ["쇠", "병", "사"]:
        analysis_parts.append("신중한 판단과 인내가 필요한 시기입니다.")
    
    return "<br>".join(analysis_parts)

def calculate_tojeong_bigyeol(pillars_info, current_year, pillars_data=None):
    """
    Calculate Tojeong Bigyeol (토정비결) fortune for the current year.
    
    토정비결은 생년의 간지와 올해의 간지를 비교하여 올해의 운세를 예측합니다.
    
    Parameters:
    - pillars_info: 사주 정보 (년, 월, 일, 시 간지 포함)
    - current_year: 현재 연도
    - pillars_data: 사주 기둥 데이터 (선택사항, year_branch를 얻기 위해 사용)
    
    Returns:
    - dict with fortune predictions
    """
    from datetime import datetime
    
    # Get birth year ganji
    birth_year_stem = pillars_info.get('year_stem', '')
    # year_branch는 pillars_data에서 가져오거나, pillars_info에 없다면 pillars_data 사용
    if pillars_data and len(pillars_data) > 0:
        birth_year_branch = pillars_data[0].get('Earthly Branch (지지)', '')
    else:
        # fallback: pillars_info에서 직접 가져오기 시도
        birth_year_branch = pillars_info.get('year_branch', '')
    
    # Extract only Chinese characters (remove Korean pronunciation)
    def extract_char(ganji_str):
        if isinstance(ganji_str, str) and "(" in ganji_str:
            return ganji_str.split()[0]
        return ganji_str
    
    birth_year_stem_char = extract_char(birth_year_stem)
    birth_year_branch_char = extract_char(birth_year_branch)
    
    # Get current year ganji
    current_year_stem, current_year_branch = get_year_ganji(current_year)
    current_year_stem_char = extract_char(current_year_stem)
    current_year_branch_char = extract_char(current_year_branch)
    
    # 토정비결 기본 운세 메시지 (생년 지지와 올해 지지 비교)
    # 삼합, 육합, 형, 충, 해 관계 등을 고려한 간단한 운세
    
    # 지지 인덱스
    branch_idx_map = {extract_char(b): i for i, b in enumerate(EARTHLY_BRANCHES)}
    birth_branch_idx = branch_idx_map.get(birth_year_branch_char, 0)
    current_branch_idx = branch_idx_map.get(current_year_branch_char, 0)
    
    # 삼합 관계 (寅午戌, 申子辰, 亥卯未, 巳酉丑)
    sanhap_groups = [
        [2, 6, 10],  # 寅午戌 (인오술)
        [8, 0, 4],   # 申子辰 (신자진)
        [11, 3, 7],  # 亥卯未 (해묘미)
        [5, 9, 1]    # 巳酉丑 (사유축)
    ]
    
    # 육합 관계 (子丑, 寅亥, 卯戌, 辰酉, 巳申, 午未)
    yukhap_pairs = [
        (0, 1), (2, 11), (3, 10), (4, 9), (5, 8), (6, 7)
    ]
    
    # 형 관계 (子卯, 寅巳申, 丑未戌, 辰午酉亥)
    hyeong_groups = [
        [0, 3], [2, 5, 8], [1, 7, 10], [4, 6, 9, 11]
    ]
    
    # 충 관계 (子午, 丑未, 寅申, 卯酉, 辰戌, 巳亥) - 6충
    chung_pairs = [
        (0, 6), (1, 7), (2, 8), (3, 9), (4, 10), (5, 11)
    ]
    
    # 관계 분석
    relationship = "평상"
    relationship_desc = ""
    fortune_level = "보통"
    fortune_message = ""
    
    # 삼합 확인
    is_sanhap = False
    for group in sanhap_groups:
        if birth_branch_idx in group and current_branch_idx in group:
            is_sanhap = True
            relationship = "삼합"
            relationship_desc = "생년 지지와 올해 지지가 삼합 관계입니다."
            fortune_level = "양호"
            fortune_message = "올해는 인연과 협력이 좋아지는 시기입니다. 새로운 사람들과의 만남이나 기존 관계의 발전이 기대됩니다."
            break
    
    # 육합 확인
    if not is_sanhap:
        is_yukhap = False
        for pair in yukhap_pairs:
            if (birth_branch_idx == pair[0] and current_branch_idx == pair[1]) or \
               (birth_branch_idx == pair[1] and current_branch_idx == pair[0]):
                is_yukhap = True
                relationship = "육합"
                relationship_desc = "생년 지지와 올해 지지가 육합 관계입니다."
                fortune_level = "좋음"
                fortune_message = "올해는 조화와 협력의 기운이 강합니다. 새로운 시작이나 변화에 유리한 시기입니다."
                break
    
    # 충 확인
    if not is_sanhap:
        is_chung = False
        for pair in chung_pairs:
            if (birth_branch_idx == pair[0] and current_branch_idx == pair[1]) or \
               (birth_branch_idx == pair[1] and current_branch_idx == pair[0]):
                is_chung = True
                relationship = "충"
                relationship_desc = "생년 지지와 올해 지지가 충 관계입니다."
                fortune_level = "주의"
                fortune_message = "올해는 변화와 변동이 많은 시기입니다. 새로운 도전을 하기 좋은 때이지만, 신중한 판단이 필요합니다."
                break
    
    # 형 확인
    if not is_sanhap and relationship == "평상":
        is_hyeong = False
        for group in hyeong_groups:
            if birth_branch_idx in group and current_branch_idx in group and birth_branch_idx != current_branch_idx:
                is_hyeong = True
                relationship = "형"
                relationship_desc = "생년 지지와 올해 지지가 형 관계입니다."
                fortune_level = "주의"
                fortune_message = "올해는 약간의 어려움이나 경쟁이 있을 수 있습니다. 인내와 노력으로 극복할 수 있는 시기입니다."
                break
    
    # 기본 메시지 (평상 관계인 경우)
    if relationship == "평상":
        fortune_message = "올해는 평온한 한 해가 될 것입니다. 꾸준한 노력과 계획을 통해 목표를 이루시길 바랍니다."
    
    # 상단 요약 카드: 종합운, 재물운, 연애·인간관계, 건강운, 직장·사업운 점수 계산 (10점 만점)
    def calculate_fortune_scores(rel, level):
        """relationship과 fortune_level에 따라 점수 계산"""
        base_scores = {
            "좋음": {"overall": 8, "wealth": 8, "love": 9, "health": 7, "career": 8},
            "양호": {"overall": 7, "wealth": 7, "love": 8, "health": 7, "career": 7},
            "보통": {"overall": 6, "wealth": 6, "love": 6, "health": 6, "career": 6},
            "주의": {"overall": 5, "wealth": 5, "love": 5, "health": 4, "career": 5}
        }
        
        scores = base_scores.get(level, base_scores["보통"]).copy()
        
        # relationship에 따른 조정
        if rel == "삼합":
            scores["love"] = min(10, scores["love"] + 1)
            scores["career"] = min(10, scores["career"] + 1)
        elif rel == "육합":
            scores["overall"] = min(10, scores["overall"] + 1)
            scores["wealth"] = min(10, scores["wealth"] + 1)
        elif rel == "충":
            scores["career"] = max(4, scores["career"] - 1)
            scores["health"] = max(3, scores["health"] - 1)
        elif rel == "형":
            scores["health"] = max(3, scores["health"] - 1)
            scores["love"] = max(4, scores["love"] - 1)
        
        return scores
    
    fortune_scores = calculate_fortune_scores(relationship, fortune_level)
    
    # 키워드 3개 추출
    def get_keywords(rel, level):
        """relationship과 fortune_level에 따라 키워드 생성"""
        keyword_map = {
            ("삼합", "양호"): ["협력", "인연", "성장"],
            ("삼합", "좋음"): ["협력", "성공", "기회"],
            ("육합", "좋음"): ["조화", "시작", "변화"],
            ("육합", "양호"): ["안정", "협력", "발전"],
            ("충", "주의"): ["변화", "전환", "신중"],
            ("형", "주의"): ["인내", "성장", "주의"],
            ("평상", "보통"): ["안정", "계획", "노력"]
        }
        
        keywords = keyword_map.get((rel, level), None)
        if not keywords:
            # 기본 키워드
            if rel in ["삼합", "육합"]:
                keywords = ["협력", "성장", "기회"]
            elif rel == "충":
                keywords = ["변화", "전환", "신중"]
            elif rel == "형":
                keywords = ["인내", "성장", "주의"]
            else:
                keywords = ["안정", "계획", "노력"]
        
        return keywords
    
    keywords = get_keywords(relationship, fortune_level)
    
    # 연운(年運) 상세 설명
    def get_yearly_detailed_fortune(rel, level, birth_ganji, current_ganji):
        """연운 상세 설명 생성"""
        if rel == "삼합":
            return {
                "traditional": "삼합은 세 개의 지지가 모여 하나의 기운을 만드는 관계로, 협력과 인연의 기운이 강합니다.",
                "interpretation": "올해는 특히 인적 네트워크가 확장되고, 협력 관계에서 큰 도움을 받을 수 있는 시기입니다. 새로운 인연이나 파트너십이 생기거나, 기존 관계가 더욱 깊어질 수 있습니다.",
                "advice": "재테크 측면에서는 공동 투자나 협업 사업에 유리하며, 이직이나 전직을 고려 중이라면 지인들의 추천을 활용하세요. 시험이나 자격증 준비에도 스터디 그룹을 만드는 것이 도움이 됩니다. 인간관계에서는 먼저 도움을 주는 자세가 좋은 결과를 가져올 것입니다."
            }
        elif rel == "육합":
            return {
                "traditional": "육합은 두 개의 지지가 서로 화합하는 관계로, 조화와 균형의 기운이 강합니다.",
                "interpretation": "올해는 안정적인 변화와 새로운 시작의 기운이 강합니다. 급격한 변화보다는 점진적이고 계획적인 변화가 성공으로 이어질 수 있습니다.",
                "advice": "재테크에서는 장기적인 안정 투자에 집중하고, 불필요한 지출을 줄이면서 저축을 늘리는 것이 좋습니다. 직장에서는 새로운 프로젝트나 업무에 도전할 수 있으며, 창업을 고려 중이라면 신중하게 계획을 세우는 것이 중요합니다. 건강 관리에 특히 신경 쓰세요."
            }
        elif rel == "충":
            return {
                "traditional": "충은 서로 대립하는 관계로, 변화와 변동의 기운이 강합니다.",
                "interpretation": "올해는 큰 변화나 전환점이 올 수 있는 시기입니다. 이는 나쁜 것만은 아니며, 오히려 새로운 기회로 작용할 수 있습니다. 하지만 신중한 판단이 필요합니다.",
                "advice": "재테크에서는 급격한 투자를 피하고, 현금 보유 비율을 높이는 것이 안전합니다. 이직이나 전직을 고려 중이라면 충분한 검토 후 결정하세요. 인간관계에서는 갈등이 생기기 쉬우므로, 소통을 잘하고 감정적으로 대응하지 않는 것이 중요합니다. 건강 면에서는 스트레스 관리가 특히 필요합니다."
            }
        elif rel == "형":
            return {
                "traditional": "형은 서로 제약하는 관계로, 약간의 어려움이나 경쟁이 있을 수 있습니다.",
                "interpretation": "올해는 시행착오가 있을 수 있지만, 이를 통해 성장할 수 있는 시기입니다. 인내와 노력이 필요한 한 해입니다.",
                "advice": "재테크에서는 보수적인 접근이 좋으며, 투자보다는 저축에 집중하세요. 직장에서는 경쟁이 치열할 수 있으므로, 자신만의 강점을 살리는 것이 중요합니다. 건강 관리에 특히 주의하시고, 정기적인 건강검진을 받으시기 바랍니다. 인간관계에서는 작은 마찰이 생길 수 있으니, 이해와 배려를 갖춰 대처하세요."
            }
        else:  # 평상
            return {
                "traditional": "평상 관계는 특별한 변화 없이 안정적으로 진행되는 관계입니다.",
                "interpretation": "올해는 특별한 변동 없이 꾸준히 진행되는 시기입니다. 이는 나쁜 것이 아니며, 계획적인 노력을 통해 목표를 달성할 수 있는 시기입니다.",
                "advice": "재테크에서는 장기적인 관점에서 꾸준한 투자를 계속하고, 급격한 변화보다는 안정적인 수익을 추구하세요. 직장에서는 현재의 업무에 충실하면서 점진적으로 발전시켜 나가세요. 건강과 인간관계를 유지하는 것이 중요하며, 새로운 기회를 찾기보다는 기존의 것을 발전시키는 것이 좋습니다."
            }
    
    yearly_fortune = get_yearly_detailed_fortune(relationship, fortune_level, f"{birth_year_stem_char}{birth_year_branch_char}", f"{current_year_stem_char}{current_year_branch_char}")
    
    # 월별 운세 생성 (1~12월)
    def generate_monthly_fortunes(rel, level):
        """월별 운세 생성"""
        months = []
        season_groups = {
            "spring": [3, 4, 5],  # 봄
            "summer": [6, 7, 8],  # 여름
            "autumn": [9, 10, 11],  # 가을
            "winter": [12, 1, 2]  # 겨울
        }
        
        for month in range(1, 13):
            # 계절 결정
            season = None
            for s, m_list in season_groups.items():
                if month in m_list:
                    season = s
                    break
            
            # relationship과 fortune_level에 따른 월별 운세
            if rel in ["삼합", "육합"]:
                if month in [3, 4, 5]:  # 봄
                    summary = "새로운 시작과 기회가 많은 시기입니다."
                    good_period = True
                    themes = ["인연", "협력", "성장"]
                elif month in [6, 7, 8]:  # 여름
                    summary = "활동이 활발하고 발전의 기운이 강한 시기입니다."
                    good_period = True
                    themes = ["사업", "재물", "성공"]
                elif month in [9, 10, 11]:  # 가을
                    summary = "수확과 성과가 나타나는 시기입니다."
                    good_period = True
                    themes = ["재물", "성취", "인정"]
                else:  # 겨울
                    summary = "정리와 준비의 시기입니다."
                    good_period = False
                    themes = ["계획", "준비", "안정"]
            elif rel == "충":
                if month in [1, 2, 3]:  # 초봄
                    summary = "변화의 기운이 강하니 신중하게 대응하세요."
                    good_period = False
                    themes = ["변화", "신중", "주의"]
                elif month in [6, 7, 8]:  # 여름
                    summary = "새로운 기회가 올 수 있지만 신중하게 검토하세요."
                    good_period = True
                    themes = ["기회", "검토", "결정"]
                elif month in [10, 11, 12]:  # 말년
                    summary = "안정을 추구하는 시기입니다."
                    good_period = False
                    themes = ["안정", "정리", "회복"]
                else:
                    summary = "주의와 신중함이 필요한 시기입니다."
                    good_period = False
                    themes = ["주의", "건강", "관계"]
            elif rel == "형":
                if month in [4, 5, 6]:  # 봄~초여름
                    summary = "경쟁이나 어려움이 있을 수 있으나 인내로 극복하세요."
                    good_period = False
                    themes = ["인내", "노력", "극복"]
                elif month in [9, 10, 11]:  # 가을
                    summary = "노력의 결실이 나타나는 시기입니다."
                    good_period = True
                    themes = ["성과", "인정", "보상"]
                else:
                    summary = "꾸준한 노력이 필요한 시기입니다."
                    good_period = False
                    themes = ["노력", "건강", "계획"]
            else:  # 평상
                if month in [3, 4, 5]:  # 봄
                    summary = "새로운 계획을 세우기에 좋은 시기입니다."
                    good_period = True
                    themes = ["계획", "시작", "준비"]
                elif month in [6, 7, 8]:  # 여름
                    summary = "꾸준히 발전하는 시기입니다."
                    good_period = True
                    themes = ["발전", "노력", "실행"]
                elif month in [9, 10, 11]:  # 가을
                    summary = "안정적으로 진행되는 시기입니다."
                    good_period = True
                    themes = ["안정", "유지", "보완"]
                else:  # 겨울
                    summary = "정리와 반성을 통해 내년을 준비하세요."
                    good_period = False
                    themes = ["정리", "반성", "준비"]
            
            months.append({
                "month": month,
                "summary": summary,
                "good_period": good_period,
                "themes": themes
            })
        
        return months
    
    monthly_fortunes = generate_monthly_fortunes(relationship, fortune_level)
    
    # 재테크/커리어 특화 조언
    def get_career_advice(rel, level):
        """재테크/커리어 특화 조언"""
        if rel in ["삼합", "육합"]:
            return {
                "investment": "상반기(1~6월)에는 새로운 투자 기회를 검토하고, 하반기(7~12월)에는 협업이나 공동 투자를 고려해보세요. 장기 투자보다는 중단기 투자에 유리합니다.",
                "career": "이직이나 전직을 고려 중이라면 상반기가 좋은 시기입니다. 새로운 프로젝트나 업무에 적극적으로 도전하세요. 네트워킹이 중요한 시기입니다.",
                "business": "창업을 고려 중이라면 파트너를 찾아 함께 시작하는 것이 좋습니다. 협업 사업이 성공할 가능성이 높습니다."
            }
        elif rel == "충":
            return {
                "investment": "상반기(1~6월)에는 투자를 삼가고 현금 보유 비율을 높이세요. 하반기(7~12월)에 조금씩 안정적인 투자로 전환하세요. 급격한 변동에 대비하세요.",
                "career": "이직이나 전직을 고려 중이라면 충분한 검토 후 결정하세요. 급하게 결정하지 말고, 여러 옵션을 비교해보세요. 변화에 대비한 준비가 필요합니다.",
                "business": "창업을 고려 중이라면 신중하게 검토하세요. 시장 상황을 충분히 분석하고, 리스크 관리에 특히 주의하세요."
            }
        elif rel == "형":
            return {
                "investment": "전체적으로 보수적인 접근이 좋습니다. 안정적인 자산에 집중하고, 리스크가 큰 투자는 피하세요. 저축을 늘리는 데 집중하세요.",
                "career": "현재 직장에서의 안정을 우선시하세요. 무리한 도전보다는 자신의 강점을 살리는 업무에 집중하세요. 건강 관리가 중요합니다.",
                "business": "창업은 신중하게 검토하세요. 준비가 완벽할 때까지 기다리는 것도 방법입니다."
            }
        else:  # 평상
            return {
                "investment": "장기적인 관점에서 꾸준한 투자를 계속하세요. 급격한 변화보다는 안정적인 수익을 추구하세요.",
                "career": "현재의 업무에 충실하면서 점진적으로 발전시켜 나가세요. 새로운 기회를 찾기보다는 기존의 것을 발전시키는 것이 좋습니다.",
                "business": "기존 사업을 안정적으로 운영하면서 점진적으로 확장하는 것이 좋습니다."
            }
    
    career_advice = get_career_advice(relationship, fortune_level)
    
    # 행동 체크리스트/TODO (월별 3개씩)
    def get_action_checklist(rel, level):
        """행동 체크리스트/TODO 생성"""
        if rel in ["삼합", "육합"]:
            return {
                "relationship": ["오래 연락 안 한 친구 1명에게 연락하기", "새로운 모임이나 네트워킹 이벤트 참여하기", "가족이나 친구들과 함께할 활동 계획하기"],
                "wealth": ["이번 달 고정지출 1개 줄이기", "월말까지 저축 목표 금액 정하기", "재테크 관련 정보 수집 및 학습하기"],
                "health": ["주 2회 이상 30분 유산소 운동", "건강검진 일정 잡기", "규칙적인 수면 패턴 유지하기"],
                "career": ["직장 내 네트워킹 이벤트 참여하기", "자기계발 강좌나 세미나 신청하기", "업무 목표와 계획 재점검하기"]
            }
        elif rel == "충":
            return {
                "relationship": ["갈등이 생기지 않도록 소통 강화하기", "가족이나 지인들과 정기적으로 시간 내기", "감정적으로 대응하지 않고 신중하게 생각하기"],
                "wealth": ["긴급 자금 마련하기", "불필요한 지출 줄이기", "현금 보유 비율 점검하기"],
                "health": ["스트레스 관리 방법 찾기 (명상, 운동 등)", "건강검진 받기", "규칙적인 생활 패턴 유지하기"],
                "career": ["이직이나 전직을 위한 정보 수집하기", "스킬 업그레이드를 위한 학습 계획하기", "현재 업무 상황 정리 및 대안 검토하기"]
            }
        elif rel == "형":
            return {
                "relationship": ["작은 마찰을 피하기 위해 배려하기", "오해를 방지하기 위한 명확한 소통하기", "가족이나 동료들에게 도움 주기"],
                "wealth": ["저축 목표 금액 설정하기", "불필요한 구매 삼가하기", "장기 재테크 계획 수립하기"],
                "health": ["정기적인 건강검진 받기", "건강한 식습관 유지하기", "충분한 휴식 시간 확보하기"],
                "career": ["현재 업무에 집중하며 성과 내기", "자신의 강점을 살리는 업무 찾기", "스트레스 관리를 위한 휴식 계획하기"]
            }
        else:  # 평상
            return {
                "relationship": ["가족이나 친구들과 정기적으로 연락하기", "새로운 인연 만들기", "감사 인사 전하기"],
                "wealth": ["월별 저축 목표 설정하기", "소비 패턴 점검하기", "장기 재테크 계획 검토하기"],
                "health": ["규칙적인 운동 습관 만들기", "건강한 식습관 유지하기", "충분한 수면 시간 확보하기"],
                "career": ["현재 업무 목표 달성하기", "자기계발 계획 수립하기", "업무 효율성 개선하기"]
            }
    
    action_checklist = get_action_checklist(relationship, fortune_level)
    
    # 월별 운세 (간단한 안내) - 기존 호환성 유지
    monthly_guidance = "월별로는 봄에는 새로운 시작, 여름에는 발전, 가을에는 수확, 겨울에는 준비의 시기입니다."
    
    return {
        "birth_year_ganji": f"{birth_year_stem_char}{birth_year_branch_char}",
        "current_year_ganji": f"{current_year_stem_char}{current_year_branch_char}",
        "current_year": current_year,
        "relationship": relationship,
        "relationship_desc": relationship_desc,
        "fortune_level": fortune_level,
        "fortune_message": fortune_message,
        "monthly_guidance": monthly_guidance,
        # 새로 추가된 필드들
        "fortune_scores": fortune_scores,
        "keywords": keywords,
        "yearly_fortune": yearly_fortune,
        "monthly_fortunes": monthly_fortunes,
        "career_advice": career_advice,
        "action_checklist": action_checklist
    }

def get_solar_terms(year):
    """
    Return list of (Date, TermName) for the year using Ephem.
    Terms: Ipchun (315), Usu (330)...
    Returns: List of (datetime, term_name_korean) tuples for the 24 solar terms.
    """
    # 24 solar terms: angles and Korean names
    # Starting from Ipchun (315 deg, approx Feb 4)
    solar_term_data = [
        (315, "입춘"), (330, "우수"), (345, "경칩"), (0, "춘분"),
        (15, "청명"), (30, "곡우"), (45, "입하"), (60, "소만"),
        (75, "망종"), (90, "하지"), (105, "소서"), (120, "대서"),
        (135, "입추"), (150, "처서"), (165, "백로"), (180, "추분"),
        (195, "한로"), (210, "상강"), (225, "입동"), (240, "소설"),
        (255, "대설"), (270, "동지"), (285, "소한"), (300, "대한")
    ]
    
    terms = []
    s = ephem.Sun()
    obs = ephem.Observer()
    
    # Start from previous year's Ipchun to catch the first term of the target year
    # (since the year starts at Ipchun, we need to go back to find it)
    search_start = datetime(year - 1, 2, 3)  # Approximate start
    
    for angle_deg, term_name in solar_term_data:
        target_rad = angle_deg * ephem.pi / 180
        
        # Find the occurrence of this term in the target year
        # For angles >= 315, it's in Feb-Mar of the target year
        # For angles < 315, it's from Mar (year) to Jan (year+1)
        if angle_deg >= 315:
            # Ipchun (315), Usu (330), Gyeongchip (345) occur in Feb-Mar
            start_search = datetime(year, 1, 25)
            end_search = datetime(year, 4, 10)
        else:
            # Other terms occur from Mar (year) to Jan (year+1)
            start_search = datetime(year, 2, 25)
            end_search = datetime(year + 1, 2, 10)
        
        # Binary search approach: check each day to find when sun reaches target angle
        best_date = None
        min_diff = float('inf')
        
        # Search day by day
        current_date = start_search
        while current_date < end_search:
            utc_datetime = current_date - timedelta(hours=9)
            obs.date = ephem.Date(utc_datetime)
            s.compute(obs)
            ecl = ephem.Ecliptic(s.ra, s.dec)
            current_long = float(ecl.lon) * 180 / ephem.pi
            current_long = current_long % 360
            
            # Calculate difference (handling wrap-around at 0/360)
            if angle_deg == 0:
                # Special case: 0 degrees (360 degrees)
                diff1 = abs(current_long - 0)
                diff2 = abs(current_long - 360)
                diff = min(diff1, diff2)
            else:
                diff = abs(current_long - angle_deg)
                # Also check wrap-around case
                if angle_deg > 350:  # Near 360, check wrap to 0
                    diff = min(diff, abs(current_long + 360 - angle_deg))
                elif angle_deg < 10:  # Near 0, check wrap from 360
                    diff = min(diff, abs(current_long - 360 - angle_deg))
            
            if diff < min_diff:
                min_diff = diff
                best_date = current_date
                # If very close, refine with hourly search
                if diff < 1.0:
                    # Refine with hourly precision
                    for hour_offset in range(-12, 13):
                        refined = current_date + timedelta(hours=hour_offset)
                        utc_refined = refined - timedelta(hours=9)
                        obs.date = ephem.Date(utc_refined)
                        s.compute(obs)
                        ecl = ephem.Ecliptic(s.ra, s.dec)
                        refined_long = float(ecl.lon) * 180 / ephem.pi
                        refined_long = refined_long % 360
                        
                        if angle_deg == 0:
                            rdiff1 = abs(refined_long - 0)
                            rdiff2 = abs(refined_long - 360)
                            rdiff = min(rdiff1, rdiff2)
                        else:
                            rdiff = abs(refined_long - angle_deg)
                            if angle_deg > 350:
                                rdiff = min(rdiff, abs(refined_long + 360 - angle_deg))
                            elif angle_deg < 10:
                                rdiff = min(rdiff, abs(refined_long - 360 - angle_deg))
                        
                        if rdiff < min_diff:
                            min_diff = rdiff
                            best_date = refined
                    break
            
            current_date += timedelta(days=1)
        
        if best_date:
            # For saju logic, the year starts at Ipchun (Feb)
            # Terms >= 315 occur in Feb-Mar of target year
            # Terms < 315 occur in Mar-Jan of target/next year
            # We want all terms from Feb (year) to Jan (year+1)
            if angle_deg >= 315:
                # Should be in Feb-Mar of target year
                if best_date >= datetime(year, 2, 1) and best_date < datetime(year, 4, 1):
                    terms.append((best_date, term_name))
            else:
                # Should be in Mar (year) to Jan (year+1)
                if (best_date >= datetime(year, 3, 1) and best_date < datetime(year + 1, 2, 1)):
                    terms.append((best_date, term_name))
    
    # Sort by date
    terms.sort(key=lambda x: x[0])
    return terms 

def calculate_pillars(dob_date, dob_time, is_lunar=False):
    """
    Main function to calculate Four Pillars.
    dob_date: datetime.date
    dob_time: datetime.time (None일 경우 정오 12시 사용)
    """
    # dob_time이 None이거나 time 객체가 아니면 기본값으로 정오 12시 사용
    from datetime import time as dt_time
    if dob_time is None or not isinstance(dob_time, dt_time):
        dob_time = dt_time(12, 0)
    
    # 1. Lunar -> Solar conversion if needed
    if is_lunar:
        calendar = KoreanLunarCalendar()
        calendar.setLunarDate(dob_date.year, dob_date.month, dob_date.day, False) # False = not leap (needs input)
        # TODO: Handle leap month UI input if we want perfection.
        # Get solar date from calendar attributes
        year = calendar.solarYear
        month = calendar.solarMonth
        day = calendar.solarDay
        dob_solar = datetime(year, month, day, dob_time.hour, dob_time.minute)
    else:
        dob_solar = datetime(dob_date.year, dob_date.month, dob_date.day, dob_time.hour, dob_time.minute)
    
    year = dob_solar.year
    month = dob_solar.month
    day = dob_solar.day
    hour = dob_solar.hour
    
    # 2. Determine Year Pillar (Check Ipchun)
    # We need the Ipchun time for the birth year.
    s = ephem.Sun()
    
    def get_solar_long(dt):
        observer = ephem.Observer()
        observer.date = dt
        s.compute(observer)
        # return longitude in degrees
        return float(s.hlon) * 180 / ephem.pi

    # Ipchun is at 315 degrees.
    # We need to see if the current date is before or after Ipchun of that year.
    # Quick check: Ipchun is usually Feb 4.
    # If date is Jan, it's definitely prev year.
    # If date is Feb, we need precision.
    
    # Algorithm: Find the exact Ipchun date for the birth year.
    # Ephem Newton method to find when hlon == 315 deg.
    
    def find_term_date(year, target_deg):
        # target_deg in radians
        target_rad = target_deg * ephem.pi / 180
        
        # Start search around Feb 4 for Ipchun (315)
        # Or generalize: 
        # 0 (Mar 20), 15, 30 ...
        # Ipchun (315) is roughly Feb 4.
        
        start_date = datetime(year, 2, 3) # approximate
        if target_deg == 315:
             start_date = datetime(year, 2, 3)
        # This is hard to generalize for all terms quickly without a table.
        # But we only need to know the Month Index.
        pass
    
    # BETTER APPROACH:
    # 1. Calculate Solar Longitude of the birth moment.
    # 2. Convert Longitude to Month Index.
    # Ipchun (315) -> Month 1 (Tiger)
    # Usu (330) -> Mid-Month 1
    # Gyeongchip (345) -> Month 2 (Rabbit)
    # Chunbun (0) -> Mid-Month 2
    # Cheongmyeong (15) -> Month 3 (Dragon)
    
    # So, Month starts at 315, 345, 15, 45, 75, 105, 135, 165, 195, 225, 255, 285.
    
    obs = ephem.Observer()
    # Ephem uses UTC. Convert KST to UTC by subtracting 9 hours
    # Use ephem.Date for proper date handling
    utc_datetime = dob_solar - timedelta(hours=9)
    obs.date = ephem.Date(utc_datetime)
    s.compute(obs)
    # Use ecliptic longitude (not heliocentric longitude)
    ecl = ephem.Ecliptic(s.ra, s.dec)
    long_deg = float(ecl.lon) * 180 / ephem.pi
    
    # Normalize to 0-360
    long_deg = long_deg % 360
    
    # Determine Saju Month Index (0=Tiger, 1=Rabbit...)
    # 315 <= L < 345 : Tiger (Month 1 in Saju, usually Solar Feb)
    # 345 <= L < 15 (375) : Rabbit
    # ...
    
    # Pivot at 315 (Ipchun). 
    # Let's shift logic: Relative to 315.
    # (L - 315) % 360
    # 0-30: Tiger
    # 30-60: Rabbit
    # ...
    
    rel_long = (long_deg - 315) % 360
    month_idx = int(rel_long // 30) # 0 to 11
    
    # Determine Saju Year
    # If we are before Ipchun (long < 315 and long > 270 approx... wait)
    # Actually, simplistic check: 
    # If date is Jan 1 to Feb 3, long is roughly 280-314.
    # If long is between 270 (Dongji) and 315 (Ipchun), it is typically "Previous Year" in some schools,
    # BUT standard Saju changes year at Ipchun.
    # So if we are currently in the [315, 360) range or [0, 315) range?
    # Wait, Ipchun is 315.
    # So if long < 315 (and > 270 i.e. Jan/Feb), it is late winter of previous year?
    # NO. Longitude increases.
    # Winter Solstice is 270.
    # Ipchun is 315.
    # So if the sun is between 315 and 360, or 0 and 315?
    # 315 is the Start of Spring.
    # If current longitude is >= 315 (until 360) OR >= 0 (until next 315? No).
    # Solar longitude goes 0 -> 360.
    # 315 is in Feb.
    # 0 is in Mar.
    # So Year starts when Longitude hits 315.
    # If calculated longitude is, say, 300 (Jan), it is BEFORE Ipchun.
    # So we use (Year - 1).
    
    # How to detect "Before Ipchun"?
    # The `long_deg` we got is for the *current* time.
    # If `long_deg` < 315 and month is 1 or 2 (early), it's previous year.
    # But wait, 270 is Dec. 
    # 300 is Jan.
    # 315 is Feb 4.
    # So if long_deg < 315 and long_deg > 270? (Jan/Feb before Ipchun) -> Previous Year.
    # If long_deg >= 315? -> Current Year.
    # If long_deg < 100 (Spring/Summer)? -> Current Year.
    
    full_year_check = year
    # Refine year logic:
    # If date is early year (Jan/Feb) and long < 315:
    # Then it belongs to previous year pillar.
    if dob_solar.month <= 2 and long_deg > 270 and long_deg < 315:
        full_year_check = year - 1
        
    saju_year_stem, saju_year_branch = get_year_ganji(full_year_check)
    
    # Month
    saju_year_stem_idx = HEAVENLY_STEMS.index(saju_year_stem)
    saju_month_stem, saju_month_branch = get_month_ganji(saju_year_stem_idx, month_idx)
    
    # Day
    # Day Ganji is independent of year/month, it's just continuous count.
    saju_day_stem, saju_day_branch = get_day_ganji(dob_solar)
    
    # Hour
    # Depends on Day Stem (which we just found).
    saju_day_stem_idx = HEAVENLY_STEMS.index(saju_day_stem)
    saju_hour_stem, saju_hour_branch = get_hour_ganji(saju_day_stem_idx, dob_solar.hour)
    
    # Get hidden stems (지장간) for each branch
    year_hidden = HIDDEN_STEMS.get(saju_year_branch, [])
    month_hidden = HIDDEN_STEMS.get(saju_month_branch, [])
    day_hidden = HIDDEN_STEMS.get(saju_day_branch, [])
    hour_hidden = HIDDEN_STEMS.get(saju_hour_branch, [])
    
    # Calculate ten gods for hidden stems (based on day stem)
    # Format: return list of [stem_char, ten_god] pairs
    def format_hidden_stems_with_ten_gods(hidden_stems, day_stem_idx):
        if not hidden_stems:
            return []
        result = []
        for hidden_stem in hidden_stems:
            hidden_stem_idx = HEAVENLY_STEMS.index(hidden_stem)
            ten_god = get_ten_god(day_stem_idx, hidden_stem_idx)
            # Extract only the Chinese character (remove Korean pronunciation)
            stem_char = hidden_stem.split()[0]  # Get "甲" from "甲 (갑)"
            result.append({"stem": stem_char, "ten_god": ten_god})
        return result
    
    year_hidden_list = format_hidden_stems_with_ten_gods(year_hidden, saju_day_stem_idx)
    month_hidden_list = format_hidden_stems_with_ten_gods(month_hidden, saju_day_stem_idx)
    day_hidden_list = format_hidden_stems_with_ten_gods(day_hidden, saju_day_stem_idx)
    hour_hidden_list = format_hidden_stems_with_ten_gods(hour_hidden, saju_day_stem_idx)
    
    # Extract Chinese characters only (remove Korean pronunciation)
    def get_stem_char(stem_str):
        return stem_str.split()[0]  # Get "甲" from "甲 (갑)"
    
    def get_branch_char(branch_str):
        return branch_str.split()[0]  # Get "子" from "子 (자)"
    
    return [
        {"Pillar": "Year (년)", "Heavenly Stem (천간)": get_stem_char(saju_year_stem), "Earthly Branch (지지)": get_branch_char(saju_year_branch), "Hidden Stems (지장간)": year_hidden_list},
        {"Pillar": "Month (월)", "Heavenly Stem (천간)": get_stem_char(saju_month_stem), "Earthly Branch (지지)": get_branch_char(saju_month_branch), "Hidden Stems (지장간)": month_hidden_list},
        {"Pillar": "Day (일)", "Heavenly Stem (천간)": get_stem_char(saju_day_stem), "Earthly Branch (지지)": get_branch_char(saju_day_branch), "Hidden Stems (지장간)": day_hidden_list},
        {"Pillar": "Hour (시)", "Heavenly Stem (천간)": get_stem_char(saju_hour_stem), "Earthly Branch (지지)": get_branch_char(saju_hour_branch), "Hidden Stems (지장간)": hour_hidden_list}
    ], {
        "year_stem": saju_year_stem,
        "year_stem_idx": saju_year_stem_idx,
        "month_stem": saju_month_stem,
        "month_branch": saju_month_branch,
        "month_stem_idx": HEAVENLY_STEMS.index(saju_month_stem),
        "month_branch_idx": EARTHLY_BRANCHES.index(saju_month_branch),
        "day_stem": saju_day_stem,
        "day_branch": saju_day_branch,
        "birth_datetime": dob_solar
    }

def prepare_ai_input(pillars_data, pillars_info, daeun_data, fortunes, sinsals, gender, current_age, current_year, current_daeun_period=None, current_year_ganji=None):
    """
    Formats the Saju calculation results into the JSON structure required by the AI Analyst.
    
    Args:
        current_daeun_period: Dictionary with current daeun period info (ganji, age_start, etc.)
        current_year_ganji: Tuple of (heavenly_stem, earthly_branch) for current year, e.g., ("丙", "午")
    """
    # Helper to get char only
    def get_char(s):
        return s.split()[0] if s else ""

    # Element Analysis
    elements = {"wood": 0, "fire": 0, "earth": 0, "metal": 0, "water": 0}
    yin_yang = {"yang": 0, "yin": 0}
    
    # Map for counting (simplified)
    elem_map = {"木": "wood", "火": "fire", "土": "earth", "金": "metal", "水": "water"}
    
    # Analyze pillars for counts
    all_chars = []
    # Stems
    for key in ["year_stem", "month_stem", "day_stem"]:
         char = pillars_info.get(key)
         full_char = next((s for s in HEAVENLY_STEMS if s.startswith(char)), None)
         if full_char:
             elem = FIVE_ELEMENTS.get(full_char)
             if elem: elements[elem_map[elem]] += 1
    
    # Branches (need to look up element)
    # This part requires iterating pillars_data because pillars_info doesn't have all branch full strings easily accessible for element lookup if we only stored partials.
    # Actually pillars_data has the full chars in 'Heavenly Stem' and 'Earthly Branch' if properly returned, but the current return above cuts them.
    # Let's use pillars_info to reconstruct or lookup.
    
    # Re-accessing data logic for elements might be complex if we only have the display strings.
    # For now, let's trust the AI can infer some if we give it the characters, but the prompt asks for specific counts.
    # Let's do a quick lookup based on characters in pillars_data which are just chars now.
    
    for p in pillars_data:
        stem = p["Heavenly Stem (천간)"]
        branch = p["Earthly Branch (지지)"]
        
        # Stem Element
        # Need to find full string to use FIVE_ELEMENTS dict which uses "甲 (갑)" keys
        stem_full = next((s for s in HEAVENLY_STEMS if s.startswith(stem)), None)
        if stem_full:
            e = FIVE_ELEMENTS[stem_full]
            elements[elem_map[e]] += 1
            # Yin/Yang (simple alternate logic: 甲=Yang, 乙=Yin...)
            idx = HEAVENLY_STEMS.index(stem_full)
            if idx % 2 == 0: yin_yang["yang"] += 1
            else: yin_yang["yin"] += 1
            
        # Branch Element
        branch_full = next((s for s in EARTHLY_BRANCHES if s.startswith(branch)), None)
        if branch_full:
            e = BRANCH_ELEMENTS[branch_full]
            elements[elem_map[e]] += 1
            idx = EARTHLY_BRANCHES.index(branch_full)
            # Branch Yin/Yang is complex, simplified here:
            # Sub(Rat):Yang, Chuk:Yin... 
            if idx % 2 == 0: yin_yang["yang"] += 1
            else: yin_yang["yin"] += 1

    # Format Pillars
    formatted_pillar = {
        "year": {"heavenlyStem": pillars_data[0]["Heavenly Stem (천간)"], "earthlyBranch": pillars_data[0]["Earthly Branch (지지)"]},
        "month": {"heavenlyStem": pillars_data[1]["Heavenly Stem (천간)"], "earthlyBranch": pillars_data[1]["Earthly Branch (지지)"]},
        "day": {"heavenlyStem": pillars_data[2]["Heavenly Stem (천간)"], "earthlyBranch": pillars_data[2]["Earthly Branch (지지)"]},
        "hour": {"heavenlyStem": pillars_data[3]["Heavenly Stem (천간)"], "earthlyBranch": pillars_data[3]["Earthly Branch (지지)"]}
    }

    # Sibiunseong
    formatted_sibi = {
        "year": fortunes[0],
        "month": fortunes[1],
        "day": fortunes[2],
        "hour": fortunes[3]
    }
    
    # Daeun (Format first 3 for context)
    formatted_daeun = []
    for d in daeun_data["periods"][:3]:
        formatted_daeun.append({
            "age": d.get("age_start", 0),
            "heavenlyStem": d["ganji"].split()[0], # Just char
            "earthlyBranch": d["ganji"].split()[1] if len(d["ganji"].split()) > 1 else "",
            "period": "10년" # Approx
        })

    result = {
        "pillar": formatted_pillar,
        "dayMaster": pillars_data[2]["Heavenly Stem (천간)"],
        "elements": elements,
        "yinYang": yin_yang,
        "sipseong": { "note": "AI will calculate based on Day Master" }, # Simplified for now
        "sinsal": sinsals,
        "sibiunseong": formatted_sibi,
        "daeun": formatted_daeun,
        "currentAge": current_age,
        "currentYear": current_year,
        "gender": gender
    }
    
    # Add current daeun period if provided
    if current_daeun_period:
        result["currentDaeun"] = {
            "ganji": current_daeun_period.get("ganji", ""),
            "ageStart": current_daeun_period.get("age_start", 0),
            "heavenlyStem": current_daeun_period["ganji"].split()[0] if current_daeun_period.get("ganji") else "",
            "earthlyBranch": current_daeun_period["ganji"].split()[1] if current_daeun_period.get("ganji") and len(current_daeun_period["ganji"].split()) > 1 else ""
        }
    
    # Add current year ganji if provided
    if current_year_ganji:
        year_stem, year_branch = current_year_ganji
        result["currentYearGanji"] = {
            "heavenlyStem": year_stem,
            "earthlyBranch": year_branch,
            "ganji": f"{year_stem}{year_branch}"
        }
    
    return result

if __name__ == "__main__":
    # Test
    now = datetime.now()
    print(calculate_pillars(now.date(), now.time()))
