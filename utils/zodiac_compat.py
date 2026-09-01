"""
띠×띠 궁합 유틸리티 (명리학 기반)
육합(六合)·삼합(三合)·육충(六沖)·원진 등 명리 이론 기반 66쌍 궁합 데이터.
dream645와 차별화: 단순 점수가 아니라 명리 근거(지지 관계) 심층 해설 제공.
"""
from utils.zodiac_fortune import ZODIAC_INFO

# 12지지 순서 (key)
ZODIAC_ORDER = ["rat", "ox", "tiger", "rabbit", "dragon", "snake",
                "horse", "sheep", "monkey", "rooster", "dog", "pig"]

# 지지 ↔ 한글 표기 (한자 사용 금지 원칙 — 한국인 타겟)
BRANCH_NAME = {
    "rat": "자", "ox": "축", "tiger": "인", "rabbit": "묘",
    "dragon": "진", "snake": "사", "horse": "오", "sheep": "미",
    "monkey": "신", "rooster": "유", "dog": "술", "pig": "해",
}

# 육합(六和): 지지 6쌍 — 화해·결합의 기운
YUKHAP = {
    frozenset(["rat", "ox"]),
    frozenset(["tiger", "pig"]),
    frozenset(["rabbit", "dog"]),
    frozenset(["dragon", "rooster"]),
    frozenset(["snake", "monkey"]),
    frozenset(["horse", "sheep"]),
}

# 삼합(三合): 4지지씩 3개 그룹 — 협력·도화
SANHAP_GROUPS = [
    frozenset(["rat", "dragon", "monkey"]),   # 신자진 삼합 (수국)
    frozenset(["tiger", "horse", "dog"]),     # 인오술 삼합 (화국)
    frozenset(["snake", "rooster", "ox"]),    # 사유축 삼합 (금국)
    frozenset(["rabbit", "sheep", "pig"]),    # 해묘미 삼합 (목국)
]

# 육충(六沖): 대립·충돌 — 단, "극이 곧 나쁨"이 아니라 역동 관계로 해설
YUKCHUNG = {
    frozenset(["rat", "horse"]),     # 자오충
    frozenset(["ox", "sheep"]),      # 축미충
    frozenset(["tiger", "monkey"]),  # 인신충
    frozenset(["rabbit", "rooster"]),# 묘유충
    frozenset(["dragon", "dog"]),    # 진술충
    frozenset(["snake", "pig"]),     # 사해충
}

# 육해(六害): 미묘한 간섭·어긋남
YUKHAE = {
    frozenset(["rat", "sheep"]),      # 자미해
    frozenset(["ox", "horse"]),       # 축오해
    frozenset(["tiger", "snake"]),    # 인사해
    frozenset(["rabbit", "dragon"]),  # 묘진해
    frozenset(["snake", "pig"]),      # 인신해 대신 전통 육해: 사신(申)은 아래 육파와 중복 주의 — 전통 육해 조합
    frozenset(["monkey", "pig"]),     # 신해해
    frozenset(["rooster", "dog"]),    # 유술해
}
# 전통 육해 정정: 子未(자미), 丑午(축오), 寅巳(인사), 卯辰(묘진), 申亥(신해), 酉戌(유술)
YUKHAE = {
    frozenset(["rat", "sheep"]),
    frozenset(["ox", "horse"]),
    frozenset(["tiger", "snake"]),
    frozenset(["rabbit", "dragon"]),
    frozenset(["monkey", "pig"]),
    frozenset(["rooster", "dog"]),
}

# 원진(元臻): 정신적 피로·감정 소모
WONJIN = {
    frozenset(["rat", "sheep"]),
    frozenset(["ox", "horse"]),  # 원진은 자미·축오·인유·묘신·진해·사술 순 (일부 육해와 겹침)
    frozenset(["tiger", "rooster"]),
    frozenset(["rabbit", "monkey"]),
    frozenset(["dragon", "pig"]),   # 진해
    frozenset(["snake", "dog"]),    # 사술
}
# 전통 원진 정정: 子未, 丑午, 寅酉, 卯申, 辰亥, 巳戌
WONJIN = {
    frozenset(["rat", "sheep"]),
    frozenset(["ox", "horse"]),
    frozenset(["tiger", "rooster"]),
    frozenset(["rabbit", "monkey"]),
    frozenset(["dragon", "pig"]),
    frozenset(["snake", "dog"]),
}

# 삼형(三刑): 지지 3그룹 형살 — 자모형/인사신형/축미술형 + 자묘형
SANHYUNG_SINGLES = {frozenset(["rat", "rabbit"])}  # 자묘형
SANHAP_GROUPS_FOR_FORM = [
    frozenset(["tiger", "snake", "monkey"]),   # 인사신 삼형
    frozenset(["ox", "sheep", "dog"]),         # 축미술 삼형
    frozenset(["dragon", "horse", "rooster"]), # 진오유 자형(삼형 취급)
]

