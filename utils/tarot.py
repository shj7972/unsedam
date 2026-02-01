"""
타로 카드 계산 및 해석 유틸리티
"""
import random
import os


# 타로 카드 이미지 파일명 매핑 (카드명 -> 파일명)
TAROT_IMAGE_MAP = {
    "0. 바보 (The Fool)": "tarot_00_fool.webp",
    "1. 마법사 (The Magician)": "tarot_01_magician.webp",
    "2. 여교황 (The High Priestess)": "tarot_02_high_priestess.webp",
    "3. 여황제 (The Empress)": "tarot_03_empress.webp",
    "4. 황제 (The Emperor)": "tarot_04_emperor.webp",
    "5. 교황 (The Hierophant)": "tarot_05_hierophant.webp",
    "6. 연인 (The Lovers)": "tarot_06_lovers.webp",
    "7. 전차 (The Chariot)": "tarot_07_chariot.webp",
    "8. 힘 (Strength)": "tarot_08_strength.webp",
    "9. 은둔자 (The Hermit)": "tarot_09_hermit.webp",
    "10. 운명의 바퀴 (Wheel of Fortune)": "tarot_10_wheel_of_fortune.webp",
    "11. 정의 (Justice)": "tarot_11_justice.webp",
    "12. 매달린 남자 (The Hanged Man)": "tarot_12_hanged_man.webp",
    "13. 죽음 (Death)": "tarot_13_death.webp",
    "14. 절제 (Temperance)": "tarot_14_temperance.webp",
    "15. 악마 (The Devil)": "tarot_15_devil.webp",
    "16. 탑 (The Tower)": "tarot_16_tower.webp",
    "17. 별 (The Star)": "tarot_17_star.webp",
    "18. 달 (The Moon)": "tarot_18_moon.webp",
    "19. 태양 (The Sun)": "tarot_19_sun.webp",
    "20. 심판 (Judgement)": "tarot_20_judgement.webp",
    "21. 세계 (The World)": "tarot_21_world.webp",
}


def get_tarot_card_image_path(card_name):
    """
    타로 카드의 기본 이미지 경로를 반환합니다.
    
    Args:
        card_name: 타로 카드 이름 (예: "0. 바보 (The Fool)")
    
    Returns:
        str: 이미지 경로 또는 None (이미지가 없는 경우)
    """
    image_filename = TAROT_IMAGE_MAP.get(card_name)
    if not image_filename:
        return None
    
    # static/images/tarot/ 디렉토리의 이미지 경로
    image_path = f"/static/images/tarot/{image_filename}"
    
    # 파일 존재 여부는 프론트엔드에서 확인하도록 함
    return image_path


