"""
띠별 운세 유틸리티
"""

# 12띠 정보
ZODIAC_INFO = {
    "rat": {
        "korean": "쥐띠", "emoji": "🐭", "english": "Rat",
        "years_mod": 0,  # 1900년이 쥐띠 → year % 12 == 4
        "element": "水", "yin_yang": "양(陽)",
        "years_example": [1900, 1912, 1924, 1936, 1948, 1960, 1972, 1984, 1996, 2008, 2020],
        "personality": "쥐띠는 영리하고 재치가 넘치며 적응력이 뛰어납니다. 사교적이고 카리스마가 있어 사람들을 끌어당기는 매력이 있습니다. 계획을 잘 세우고 기회를 포착하는 능력이 탁월합니다.",
        "strengths": ["영리함", "적응력", "사교성", "기회 포착력", "재치"],
        "weaknesses": ["우유부단", "소심함", "지나친 계산", "비밀주의"],
        "lucky_numbers": [2, 3],
        "lucky_colors": ["파란색", "금색", "초록색"],
        "lucky_direction": "북쪽",
        "career": "비즈니스, 금융, 작가, 정치인, 연구원",
        "compatible": ["용띠", "원숭이띠", "소띠"],
        "incompatible": ["말띠", "양띠"],
        "2026_fortune": "2026년 병오년(丙午)은 쥐띠에게 변화와 도전의 해입니다. 상반기에는 새로운 기회가 찾아오며, 특히 재물운이 상승합니다. 하반기에는 인간관계에 집중하고 협력을 강화하는 것이 중요합니다. 건강 관리에 주의를 기울이세요.",
    },
    "ox": {
        "korean": "소띠", "emoji": "🐂", "english": "Ox",
        "years_mod": 1,
        "element": "土", "yin_yang": "음(陰)",
        "years_example": [1901, 1913, 1925, 1937, 1949, 1961, 1973, 1985, 1997, 2009, 2021],
        "personality": "소띠는 성실하고 인내심이 강하며 믿음직스럽습니다. 한번 목표를 정하면 끝까지 밀고 나가는 끈기와 책임감이 있습니다. 조용하지만 강한 내면을 가지고 있습니다.",
        "strengths": ["성실함", "인내심", "책임감", "신뢰성", "끈기"],
        "weaknesses": ["완고함", "변화 거부", "고집", "표현 부족"],
        "lucky_numbers": [1, 4],
        "lucky_colors": ["흰색", "노란색", "초록색"],
        "lucky_direction": "북동쪽",
        "career": "농업, 의학, 법률, 엔지니어링, 예술",
        "compatible": ["쥐띠", "닭띠", "뱀띠"],
        "incompatible": ["양띠", "말띠", "개띠"],
        "2026_fortune": "2026년은 소띠에게 안정과 성취의 해입니다. 꾸준한 노력이 결실을 맺는 시기로, 직장이나 사업에서 인정받을 기회가 옵니다. 새로운 도전보다는 기존 역량을 강화하는 데 집중하세요. 연애운도 긍정적입니다.",
    },
    "tiger": {
        "korean": "호랑이띠", "emoji": "🐯", "english": "Tiger",
        "years_mod": 2,
        "element": "木", "yin_yang": "양(陽)",
        "years_example": [1902, 1914, 1926, 1938, 1950, 1962, 1974, 1986, 1998, 2010, 2022],
        "personality": "호랑이띠는 용감하고 카리스마 넘치며 독립심이 강합니다. 열정적이고 경쟁심이 강해 어떤 일에서든 최선을 다합니다. 리더십이 뛰어나고 정의감이 강합니다.",
        "strengths": ["용감함", "리더십", "열정", "독립심", "정의감"],
        "weaknesses": ["성급함", "고집", "과도한 자신감", "지나친 경쟁심"],
        "lucky_numbers": [1, 3, 4],
        "lucky_colors": ["파란색", "회색", "주황색"],
        "lucky_direction": "동쪽",
        "career": "군인, 경찰, 정치인, 사업가, 운동선수",
        "compatible": ["말띠", "개띠", "돼지띠"],
        "incompatible": ["원숭이띠", "뱀띠"],
        "2026_fortune": "2026년은 호랑이띠에게 도약의 해입니다. 준비해온 일들이 빛을 발하며 새로운 기회가 찾아옵니다. 특히 상반기에 중요한 결정을 내릴 기회가 있으니 신중하게 판단하세요. 재물운과 직장운이 함께 상승하는 좋은 해입니다.",
    },
    "rabbit": {
        "korean": "토끼띠", "emoji": "🐰", "english": "Rabbit",
        "years_mod": 3,
        "element": "木", "yin_yang": "음(陰)",
        "years_example": [1903, 1915, 1927, 1939, 1951, 1963, 1975, 1987, 1999, 2011, 2023],
        "personality": "토끼띠는 온화하고 섬세하며 예술적 감각이 뛰어납니다. 사교성이 좋고 타인을 배려하는 마음이 깊습니다. 직관력이 뛰어나고 기회를 잘 포착합니다.",
        "strengths": ["섬세함", "사교성", "예술성", "직관력", "배려심"],
        "weaknesses": ["우유부단", "소심함", "감정 기복", "회피적"],
        "lucky_numbers": [3, 4, 9],
        "lucky_colors": ["빨간색", "분홍색", "보라색", "파란색"],
        "lucky_direction": "동쪽",
        "career": "외교관, 작가, 디자이너, 상담사, 예술가",
        "compatible": ["양띠", "돼지띠", "개띠"],
        "incompatible": ["닭띠", "용띠"],
        "2026_fortune": "2026년은 토끼띠에게 인간관계가 중심이 되는 해입니다. 새로운 인연이 중요한 기회로 연결될 수 있으며, 협력 관계에서 큰 이득을 얻을 수 있습니다. 예술이나 창작 활동에서 좋은 성과를 거둘 수 있는 해입니다.",
    },
    "dragon": {
        "korean": "용띠", "emoji": "🐲", "english": "Dragon",
        "years_mod": 4,
        "element": "土", "yin_yang": "양(陽)",
        "years_example": [1904, 1916, 1928, 1940, 1952, 1964, 1976, 1988, 2000, 2012, 2024],
        "personality": "용띠는 카리스마 넘치고 자신감이 강하며 야망이 큽니다. 타고난 리더로 사람들을 이끄는 능력이 탁월합니다. 혁신적이고 창의적이며 큰 꿈을 꿉니다.",
        "strengths": ["카리스마", "자신감", "리더십", "창의성", "야망"],
        "weaknesses": ["자만", "고집", "참을성 부족", "완벽주의"],
        "lucky_numbers": [1, 6, 7],
        "lucky_colors": ["금색", "은색", "노란색", "회색"],
        "lucky_direction": "동쪽, 북쪽",
        "career": "CEO, 정치인, 예술가, 군인, 방송인",
        "compatible": ["쥐띠", "원숭이띠", "닭띠"],
        "incompatible": ["개띠", "토끼띠"],
        "2026_fortune": "2026년은 용띠에게 확장과 성장의 해입니다. 사업이나 직장에서 중요한 전환점이 찾아올 수 있으며, 대담한 결정이 큰 성과로 이어집니다. 다만 지나친 자신감은 경계하고, 주변의 조언에 귀 기울이는 것이 중요합니다.",
    },
    "snake": {
        "korean": "뱀띠", "emoji": "🐍", "english": "Snake",
        "years_mod": 5,
        "element": "火", "yin_yang": "음(陰)",
        "years_example": [1905, 1917, 1929, 1941, 1953, 1965, 1977, 1989, 2001, 2013, 2025],
        "personality": "뱀띠는 지혜롭고 신중하며 직관력이 뛰어납니다. 깊은 생각과 통찰력을 가지고 있어 문제 해결 능력이 뛰어납니다. 우아하고 매력적이며 비밀스러운 면이 있습니다.",
        "strengths": ["지혜", "직관력", "신중함", "통찰력", "우아함"],
        "weaknesses": ["의심", "비밀주의", "질투심", "완고함"],
        "lucky_numbers": [2, 8, 9],
        "lucky_colors": ["빨간색", "밝은 노란색", "검은색"],
        "lucky_direction": "남쪽",
        "career": "철학자, 심리학자, 점성술사, 작가, 재정 전문가",
        "compatible": ["소띠", "닭띠"],
        "incompatible": ["호랑이띠", "돼지띠"],
        "2026_fortune": "2026년은 뱀띠에게 내면 성장과 실력을 쌓는 해입니다. 직접적인 성과보다는 기반을 다지는 시기이며, 학업이나 자기 개발에 투자하면 나중에 큰 보상이 옵니다. 재물 관리에 신중함이 요구됩니다.",
    },
    "horse": {
        "korean": "말띠", "emoji": "🐴", "english": "Horse",
        "years_mod": 6,
        "element": "火", "yin_yang": "양(陽)",
        "years_example": [1906, 1918, 1930, 1942, 1954, 1966, 1978, 1990, 2002, 2014, 2026],
        "personality": "말띠는 활동적이고 자유를 사랑하며 열정이 넘칩니다. 독립적이고 자신감이 강하며 어떤 환경에서도 빠르게 적응합니다. 유머 감각이 뛰어나고 사교적입니다.",
        "strengths": ["활동성", "열정", "자유로움", "적응력", "유머"],
        "weaknesses": ["인내 부족", "변덕", "충동성", "자기중심적"],
        "lucky_numbers": [2, 3, 7],
        "lucky_colors": ["노란색", "초록색", "빨간색"],
        "lucky_direction": "남쪽",
        "career": "스포츠, 여행, 영업, 정치, 언론",
        "compatible": ["호랑이띠", "양띠", "개띠"],
        "incompatible": ["쥐띠", "소띠"],
        "2026_fortune": "2026년 병오년(丙午)은 말띠의 해입니다! 본명년(本命年)인 만큼 큰 변화와 기회가 찾아옵니다. 새로운 시작에 최적의 시기이며, 용기 있는 결정이 인생을 바꿀 수 있습니다. 붉은 실을 착용하면 액운을 막는다고 전해집니다.",
    },
    "sheep": {
        "korean": "양띠", "emoji": "🐑", "english": "Sheep",
        "years_mod": 7,
        "element": "土", "yin_yang": "음(陰)",
        "years_example": [1907, 1919, 1931, 1943, 1955, 1967, 1979, 1991, 2003, 2015, 2027],
        "personality": "양띠는 온화하고 친절하며 예술적 감수성이 풍부합니다. 타인에 대한 배려심이 깊고 평화를 사랑합니다. 창의적이고 감성이 풍부하여 예술 분야에서 두각을 나타냅니다.",
        "strengths": ["친절함", "배려심", "창의성", "예술성", "평화로움"],
        "weaknesses": ["우유부단", "의존성", "비관적", "걱정 많음"],
        "lucky_numbers": [2, 7],
        "lucky_colors": ["갈색", "빨간색", "보라색"],
        "lucky_direction": "남쪽",
        "career": "예술가, 음악가, 디자이너, 간호사, 교사",
        "compatible": ["토끼띠", "돼지띠", "말띠"],
        "incompatible": ["소띠", "개띠"],
        "2026_fortune": "2026년은 양띠에게 평화와 안정을 찾는 해입니다. 급격한 변화보다는 현재의 상황을 유지하고 다지는 것이 좋습니다. 인간관계에서 따뜻함을 나누면 긍정적인 에너지가 돌아옵니다. 창작 활동이나 취미생활로 내면을 풍요롭게 하세요.",
    },
    "monkey": {
        "korean": "원숭이띠", "emoji": "🐵", "english": "Monkey",
        "years_mod": 8,
        "element": "金", "yin_yang": "양(陽)",
        "years_example": [1908, 1920, 1932, 1944, 1956, 1968, 1980, 1992, 2004, 2016, 2028],
        "personality": "원숭이띠는 영리하고 재치 있으며 적응력이 뛰어납니다. 호기심이 강하고 창의적이며 어떤 문제도 기발한 방법으로 해결합니다. 낙천적이고 유머가 넘칩니다.",
        "strengths": ["영리함", "적응력", "창의성", "낙천성", "재치"],
        "weaknesses": ["집중력 부족", "불성실", "자기과신", "변덕"],
        "lucky_numbers": [1, 7, 8],
        "lucky_colors": ["흰색", "파란색", "금색"],
        "lucky_direction": "북쪽, 북서쪽",
        "career": "과학자, 프로그래머, 사업가, 엔지니어, 코미디언",
        "compatible": ["용띠", "쥐띠"],
        "incompatible": ["호랑이띠", "돼지띠"],
        "2026_fortune": "2026년은 원숭이띠에게 지혜를 발휘하는 해입니다. 기발한 아이디어가 큰 성과로 이어질 수 있으며, 네트워킹과 협력이 중요한 열쇠입니다. 충동적인 결정보다 신중한 판단이 필요한 시기입니다.",
    },
    "rooster": {
        "korean": "닭띠", "emoji": "🐓", "english": "Rooster",
        "years_mod": 9,
        "element": "金", "yin_yang": "음(陰)",
        "years_example": [1909, 1921, 1933, 1945, 1957, 1969, 1981, 1993, 2005, 2017, 2029],
        "personality": "닭띠는 근면하고 꼼꼼하며 성실합니다. 자신에 대한 기준이 높고 완벽을 추구합니다. 직설적이고 솔직하며 자신의 능력에 자신감이 있습니다.",
        "strengths": ["근면함", "꼼꼼함", "솔직함", "자신감", "성실함"],
        "weaknesses": ["완고함", "지나친 비판", "과장", "허영심"],
        "lucky_numbers": [5, 7, 8],
        "lucky_colors": ["금색", "갈색", "노란색"],
        "lucky_direction": "남쪽, 동남쪽",
        "career": "군인, 의사, 요리사, 농부, 교사",
        "compatible": ["소띠", "용띠", "뱀띠"],
        "incompatible": ["토끼띠", "개띠"],
        "2026_fortune": "2026년은 닭띠에게 실력과 능력을 인정받는 해입니다. 그동안 쌓아온 전문성이 빛을 발하며, 직장이나 사업에서 중요한 기회가 찾아옵니다. 인내심을 발휘하고 꾸준히 나아가면 큰 성취를 이룰 수 있습니다.",
    },
    "dog": {
        "korean": "개띠", "emoji": "🐕", "english": "Dog",
        "years_mod": 10,
        "element": "土", "yin_yang": "양(陽)",
        "years_example": [1910, 1922, 1934, 1946, 1958, 1970, 1982, 1994, 2006, 2018, 2030],
        "personality": "개띠는 충성스럽고 정직하며 따뜻한 마음을 가지고 있습니다. 믿음직스럽고 신뢰를 중요시하며 헌신적으로 주변을 돕습니다. 정의감이 강하고 불의를 참지 못합니다.",
        "strengths": ["충성심", "정직함", "헌신", "신뢰성", "정의감"],
        "weaknesses": ["불안감", "고집", "비관적", "완고함"],
        "lucky_numbers": [3, 4, 9],
        "lucky_colors": ["빨간색", "초록색", "보라색"],
        "lucky_direction": "동쪽",
        "career": "경찰, 상담사, 봉사직, 교사, 의사",
        "compatible": ["호랑이띠", "말띠", "토끼띠"],
        "incompatible": ["용띠", "양띠"],
        "2026_fortune": "2026년은 개띠에게 신뢰를 쌓는 해입니다. 성실한 노력이 주변의 인정으로 이어지며, 중요한 인연이 새롭게 시작될 수 있습니다. 건강에 특히 신경을 쓰고 무리하지 않는 것이 중요합니다.",
    },
    "pig": {
        "korean": "돼지띠", "emoji": "🐷", "english": "Pig",
        "years_mod": 11,
        "element": "水", "yin_yang": "음(陰)",
        "years_example": [1911, 1923, 1935, 1947, 1959, 1971, 1983, 1995, 2007, 2019, 2031],
        "personality": "돼지띠는 순수하고 관대하며 풍요를 상징합니다. 낙천적이고 즐거움을 추구하며 사람들과 어울리기를 좋아합니다. 성실하고 책임감이 있으며 가정을 중시합니다.",
        "strengths": ["관대함", "순수함", "낙천성", "성실함", "가정적"],
        "weaknesses": ["순진함", "게으름", "과도한 소비", "우유부단"],
        "lucky_numbers": [2, 5, 8],
        "lucky_colors": ["노란색", "회색", "갈색", "금색"],
        "lucky_direction": "북동쪽",
        "career": "요리사, 의사, 연예인, 교사, 사업가",
        "compatible": ["호랑이띠", "토끼띠", "양띠"],
        "incompatible": ["뱀띠", "원숭이띠"],
        "2026_fortune": "2026년은 돼지띠에게 풍요와 행복이 찾아오는 해입니다. 재물운이 상승하고 가정이나 사랑에서 즐거운 소식이 있을 수 있습니다. 건강 관리에도 신경을 쓰고, 새로운 활동에 적극적으로 참여해보세요.",
    },
}

