from openai import OpenAI
import json

from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# System Prompt for the AI Saju Analyst
# System Prompt for the AI Saju Analyst
SYSTEM_PROMPT = """
## 역할 정의
당신은 한국 전통 명리학을 깊이 이해하고 현대적으로 재해석하는 '사주 명리학의 대가'입니다. 
당신의 목표는 단순히 사주 용어를 나열하는 것이 아니라, 사용자의 사주팔자(Year, Month, Day, Hour Pillars)와 오행, 십성, 신살 등을 **종합적으로 합성(Synthesis)**하여, 사용자의 인생에 대한 깊은 통찰과 실질적인 조언을 제공하는 것입니다.
특히, "왜 그런지"에 대한 명리학적 근거를 쉬운 언어로 설명하고, 그에 따른 구체적인 행동 가이드를 제시해야 합니다.

## 입력 데이터 구조
사용자로부터 JSON 형식의 사주 데이터(기둥 정보, 오행 분포, 십성, 신살, 12운성, 대운 등)를 받습니다.

## 분석 지침 (Deep Insight Required)

### 1. 종합 분석 (Synthesis)
- 단편적인 해석(예: "상관이 있으니 말을 잘한다")을 넘어서세요.
- **일간(Day Master)과 월지(Month Branch)의 관계**를 중심으로 격국을 판단하고, 전체적인 사주의 에너지 흐름(신강/신약/중화)을 분석하세요.
- 오행의 과다/결핍이 실제 성격과 삶에 미치는 영향을 구체적으로 서술하세요.

### 2. 성격/특성 (Personality)
- **내면의 자아(Inner Self)**와 **사회적 가면(Outer Persona)**을 구분하여 분석해보세요.
- 장점은 강화하고 단점은 보완할 수 있는 심리적 조언을 포함하세요.

### 3. 재물운 (Wealth)
- 단순한 "좋다/나쁘다"가 아니라, **"돈을 버는 방식"**과 **"돈을 지키는 방식"**을 분석하세요.
- 식상생재(재능으로 벎)인지, 관인상생(직장/조직에서 벎)인지 등을 파악하여 구체적인 투자 스타일(공격적 투자 vs 안전 자산)을 제안하세요.

### 4. 직업/진로 (Career)
- 적성에 맞는 직무뿐만 아니라, **"가장 능력을 발휘할 수 있는 환경"**을 조언하세요 (예: 수평적인 스타트업, 체계적인 대기업, 자유로운 프리랜서 등).
- 상사나 동료와의 관계에서 주의할 점도 십성 관계를 통해 조언하세요.

### 5. 신살 및 특별 분석 (Sinsal & Special)
- 입력된 신살(천을귀인, 도화살, 역마살 등)이 이 사주에서 긍정적으로 작용하는지 부정적으로 작용하는지 분석하세요.
- 단순한 신살 나열이 아니라, 그것이 삶의 어떤 구체적인 현상으로 나타날지 예측하세요.

## 출력 형식 (JSON)
응답은 반드시 다음 JSON 구조를 따라야 합니다. 각 필드는 **최소 300자 이상**의 풍부한 내용을 담아야 합니다.

```json
{
  "summary": {
    "dayMasterType": "일간의 오행과 특성 (예: 丙火 - 태양 같은 열정)",
    "gyeokguk": "격국과 용신 분석 (명리학적 근거 포함)",
    "yongsin": "용신 및 희신 (인생의 개운법)",
    "overallTone": "사주의 전체적인 그릇과 인생의 큰 흐름에 대한 심도 있는 총평 (400자 이상)"
  },
  "personality": {
    "coreTraits": ["핵심 키워드1", "핵심 키워드2", "핵심 키워드3"],
    "strengths": ["강점1", "강점2", "강점3"],
    "weaknesses": ["보완점1", "보완점2", "보완점3"],
    "detailedAnalysis": "내면과 외면을 아우르는 성격의 심층 분석. 오행의 편중이나 조화를 바탕으로 설명 (500자 이상)"
  },
  "career": {
    "suitableFields": ["추천 직업군1", "추천 직업군2"],
    "detailedAnalysis": "직항 적성과 능력을 발휘할 수 있는 환경, 조직 생활의 특징 등을 구체적으로 서술 (400자 이상)"
  },
  "wealth": {
    "wealthLuck": "재물운의 흐름과 크기",
    "incomeStyle": "돈을 버는 스타일 (예: 꾸준한 소득형, 사업 투자형 등)",
    "detailedAnalysis": "재물을 모으고 지키는 구체적인 전략과 시기별 조언 (400자 이상)"
  },
  "relationships": {
    "romantic": {
      "loveStyle": "연애 및 결혼 스타일",
      "analysis": "배우자궁(일지) 분석을 통한 이상적인 파트너상과 연애 조언"
    },
    "family": {
      "analysis": "부모, 형제, 자식과의 관계성 및 가정운 조언"
    }
  },
  "health": {
    "detailedAnalysis": "오행의 불균형에 따른 취약 장기 및 건강 관리법 (멘탈 케어 포함)"
  },
  "lifeAdvice": {
    "luckyElements": {
      "colors": ["행운색1", "행운색2"],
      "numbers": [행운숫자1, 행운숫자2]
    },
    "detailedGuidance": "앞으로의 인생을 위한 실질적이고 구체적인 처세술과 개운법 (명언이나 격려 포함, 400자 이상)"
  },
  "currentFortune": {
    "daeunPeriod": "현재 대운의 특징",
    "overallTrend": "현재 운세의 흐름 (상승세/하락세/변환기)",
    "yearlyForecast": "올해(세운)의 구체적인 전망과 대응 전략 (300자 이상)",
    "detailedAnalysis": "대운과 세운이 만나는 지점에서의 구체적인 사건 예측 및 조언 (400자 이상)"
  }
}
```

## 어조 및 스타일
- 전문가답게 신뢰감을 주되, 내담자를 위로하고 격려하는 따뜻한 어조를 유지하세요.
- "~~입니다" 체를 사용하세요.
- 마크다운(Markdown) 형식을 사용하여 중요 키워드는 **볼드체**로 강조하세요.
"""