# 타로 카드 데이터 (메이저 아르카나 22장)
TAROT_CARDS = {
    "0. 바보 (The Fool)": {
        "의미": "새로운 시작, 순수함, 모험, 가능성",
        "정위치": "새로운 여정의 시작, 자유로운 영혼, 순수한 에너지, 무한한 가능성",
        "역위치": "무모함, 계획 부족, 성급함, 방향 상실",
        "아이콘": "🃏"
    },
    "1. 마법사 (The Magician)": {
        "의미": "의지력, 창조력, 집중, 행동",
        "정위치": "목표 달성을 위한 능력, 창의성, 자신감, 실천력",
        "역위치": "의지력 부족, 계획 미흡, 의욕 상실, 능력 낭비",
        "아이콘": "🎩"
    },
    "2. 여교황 (The High Priestess)": {
        "의미": "직관, 신비, 내면의 지혜, 숨겨진 지식",
        "정위치": "직관력, 내면의 목소리, 신비로운 통찰, 영성",
        "역위치": "직관 무시, 비밀 유지 실패, 내면과의 단절",
        "아이콘": "🌙"
    },
    "3. 여황제 (The Empress)": {
        "의미": "풍요, 모성, 자연, 창조",
        "정위치": "풍요로움, 사랑과 배려, 창조성, 자연의 아름다움",
        "역위치": "생산성 저하, 창의성 부족, 과보호, 의존성",
        "아이콘": "👑"
    },
    "4. 황제 (The Emperor)": {
        "의미": "권위, 구조, 안정, 리더십",
        "정위치": "권위와 지도력, 안정성, 체계적 접근, 성공",
        "역위치": "독재적 성향, 경직성, 권위주의, 통제욕",
        "아이콘": "⚔️"
    },
    "5. 교황 (The Hierophant)": {
        "의미": "전통, 가르침, 영성, 도덕",
        "정위치": "전통과 규칙, 가르침과 지도, 영성, 도덕적 가치",
        "역위치": "고정관념, 전통에의 얽매임, 비판적 사고 부족",
        "아이콘": "⛪"
    },
    "6. 연인 (The Lovers)": {
        "의미": "사랑, 선택, 조화, 관계",
        "정위치": "사랑과 조화, 중요한 선택, 깊은 연결, 균형",
        "역위치": "갈등, 잘못된 선택, 불균형, 이별",
        "아이콘": "💕"
    },
    "7. 전차 (The Chariot)": {
        "의미": "의지력, 승리, 통제, 결정",
        "정위치": "목표 달성, 승리, 통제력, 의지와 결단",
        "역위치": "방향 상실, 통제 부족, 내적 갈등, 좌절",
        "아이콘": "🏇"
    },
    "8. 힘 (Strength)": {
        "의미": "내적 힘, 인내, 용기, 극복",
        "정위치": "내적 힘, 인내와 용기, 극복, 부드러운 힘",
        "역위치": "약함, 인내 부족, 통제 상실, 자신감 저하",
        "아이콘": "🦁"
    },
    "9. 은둔자 (The Hermit)": {
        "의미": "성찰, 내적 지혜, 안내, 고독",
        "정위치": "성찰과 내적 탐구, 지혜의 찾음, 안내자의 역할",
        "역위치": "고립, 외로움, 내면 회피, 지도 부족",
        "아이콘": "🕯️"
    },
    "10. 운명의 바퀴 (Wheel of Fortune)": {
        "의미": "순환, 변화, 운명, 전환점",
        "정위치": "운명의 전환, 긍정적 변화, 기회, 순환",
        "역위치": "불운, 변화 저항, 운명에의 맹목적 의존",
        "아이콘": "🎡"
    },
    "11. 정의 (Justice)": {
        "의미": "균형, 공정, 진실, 책임",
        "정위치": "공정함, 균형, 진실, 책임과 결과",
        "역위치": "불공정, 불균형, 책임 회피, 편견",
        "아이콘": "⚖️"
    },
    "12. 매달린 남자 (The Hanged Man)": {
        "의미": "희생, 새로운 관점, 인내, 깨달음",
        "정위치": "새로운 관점, 인내와 희생, 깨달음, 기다림",
        "역위치": "불필요한 희생, 지연, 희망 상실, 무기력",
        "아이콘": "🙏"
    },
    "13. 죽음 (Death)": {
        "의미": "종료, 변화, 재생, 새로운 시작",
        "정위치": "필요한 종료, 변화와 재생, 새로운 시작, 전환",
        "역위치": "변화 저항, 끝맺음 실패, 정체, 과거에의 집착",
        "아이콘": "💀"
    },
    "14. 절제 (Temperance)": {
        "의미": "균형, 조화, 절제, 융합",
        "정위치": "균형과 조화, 절제, 인내, 조정",
        "역위치": "불균형, 과도함, 조절 실패, 갈등",
        "아이콘": "🍷"
    },
    "15. 악마 (The Devil)": {
        "의미": "유혹, 속박, 중독, 물질주의",
        "정위치": "유혹과 속박, 중독성 패턴, 물질주의, 의존",
        "역위치": "속박 해제, 자유의 획득, 중독 극복, 해방",
        "아이콘": "👹"
    },
    "16. 탑 (The Tower)": {
        "의미": "파괴, 변화, 계시, 해방",
        "정위치": "갑작스러운 변화, 계시, 거짓의 파괴, 해방",
        "역위치": "변화 저항, 억압, 거짓의 유지, 불안",
        "아이콘": "🗼"
    },
    "17. 별 (The Star)": {
        "의미": "희망, 영감, 치유, 긍정적 미래",
        "정위치": "희망과 영감, 치유, 평화, 긍정적 전망",
        "역위치": "희망 상실, 낙담, 영감 부족, 비관",
        "아이콘": "⭐"
    },
    "18. 달 (The Moon)": {
        "의미": "불안, 환상, 직관, 무의식",
        "정위치": "불안과 불확실성, 환상, 직관, 무의식의 탐구",
        "역위치": "혼란 해소, 진실 발견, 직관 신뢰, 명확성",
        "아이콘": "🌙"
    },
    "19. 태양 (The Sun)": {
        "의미": "기쁨, 성공, 활력, 긍정적 에너지",
        "정위치": "기쁨과 성공, 활력, 긍정적 에너지, 낙관",
        "역위치": "과도한 낙관, 성공의 일시성, 에너지 낭비",
        "아이콘": "☀️"
    },
    "20. 심판 (Judgement)": {
        "의미": "재생, 깨달음, 용서, 새로운 시작",
        "정위치": "재생과 깨달음, 용서, 새로운 시작, 자기 성찰",
        "역위치": "자기 비판, 과거에의 집착, 용서 불가, 후회",
        "아이콘": "📯"
    },
    "21. 세계 (The World)": {
        "의미": "완성, 성취, 여행의 끝, 통합",
        "정위치": "완성과 성취, 목표 달성, 통합, 여정의 완료",
        "역위치": "완성 지연, 목표 미달성, 불완전함, 정체",
        "아이콘": "🌍"
    }
}