PAIR_RELATIONS_TEXT = {
    "yukhap": ("육합", "지지가 서로 결합해 가장 조화로운 조합입니다. 서로의 부족한 부분을 채워주는 상호 보완 관계예요."),
    "sanhap": ("삼합", "세 지지가 한 그룹의 기운을 이루는 강한 협력 관계입니다. 셋 중 하나는 서로 완벽히 통하지만, 두 사람만으로도 강한 동지 애착이 생깁니다."),
    "yukchung": ("육충", "지지가 정반대 방향으로 충돌하는 관계입니다. 갈등도 크지만 서로를 성장시키는 역동적 에너지가 있어, 마음만 먹으면 최고의 화학조합이 됩니다."),
    "yukhae": ("육해", "겉으로는 무난하지만 미묘한 어긋남이 쌓일 수 있는 조합입니다. 사소한 오해를 쌓아두지 않는 소통이 관건입니다."),
    "wonjin": ("원진", "가까워질수록 감정 소모가 생기기 쉬운 조합입니다. 서로 다름을 인정하고 거리를 두는 지혜가 필요해요."),
    "javye": ("자묘형", "예민하게 부딪히는 형 관계이지만, 서로에 대한 관심이 깊어 애증의 관계로 발전하기도 합니다."),
    "sanhap_form": ("삼형 그룹", "셋 중 한 쌍이 만나면 형 관계가 성립합니다. 서두르지 않고 정직하게 대화하면 충분히 좋은 관계가 됩니다."),
    "normal": ("보통", "특별한 합·충 없이 중립적인 관계입니다. 오행 흐름과 본인 사주를 함께 보면 더 정확해집니다."),
}


def _pair_key(a: str, b: str) -> frozenset:
    return frozenset([a, b])


def get_pair_relation(a: str, b: str) -> str:
    """두 띠의 최우선 명리 관계 판정 (우선순위: 육합 > 삼합 > 육충 > 원진 > 육해 > 자묘형 > 삼형 > 보통)"""
    k = _pair_key(a, b)
    sanhap_forms = [
        frozenset(["tiger", "snake"]), frozenset(["snake", "monkey"]),
        frozenset(["tiger", "monkey"]),
        frozenset(["ox", "sheep"]), frozenset(["sheep", "dog"]), frozenset(["ox", "dog"]),
        frozenset(["dragon", "horse"]), frozenset(["horse", "rooster"]), frozenset(["dragon", "rooster"]),
    ]
    if k in YUKHAP:
        return "yukhap"
    # 삼형 그룹 내부 쌍 (진오유·축미술·인사신) — 삼형이 삼합보다 우선하는 경우로 명시
    sanhap_form_pairs = {
        frozenset(["tiger", "snake"]), frozenset(["snake", "monkey"]), frozenset(["tiger", "monkey"]),
        frozenset(["ox", "sheep"]), frozenset(["sheep", "dog"]), frozenset(["ox", "dog"]),
    }
    if k in sanhap_form_pairs:
        return "sanhap_form"
    for g in SANHAP_GROUPS:
        if a in g and b in g:
            return "sanhap"
    if k in YUKCHUNG:
        return "yukchung"
    if k in WONJIN:
        return "wonjin"
    if k in YUKHAE:
        return "yukhae"
    if k in SANHYUNG_SINGLES:
        return "javye" if False else "javye"
    if k == frozenset(["rat", "rabbit"]):
        return "javye"
    return "normal"


PAIR_RELATION_KEYS = {
    "yukhap": ("육합", "지지가 서로 결합하는 최고 조화 조합으로, 서로의 빈곳을 채워주는 관계입니다."),
    "sanhap": ("삼합", "같은 기운 그룹의 협력 관계로, 함께할 때 시너지가 큽니다."),
    "yukchung": ("육충", "정반대 지끼가 부딪히는 역동적 관계. 갈등이 곧 끌림으로 이어질 수 있습니다."),
    "wonjin": ("원진", "감정 소모가 쉽상하는 조합. 서로의 다름을 인정하는 자세가 관건입니다."),
    "yukhae": ("육해", "미묘한 간섭이 쌓일 수 있는 조합. 사전 소통과 배려가 필요합니다."),
    "javye": ("자묘형", "예민한 애증 관계지만 깊은 관심에서 비롯된 마음이 담습니다."),
    "sanhap_form": ("삼형", "서두르면 걸리고 느긋하면 풀리는 관계. 정직한 대화가 해법입니다."),
    "normal": ("보통", "합·충 없는 중립 관계로, 서로의 본연 모습 그대로 만나는 편안함이 있습니다."),
}