# year % 12 → zodiac key 매핑 (1900년 = 쥐띠, 1900 % 12 = 4)
YEAR_TO_ZODIAC_KEY = {
    4: "rat", 5: "ox", 6: "tiger", 7: "rabbit",
    8: "dragon", 9: "snake", 10: "horse", 11: "sheep",
    0: "monkey", 1: "rooster", 2: "dog", 3: "pig"
}


def get_zodiac_by_year(year: int) -> dict:
    """출생연도로 띠 정보 반환"""
    key = YEAR_TO_ZODIAC_KEY.get(year % 12)
    if key:
        return {"key": key, **ZODIAC_INFO[key]}
    return None


def get_zodiac_by_key(key: str) -> dict:
    """띠 키로 정보 반환"""
    info = ZODIAC_INFO.get(key.lower())
    if info:
        return {"key": key.lower(), **info}
    return None


def get_all_zodiacs() -> list:
    """12띠 전체 목록 반환"""
    order = ["rat", "ox", "tiger", "rabbit", "dragon", "snake",
             "horse", "sheep", "monkey", "rooster", "dog", "pig"]
    return [{"key": k, **ZODIAC_INFO[k]} for k in order]


def get_year_fortune(year: int) -> dict:
    """
    특정 출생연도의 운세 정보 반환
    """
    from datetime import datetime
    current_year = datetime.now().year
    age_korean = current_year - year + 1  # 한국 나이
    age_western = current_year - year      # 만 나이

    zodiac = get_zodiac_by_year(year)

    # 간지 계산 (saju_logic 없이 간단 구현)
    stems = ["甲(갑)", "乙(을)", "丙(병)", "丁(정)", "戊(무)",
             "己(기)", "庚(경)", "辛(신)", "壬(임)", "癸(계)"]
    branches = ["子(자)", "丑(축)", "寅(인)", "卯(묘)", "辰(진)", "巳(사)",
                "午(오)", "未(미)", "申(신)", "酉(유)", "戌(술)", "亥(해)"]
    stem = stems[(year - 4) % 10]
    branch = branches[(year - 4) % 12]
    birth_ganji = f"{stem} {branch}년"

    return {
        "year": year,
        "birth_ganji": birth_ganji,
        "age_korean": age_korean,
        "age_western": age_western,
        "zodiac": zodiac,
    }