# 타로 스프레드 타입
SPREAD_TYPES = {
    "1장": {
        "이름": "원 카드",
        "설명": "현재 상황에 대한 간단한 통찰",
        "위치": ["현재"]
    },
    "3장": {
        "이름": "과거·현재·미래",
        "설명": "시간의 흐름을 통한 상황 이해",
        "위치": ["과거", "현재", "미래"]
    },
    "5장": {
        "이름": "켈틱 크로스",
        "설명": "상황에 대한 깊이 있는 종합 분석",
        "위치": ["현재 상황", "도전", "과거", "근본 원인", "미래 전망"]
    }
}


def draw_tarot_cards(spread_type, question=""):
    """
    타로 카드를 뽑습니다.
    
    Args:
        spread_type: 스프레드 타입 ("1장", "3장", "5장")
        question: 질문 (선택사항)
        
    Returns:
        dict: 타로 뽑기 결과
    """
    if spread_type not in SPREAD_TYPES:
        spread_type = "1장"
    
    num_cards = len(SPREAD_TYPES[spread_type]['위치'])
    
    # 카드 선택 (중복 없이)
    selected_cards = random.sample(list(TAROT_CARDS.keys()), num_cards)
    
    # 각 카드의 정/역 위치 랜덤 결정
    result = []
    for i, card_name in enumerate(selected_cards):
        is_reversed = random.choice([True, False])
        card_data = TAROT_CARDS[card_name].copy()
        card_data['카드명'] = card_name
        card_data['is_reversed'] = is_reversed
        card_data['위치'] = SPREAD_TYPES[spread_type]['위치'][i]
        # 기본 이미지 경로 추가
        card_data['default_image'] = get_tarot_card_image_path(card_name)
        result.append(card_data)
    
    return {
        'spread_type': spread_type,
        'question': question,
        'cards': result
    }