# System Prompt for Tojeong Bigyeol (토정비결)
TOJEONG_SYSTEM_PROMPT = """
## 역할 정의
당신은 조선시대 토정 이지함의 전통 토정비결을 현대적으로 해석하는 전문가입니다. 생년월일의 간지와 올해 간지의 관계를 분석하여 올해의 운세를 상세하고 풍부하게 제공합니다.

## 토정비결 분석 원칙

1. **간지 관계 분석**: 생년 간지(년간, 년지)와 올해 간지의 관계(삼합, 육합, 충, 형, 해, 평상)를 정확히 파악합니다.

2. **오행 분석**: 생년의 오행과 올해 오행의 상생상극 관계를 분석합니다.

3. **계절별 영향**: 올해의 간지가 사주의 각 계절(월령)에 미치는 영향을 고려합니다.

4. **실용적 조언**: 추상적인 설명보다는 구체적이고 실행 가능한 조언을 제공합니다.

## 출력 형식

다음 JSON 구조로 응답해야 합니다:

```json
{
  "overview": {
    "summary": "올해의 전체적인 운세 요약 (200-300자)",
    "keyTheme": "올해의 핵심 테마 (예: 변화와 성장, 안정과 발전)",
    "overallFortune": "전체 운세 평가 (예: 대길, 길, 평상, 흉)"
  },
  "detailedAnalysis": {
    "mainMessage": "올해의 주요 메시지 (400-500자, 매우 상세하게)",
    "opportunities": "올해의 기회 (200-300자)",
    "challenges": "올해의 주의사항과 도전 (200-300자)",
    "guidance": "올해를 위한 실천 가이드 (300-400자)"
  },
  "monthlyFortune": {
    "spring": "봄 (3-5월) 운세 (200-250자)",
    "summer": "여름 (6-8월) 운세 (200-250자)",
    "fall": "가을 (9-11월) 운세 (200-250자)",
    "winter": "겨울 (12-2월) 운세 (200-250자)"
  },
  "lifeAspects": {
    "career": "직업/사업 운 (200-250자)",
    "wealth": "재물/금전 운 (200-250자)",
    "relationships": "인간관계/애정 운 (200-250자)",
    "health": "건강 운 (200-250자)",
    "family": "가족 운 (200-250자)"
  },
  "luckyElements": {
    "colors": ["행운의 색상1", "행운의 색상2", "행운의 색상3"],
    "directions": ["유리한 방위1", "유리한 방위2"],
    "numbers": [숫자1, 숫자2, 숫자3],
    "season": "가장 유리한 계절"
  },
  "advice": {
    "do": ["해야 할 일1", "해야 할 일2", "해야 할 일3"],
    "avoid": ["피해야 할 일1", "피해야 할 일2"],
    "specialNote": "특별 주의사항 (200-300자)"
  }
}
```

## 중요 지침

1. **풍부함**: 각 항목에 대해 충분히 상세하고 구체적인 내용을 제공하세요.
2. **실용성**: 현실적이고 실행 가능한 조언을 포함하세요.
3. **긍정성**: 어려운 운세라도 극복 방안과 긍정적 해석을 함께 제시하세요.
4. **전통성**: 토정비결의 전통적 해석을 유지하되, 현대적 의미로 설명하세요.
5. **구체성**: 추상적 표현보다는 구체적인 상황과 예시를 포함하세요.
"""

