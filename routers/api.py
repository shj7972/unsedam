"""
API 라우터
AJAX 요청을 처리하는 API 엔드포인트를 정의합니다.
"""
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from datetime import datetime
import logging
import json
import saju_logic
import ai_analyst
from utils.api_key_fastapi import get_api_key, validate_api_key
from utils.security import validate_name, safe_error_message, is_production

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/calculate")
async def calculate_pillars(
    request: Request,
    name: str = Form(...),
    birth_date: str = Form(...),
    birth_time: str = Form(default=""),
    gender: str = Form(...),
    is_lunar: bool = Form(False)
):
    """사주 계산 API"""
    try:
        # is_lunar는 체크박스이므로 문자열로 올 수 있음
        if isinstance(is_lunar, str):
            is_lunar = is_lunar.lower() in ('true', '1', 'yes', 'on', 'checked')
        is_lunar = bool(is_lunar)
        
        # 입력 검증
        name_valid, name_error = validate_name(name)
        if not name_valid:
            raise HTTPException(status_code=400, detail=name_error)
        
        if gender == "선택해주세요":
            raise HTTPException(status_code=400, detail="성별을 선택해주세요.")
        
        # 날짜 파싱 - calculate_pillars는 datetime.date를 기대하므로 .date()로 변환
        birth_dt = datetime.strptime(birth_date, "%Y-%m-%d").date()
        
        # 시간 파싱 - None이거나 빈 문자열이면 기본값(정오 12시) 사용
        from datetime import time as dt_time
        birth_tm = dt_time(12, 0)  # 기본값: 정오 12시
        
        # birth_time이 None이 아니고 빈 문자열이 아닌 경우만 파싱 시도
        if birth_time and str(birth_time).strip():
            birth_time_stripped = str(birth_time).strip()
            try:
                # HH:MM 형식 시도
                birth_tm = datetime.strptime(birth_time_stripped, "%H:%M").time()
            except ValueError:
                try:
                    # HH:MM:SS 형식 시도
                    birth_tm = datetime.strptime(birth_time_stripped, "%H:%M:%S").time()
                except ValueError:
                    # 형식이 맞지 않으면 기본값(정오) 유지
                    birth_tm = dt_time(12, 0)
        
        # 최종 확인: birth_tm이 time 객체인지 확인
        if not isinstance(birth_tm, dt_time):
            birth_tm = dt_time(12, 0)
        
        # 사주 계산 (기존 로직 그대로 사용)
        result = saju_logic.calculate_pillars(birth_dt, birth_tm, is_lunar)
        
        # birth_datetime이 없으면 생성 (birth_dt와 birth_tm으로부터)
        # calculate_pillars는 datetime.date를 받지만, birth_datetime은 datetime.datetime이어야 함
        from datetime import datetime as dt
        birth_datetime = result[1].get('birth_datetime')
        
        # birth_datetime이 None이거나 datetime 객체가 아니면 생성
        if birth_datetime is None or not isinstance(birth_datetime, dt):
            birth_datetime = dt.combine(birth_dt, birth_tm)
            result[1]['birth_datetime'] = birth_datetime
        
        # 세션에 저장하기 전에 datetime 객체를 문자열로 변환
        # Starlette SessionMiddleware는 JSON 직렬화를 사용하므로 datetime 객체를 직접 저장할 수 없음
        pillars_info_for_session = result[1].copy()
        if 'birth_datetime' in pillars_info_for_session:
            pillars_info_for_session['birth_datetime'] = pillars_info_for_session['birth_datetime'].isoformat()
        
        # 세션에 저장 (st.session_state 대체)
        # 큰 데이터는 세션에 저장하지 않고 응답에 포함시켜 클라이언트에서 관리
        # Heroku 쿠키 크기 제한(4KB)을 피하기 위해 최소한의 정보만 세션에 저장
        request.session['user_name'] = str(name) if name else ""
        request.session['user_gender'] = str(gender) if gender else ""
        request.session['birth_date'] = str(birth_date) if birth_date else ""  # YYYY-MM-DD 형식으로 저장
        request.session['birth_time'] = str(birth_time) if birth_time else ""  # HH:MM 형식으로 저장
        request.session['is_lunar'] = bool(is_lunar)  # boolean으로 명시적 변환
        request.session['processed'] = True
        
        # AI 분석을 위한 데이터 준비
        from datetime import datetime as dt
        today = dt.now()
        korean_age = today.year - birth_dt.year + 1
        current_age = today.year - birth_dt.year - ((today.month, today.day) < (birth_dt.month, birth_dt.day))
        
        # 대운 계산 (원본 result[1]의 birth_datetime 사용)
        # birth_datetime이 None이면 생성
        birth_datetime_for_daeun = result[1].get('birth_datetime')
        if birth_datetime_for_daeun is None:
            birth_datetime_for_daeun = dt.combine(birth_dt, birth_tm)
        daeun = saju_logic.calculate_daeun(result[1], gender, birth_datetime_for_daeun)
        
        # daeun 데이터는 세션에 저장하지 않고 응답에 포함 (쿠키 크기 제한 회피)
        
        # 현재 대운 기간 찾기
        current_daeun_period = None
        for period in daeun['periods']:
            age_start = float(period['age_start'])
            if age_start <= current_age < age_start + 10:
                current_daeun_period = period
                break
        
        # 현재 연도 간지 계산
        current_year = today.year
        current_year_stem, current_year_branch = saju_logic.get_year_ganji(current_year)
        current_year_stem_char = current_year_stem.split()[0] if isinstance(current_year_stem, str) and "(" in current_year_stem else current_year_stem
        current_year_branch_char = current_year_branch.split()[0] if isinstance(current_year_branch, str) and "(" in current_year_branch else current_year_branch
        current_year_ganji = (current_year_stem_char, current_year_branch_char)
        
        # 십이운성, 신살 계산
        day_stem = result[1].get('day_stem', '')
        day_stem_full = next((s for s in saju_logic.HEAVENLY_STEMS if s.split()[0] == day_stem.split()[0]), day_stem)
        hidden_lists = [p.get("Hidden Stems (지장간)", []) for p in result[0]]
        fortunes = saju_logic.calculate_twelve_fortunes(result[0], day_stem_full)
        day_branch = result[1].get('day_branch', '')
        year_branch = result[0][0]["Earthly Branch (지지)"]
        sinsals = saju_logic.calculate_sinsal(result[0], day_stem_full, year_branch, day_branch)
        
        # AI 입력 데이터 준비
        ai_input_data = saju_logic.prepare_ai_input(
            result[0],
            result[1],
            daeun,
            fortunes,
            sinsals,
            gender,
            korean_age,
            current_year,
            current_daeun_period,
            current_year_ganji
        )
        
        # 큰 데이터는 세션에 저장하지 않고 응답에 포함 (쿠키 크기 제한 회피)
        # request.session['ai_input_data'] = ai_input_data
        # request.session['fortunes'] = fortunes
        # request.session['sinsals'] = sinsals
        request.session['current_year'] = current_year  # 작은 값만 저장
        
        # JSON 직렬화를 위해 datetime 객체를 문자열로 변환
        pillars_info_serializable = result[1].copy()
        if 'birth_datetime' in pillars_info_serializable:
            pillars_info_serializable['birth_datetime'] = pillars_info_serializable['birth_datetime'].isoformat()
        
        # daeun도 직렬화 가능한 형태로 변환
        daeun_serializable = daeun.copy()
        if 'periods' in daeun_serializable:
            daeun_serializable['periods'] = [
                {k: (v.isoformat() if isinstance(v, datetime) else v) 
                 for k, v in period.items()} 
                for period in daeun['periods']
            ]
        
        # ai_input_data도 직렬화 가능한 형태로 변환 (datetime 객체가 있을 수 있음)
        import json
        def serialize_for_json(obj):
            """재귀적으로 객체를 JSON 직렬화 가능한 형태로 변환"""
            if isinstance(obj, datetime):
                return obj.isoformat()
            elif isinstance(obj, dict):
                return {k: serialize_for_json(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [serialize_for_json(item) for item in obj]
            elif isinstance(obj, (int, float, str, bool, type(None))):
                return obj
            else:
                return str(obj)  # 기타 타입은 문자열로 변환
        
        ai_input_data_serializable = serialize_for_json(ai_input_data) if ai_input_data else None
        
        return JSONResponse({
            "success": True,
            "data": {
                "pillars_data": result[0],
                "pillars_info": pillars_info_serializable,
                "daeun": daeun_serializable,
                "fortunes": fortunes,
                "sinsals": sinsals,
                "ai_input_data": ai_input_data_serializable,  # AI 분석을 위한 데이터도 포함
                # 세션에 저장된 값도 함께 반환하여 다른 페이지에서 사용할 수 있도록 함
                "session_data": {
                    "user_name": str(name) if name else "",
                    "user_gender": str(gender) if gender else "",
                    "birth_date": str(birth_date) if birth_date else "",
                    "birth_time": str(birth_time) if birth_time else "",
                    "is_lunar": bool(is_lunar)
                }
            }
        })
    except ValueError as e:
        error_msg = safe_error_message(e, show_details=not is_production())
        raise HTTPException(status_code=400, detail=error_msg)
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        error_msg = str(e)
        # 개발 환경에서는 전체 트레이스백 포함
        if not is_production():
            error_msg = f"{error_msg}\n\nTraceback:\n{error_trace}"
        else:
            error_msg = safe_error_message(e, show_details=False)
        raise HTTPException(status_code=500, detail=f"오류가 발생했습니다: {error_msg}")


@router.post("/save-api-key")
async def save_api_key(request: Request):
    """API Key를 세션에 저장 (빈 문자열이면 제거)"""
    try:
        data = await request.json()
        api_key = data.get('api_key', '').strip()
        
        # 빈 문자열이면 세션에서 제거
        if not api_key:
            if 'user_api_key' in request.session:
                del request.session['user_api_key']
            return JSONResponse({"success": True, "message": "API Key가 제거되었습니다."})
        
        # API Key 검증
        api_key_valid, api_key_error = validate_api_key(api_key)
        if not api_key_valid:
            raise HTTPException(status_code=400, detail=api_key_error)
        
        # 세션에 저장
        request.session['user_api_key'] = api_key
        
        return JSONResponse({"success": True, "message": "API Key가 저장되었습니다."})
    except HTTPException:
        raise
    except Exception as e:
        error_msg = safe_error_message(e, show_details=not is_production())
        raise HTTPException(status_code=500, detail=error_msg)

@router.post("/ai-analysis")
async def ai_analysis(request: Request):
    """AI 사주 분석 API"""
    # 요청 본문에서 계산된 데이터와 API Key를 받기 (세션에 큰 데이터를 저장하지 않으므로 필수)
    try:
        body = await request.json()
        calculated_data = body.get('calculated_data')
        API_KEY = body.get('api_key', '').strip()  # API Key는 요청 본문에서 받음 (저장하지 않고 입력 시에만 사용)
        
        if not calculated_data:
            raise HTTPException(status_code=400, detail="사주 데이터가 없습니다. 먼저 사주를 계산해주세요.")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"AI 분석 요청 데이터 읽기 오류: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail="요청 데이터를 읽을 수 없습니다. 먼저 사주를 계산해주세요.")
    
    # 요청 본문에서 데이터 추출
    pillars_data = calculated_data.get('pillars_data', [])
    pillars_info = calculated_data.get('pillars_info', {})
    daeun = calculated_data.get('daeun', {})
    fortunes = calculated_data.get('fortunes', [])
    sinsals = calculated_data.get('sinsals', [])
    ai_input_data = calculated_data.get('ai_input_data')
    
    # 데이터 검증
    if not pillars_data:
        raise HTTPException(status_code=400, detail="사주 데이터가 없습니다. 먼저 사주를 계산해주세요.")
    
    logger.info(f"AI 분석 요청 - API Key 존재 여부: {bool(API_KEY)}, ai_input_data 존재 여부: {bool(ai_input_data)}")
    
    # API Key가 없으면 기본 분석 데이터만 반환 (안내 문구 없이)
    # 기본 사주 분석 결과는 이미 renderResults에서 풍부하게 표시되므로, 여기서는 AI 분석만 처리
    if not API_KEY:
        # 기본 분석 데이터 반환 (안내 문구 제거)
        return JSONResponse({
            "success": True,
            "data": {
                "is_ai_analysis": False,
                "pillars_data": pillars_data,
                "pillars_info": pillars_info,
                "daeun": daeun,
                "fortunes": fortunes,
                "sinsals": sinsals
            }
        })
    
    # AI 분석 - 스트리밍 방식으로 변경 (Heroku H12 타임아웃 방지)
    if not ai_input_data:
        logger.warning("AI 분석 요청 - ai_input_data가 없습니다.")
        raise HTTPException(status_code=400, detail="AI 분석을 위한 데이터가 준비되지 않았습니다.")
    
    # 스트리밍 응답 생성
    async def generate_stream():
        try:
            logger.info("OpenAI API 스트리밍 시작...")
            # SSE 헤더 전송
            yield "data: " + json.dumps({"type": "start"}, ensure_ascii=False) + "\n\n"
            
            # 스트리밍 생성기 호출
            for chunk in ai_analyst.generate_saju_analysis_stream(API_KEY, ai_input_data):
                yield chunk
            
            logger.info("OpenAI API 스트리밍 완료")
        except Exception as e:
            logger.error(f"AI 분석 스트리밍 중 오류 발생: {e}", exc_info=True)
            error_msg = safe_error_message(e, show_details=False)
            yield f"data: {json.dumps({'type': 'error', 'error': error_msg}, ensure_ascii=False)}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Nginx 버퍼링 비활성화
        }
    )