def get_pair_score(relation: str) -> int:
    """명리 관계 기반 궁합 점수 (0~100)"""
    return {
        "yukhap": 95, "sanhap": 88, "normal": 65,
        "yukchung": 55, "yukhae": 48, "wonjin": 42,
        "javye": 45, "sanhap_form": 50,
    }.get(relation, 65)


def get_relation_label(relation: str):
    """(라벨, 한줄 설명) 반환"""
    return PAIR_RELATION_KEYS.get(relation, PAIR_RELATION_KEYS["normal"])


def _scores_of_5elements(zodiac_key: str):
    """띠의 오행 → 상세 오행 힌트."""
    elem = ZODIAC_INFO[zodiac_key]["element"]
    return elem


ELEMENT_RELATION_TEXT = {
    ("水", "水"): "같은 물 기운이라 서로의 마음을 잘 이해합니다. 다만 감정이 잠수처럼 깊어져 오해가 가라앉을 수 있으니 솔직한 대화가 필요해요.",
    ("木", "木"): "같은 나무들이라 함께 자라는 기운. 서로의 성장을 응원하지만, 의견이 갈리면 서로 굽히지 않을 수 있어요.",
    ("火", "火"): "두 개의 불꽃이 만나 열정이 넘치는 조합입니다. 다만 모두 앞서 나가려 하면 지칠 수 있으니 번갈아 쉬어가세요.",
    ("土", "土"): "두 개의 산이 서로 마주 보듯 안정적입니다. 꾸준함이 강점이지만 새로운 변화는 의도적으로 노력해야 해요.",
    ("金", "金"): "두 개의 금속 — 단단하고 신뢰 강한 관계입니다. 다만 표현이 서툴 수 있으니 말로 마음을 옮기는 연습이 좋아요.",
    ("水", "木"): "물이 나무를 키우는 상생 관계. 한쪽의 배려가 다른 쪽의 성장으로 이어지는 흐름입니다.",
    ("木", "火"): "나무가 불을 지피는 상생. 영감을 주고 받으며 함께 성장하는 관계예요.",
    ("火", "土"): "불이 흙을 다져주는 상생. 한쪽의 열정이 현실적 결과로 이어집니다.",
    ("土", "金"): "흙에서 금속이 나오는 상생. 지원하고 기대주는 구조로 서로에게 힘이 됩니다.",
    ("金", "水"): "금속이 물을 맑게 하는 상생. 냉정과 온정의 균형, 좋은 조합입니다.",
    ("木", "土"): "나무가 땅을 헤집을 수 있는 상극. 서로의 방식을 존중하면 좋은 파트너가 됩니다.",
    ("土", "水"): "흙이 물을 막는 상극. 답답함보다는 보호자로 이해하면 관계가 부드러워집니다.",
    ("水", "火"): "물이 불을 끄는 상극. 감정 폭발 서로를 삼갈 줄 알면 보완 관계가 됩니다.",
    ("火", "金"): "불이 금속을 녹이는 상극. 강압적 방식보다 부드러운 설득이 통합니다.",
    ("金", "木"): "도끼가 나무를 자르는 상극. 잔소리와 지적은 절제, 격려로 바꿔 보세요.",
}


def get_element_match(a: str, b: str):
    """띠 오행 간 상생/상극/동행 판정 + 해설."""
    a_e, b_e = ZODIAC_INFO[a]["element"], ZODIAC_INFO[b]["element"]
    sangsaeng = [("木", "火"), ("火", "土"), ("土", "金"), ("金", "水"), ("水", "木")]
    sunguk = [("木", "土"), ("土", "水"), ("水", "火"), ("火", "金"), ("金", "木")]
    key = (a_e, b_e) if (a_e, b_e) in ELEMENT_RELATION_TEXT else (b_e, a_e)
    if a_e == b_e:
        kind = "같은 오행"
    elif key in ELEMENT_RELATION_TEXT:
        kind = "상생" if (a_e, b_e) in sangsaeng or (b_e, a_e) in sangsaeng else "상극"
    else:
        kind = "보통"
    text = ELEMENT_RELATION_TEXT.get(key, "특별한 오행 조합 없이 중립적인 기운입니다.")
    return kind, text