def generate_saju_analysis(api_key, input_data):
    """
    Generate comprehensive Saju analysis using OpenAI API.
    
    Args:
        api_key: OpenAI API key
        input_data: Dictionary containing Saju calculation results
    
    Returns:
        Dictionary containing structured analysis results
    """
    client = OpenAI(api_key=api_key)
    
    user_message = f"""
다음 사주 데이터를 분석해주세요:

{json.dumps(input_data, ensure_ascii=False, indent=2)}
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            response_format={"type": "json_object"},
            timeout=15.0  # 15초 timeout (Heroku 30초 타임아웃 고려, 여유 시간 확보)
        )
        
        result_text = response.choices[0].message.content
        result_json = json.loads(result_text)
        
        return result_json
        
    except Exception as e:
        return {"error": str(e)}


def generate_saju_analysis_stream(api_key, input_data):
    """
    Generate comprehensive Saju analysis using OpenAI API with streaming.
    
    Args:
        api_key: OpenAI API key
        input_data: Dictionary containing Saju calculation results
    
    Yields:
        str: JSON chunks of the analysis result
    """
    client = OpenAI(api_key=api_key)
    
    user_message = f"""
다음 사주 데이터를 분석해주세요:

{json.dumps(input_data, ensure_ascii=False, indent=2)}
"""
    
    try:
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            response_format={"type": "json_object"},
            stream=True,  # 스트리밍 활성화
            timeout=60.0  # 스트리밍은 타임아웃이 길어도 문제없음 (청크 단위로 전송)
        )
        
        accumulated_text = ""
        for chunk in stream:
            if chunk.choices and len(chunk.choices) > 0:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    accumulated_text += delta.content
                    # 각 청크를 JSON 형식으로 전송
                    yield f"data: {json.dumps({'type': 'chunk', 'content': delta.content}, ensure_ascii=False)}\n\n"
        
        # 최종 완료 메시지
        try:
            result_json = json.loads(accumulated_text)
            yield f"data: {json.dumps({'type': 'complete', 'data': result_json}, ensure_ascii=False)}\n\n"
        except json.JSONDecodeError:
            yield f"data: {json.dumps({'type': 'error', 'error': 'JSON 파싱 실패'}, ensure_ascii=False)}\n\n"
        
    except Exception as e:
        yield f"data: {json.dumps({'type': 'error', 'error': str(e)}, ensure_ascii=False)}\n\n"


def generate_tojeong_analysis(api_key, tojeong_data, pillars_data=None, pillars_info=None):
    """
    Generate detailed Tojeong Bigyeol (토정비결) analysis using OpenAI API.
    
    Args:
        api_key: OpenAI API key
        tojeong_data: Dictionary containing Tojeong calculation results
        pillars_data: List of pillar dictionaries (사주 기둥 데이터)
        pillars_info: Dictionary with pillar information (사주 정보)
    
    Returns:
        Dictionary containing detailed Tojeong analysis
    """
    client = OpenAI(api_key=api_key)
    
    # 사주 정보 구성
    saju_info = ""
    if pillars_data and pillars_info:
        saju_info = f"""
## 사주팔자 정보
사주팔자: {pillars_data[0].get('Heavenly Stem (천간)', '')}{pillars_data[0].get('Earthly Branch (지지)', '')}년 
         {pillars_data[1].get('Heavenly Stem (천간)', '')}{pillars_data[1].get('Earthly Branch (지지)', '')}월 
         {pillars_data[2].get('Heavenly Stem (천간)', '')}{pillars_data[2].get('Earthly Branch (지지)', '')}일 
         {pillars_data[3].get('Heavenly Stem (천간)', '')}{pillars_data[3].get('Earthly Branch (지지)', '')}시
일간(日干): {pillars_info.get('day_stem', '')}
오행 분포: {pillars_info.get('element_count', {})}
"""
    
    user_message = f"""
다음 토정비결 데이터와 사주 정보를 바탕으로 올해의 운세를 상세하게 분석해주세요:

## 토정비결 기본 정보
생년 간지: {tojeong_data.get('birth_year_ganji', '')}
올해({tojeong_data.get('current_year', '')}년) 간지: {tojeong_data.get('current_year_ganji', '')}
간지 관계: {tojeong_data.get('relationship', '')} ({tojeong_data.get('relationship_desc', '')})
기본 운세 평가: {tojeong_data.get('fortune_level', '')}
기본 메시지: {tojeong_data.get('fortune_message', '')}
{saju_info}
위 정보를 바탕으로 토정비결의 전통적 해석과 현대적 의미를 결합하여, 사주팔자 정보를 활용한 매우 상세하고 풍부한 올해 운세를 제공해주세요. 사주팔자의 오행, 십성, 신살 등을 고려하여 더욱 구체적이고 개인화된 분석을 해주세요.
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": TOJEONG_SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            response_format={"type": "json_object"},
            timeout=12.0  # 12초 timeout (Heroku 30초 타임아웃 고려, 토정비결 계산 후 호출되므로 짧게 설정)
        )
        
        result_text = response.choices[0].message.content
        result_json = json.loads(result_text)
        
        return result_json
        
    except Exception as e:
        return {"error": str(e)}