@router.post("/tojeong")
async def calculate_tojeong(request: Request):
    """토정비결 계산 API"""
    # 요청 본문에서 계산된 데이터를 받기 (세션에 큰 데이터를 저장하지 않으므로 필수)
    try:
        body = await request.json()
        calculated_data = body.get('calculated_data')
        if not calculated_data:
            raise HTTPException(status_code=400, detail="사주 데이터가 없습니다. 먼저 사주를 계산해주세요.")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail="요청 데이터를 읽을 수 없습니다. 먼저 사주를 계산해주세요.")
    
    # 요청 본문에서 데이터 추출
    pillars_data = calculated_data.get('pillars_data', [])
    pillars_info = calculated_data.get('pillars_info', {})
    
    # 데이터 검증
    if not pillars_data or not pillars_info:
        raise HTTPException(status_code=400, detail="사주 데이터가 없습니다. 먼저 사주를 계산해주세요.")
    
    current_year = datetime.now().year
    
    try:
        # pillars_info의 birth_datetime이 문자열이면 datetime 객체로 변환
        if pillars_info and 'birth_datetime' in pillars_info:
            if isinstance(pillars_info['birth_datetime'], str):
                from datetime import datetime as dt
                pillars_info['birth_datetime'] = dt.fromisoformat(pillars_info['birth_datetime'])
        
        # 토정비결 계산
        tojeong_result = saju_logic.calculate_tojeong_bigyeol(pillars_info, current_year, pillars_data)
        
        # 세션에 저장하지 않음 (쿠키 크기 제한 회피)
        # request.session['tojeong_result'] = tojeong_result
        
        # 사주 계산 데이터도 세션에 저장하지 않음 (쿠키 크기 제한 회피)
        # JSON 직렬화를 위해 datetime 객체를 문자열로 변환 (응답에만 사용)
        pillars_info_serializable = pillars_info.copy()
        if 'birth_datetime' in pillars_info_serializable and pillars_info_serializable['birth_datetime']:
            if isinstance(pillars_info_serializable['birth_datetime'], datetime):
                pillars_info_serializable['birth_datetime'] = pillars_info_serializable['birth_datetime'].isoformat()
            elif not isinstance(pillars_info_serializable['birth_datetime'], str):
                pillars_info_serializable['birth_datetime'] = str(pillars_info_serializable['birth_datetime'])
        
        # request.session['tojeong_pillars_data'] = pillars_data  # 쿠키 크기 제한으로 제거
        # request.session['tojeong_pillars_info'] = pillars_info_serializable  # 쿠키 크기 제한으로 제거
        
        return JSONResponse(
            content={
                "success": True,
                "data": {
                    "tojeong_result": tojeong_result,
                    "current_year": current_year
                }
            },
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
    except Exception as e:
        error_msg = safe_error_message(e, show_details=not is_production())
        logger.error(f"Unhandled exception in calculate_tojeong: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"토정비결 계산 중 오류가 발생했습니다: {error_msg}")


@router.post("/byeoljari")
async def calculate_byeoljari(request: Request):
    """별자리운세 계산 API"""
    from datetime import datetime
    from utils.constellation import (
        get_constellation, get_constellation_info, get_daily_fortune,
        get_weekly_fortune, get_monthly_fortune, get_yearly_fortune,
        get_lucky_elements, get_compatibility, get_constellation_advice,
        get_life_aspects_fortune, get_career_hobby, get_love_style,
        get_health_info, get_monthly_detailed_fortune
    )
    
    # 요청 본문에서 생년월일과 이름 가져오기 (없으면 세션에서)
    try:
        body = await request.json()
        birth_date_str = body.get('birth_date', '')
        user_name = body.get('user_name', '')
    except Exception:
        birth_date_str = ''
        user_name = ''
    
    # 요청 본문에 없으면 세션에서 가져오기
    if not birth_date_str:
        birth_date_str = request.session.get('birth_date', '')
    if not user_name:
        user_name = request.session.get('user_name', '')
    
    if not birth_date_str:
        raise HTTPException(status_code=400, detail="생년월일이 없습니다. 먼저 사주를 계산해주세요.")
    
    try:
        birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="생년월일 형식이 올바르지 않습니다.")
    current_date = datetime.now()
    current_year = current_date.year
    
    # 별자리 계산
    korean_name, emoji, english_name = get_constellation(birth_date)
    
    # 별자리 정보 수집
    constellation_info = get_constellation_info(korean_name)
    today_fortune = get_daily_fortune(korean_name, current_date)
    weekly_fortune = get_weekly_fortune(korean_name, current_date)
    monthly_fortune = get_monthly_fortune(korean_name, current_date)
    yearly_fortune = get_yearly_fortune(korean_name, current_year)
    lucky_elements = get_lucky_elements(korean_name)
    compatibility = get_compatibility(korean_name)
    advice = get_constellation_advice(korean_name)
    life_aspects = get_life_aspects_fortune(korean_name, current_date)
    career_hobby = get_career_hobby(korean_name)
    love_style = get_love_style(korean_name)
    health_info = get_health_info(korean_name)
    monthly_detailed = get_monthly_detailed_fortune(korean_name, current_year)
    
    result = {
        "korean_name": korean_name,
        "emoji": emoji,
        "english_name": english_name,
        "birth_date": birth_date_str,
        "birth_date_formatted": birth_date.strftime('%Y년 %m월 %d일'),
        "user_name": user_name,
        "constellation_info": constellation_info,
        "today_fortune": today_fortune,
        "weekly_fortune": weekly_fortune,
        "monthly_fortune": monthly_fortune,
        "yearly_fortune": yearly_fortune,
        "lucky_elements": lucky_elements,
        "compatibility": compatibility,
        "advice": advice,
        "life_aspects": life_aspects,
        "career_hobby": career_hobby,
        "love_style": love_style,
        "health_info": health_info,
        "monthly_detailed": monthly_detailed,
        "current_date": current_date.strftime('%Y년 %m월 %d일'),
        "current_year": current_year
    }
    
    # 세션에 저장하지 않음 (쿠키 크기 제한 회피)
    # request.session['byeoljari_result'] = result
    
    return JSONResponse({
        "success": True,
        "data": result
    })


@router.post("/dream")
async def calculate_dream(request: Request):
    """꿈해몽 계산 API"""
    from utils.dream import get_dream_meaning, DREAM_CATEGORIES
    from utils.api_key_fastapi import get_api_key
    
    try:
        body = await request.json()
        keyword = body.get('keyword', '').strip()
    except Exception:
        keyword = ''
    
    if not keyword:
        raise HTTPException(status_code=400, detail="검색할 키워드를 입력해주세요.")
    
    # API Key는 요청 본문에서 받음 (저장하지 않고 입력 시에만 사용)
    api_key = body.get('api_key', '').strip()
    
    # 꿈해몽 정보 가져오기
    dream_meaning = get_dream_meaning(keyword, api_key)
    
    # 카테고리 정보 추가
    category = None
    for cat_name, cat_data in DREAM_CATEGORIES.items():
        if keyword in cat_data["키워드"]:
            category = cat_name
            break
    
    result = {
        "keyword": keyword,
        "category": category,
        "dream_meaning": dream_meaning
    }
    
    # 세션에 저장하지 않음 (쿠키 크기 제한 회피)
    # request.session['dream_result'] = result
    
    return JSONResponse({
        "success": True,
        "data": result
    })


@router.post("/tarot")
async def draw_tarot(request: Request):
    """타로 카드 뽑기 API"""
    from utils.tarot import (
        draw_tarot_cards, generate_comprehensive_analysis,
        SPREAD_TYPES, TAROT_CARDS
    )
    
    try:
        body = await request.json()
        spread_type = body.get('spread_type', '1장')
        question = body.get('question', '').strip()
        API_KEY = body.get('api_key', '').strip()  # API Key는 요청 본문에서 받음 (저장하지 않고 입력 시에만 사용)
    except Exception:
        spread_type = '1장'
        question = ''
        API_KEY = ''
    
    # 스프레드 타입 검증
    if spread_type not in SPREAD_TYPES:
        spread_type = '1장'
    
    # 카드 뽑기
    result = draw_tarot_cards(spread_type, question)
    
    # 종합 해석 생성
    comprehensive_analysis = generate_comprehensive_analysis(result)
    result['analysis'] = comprehensive_analysis
    
    # API Key가 있으면 각 카드에 대한 이미지 생성 시도 (타임아웃 방지를 위해 제한적으로)
    # 1장일 때만 AI 이미지 생성 (3장, 5장은 타임아웃 위험으로 제외)
    if API_KEY and spread_type == '1장':
        logger.info("타로 카드 이미지 생성 시작...")
        for card in result.get('cards', []):
            # 기본 이미지가 없거나 API Key로 생성된 이미지를 원하는 경우에만 생성
            # 기본 이미지가 있으면 우선 사용하고, API Key로 생성한 이미지는 추가 옵션으로 제공
            try:
                image_url = ai_analyst.generate_tarot_card_image(
                    API_KEY,
                    card.get('카드명', ''),
                    card.get('역위치', False)
                )
                if image_url:
                    # AI 생성 이미지는 ai_image_url로 저장 (기본 이미지와 구분)
                    card['ai_image_url'] = image_url
                    logger.info(f"타로 카드 AI 이미지 생성 성공: {card.get('카드명', '')}")
            except Exception as e:
                logger.error(f"타로 카드 이미지 생성 오류 ({card.get('카드명', '')}): {e}", exc_info=True)
                # 이미지 생성 실패해도 계속 진행
                continue
        logger.info("타로 카드 이미지 생성 완료")
    elif API_KEY and spread_type in ['3장', '5장']:
        logger.info(f"타로 {spread_type}은 타임아웃 방지를 위해 기본 이미지만 사용합니다.")
    
    # 세션에 저장하지 않음 (쿠키 크기 제한 회피)
    # request.session['tarot_result'] = result
    
    return JSONResponse({
        "success": True,
        "data": result
    })


@router.post("/lotto")
async def generate_lotto(request: Request):
    """로또 번호 생성 API"""
    from utils.lotto import generate_lotto_numbers, calculate_statistics
    from datetime import datetime, date
    
    try:
        body = await request.json()
        method = body.get('method', '완전 랜덤')
        num_sets = body.get('num_sets', 3)
    except Exception:
        method = '완전 랜덤'
        num_sets = 3
    
    # 사용자 정보 확인
    birth_date_str = request.session.get('birth_date', '')
    birth_date = None
    if birth_date_str:
        try:
            birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
        except ValueError:
            pass
    
    pillars_info = request.session.get('pillars_info')
    
    # 사용자 정보가 필요한 방식이 선택되었지만 정보가 없는 경우 완전 랜덤으로 변경
    user_info_required_methods = ["생년월일 기반", "사주 기반", "행운 숫자 조합", "생일 합산 기반", "사주 오행 기반"]
    actual_method = method
    if method in user_info_required_methods:
        if method in ["생년월일 기반", "행운 숫자 조합", "생일 합산 기반"] and not birth_date:
            actual_method = "완전 랜덤"
        elif method in ["사주 기반", "사주 오행 기반"] and not pillars_info:
            actual_method = "완전 랜덤"
    
    # 번호 생성 (실제로 사용된 방법으로 생성)
    results = []
    for i in range(num_sets):
        numbers = generate_lotto_numbers(actual_method, birth_date, pillars_info, i)
        results.append(numbers)
    
    # 통계 계산
    statistics = calculate_statistics(results)
    
    # 사용자가 선택한 원본 method를 반환 (실제로 사용된 method와 다를 수 있음)
    result = {
        'method': method,  # 사용자가 선택한 원본 method 표시
        'sets': results,
        'generated_at': datetime.now().isoformat(),
        'statistics': statistics
    }
    
    # 세션에 저장하지 않음 (쿠키 크기 제한 회피)
    # request.session['lotto_result'] = result
    
    return JSONResponse({
        "success": True,
        "data": result
    })


@router.post("/manse")
async def get_manse_calendar(request: Request):
    """만세력 달력 데이터 API"""
    from utils.manse import generate_calendar_data
    from datetime import datetime
    
    try:
        body = await request.json()
        year = body.get('year', datetime.now().year)
        month = body.get('month', datetime.now().month)
        show_lunar = body.get('show_lunar', True)
        show_ganji = body.get('show_ganji', True)
    except Exception:
        now = datetime.now()
        year = now.year
        month = now.month
        show_lunar = True
        show_ganji = True
    
    # 년월 유효성 검증
    if year < 1900 or year > 2100:
        year = datetime.now().year
    if month < 1 or month > 12:
        month = datetime.now().month
    
    # 달력 데이터 생성
    calendar_data = generate_calendar_data(year, month, show_lunar, show_ganji)
    
    return JSONResponse({
        "success": True,
        "data": calendar_data
    })


@router.post("/gonghap")
async def calculate_gonghap(request: Request):
    """궁합 계산 API"""
    from utils.gonghap import calculate_gonghap as calc_gonghap
    import json
    
    try:
        body = await request.json()
        person1_pillars_data = body.get('person1_pillars_data')
        person1_pillars_info = body.get('person1_pillars_info')
        person1_gender = body.get('person1_gender')
        person2_pillars_data = body.get('person2_pillars_data')
        person2_pillars_info = body.get('person2_pillars_info')
        person2_gender = body.get('person2_gender')
        
        if not all([person1_pillars_data, person1_pillars_info, person1_gender,
                   person2_pillars_data, person2_pillars_info, person2_gender]):
            raise HTTPException(status_code=400, detail="필수 정보가 누락되었습니다.")
        
        # 궁합 계산
        gonghap_result = calc_gonghap(
            person1_pillars_data,
            person1_pillars_info,
            person1_gender,
            person2_pillars_data,
            person2_pillars_info,
            person2_gender
        )
        
        # AI 분석은 별도 엔드포인트(/api/gonghap-ai-analysis)에서 처리
        # 기본 궁합 계산 결과만 반환 (AI 분석은 클라이언트에서 별도로 요청)
        ai_analysis_result = None
        
        # 세션에 저장하지 않음 (쿠키 크기 제한 회피)
        # request.session['gonghap_result'] = gonghap_result
        # if ai_analysis_result and 'error' not in ai_analysis_result:
        #     request.session['gonghap_ai_analysis'] = ai_analysis_result
        
        return JSONResponse({
            "success": True,
            "data": {
                **gonghap_result,
                "is_ai_analysis": ai_analysis_result is not None and 'error' not in ai_analysis_result,
                "ai_analysis": ai_analysis_result if ai_analysis_result and 'error' not in ai_analysis_result else None
            }
        })
        
    except Exception as e:
        logger.error(f"궁합 계산 오류: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"궁합 계산 중 오류가 발생했습니다: {str(e)}")


@router.post("/gonghap-ai-analysis")
async def gonghap_ai_analysis(request: Request):
    """궁합 AI 분석 API - 스트리밍 방식"""
    try:
        body = await request.json()
        gonghap_data = body.get('gonghap_data')
        person1_pillars_data = body.get('person1_pillars_data', [])
        person1_pillars_info = body.get('person1_pillars_info', {})
        person2_pillars_data = body.get('person2_pillars_data', [])
        person2_pillars_info = body.get('person2_pillars_info', {})
        
        if not gonghap_data:
            raise HTTPException(status_code=400, detail="궁합 데이터가 없습니다. 먼저 궁합을 계산해주세요.")
        
        # API Key는 요청 본문에서 받음 (저장하지 않고 입력 시에만 사용)
        API_KEY = body.get('api_key', '').strip()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"궁합 AI 분석 요청 데이터 읽기 오류: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail="요청 데이터를 읽을 수 없습니다.")
    
    if not API_KEY:
        return JSONResponse({
            "success": True,
            "data": {
                "is_ai_analysis": False,
                "message": "기본 궁합 결과입니다. 더 상세한 AI 분석을 받으시려면 OpenAI API Key를 입력해주세요."
            }
        })
    
    # AI 분석 - 스트리밍 방식으로 변경 (Heroku H12 타임아웃 방지)
    # 스트리밍 응답 생성
    async def generate_stream():
        try:
            logger.info("궁합 OpenAI API 스트리밍 시작...")
            # SSE 헤더 전송
            yield "data: " + json.dumps({"type": "start"}, ensure_ascii=False) + "\n\n"
            
            # 스트리밍 생성기 호출
            for chunk in ai_analyst.generate_gonghap_analysis_stream(
                API_KEY, 
                gonghap_data,
                person1_pillars_data=person1_pillars_data,
                person1_pillars_info=person1_pillars_info,
                person2_pillars_data=person2_pillars_data,
                person2_pillars_info=person2_pillars_info
            ):
                yield chunk
            
            logger.info("궁합 OpenAI API 스트리밍 완료")
        except Exception as e:
            logger.error(f"궁합 AI 분석 스트리밍 중 오류 발생: {e}", exc_info=True)
            error_msg = safe_error_message(e, show_details=not is_production())
            yield f"data: {json.dumps({'type': 'error', 'error': error_msg}, ensure_ascii=False)}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Nginx 버퍼링 비활성화
        }
    )


