# -*- coding: utf-8 -*-
import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from datetime import datetime, date, time
import saju_logic

# 테스트 1: birth_time이 None인 경우
print("=" * 50)
print("테스트: calculate_pillars 직접 호출")
print("=" * 50)

birth_dt = date(2000, 1, 1)
birth_tm = None

print(f"birth_dt: {birth_dt}")
print(f"birth_tm: {birth_tm}")
print(f"birth_tm type: {type(birth_tm)}")

try:
    result = saju_logic.calculate_pillars(birth_dt, birth_tm, False)
    print("성공!")
    print(f"Result type: {type(result)}")
    print(f"Result length: {len(result)}")
    if len(result) > 1:
        print(f"Result[1] keys: {result[1].keys() if isinstance(result[1], dict) else 'Not a dict'}")
        if 'birth_datetime' in result[1]:
            print(f"birth_datetime: {result[1]['birth_datetime']}")
            print(f"birth_datetime type: {type(result[1]['birth_datetime'])}")
except Exception as e:
    print(f"오류 발생: {e}")
    import traceback
    traceback.print_exc()