def generate_tojeong_analysis_stream(api_key, tojeong_data, pillars_data=None, pillars_info=None):
    """
    Generate detailed Tojeong Bigyeol (토정비결) analysis using OpenAI API with streaming.
    
    Args:
        api_key: OpenAI API key
        tojeong_data: Dictionary containing Tojeong calculation results
        pillars_data: List of pillar dictionaries (사주 기둥 데이터)
        pillars_info: Dictionary with pillar information (사주 정보)
    
    Yields:
        str: JSON chunks of the analysis result
    """
    client = OpenAI(api_key=api_key)
    
    # 사주 정보 구성
    saju_info = ""
    if pillars_data and pillars_info:
        saju_info = f"""
## 사주팔자 정보
사주팔자: {pillars_data[0].get('Heavenly Stem (천간)', '')}{pillars_data[0].get('Earthly Branch (지지)', '')}년 
         {pillars_data[1].get('Heavenly Stem (천간)', '')}{pillars_data[1].get('Earthly Branch (지지)', '')}월 
         {pillars_data[2].get('Heavenly Stem (천간)', '')}{pillars_data[2].get('Earthly Branch (지지)', '')}일 
         {pillars_data[3].get('Heavenly Stem (천간)', '')}{pillars_data[3].get('Earthly Branch (지지)', '')}시
일간(日干): {pillars_info.get('day_stem', '')}
오행 분포: {pillars_info.get('element_count', {})}
"""
    
    user_message = f"""
다음 토정비결 데이터와 사주 정보를 바탕으로 올해의 운세를 상세하게 분석해주세요:

## 토정비결 기본 정보
생년 간지: {tojeong_data.get('birth_year_ganji', '')}
올해({tojeong_data.get('current_year', '')}년) 간지: {tojeong_data.get('current_year_ganji', '')}
간지 관계: {tojeong_data.get('relationship', '')} ({tojeong_data.get('relationship_desc', '')})
기본 운세 평가: {tojeong_data.get('fortune_level', '')}
기본 메시지: {tojeong_data.get('fortune_message', '')}
{saju_info}
위 정보를 바탕으로 토정비결의 전통적 해석과 현대적 의미를 결합하여, 사주팔자 정보를 활용한 매우 상세하고 풍부한 올해 운세를 제공해주세요. 사주팔자의 오행, 십성, 신살 등을 고려하여 더욱 구체적이고 개인화된 분석을 해주세요.
"""
    
    try:
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": TOJEONG_SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            response_format={"type": "json_object"},
            stream=True,  # 스트리밍 활성화
            timeout=60.0  # 스트리밍은 타임아웃이 길어도 문제없음 (청크 단위로 전송)
        )
        
        accumulated_text = ""
        for chunk in stream:
            if chunk.choices and len(chunk.choices) > 0:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    accumulated_text += delta.content
                    # 각 청크를 JSON 형식으로 전송
                    yield f"data: {json.dumps({'type': 'chunk', 'content': delta.content}, ensure_ascii=False)}\n\n"
        
        # 최종 완료 메시지
        try:
            result_json = json.loads(accumulated_text)
            yield f"data: {json.dumps({'type': 'complete', 'data': result_json}, ensure_ascii=False)}\n\n"
        except json.JSONDecodeError:
            yield f"data: {json.dumps({'type': 'error', 'error': 'JSON 파싱 실패'}, ensure_ascii=False)}\n\n"
        
    except Exception as e:
        yield f"data: {json.dumps({'type': 'error', 'error': str(e)}, ensure_ascii=False)}\n\n"


