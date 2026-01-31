"""
궁합 계산 유틸리티
두 사람의 사주 정보를 비교하여 궁합을 분석합니다.
"""
import saju_logic


def extract_char(ganji_str):
    """간지 문자열에서 한자만 추출"""
    if isinstance(ganji_str, str) and "(" in ganji_str:
        return ganji_str.split()[0]
    return ganji_str


def get_element_from_stem(stem):
    """천간에서 오행을 추출합니다."""
    stem_char = extract_char(stem)
    element_map = {
        "甲": "木", "乙": "木",
        "丙": "火", "丁": "火",
        "戊": "土", "己": "土",
        "庚": "金", "辛": "金",
        "壬": "水", "癸": "水"
    }
    return element_map.get(stem_char, "土")


def check_element_compatibility(element1, element2):
    """두 오행의 상생/상극 관계를 확인합니다."""
    sangsaeng = [("木", "火"), ("火", "土"), ("土", "金"), ("金", "水"), ("水", "木")]
    sanggeuk = [("木", "土"), ("土", "水"), ("水", "火"), ("火", "金"), ("金", "木")]
    
    if (element1, element2) in sangsaeng or (element2, element1) in sangsaeng:
        return "상생"
    elif (element1, element2) in sanggeuk or (element2, element1) in sanggeuk:
        return "상극"
    else:
        return "보통"


def generate_pillar_analysis(pillar_name, score, stem_compat, branch_relation, branch_desc):
    """기둥별 분석 텍스트 생성"""
    analysis_parts = []
    
    if stem_compat == "상생":
        analysis_parts.append(f"천간 오행이 상생 관계로 서로 도와주는 구조입니다.")
    elif stem_compat == "상극":
        analysis_parts.append(f"천간 오행이 상극 관계로 서로 다른 성향을 가지고 있습니다.")
    
    if branch_relation == "육합":
        analysis_parts.append(f"지지가 육합 관계로 매우 조화롭습니다.")
    elif branch_relation == "삼합":
        analysis_parts.append(f"지지가 삼합 관계로 협력이 좋습니다.")
    elif branch_relation == "충":
        analysis_parts.append(f"지지가 충 관계로 변화와 대립이 있습니다.")
    elif branch_relation == "형":
        analysis_parts.append(f"지지가 형 관계로 약간의 마찰이 있을 수 있습니다.")
    
    if not analysis_parts:
        analysis_parts.append("평상 관계로 안정적입니다.")
    
    return " ".join(analysis_parts)


def analyze_strengths_weaknesses(result):
    """강점과 약점 분석"""
    strengths = []
    weaknesses = []
    
    # 지지 관계 분석
    yukhap_count = sum(1 for rel in result["branch_relationships"] if "육합" in rel)
    sanhap_count = sum(1 for rel in result["branch_relationships"] if "삼합" in rel)
    chung_count = sum(1 for rel in result["branch_relationships"] if "충" in rel)
    
    if yukhap_count > 0:
        strengths.append(f"{yukhap_count}개의 기둥에서 육합 관계가 나타나 서로를 보완하는 조화로운 관계입니다.")
    if sanhap_count > 0:
        strengths.append(f"{sanhap_count}개의 기둥에서 삼합 관계가 나타나 협력과 조화가 좋습니다.")
    if chung_count > 0:
        weaknesses.append(f"{chung_count}개의 기둥에서 충 관계가 나타나 변화와 대립이 있을 수 있습니다. 서로의 차이를 이해하는 노력이 필요합니다.")
    
    # 일주 점수 확인
    day_pillar = next((p for p in result["pillar_compatibilities"] if p["pillar"] == "일주"), None)
    if day_pillar and day_pillar["score"] >= 80:
        strengths.append("일주 궁합이 매우 좋아 서로를 잘 이해하고 조화를 이룹니다.")
    elif day_pillar and day_pillar["score"] < 50:
        weaknesses.append("일주 궁합에서 주의가 필요합니다. 서로의 성격과 성향을 이해하는 시간이 필요합니다.")
    
    # 십성 분석
    if result["ten_god_analysis"]:
        ten_god_text = result["ten_god_analysis"][0]
        if "正財" in ten_god_text or "正官" in ten_god_text or "正印" in ten_god_text:
            strengths.append("십성 관계가 좋아 서로를 도와주고 보완하는 구조입니다.")
        elif "劫財" in ten_god_text or "傷官" in ten_god_text:
            weaknesses.append("십성 관계에서 약간의 경쟁이나 갈등이 있을 수 있으나, 서로를 이해하면 오히려 성장하는 관계가 될 수 있습니다.")
    
    # 기본 메시지
    if not strengths:
        strengths.append("서로 다른 성향을 가지고 있어 보완할 수 있는 관계입니다.")
    if not weaknesses:
        weaknesses.append("서로의 차이를 이해하고 소통하는 노력이 중요합니다.")
    
    return strengths, weaknesses


