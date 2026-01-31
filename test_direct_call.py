# -*- coding: utf-8 -*-
import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from datetime import date, time, datetime
import saju_logic

print("=" * 50)
print("직접 함수 호출 테스트")
print("=" * 50)

# 테스트 1: birth_time이 None인 경우
birth_dt = date(2000, 1, 1)
birth_tm = None

print(f"\n테스트 1: birth_tm = None")
print(f"birth_dt: {birth_dt}, type: {type(birth_dt)}")
print(f"birth_tm: {birth_tm}, type: {type(birth_tm)}")

try:
    result = saju_logic.calculate_pillars(birth_dt, birth_tm, False)
    print("✅ 성공!")
    print(f"Result[1] keys: {result[1].keys() if isinstance(result[1], dict) else 'Not a dict'}")
    if 'birth_datetime' in result[1]:
        print(f"birth_datetime: {result[1]['birth_datetime']}, type: {type(result[1]['birth_datetime'])}")
except Exception as e:
    print(f"❌ 오류: {e}")
    import traceback
    traceback.print_exc()

# 테스트 2: birth_time이 time 객체인 경우
birth_tm2 = time(14, 30)
print(f"\n테스트 2: birth_tm = time(14, 30)")
print(f"birth_dt: {birth_dt}, type: {type(birth_dt)}")
print(f"birth_tm: {birth_tm2}, type: {type(birth_tm2)}")

try:
    result2 = saju_logic.calculate_pillars(birth_dt, birth_tm2, False)
    print("✅ 성공!")
    print(f"Result[1] keys: {result2[1].keys() if isinstance(result2[1], dict) else 'Not a dict'}")
    if 'birth_datetime' in result2[1]:
        print(f"birth_datetime: {result2[1]['birth_datetime']}, type: {type(result2[1]['birth_datetime'])}")
        
    # calculate_daeun 테스트
    print(f"\ncalculate_daeun 테스트:")
    daeun = saju_logic.calculate_daeun(result2[1], "남성", result2[1]['birth_datetime'])
    print("✅ calculate_daeun 성공!")
except Exception as e:
    print(f"❌ 오류: {e}")
    import traceback
    traceback.print_exc()