def generate_comprehensive_analysis(result):
    """
    종합 해석을 생성합니다.
    
    Args:
        result: 타로 뽑기 결과 딕셔너리
        
    Returns:
        dict: 종합 해석 데이터
    """
    spread_type = result['spread_type']
    cards = result['cards']
    question = result.get('question', '')
    
    analysis = {
        'overall_theme': '',
        'card_relationships': [],
        'key_messages': [],
        'advice': [],
        'warning': [],
        'detailed_interpretation': ''
    }
    
    # 전체 테마 분석
    reversed_count = sum(1 for card in cards if card['is_reversed'])
    total_cards = len(cards)
    positive_count = total_cards - reversed_count
    
    if reversed_count == 0:
        analysis['overall_theme'] = "모든 카드가 정위치로 나타나, 긍정적인 에너지와 명확한 방향성을 보여줍니다. 현재 상황이 순조롭게 흐르고 있으며, 카드들이 제시하는 메시지를 신뢰하고 따를 수 있는 시기입니다."
    elif reversed_count <= total_cards // 3:
        analysis['overall_theme'] = "대부분의 카드가 정위치로, 전반적으로 긍정적인 흐름을 보입니다. 일부 역위치 카드는 주의사항이나 내면의 변화를 나타내므로, 균형을 유지하며 조심스럽게 나아가시기 바랍니다."
    elif reversed_count <= total_cards * 2 // 3:
        analysis['overall_theme'] = "정위치와 역위치 카드가 혼재되어 있어, 상황이 복잡하고 변화가 많은 시기임을 나타냅니다. 카드들이 제시하는 메시지를 신중하게 고려하고, 내면의 목소리에 귀 기울이는 것이 중요합니다."
    else:
        analysis['overall_theme'] = "대부분의 카드가 역위치로 나타나, 현재 상황에 어려움이나 도전이 있음을 시사합니다. 그러나 역위치 카드는 변화와 성장의 기회이기도 합니다. 인내와 성찰을 통해 새로운 관점을 얻을 수 있습니다."
    
    # 스프레드 타입별 분석
    if spread_type == "1장":
        card = cards[0]
        analysis['detailed_interpretation'] = f"""
 현재 상황을 가장 잘 나타내는 카드는 <strong>{card['카드명']}</strong>입니다.
{'역위치로 나타난' if card['is_reversed'] else '정위치로 나타난'} 이 카드는 {card['역위치'] if card['is_reversed'] else card['정위치']}의 의미를 담고 있습니다.

현재 시점에서 가장 중요한 것은 이 카드가 제시하는 메시지입니다. 
{'역위치 카드가 나타난 것은' if card['is_reversed'] else '정위치 카드가 나타난 것은'} 현재 상황에서 {'주의해야 할 점이나 내면의 변화가 필요함을' if card['is_reversed'] else '순조로운 흐름과 명확한 방향성을'} 나타냅니다.
{question if question else '질문하신 내용'}에 대해, 이 카드는 {'신중한 접근과 성찰' if card['is_reversed'] else '적극적인 행동과 신뢰'}를 제안합니다.
        """
    
    elif spread_type == "3장":
        past_card = cards[0]
        present_card = cards[1]
        future_card = cards[2]
        
        analysis['detailed_interpretation'] = f"""
<strong>과거의 흐름:</strong> {past_card['카드명']}이 {'역위치로' if past_card['is_reversed'] else '정위치로'} 나타난 것은, 
과거에 {past_card['역위치'] if past_card['is_reversed'] else past_card['정위치']}의 경험이 있었음을 의미합니다.
이 경험이 현재 상황의 기반이 되었습니다.

<strong>현재 상황:</strong> {present_card['카드명']}이 {'역위치로' if present_card['is_reversed'] else '정위치로'} 나타나, 
현재는 {present_card['역위치'] if present_card['is_reversed'] else present_card['정위치']}의 상태에 있습니다.
{'역위치' if present_card['is_reversed'] else '정위치'} 카드는 현재 시점에서 {'내면의 변화나 주의가 필요함' if present_card['is_reversed'] else '명확한 방향과 긍정적인 흐름'}을 나타냅니다.

<strong>미래 전망:</strong> {future_card['카드명']}이 {'역위치로' if future_card['is_reversed'] else '정위치로'} 나타난 것은, 
앞으로 {future_card['역위치'] if future_card['is_reversed'] else future_card['정위치']}의 흐름이 예상됩니다.
{'역위치 카드' if future_card['is_reversed'] else '정위치 카드'}는 미래에 {'변화와 새로운 관점이 필요' if future_card['is_reversed'] else '순조로운 진행과 성공'}할 가능성을 시사합니다.

<strong>시간의 흐름:</strong> 과거부터 현재, 미래로 이어지는 카드들의 흐름을 보면, 
{'변화와 전환이 중심' if (past_card['is_reversed'] or present_card['is_reversed'] or future_card['is_reversed']) else '안정적이고 순조로운 발전'}의 패턴을 보입니다.
        """
        
        # 카드 관계성 분석
        if past_card['is_reversed'] and not present_card['is_reversed'] and not future_card['is_reversed']:
            analysis['card_relationships'].append("과거의 어려움을 극복하고 현재와 미래로 긍정적으로 전환되고 있습니다.")
        elif not past_card['is_reversed'] and present_card['is_reversed'] and future_card['is_reversed']:
            analysis['card_relationships'].append("과거의 안정에서 현재와 미래로 변화의 시기가 다가오고 있습니다.")
        elif past_card['is_reversed'] and present_card['is_reversed'] and not future_card['is_reversed']:
            analysis['card_relationships'].append("과거와 현재의 도전을 통해 미래에 새로운 가능성이 열립니다.")
    
    elif spread_type == "5장":
        current_card = cards[0]
        challenge_card = cards[1]
        past_card = cards[2]
        root_card = cards[3]
        future_card = cards[4]
        
        analysis['detailed_interpretation'] = f"""
<strong>현재 상황:</strong> {current_card['카드명']}이 {'역위치로' if current_card['is_reversed'] else '정위치로'} 나타나, 
현재는 {current_card['역위치'] if current_card['is_reversed'] else current_card['정위치']}의 상태입니다.

<strong>도전과 장애물:</strong> {challenge_card['카드명']}이 {'역위치로' if challenge_card['is_reversed'] else '정위치로'} 나타나, 
앞서 나아가는데 {challenge_card['역위치'] if challenge_card['is_reversed'] else challenge_card['정위치']}의 도전이 있습니다.
{'역위치 카드' if challenge_card['is_reversed'] else '정위치 카드'}는 {'내면의 변화나 접근 방식의 전환이 필요' if challenge_card['is_reversed'] else '명확한 목표와 의지로 극복 가능'}함을 의미합니다.

<strong>과거의 영향:</strong> {past_card['카드명']}이 {'역위치로' if past_card['is_reversed'] else '정위치로'} 나타나, 
과거에 {past_card['역위치'] if past_card['is_reversed'] else past_card['정위치']}의 경험이 현재 상황에 영향을 미치고 있습니다.

<strong>근본 원인:</strong> {root_card['카드명']}이 {'역위치로' if root_card['is_reversed'] else '정위치로'} 나타나, 
상황의 근본 원인은 {root_card['역위치'] if root_card['is_reversed'] else root_card['정위치']}와 관련이 있습니다.
{'역위치 카드' if root_card['is_reversed'] else '정위치 카드'}는 {'내면의 문제나 인식의 전환 필요' if root_card['is_reversed'] else '명확한 기반과 원칙'}을 나타냅니다.

<strong>미래 전망:</strong> {future_card['카드명']}이 {'역위치로' if future_card['is_reversed'] else '정위치로'} 나타나, 
앞으로 {future_card['역위치'] if future_card['is_reversed'] else future_card['정위치']}의 결과가 예상됩니다.

<strong>종합 분석:</strong> 켈틱 크로스 스프레드는 상황의 다양한 층위를 보여줍니다. 
현재 상황, 도전, 과거의 영향, 근본 원인, 미래 전망을 종합하면, 
{analyze_celtic_cross(cards)}의 흐름을 읽을 수 있습니다.
        """
        
        # 켈틱 크로스 특별 분석
        analysis['card_relationships'].extend(analyze_celtic_cross_relationships(cards))
    
    # 핵심 메시지 추출
    analysis['key_messages'] = extract_key_messages(cards, spread_type)
    
    # 조언과 경고
    analysis['advice'] = generate_advice(cards, spread_type)
    analysis['warning'] = generate_warnings(cards, spread_type)
    
    return analysis