def generate_advice(result):
    """조언 생성"""
    advice_parts = []
    
    score = result["overall_score"]
    if score >= 85:
        advice_parts.append("두 분의 궁합이 매우 좋습니다. 서로를 신뢰하고 지지하며 함께 성장해 나가시기 바랍니다.")
    elif score >= 75:
        advice_parts.append("좋은 궁합을 바탕으로 서로를 이해하고 존중하며 발전적인 관계를 만들어 나가시기 바랍니다.")
    elif score >= 65:
        advice_parts.append("약간의 차이가 있지만, 서로를 이해하고 보완하며 좋은 관계를 유지할 수 있습니다.")
    else:
        advice_parts.append("서로의 차이를 인정하고 소통을 통해 이해를 깊게 하는 것이 중요합니다.")
    
    # 충 관계가 있으면 특별 조언
    chung_relations = [rel for rel in result["branch_relationships"] if "충" in rel]
    if chung_relations:
        advice_parts.append("충 관계가 있는 기둥에서는 변화와 대립이 있을 수 있으므로, 서로의 의견을 존중하고 타협점을 찾는 것이 중요합니다.")
    
    return " ".join(advice_parts)


def generate_detailed_guidance(result, person1_pillars_info, person2_pillars_info):
    """상세 가이드 생성"""
    guidance = {
        "relationship": "서로를 이해하고 존중하는 관계를 유지하세요.",
        "communication": "소통을 통해 서로의 생각과 감정을 공유하는 것이 중요합니다.",
        "conflict_resolution": "의견 차이가 있을 때는 상대방의 입장을 먼저 이해하려고 노력하세요.",
        "growth": "서로의 차이를 보완하며 함께 성장할 수 있는 관계입니다."
    }
    
    score = result["overall_score"]
    if score >= 85:
        guidance["relationship"] = "매우 좋은 궁합이므로 서로를 신뢰하고 지지하며 이상적인 관계를 만들어 나가세요."
        guidance["communication"] = "자연스러운 소통이 가능하며, 서로의 마음을 잘 이해할 수 있습니다."
        guidance["conflict_resolution"] = "갈등이 생겨도 쉽게 해결할 수 있으며, 서로를 이해하려는 노력이 돋보입니다."
        guidance["growth"] = "서로를 도와주며 함께 성장하는 관계입니다."
    elif score < 50:
        guidance["relationship"] = "서로의 차이를 이해하고 보완하는 노력이 필요한 관계입니다."
        guidance["communication"] = "솔직하고 정직한 소통을 통해 서로를 이해하는 시간이 필요합니다."
        guidance["conflict_resolution"] = "의견 차이가 있을 때는 감정적으로 대응하기보다, 차분히 대화를 통해 해결하려고 노력하세요."
        guidance["growth"] = "서로의 다른 점을 보완하며 함께 발전할 수 있습니다."
    
    return guidance


