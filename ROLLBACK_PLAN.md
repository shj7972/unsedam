# 운세담 롤백 계획 (2026-09-01 띠궁합 배포 기준)

## 현재 배포 정보
- 커밋: f6a4c29 (feat: 띠×띠 궁합 페이지 67개 신규 추가)
- 이전 안정 커밋: b4cc18e (광고 단위 ID 실제값으로 교체)
- 배포 경로: GitHub push → Vercel 자동 배포 (unsedam.kr)

## 롤백 절차

### 방법 1: git revert (권장 — 이력 보존)
```bash
cd ~/.openclaw/workspace/unsedam
git revert f6a4c29
git push origin main
```
- Vercel이 자동으로 이전 상태로 재배포 (3~5분 소요)
- 장점: 새 커밋이 되어 이력 추적 가능

### 방법 2: 강제 되돌리기 (긴급 시)
```bash
cd ~/.openclaw/workspace/unsedam
git reset --hard b4cc18e
git push --force origin main
```
- 장점: 확실한 이전 복원
- 단점: 이력 날아감 (긴급 상황에서만)

### 방법 3: Vercel 대시보드 (수동)
- vercel.com → 운세담 프로젝트 → Deployments 탭
- b4cc18e 시점 배포 → "Instant Rollback" 클릭

## 롤백 판단 기준 (즉시 롤백 신호)
1. /compat 또는 /compat/{pair} 페이지 500 오류 다발
2. 기존 페이지(/, /zodiac, /fortune) 오류 발생
3. AdSense 광고 로드 실패 (수익 직결)
4. 서버 응답 시간 5초 이상 지속 (66쌍 렌더링 부하)

## 배포 검증 명령 (배포 후 항상 실행)
```bash
curl -s -o /dev/null -w "%{http_code}" https://unsedam.kr/compat           # 200 기대
curl -s -o /dev/null -w "%{http_code}" https://unsedam.kr/compat/rat-vs-ox # 200 기대
curl -s https://unsedam.kr/sitemap.xml | grep -c "/compat/"                # 67 기대 (허브1+쌍66)
curl -s -o /dev/null -w "%{http_code}" https://unsedam.kr/                 # 200 기대
```

## 로컬 테스트 환경 (롤백 전 검증용)
- 테스트 venv: ~/.openclaw/workspace/unsedam/.venv-local
- 사용법:
```bash
cd ~/.openclaw/workspace/unsedam
./.venv-local/bin/python -c "
from main import app
from fastapi.testclient import TestClient
c = TestClient(app)
print(c.get('/compat').status_code)
"
```
- 의존성: fastapi, jinja2, itsdangerous, uvicorn, ephem, httpx, python-multipart, korean-lunar-calendar, openai

## 내부링크 개선 (06e0d8d9 → 실제 6e0d8d9, 9/1 2차 배포)
- 헤더 nav에 "띠 궁합 66쌍" 메뉴 추가 (PAGE_NAMES — 모든 페이지 자동 반영)
- 하단 연관 운세 섹션 + 푸터에 compat/zodiac 링크 추가
- zodiac 상세 12개 페이지: 잘 맞는 띠·주의할 띠 카드 → compat 상세 링크로 전환
- 롤백 시: git revert 6e0d8d9 f6a4c29 (2개 커밋 함께)

## 신규 생성 파일 목록 (롤백 시 영향 범위)
- utils/zodiac_compat.py (신규 — 궁합 계산 로직)
- templates/compat.html (신규 — 허브)
- templates/compat_detail.html (신규 — 상세 66쌍)
- routers/pages.py (/compat 라우트 2개 추가)
- utils/seo_fastapi.py (sitemap에 compat 67 URLs 추가)

## 메모
- 9/2 이후 작업 시 이 커밋 해시(f6a4c29) 위에 쌓임. 롤백 시 최신 커밋 목록 확인 필수: git log --oneline -10
- 애드센스 슬롯 ID 2173340919 재사용 (기존 광고 단위) — 신규 생성 불필요