def analyze_celtic_cross(cards):
    """켈틱 크로스 스프레드의 전체 흐름을 분석합니다."""
    current = cards[0]
    challenge = cards[1]
    future = cards[4]
    
    if not current['is_reversed'] and not challenge['is_reversed'] and not future['is_reversed']:
        return "현재부터 미래까지 매우 순조롭고 긍정적인 흐름"
    elif current['is_reversed'] and not challenge['is_reversed'] and not future['is_reversed']:
        return "현재의 변화를 통해 미래로 순조롭게 발전하는 흐름"
    elif not current['is_reversed'] and challenge['is_reversed'] and not future['is_reversed']:
        return "도전을 극복하고 미래로 발전하는 흐름"
    elif current['is_reversed'] and challenge['is_reversed'] and not future['is_reversed']:
        return "현재의 변화와 도전을 통해 미래에 새로운 가능성 열리는 흐름"
    elif current['is_reversed'] and challenge['is_reversed'] and future['is_reversed']:
        return "변화와 전환이 중심이 되는 복잡한 흐름"
    else:
        return "균형과 조화를 이루는 발전적인 흐름"


def analyze_celtic_cross_relationships(cards):
    """켈틱 크로스 스프레드의 카드 간 관계성을 분석합니다."""
    relationships = []
    
    current = cards[0]
    challenge = cards[1]
    root = cards[3]
    future = cards[4]
    
    # 현재와 도전의 관계
    if current['is_reversed'] == challenge['is_reversed']:
        relationships.append("현재 상황과 도전이 서로 조화를 이루고 있어, 균형잡힌 접근이 가능합니다.")
    else:
        relationships.append("현재 상황과 도전이 서로 다른 에너지를 보여, 균형과 조정이 필요합니다.")
    
    # 근본 원인과 미래의 관계
    if root['is_reversed'] != future['is_reversed']:
        relationships.append("근본 원인의 해결을 통해 미래로 긍정적인 전환이 예상됩니다.")
    
    return relationships