def calculate_gonghap(person1_pillars_data, person1_pillars_info, person1_gender,
                     person2_pillars_data, person2_pillars_info, person2_gender):
    """
    두 사람의 사주를 비교하여 궁합을 계산합니다.
    
    Args:
        person1_pillars_data: 첫 번째 사람의 사주 기둥 데이터
        person1_pillars_info: 첫 번째 사람의 사주 정보
        person1_gender: 첫 번째 사람의 성별
        person2_pillars_data: 두 번째 사람의 사주 기둥 데이터
        person2_pillars_info: 두 번째 사람의 사주 정보
        person2_gender: 두 번째 사람의 성별
        
    Returns:
        dict: 궁합 분석 결과
    """
    result = {
        "overall_score": 75,
        "overall_level": "보통",
        "overall_desc": "두 분의 궁합은 보통 수준입니다.",
        "pillar_compatibilities": [],
        "element_analysis": {},
        "branch_relationships": [],
        "ten_god_analysis": [],
        "strengths": [],
        "weaknesses": [],
        "advice": "",
        "detailed_guidance": {}
    }
    
    # 지지 인덱스 매핑
    branch_idx_map = {saju_logic.EARTHLY_BRANCHES[i].split()[0]: i for i in range(len(saju_logic.EARTHLY_BRANCHES))}
    
    # 지지 관계 정의
    sanhap_groups = [[2, 6, 10], [8, 0, 4], [11, 3, 7], [5, 9, 1]]  # 삼합
    yukhap_pairs = [(0, 1), (2, 11), (3, 10), (4, 9), (5, 8), (6, 7)]  # 육합
    chung_pairs = [(0, 6), (1, 7), (2, 8), (3, 9), (4, 10), (5, 11)]  # 충
    hyeong_groups = [[0, 3], [2, 5, 8], [1, 7, 10], [4, 6, 9, 11]]  # 형
    hae_pairs = [(0, 7), (1, 8), (2, 9), (3, 10), (4, 11), (5, 0)]  # 해 (간단한 예시)
    
    pillar_names = ["년주", "월주", "일주", "시주"]
    pillar_weights = [0.2, 0.3, 0.4, 0.1]  # 일주가 가장 중요
    
    total_score = 0
    total_weight = 0
    
    # 각 기둥별 궁합 분석
    for i, pillar_name in enumerate(pillar_names):
        p1_stem = person1_pillars_data[i].get('Heavenly Stem (천간)', '')
        p1_branch = person1_pillars_data[i].get('Earthly Branch (지지)', '')
        p2_stem = person2_pillars_data[i].get('Heavenly Stem (천간)', '')
        p2_branch = person2_pillars_data[i].get('Earthly Branch (지지)', '')
        
        # 천간 추출 (한글 제거)
        p1_stem_char = extract_char(p1_stem)
        p1_branch_char = extract_char(p1_branch)
        p2_stem_char = extract_char(p2_stem)
        p2_branch_char = extract_char(p2_branch)
        
        # 오행 분석
        p1_stem_element = get_element_from_stem(p1_stem)
        p2_stem_element = get_element_from_stem(p2_stem)
        p1_branch_element = saju_logic.BRANCH_ELEMENTS.get(p1_branch, "土")
        p2_branch_element = saju_logic.BRANCH_ELEMENTS.get(p2_branch, "土")
        
        # 천간 오행 상생/상극
        stem_compat = check_element_compatibility(p1_stem_element, p2_stem_element)
        branch_compat = check_element_compatibility(p1_branch_element, p2_branch_element)
        
        # 지지 관계 분석
        p1_branch_idx = branch_idx_map.get(p1_branch_char, -1)
        p2_branch_idx = branch_idx_map.get(p2_branch_char, -1)
        
        branch_relation = "평상"
        branch_desc = ""
        relation_score = 50  # 기본 점수
        
        if p1_branch_idx >= 0 and p2_branch_idx >= 0:
            # 육합 확인
            for pair in yukhap_pairs:
                if (p1_branch_idx == pair[0] and p2_branch_idx == pair[1]) or \
                   (p1_branch_idx == pair[1] and p2_branch_idx == pair[0]):
                    branch_relation = "육합"
                    branch_desc = "조화로운 관계로 서로를 보완합니다."
                    relation_score = 90
                    result["branch_relationships"].append(f"{pillar_name}: {branch_relation} ({branch_desc})")
                    break
            
            # 삼합 확인
            if branch_relation == "평상":
                for group in sanhap_groups:
                    if p1_branch_idx in group and p2_branch_idx in group:
                        branch_relation = "삼합"
                        branch_desc = "협력과 조화가 좋은 관계입니다."
                        relation_score = 85
                        result["branch_relationships"].append(f"{pillar_name}: {branch_relation} ({branch_desc})")
                        break
            
            # 충 확인
            if branch_relation == "평상":
                for pair in chung_pairs:
                    if (p1_branch_idx == pair[0] and p2_branch_idx == pair[1]) or \
                       (p1_branch_idx == pair[1] and p2_branch_idx == pair[0]):
                        branch_relation = "충"
                        branch_desc = "대립과 변화가 있는 관계입니다. 서로 다른 성향을 이해하는 노력이 필요합니다."
                        relation_score = 40
                        result["branch_relationships"].append(f"{pillar_name}: {branch_relation} ({branch_desc})")
                        break
            
            # 형 확인
            if branch_relation == "평상":
                for group in hyeong_groups:
                    if p1_branch_idx in group and p2_branch_idx in group and p1_branch_idx != p2_branch_idx:
                        branch_relation = "형"
                        branch_desc = "약간의 마찰이나 경쟁이 있을 수 있는 관계입니다."
                        relation_score = 55
                        result["branch_relationships"].append(f"{pillar_name}: {branch_relation} ({branch_desc})")
                        break
        
        # 십성 분석 (일주만)
        ten_god_relation = ""
        if i == 2:  # 일주
            p1_day_stem_idx = person1_pillars_info.get('day_stem_idx', 0)
            p2_day_stem_idx = person2_pillars_info.get('day_stem_idx', 0)
            
            # person1의 입장에서 person2의 일간이 어떤 십성인지
            p1_to_p2_ten_god = saju_logic.get_ten_god(p1_day_stem_idx, p2_day_stem_idx)
            # person2의 입장에서 person1의 일간이 어떤 십성인지
            p2_to_p1_ten_god = saju_logic.get_ten_god(p2_day_stem_idx, p1_day_stem_idx)
            
            ten_god_relation = f"십성: {p1_to_p2_ten_god} / {p2_to_p1_ten_god}"
            result["ten_god_analysis"].append(ten_god_relation)
            
            # 십성 관계 점수 조정
            good_ten_gods = ["正財", "正官", "正印", "食神"]
            if p1_to_p2_ten_god in good_ten_gods or p2_to_p1_ten_god in good_ten_gods:
                relation_score += 10
            elif p1_to_p2_ten_god in ["劫財", "傷官", "偏官"] or p2_to_p1_ten_god in ["劫財", "傷官", "偏官"]:
                relation_score -= 5
        
        # 오행 관계 점수 조정
        if stem_compat == "상생":
            relation_score += 15
        elif stem_compat == "상극":
            relation_score -= 10
        if branch_compat == "상생":
            relation_score += 10
        elif branch_compat == "상극":
            relation_score -= 5
        
        relation_score = max(0, min(100, relation_score))  # 0-100 범위 제한
        
        # 기둥별 궁합 정보
        pillar_compat = {
            "pillar": pillar_name,
            "score": relation_score,
            "level": "매우좋음" if relation_score >= 85 else "좋음" if relation_score >= 75 else "양호" if relation_score >= 65 else "보통" if relation_score >= 50 else "주의",
            "stem_compatibility": stem_compat,
            "branch_compatibility": branch_compat,
            "branch_relation": branch_relation,
            "branch_desc": branch_desc,
            "ten_god": ten_god_relation if i == 2 else "",
            "analysis": generate_pillar_analysis(pillar_name, relation_score, stem_compat, branch_relation, branch_desc)
        }
        result["pillar_compatibilities"].append(pillar_compat)
        
        # 가중 평균 계산
        total_score += relation_score * pillar_weights[i]
        total_weight += pillar_weights[i]
    
    # 전체 점수 계산
    if total_weight > 0:
        result["overall_score"] = int(total_score / total_weight)
    
    # 전체 레벨 결정
    if result["overall_score"] >= 85:
        result["overall_level"] = "매우 좋음"
        result["overall_desc"] = "두 분의 궁합이 매우 좋습니다. 서로를 보완하고 조화를 이루는 이상적인 관계입니다."
    elif result["overall_score"] >= 75:
        result["overall_level"] = "좋음"
        result["overall_desc"] = "두 분의 궁합이 좋습니다. 서로 이해하고 협력하며 발전할 수 있는 관계입니다."
    elif result["overall_score"] >= 65:
        result["overall_level"] = "양호"
        result["overall_desc"] = "두 분의 궁합이 양호합니다. 약간의 차이를 이해하고 노력하면 좋은 관계를 유지할 수 있습니다."
    elif result["overall_score"] >= 50:
        result["overall_level"] = "보통"
        result["overall_desc"] = "두 분의 궁합은 보통 수준입니다. 서로의 차이를 존중하고 소통을 통해 이해를 깊게 하는 것이 중요합니다."
    else:
        result["overall_level"] = "주의"
        result["overall_desc"] = "두 분의 궁합에서 일부 주의할 점이 있습니다. 서로의 차이를 이해하고 보완하는 노력이 필요합니다."
    
    # 강점과 약점 분석
    strengths, weaknesses = analyze_strengths_weaknesses(result)
    result["strengths"] = strengths
    result["weaknesses"] = weaknesses
    
    # 조언 생성
    result["advice"] = generate_advice(result)
    
    # 상세 가이드 생성
    result["detailed_guidance"] = generate_detailed_guidance(result, person1_pillars_info, person2_pillars_info)
    
    return result