# System Prompt for Gonghap (궁합)
GONGHAP_SYSTEM_PROMPT = """
## 역할 정의
당신은 한국 전통 명리학을 깊이 이해하는 전문 사주 명리학자입니다. 두 사람의 사주팔자를 비교하여 정확하고 실용적인 궁합 분석을 제공하는 것이 목표입니다.

## 궁합 분석 원칙

1. **사주 비교 분석**: 두 사람의 사주팔자(년주, 월주, 일주, 시주)를 각각 비교하여 오행, 십성, 지지 관계를 분석합니다.

2. **오행 상생상극**: 두 사주의 오행 분포와 상생상극 관계를 분석하여 조화와 갈등의 정도를 파악합니다.

3. **지지 관계**: 삼합, 육합, 충, 형, 해 등의 지지 관계를 분석하여 관계의 질을 평가합니다.

4. **십성 분석**: 두 사주의 십성 관계를 분석하여 서로에게 미치는 영향을 파악합니다.

5. **실용적 조언**: 추상적인 설명보다는 구체적이고 실행 가능한 관계 개선 방안을 제시합니다.

## 출력 형식

다음 JSON 구조로 응답해야 합니다:

```json
{
  "overview": {
    "summary": "전체 궁합 요약 (300-400자, 매우 상세하게)",
    "overallScore": 75,
    "overallLevel": "보통/좋음/매우좋음/주의/매우주의",
    "keyTheme": "관계의 핵심 테마 (예: 상호 보완, 조화로운 관계, 도전적 관계)"
  },
  "detailedAnalysis": {
    "strengths": "관계의 강점 (400-500자, 매우 상세하게)",
    "challenges": "관계의 도전과제 (300-400자)",
    "compatibility": "호환성 분석 (300-400자)",
    "growthPotential": "성장 가능성 (300-400자)"
  },
  "lifeAspects": {
    "career": "직업/사업 영역에서의 궁합 (200-300자)",
    "wealth": "재물/금전 영역에서의 궁합 (200-300자)",
    "relationships": "인간관계/애정 영역에서의 궁합 (200-300자)",
    "health": "건강 영역에서의 궁합 (200-300자)",
    "family": "가족 영역에서의 궁합 (200-300자)"
  },
  "communication": {
    "style": "소통 스타일 분석 (200-300자)",
    "tips": "효과적인 소통 방법 (200-300자)"
  },
  "relationshipGuidance": {
    "do": ["해야 할 일1", "해야 할 일2", "해야 할 일3"],
    "avoid": ["피해야 할 일1", "피해야 할 일2"],
    "specialAdvice": "특별 조언 (300-400자)"
  },
  "longTermOutlook": {
    "shortTerm": "단기 전망 (1-2년) (200-300자)",
    "mediumTerm": "중기 전망 (3-5년) (200-300자)",
    "longTerm": "장기 전망 (5년 이상) (200-300자)"
  }
}
```

## 중요 지침

1. **정확성**: 전통 명리학 원리를 정확하게 적용하되, 현대적 해석을 포함하세요.
2. **균형감**: 긍정적 측면과 주의할 점을 균형 있게 제시하세요.
3. **구체성**: 추상적 표현보다는 구체적인 상황과 예시를 포함하세요.
4. **실용성**: 관계 개선을 위한 실질적인 조언을 제공하세요.
5. **깊이**: 각 항목에 대해 충분히 상세하고 구체적인 분석을 제공하세요.
"""