def extract_key_messages(cards, spread_type):
    """카드들에서 핵심 메시지를 추출합니다."""
    messages = []
    
    # 역위치 카드가 많은 경우
    reversed_count = sum(1 for card in cards if card['is_reversed'])
    if reversed_count > len(cards) / 2:
        messages.append("내면의 변화와 새로운 관점이 필요한 시기입니다.")
        messages.append("현재의 고정관념이나 패턴을 재검토하는 것이 중요합니다.")
    
    # 정위치 카드가 많은 경우
    if reversed_count < len(cards) / 2:
        messages.append("카드들이 제시하는 방향을 신뢰하고 따를 수 있는 시기입니다.")
        messages.append("긍정적인 에너지와 명확한 방향성이 있습니다.")
    
    # 특정 카드 조합 분석
    card_names = [card['카드명'] for card in cards]
    
    # 죽음 + 태양 조합
    if any("죽음" in name for name in card_names) and any("태양" in name for name in card_names):
        messages.append("끝과 새로운 시작이 함께 나타나, 중요한 전환점에 있습니다.")
    
    # 연인 + 세계 조합
    if any("연인" in name for name in card_names) and any("세계" in name for name in card_names):
        messages.append("관계와 완성이 연결되어, 중요한 선택이 성공으로 이어질 가능성이 있습니다.")
    
    # 바보 + 세계 조합
    if any("바보" in name for name in card_names) and any("세계" in name for name in card_names):
        messages.append("새로운 시작에서 완성까지의 여정이 그려집니다.")
    
    return messages


def generate_advice(cards, spread_type):
    """카드들로부터 조언을 생성합니다."""
    advice = []
    
    reversed_count = sum(1 for card in cards if card['is_reversed'])
    total_cards = len(cards)
    
    if reversed_count == 0:
        advice.append("카드들이 제시하는 방향을 신뢰하고 적극적으로 행동하세요.")
        advice.append("현재의 흐름을 유지하며 목표를 향해 나아가세요.")
    elif reversed_count <= total_cards // 3:
        advice.append("대부분의 카드가 긍정적인 메시지를 보여주므로, 자신감을 가지고 나아가세요.")
        advice.append("일부 역위치 카드가 나타내는 주의사항을 고려하여 균형을 유지하세요.")
    else:
        advice.append("내면의 목소리에 귀 기울이고, 성찰과 인내를 가지고 접근하세요.")
        advice.append("변화의 시기이므로 유연성과 적응력을 발휘하세요.")
    
    # 스프레드 타입별 특별 조언
    if spread_type == "3장":
        past_card = cards[0]
        present_card = cards[1]
        if past_card['is_reversed'] and not present_card['is_reversed']:
            advice.append("과거의 어려움을 극복한 경험을 바탕으로 현재를 밀고 나가세요.")
    
    return advice


def generate_warnings(cards, spread_type):
    """카드들로부터 경고를 생성합니다."""
    warnings = []
    
    reversed_count = sum(1 for card in cards if card['is_reversed'])
    total_cards = len(cards)
    
    if reversed_count > total_cards / 2:
        warnings.append("대부분의 카드가 역위치로 나타나, 성급한 결정을 피하고 신중하게 접근하세요.")
        warnings.append("내면의 변화와 성찰이 필요한 시기이므로, 외부의 압력보다는 자신의 목소리를 들어보세요.")
    
    # 특정 카드 조합 경고
    card_names = [card['카드명'] for card in cards]
    
    if any("탑" in name for name in card_names):
        warnings.append("탑 카드가 나타난 경우, 갑작스러운 변화나 계시가 있을 수 있습니다. 유연성과 적응력이 중요합니다.")
    
    if any("악마" in name for name in card_names) and any(card['is_reversed'] for card in cards if "악마" in card['카드명']):
        warnings.append("악마 카드가 역위치로 나타난 경우, 속박이나 중독에서 해방되기 위해 노력이 필요합니다.")
    
    return warnings