@router.post("/tojeong-ai-analysis")
async def tojeong_ai_analysis(request: Request):
    """토정비결 AI 분석 API"""
    # 요청 본문에서 데이터와 API Key를 받기 (세션에 큰 데이터를 저장하지 않으므로)
    try:
        body = await request.json()
        tojeong_result = body.get('tojeong_result')
        pillars_data = body.get('pillars_data', [])
        pillars_info = body.get('pillars_info', {})
        API_KEY = body.get('api_key', '').strip()  # API Key는 요청 본문에서 받음 (저장하지 않고 입력 시에만 사용)
        
        if not tojeong_result:
            raise HTTPException(status_code=400, detail="토정비결 데이터가 없습니다. 먼저 토정비결을 계산해주세요.")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"토정비결 AI 분석 요청 데이터 읽기 오류: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail="요청 데이터를 읽을 수 없습니다.")
    
    if not API_KEY:
        return JSONResponse({
            "success": True,
            "data": {
                "is_ai_analysis": False,
                "message": "기본 토정비결 결과입니다. 더 상세한 AI 분석을 받으시려면 OpenAI API Key를 입력해주세요."
            }
        })
    
    # AI 분석 - 스트리밍 방식으로 변경 (Heroku H12 타임아웃 방지)
    # 스트리밍 응답 생성
    async def generate_stream():
        try:
            logger.info("토정비결 OpenAI API 스트리밍 시작...")
            # SSE 헤더 전송
            yield "data: " + json.dumps({"type": "start"}, ensure_ascii=False) + "\n\n"
            
            # 스트리밍 생성기 호출
            for chunk in ai_analyst.generate_tojeong_analysis_stream(
                API_KEY, 
                tojeong_result,
                pillars_data=pillars_data,
                pillars_info=pillars_info
            ):
                yield chunk
            
            logger.info("토정비결 OpenAI API 스트리밍 완료")
        except Exception as e:
            logger.error(f"토정비결 AI 분석 스트리밍 중 오류 발생: {e}", exc_info=True)
            error_msg = safe_error_message(e, show_details=not is_production())
            yield f"data: {json.dumps({'type': 'error', 'error': error_msg}, ensure_ascii=False)}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Nginx 버퍼링 비활성화
        }
    )