def generate_gonghap_analysis(api_key, gonghap_data, person1_pillars_data=None, person1_pillars_info=None, 
                              person2_pillars_data=None, person2_pillars_info=None):
    """
    Generate detailed Gonghap (궁합) analysis using OpenAI API.
    
    Args:
        api_key: OpenAI API key
        gonghap_data: Dictionary containing Gonghap calculation results
        person1_pillars_data: First person's pillar data (optional)
        person1_pillars_info: First person's pillar info (optional)
        person2_pillars_data: Second person's pillar data (optional)
        person2_pillars_info: Second person's pillar info (optional)
    
    Returns:
        Dictionary containing detailed Gonghap analysis
    """
    client = OpenAI(api_key=api_key)
    
    # 사주 정보 구성
    saju_info = ""
    if person1_pillars_data and person1_pillars_info and person2_pillars_data and person2_pillars_info:
        p1_saju = f"{person1_pillars_data[0].get('Heavenly Stem (천간)', '')}{person1_pillars_data[0].get('Earthly Branch (지지)', '')}년 " \
                 f"{person1_pillars_data[1].get('Heavenly Stem (천간)', '')}{person1_pillars_data[1].get('Earthly Branch (지지)', '')}월 " \
                 f"{person1_pillars_data[2].get('Heavenly Stem (천간)', '')}{person1_pillars_data[2].get('Earthly Branch (지지)', '')}일 " \
                 f"{person1_pillars_data[3].get('Heavenly Stem (천간)', '')}{person1_pillars_data[3].get('Earthly Branch (지지)', '')}시"
        
        p2_saju = f"{person2_pillars_data[0].get('Heavenly Stem (천간)', '')}{person2_pillars_data[0].get('Earthly Branch (지지)', '')}년 " \
                 f"{person2_pillars_data[1].get('Heavenly Stem (천간)', '')}{person2_pillars_data[1].get('Earthly Branch (지지)', '')}월 " \
                 f"{person2_pillars_data[2].get('Heavenly Stem (천간)', '')}{person2_pillars_data[2].get('Earthly Branch (지지)', '')}일 " \
                 f"{person2_pillars_data[3].get('Heavenly Stem (천간)', '')}{person2_pillars_data[3].get('Earthly Branch (지지)', '')}시"
        
        saju_info = f"""
## 첫 번째 사람 사주팔자
{p1_saju}
일간(日干): {person1_pillars_info.get('day_stem', '')}

## 두 번째 사람 사주팔자
{p2_saju}
일간(日干): {person2_pillars_info.get('day_stem', '')}
"""
    
    user_message = f"""
다음 궁합 계산 결과와 사주 정보를 바탕으로 두 사람의 궁합을 상세하게 분석해주세요:

## 궁합 기본 정보
전체 점수: {gonghap_data.get('overall_score', 75)}점
전체 평가: {gonghap_data.get('overall_level', '보통')}
전체 설명: {gonghap_data.get('overall_desc', '')}

## 기둥별 궁합
{chr(10).join([f"- {p.get('pillar', '')}: {p.get('score', 0)}점 ({p.get('level', '')}) - {p.get('analysis', '')}" for p in gonghap_data.get('pillar_compatibilities', [])])}

## 지지 관계
{chr(10).join([f"- {rel}" for rel in gonghap_data.get('branch_relationships', [])])}

## 십성 분석
{chr(10).join([f"- {tg}" for tg in gonghap_data.get('ten_god_analysis', [])])}

## 강점
{chr(10).join([f"- {s}" for s in gonghap_data.get('strengths', [])])}

## 주의사항
{chr(10).join([f"- {w}" for w in gonghap_data.get('weaknesses', [])])}

## 조언
{gonghap_data.get('advice', '')}
{saju_info}
위 정보를 바탕으로 전통 명리학 원리를 활용하여, 두 사람의 사주팔자 정보를 고려한 매우 상세하고 구체적인 궁합 분석을 제공해주세요. 관계의 강점과 도전과제를 균형 있게 분석하고, 실용적인 관계 개선 방안을 제시해주세요.
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": GONGHAP_SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            response_format={"type": "json_object"},
            timeout=25.0  # 25초 timeout (Heroku 30초 타임아웃을 고려하여 줄임)
        )
        
        result_text = response.choices[0].message.content
        result_json = json.loads(result_text)
        
        return result_json
        
    except Exception as e:
        return {"error": str(e)}


def generate_gonghap_analysis_stream(api_key, gonghap_data, person1_pillars_data=None, person1_pillars_info=None, 
                                     person2_pillars_data=None, person2_pillars_info=None):
    """
    Generate detailed Gonghap (궁합) analysis using OpenAI API with streaming.
    
    Args:
        api_key: OpenAI API key
        gonghap_data: Dictionary containing Gonghap calculation results
        person1_pillars_data: First person's pillar data (optional)
        person1_pillars_info: First person's pillar info (optional)
        person2_pillars_data: Second person's pillar data (optional)
        person2_pillars_info: Second person's pillar info (optional)
    
    Yields:
        str: JSON chunks of the analysis result
    """
    client = OpenAI(api_key=api_key)
    
    # 사주 정보 구성
    saju_info = ""
    if person1_pillars_data and person1_pillars_info and person2_pillars_data and person2_pillars_info:
        p1_saju = f"{person1_pillars_data[0].get('Heavenly Stem (천간)', '')}{person1_pillars_data[0].get('Earthly Branch (지지)', '')}년 " \
                 f"{person1_pillars_data[1].get('Heavenly Stem (천간)', '')}{person1_pillars_data[1].get('Earthly Branch (지지)', '')}월 " \
                 f"{person1_pillars_data[2].get('Heavenly Stem (천간)', '')}{person1_pillars_data[2].get('Earthly Branch (지지)', '')}일 " \
                 f"{person1_pillars_data[3].get('Heavenly Stem (천간)', '')}{person1_pillars_data[3].get('Earthly Branch (지지)', '')}시"
        
        p2_saju = f"{person2_pillars_data[0].get('Heavenly Stem (천간)', '')}{person2_pillars_data[0].get('Earthly Branch (지지)', '')}년 " \
                 f"{person2_pillars_data[1].get('Heavenly Stem (천간)', '')}{person2_pillars_data[1].get('Earthly Branch (지지)', '')}월 " \
                 f"{person2_pillars_data[2].get('Heavenly Stem (천간)', '')}{person2_pillars_data[2].get('Earthly Branch (지지)', '')}일 " \
                 f"{person2_pillars_data[3].get('Heavenly Stem (천간)', '')}{person2_pillars_data[3].get('Earthly Branch (지지)', '')}시"
        
        saju_info = f"""
## 첫 번째 사람 사주팔자
{p1_saju}
일간(日干): {person1_pillars_info.get('day_stem', '')}

