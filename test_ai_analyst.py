
import ai_analyst
import json

# Dummy Saju Data based on the structure in ai_analyst.py
dummy_data = {
  "pillar": {
    "year": { "heavenlyStem": "甲", "earthlyBranch": "子" },
    "month": { "heavenlyStem": "乙", "earthlyBranch": "丑" },
    "day": { "heavenlyStem": "丙", "earthlyBranch": "寅" },
    "hour": { "heavenlyStem": "丁", "earthlyBranch": "卯" }
  },
  "dayMaster": "丙",
  "elements": {
    "wood": 3,
    "fire": 2,
    "earth": 1,
    "metal": 1,
    "water": 1
  },
  "yinYang": {
    "yang": 5,
    "yin": 3
  },
  "sipseong": {
    "bijeon": ["甲"],
    "겁재": [],
    "식신": ["戊"],
    "상관": ["己"],
    "편재": ["庚", "申"],
    "정재": ["辛", "酉"],
    "편관": ["壬", "亥"],
    "정관": ["癸", "子"],
    "편인": ["甲", "寅"],
    "정인": ["乙", "卯"]
  },
  "sinsal": ["천을귀인", "문창귀인", "역마"],
  "sibiunseong": {
    "year": "병",
    "month": "사",
    "day": "제왕",
    "hour": "건록"
  },
  "daeun": [
    {
      "age": "8-17",
      "heavenlyStem": "甲",
      "earthlyBranch": "寅",
      "period": "8년"
    }
  ],
  "currentAge": 35,
  "gender": "남성"
}

# SECURITY: API 키는 환경 변수에서 가져옵니다.
# 절대 하드코딩하지 마세요!
import os
API_KEY = os.environ.get('OPENAI_API_KEY', '')

if not API_KEY:
    print("ERROR: OPENAI_API_KEY environment variable is not set.")
    print("Please set it before running the test:")
    print("  export OPENAI_API_KEY=your-api-key-here")
    exit(1)

print("Sending request to OpenAI...")
result = ai_analyst.generate_saju_analysis(API_KEY, dummy_data)
print("Result received:")
print(json.dumps(result, indent=2, ensure_ascii=False))

if "error" in result:
    print("TEST FAILED")
    exit(1)
else:
    print("TEST PASSED")