@router.post("/byeoljari-ai-analysis")
async def byeoljari_ai_analysis(request: Request):
    """별자리 운세 AI 분석 API - 스트리밍 방식"""
    try:
        body = await request.json()
        byeoljari_data = body.get('byeoljari_data')
        
        if not byeoljari_data:
            raise HTTPException(status_code=400, detail="별자리 데이터가 없습니다. 먼저 별자리 운세를 확인해주세요.")
        
        # API Key는 요청 본문에서 받음
        API_KEY = body.get('api_key', '').strip()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"별자리 AI 분석 요청 데이터 읽기 오류: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail="요청 데이터를 읽을 수 없습니다.")
    
    if not API_KEY:
        return JSONResponse({
            "success": True,
            "data": {
                "is_ai_analysis": False,
                "message": "기본 별자리 운세 결과입니다. 더 상세한 AI 분석을 받으시려면 OpenAI API Key를 입력해주세요."
            }
        })
    
    # AI 분석 - 스트리밍 방식
    async def generate_stream():
        try:
            logger.info("별자리 OpenAI API 스트리밍 시작...")
            yield "data: " + json.dumps({"type": "start"}, ensure_ascii=False) + "\n\n"
            
            for chunk in ai_analyst.generate_byeoljari_analysis_stream(API_KEY, byeoljari_data):
                yield chunk
            
            logger.info("별자리 OpenAI API 스트리밍 완료")
        except Exception as e:
            logger.error(f"별자리 AI 분석 스트리밍 중 오류 발생: {e}", exc_info=True)
            error_msg = safe_error_message(e, show_details=not is_production())
            yield f"data: {json.dumps({'type': 'error', 'error': error_msg}, ensure_ascii=False)}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