## 두 번째 사람 사주팔자
{p2_saju}
일간(日干): {person2_pillars_info.get('day_stem', '')}
"""
    
    user_message = f"""
다음 궁합 계산 결과와 사주 정보를 바탕으로 두 사람의 궁합을 상세하게 분석해주세요:

## 궁합 기본 정보
전체 점수: {gonghap_data.get('overall_score', 75)}점
전체 평가: {gonghap_data.get('overall_level', '보통')}
전체 설명: {gonghap_data.get('overall_desc', '')}

## 기둥별 궁합
{chr(10).join([f"- {p.get('pillar', '')}: {p.get('score', 0)}점 ({p.get('level', '')}) - {p.get('analysis', '')}" for p in gonghap_data.get('pillar_compatibilities', [])])}

## 지지 관계
{chr(10).join([f"- {rel}" for rel in gonghap_data.get('branch_relationships', [])])}

## 십성 분석
{chr(10).join([f"- {tg}" for tg in gonghap_data.get('ten_god_analysis', [])])}

## 강점
{chr(10).join([f"- {s}" for s in gonghap_data.get('strengths', [])])}

## 주의사항
{chr(10).join([f"- {w}" for w in gonghap_data.get('weaknesses', [])])}

## 조언
{gonghap_data.get('advice', '')}
{saju_info}
위 정보를 바탕으로 전통 명리학 원리를 활용하여, 두 사람의 사주팔자 정보를 고려한 매우 상세하고 구체적인 궁합 분석을 제공해주세요. 관계의 강점과 도전과제를 균형 있게 분석하고, 실용적인 관계 개선 방안을 제시해주세요.
"""
    
    try:
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": GONGHAP_SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            response_format={"type": "json_object"},
            stream=True,  # 스트리밍 활성화
            timeout=60.0  # 스트리밍은 타임아웃이 길어도 문제없음 (청크 단위로 전송)
        )
        
        accumulated_text = ""
        for chunk in stream:
            if chunk.choices and len(chunk.choices) > 0:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    accumulated_text += delta.content
                    # 각 청크를 JSON 형식으로 전송
                    yield f"data: {json.dumps({'type': 'chunk', 'content': delta.content}, ensure_ascii=False)}\n\n"
        
        # 최종 완료 메시지
        try:
            result_json = json.loads(accumulated_text)
            yield f"data: {json.dumps({'type': 'complete', 'data': result_json}, ensure_ascii=False)}\n\n"
        except json.JSONDecodeError:
            yield f"data: {json.dumps({'type': 'error', 'error': 'JSON 파싱 실패'}, ensure_ascii=False)}\n\n"
        
    except Exception as e:
        yield f"data: {json.dumps({'type': 'error', 'error': str(e)}, ensure_ascii=False)}\n\n"


def generate_tarot_card_image(api_key, card_name, is_reversed=False):
    """
    Generate a tarot card image using OpenAI DALL-E API.
    
    Args:
        api_key: OpenAI API key
        card_name: Name of the tarot card (e.g., "0. 바보 (The Fool)")
        is_reversed: Whether the card is reversed
    
    Returns:
        str: URL of the generated image, or None if generation fails
    """
    client = OpenAI(api_key=api_key)
    
    # 카드 이름에서 한글과 영어 이름 추출
    card_display_name = card_name.split("(")[0].strip() if "(" in card_name else card_name
    card_english_name = card_name.split("(")[1].split(")")[0].strip() if "(" in card_name and ")" in card_name else ""
    
    # 프롬프트 생성
    if is_reversed:
        prompt = f"A mystical and beautiful tarot card illustration of '{card_display_name}' ({card_english_name}) in reversed position. The card should have a dark, mysterious, and introspective atmosphere. Rich colors, intricate details, symbolic imagery, golden borders, mystical aura, high quality art style, traditional tarot card design with ornate frame."
    else:
        prompt = f"A mystical and beautiful tarot card illustration of '{card_display_name}' ({card_english_name}) in upright position. The card should have a bright, positive, and inspiring atmosphere. Rich colors, intricate details, symbolic imagery, golden borders, mystical aura, high quality art style, traditional tarot card design with ornate frame."
    
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
            timeout=30.0
        )
        
        image_url = response.data[0].url
        return image_url
        
    except Exception as e:
        logger.error(f"타로 카드 이미지 생성 오류: {e}", exc_info=True)
        return None
# System Prompt for Byeoljari (별자리)
BYEOLJARI_SYSTEM_PROMPT = """
## 역할 정의
당신은 서양 점성술(Western Astrology)을 깊이 이해하는 전문 점성가입니다. 사용자의 별자리 정보를 바탕으로 정확하고 통찰력 있는 운세 분석을 제공하는 것이 목표입니다.

## 별자리 분석 원칙