def get_pair_fortune(a: str, b: str) -> dict:
    """궁합 페이지에 필요한 데이터를 반환합니다."""
    rel = get_pair_relation(a, b)
    label, short = PAIR_RELATIONS_TEXT.get(rel, PAIR_RELATIONS_TEXT["normal"])
    score = get_pair_score(rel)
    elem_kind, elem_text = get_element_match(a, b)
    za, zb = ZODIAC_INFO[a], ZODIAC_INFO[b]

    # 영역별 해설
    rel_to_area = {
        "yukhap": {"love": 90, "friend": 92, "work": 88, "marriage": 90},
        "sanhap": {"love": 82, "friend": 88, "work": 90, "marriage": 84},
        "normal": {"love": 62, "friend": 68, "work": 66, "marriage": 64},
        "yukchung": {"love": 58, "friend": 55, "work": 60, "marriage": 50},
        "wonjin": {"love": 48, "friend": 52, "work": 45, "marriage": 40},
        "yukhae": {"love": 55, "friend": 58, "work": 42, "marriage": 48},
        "javye": {"love": 52, "friend": 46, "work": 50, "marriage": 42},
        "sanhap_form": {"love": 56, "friend": 60, "work": 58, "marriage": 52},
    }[rel]

    # 세부 해설 (명리 근거 중심) — 지지명은 한글 음차 표기 사용
    han_a, han_b = BRANCH_NAME[a], BRANCH_NAME[b]
    detail = f"{za['korean']}({han_a}지)와 {zb['korean']}({han_b}지)의 관계는 명리학에서 「{label}」입니다. {short} "

    if rel == "yukhap":
        detail += "특히 육합은 두 지지가 하나로 묶이는 음양의 조화라, 첫 만남부터 편안함을 느끼기 쉽습니다. 연애·결혼 모두에서 안정적인 조합으로 꼽힙니다."
    elif rel == "sanhap":
        detail += "같은 삼합 그룹에 속해 넓은 인간관계에서 서로를 알아보는 특별한 인연이라 해석됩니다. 동업·협업에서 두각을 나타냅니다."
    elif rel == "yukchung":
        detail += "다만 충은 '부딪힌다'가 전부가 아니라 서로의 숨겨진 면을 드러내게 하는 관계. 초반에 다툼이 잦더라도 시간이 지나면 가장 깊이 이해하는 사이가 될 수 있습니다."
    elif rel == "wonjin":
        detail += "원진은 싫어서 그런 게 아니라 서로의 민감한 부분을 건드려 지치는 관계. 물리적 거리와 기다림이 관계를 살리는 처방입니다."
    elif rel == "yukhae":
        detail += "육해는 큰 갈등보다 잔잔한 미묘함(미묘한 어긋남)이 쌓이는 관계. 정기적인 대화 시간을 갖는 루틴화가 좋습니다."
    elif rel == "javye":
        detail += "자묘형은 흔히 '애증의 인연'이라 불립니다. 오히려 서로에게 가장 눈이 가는 관계라, 감정 조절만 잘 되면 남다른 이해를 나눕니다."
    elif rel == "sanhap_form":
        detail += "형은 검열의 관계. 서로의 허점이 드러나 답답할 수 있으나, 직설을 배려로 바꾸면 강한 팀이 됩니다."
    else:
        detail += "특별한 합·충이 없다는 말은, 두 사람의 관계가 외부 조건보다 노력으로 그려진다는 뜻이기도 합니다."

    ELEM_KR = {"水": "물(水)".replace("(水)", ""), "木": "나무", "火": "불", "土": "흙", "金": "쇠"}
    detail += f" 오행으로 보면 {za['korean']}는 {ELEM_KR.get(za['element'], za['element'])} 기운, {zb['korean']}는 {ELEM_KR.get(zb['element'], zb['element'])}입니다. {elem_text}"

    return {
        "a": a, "b": b,
        "zodiac_a": {**{k: v for k, v in za.items() if k != "years_example"}, "key": a},
        "zodiac_b": {**{k: v for k, v in zb.items() if k != "years_example"}, "key": b},
        "relation": rel,
        "relation_label": label,
        "relation_short": short,
        "detail": detail,
        "score": score,
        "area": rel_to_area,
        "element_kind": elem_kind,
        "element_text": elem_text,
        "lucky_tip": f"{za['lucky_colors'][0]}·{zb['lucky_colors'][0]} 계열 아이템을 함께 두면 기운이 맞춰진다고 여겨집니다.",
    }


def get_best_matches(key: str, top_n: int = 3):
    """특정 띠 기준 최고 궁합 3쌍"""
    scored = []
    for other in ZODIAC_ORDER:
        if other == key:
            continue
        d = get_pair_fortune(key, other)
        scored.append((other, d["score"]))
    scored.sort(key=lambda x: -x[1])
    return scored[:top_n]


def get_all_pairs() -> dict:
    """66쌍 데이터 캐시 없이 dict로 반환 (라우팅 검증용)"""
    pairs = {}
    for i, a in enumerate(ZODIAC_ORDER):
        for b in ZODIAC_ORDER[i + 1:]:
            pairs[f"{a}-vs-{b}"] = get_pair_fortune(a, b)
    return pairs