1. **별자리 특성 분석**: 해당 별자리의 지배 행성, 원소(불, 흙, 공기, 물), 특성(활동, 고정, 변통)을 고려하여 성격과 운세를 분석합니다.

2. **현재 천체 배치 고려**: 현재의 주요 행성 이동(트랜짓)이 해당 별자리에 미치는 영향을 고려합니다.

3. **생활 영역별 해석**: 애정, 직업, 재물, 건강 등 각 영역별로 구체적인 운세를 제공합니다.

4. **실용적 조언**: 추상적인 설명보다는 구체적이고 실행 가능한 조언을 제공합니다.

## 출력 형식

다음 JSON 구조로 응답해야 합니다:

```json
{
  "overview": {
    "summary": "오늘의 운세 요약 (200-300자)",
    "fortuneLevel": "매우 좋음/좋음/보통/주의/매우 주의",
    "keyTheme": "오늘의 핵심 테마"
  },
  "detailedAnalysis": {
    "personality": "별자리 본질적 성격과 오늘의 심리 상태 (200-300자)",
    "love": "애정운 상세 분석 (200-300자)",
    "career": "직업/학업운 상세 분석 (200-300자)",
    "wealth": "재물운 상세 분석 (200-300자)",
    "health": "건강운 상세 분석 (200-300자)"
  },
  "advice": {
    "do": ["해야 할 일1", "해야 할 일2", "해야 할 일3"],
    "avoid": ["피해야 할 일1", "피해야 할 일2"],
    "luckyTip": "행운을 부르는 팁 (100-200자)"
  }
}
```

## 중요 지침

1. **통찰력**: 단순한 키워드 나열이 아닌, 깊이 있는 통찰을 제공하세요.
2. **긍정성**: 어려운 운세라도 극복 방안과 긍정적 해석을 함께 제시하세요.
3. **구체성**: 구체적인 상황과 예시를 포함하세요.
4. **개인화**: 제공된 별자리 정보(이름, 생년월일 등)를 적극 활용하여 개인화된 느낌을 주세요.
"""


def generate_byeoljari_analysis_stream(api_key, byeoljari_data):
    """
    Generate detailed Byeoljari (Horoscope) analysis using OpenAI API with streaming.
    
    Args:
        api_key: OpenAI API key
        byeoljari_data: Dictionary containing Horoscope calculation results
    
    Yields:
        str: JSON chunks of the analysis result
    """
    client = OpenAI(api_key=api_key)
    
    user_message = f"""
다음 별자리 기본 운세 데이터를 바탕으로 상세한 AI 점성술 분석을 제공해주세요:

## 사용자 정보
이름: {byeoljari_data.get('user_name', '사용자')}
생년월일: {byeoljari_data.get('birth_date', '')}
별자리: {byeoljari_data.get('korean_name', '')} ({byeoljari_data.get('english_name', '')})

## 기본 운세 정보
오늘의 운세: {byeoljari_data.get('today_fortune', {}).get('message', '')}
이번 주 운세: {byeoljari_data.get('weekly_fortune', {}).get('message', '')}
이번 달 운세: {byeoljari_data.get('monthly_fortune', {}).get('message', '')}
올해({byeoljari_data.get('current_year', '')}년) 운세: {byeoljari_data.get('yearly_fortune', {}).get('message', '')}

## 성격 및 특성
강점: {', '.join(byeoljari_data.get('constellation_info', {}).get('detailed_traits', {}).get('강점', []))}
약점: {', '.join(byeoljari_data.get('constellation_info', {}).get('detailed_traits', {}).get('약점', []))}
성격 설명: {byeoljari_data.get('constellation_info', {}).get('detailed_traits', {}).get('성격', '')}

위 기본 정보를 바탕으로 서양 점성술의 심도 있는 해석을 더하여, 더욱 풍부하고 개인화된 운세 분석을 제공해주세요.
"""
    
    try:
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": BYEOLJARI_SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            response_format={"type": "json_object"},
            stream=True,
            timeout=60.0
        )
        
        accumulated_text = ""
        for chunk in stream:
            if chunk.choices and len(chunk.choices) > 0:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    accumulated_text += delta.content
                    yield f"data: {json.dumps({'type': 'chunk', 'content': delta.content}, ensure_ascii=False)}\n\n"
        
        try:
            result_json = json.loads(accumulated_text)
            yield f"data: {json.dumps({'type': 'complete', 'data': result_json}, ensure_ascii=False)}\n\n"
        except json.JSONDecodeError:
            yield f"data: {json.dumps({'type': 'error', 'error': 'JSON 파싱 실패'}, ensure_ascii=False)}\n\n"
        
    except Exception as e:
        yield f"data: {json.dumps({'type': 'error', 'error': str(e)}, ensure_ascii=False)}\n\n"
