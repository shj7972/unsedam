# 신살 계산 로직 점검 보고서

## 현재 구현 분석

### 1. 함수 시그니처
```python
calculate_sinsal(pillars_data, day_stem, year_branch, day_branch)
```

### 2. 전달되는 데이터 형식
- `pillars_data`: 각 기둥의 지지는 "甲", "子" 형식 (한자만)
- `day_stem`: "甲 (갑)" 형식 (전체 형식)
- `year_branch`: "子 (자)" 형식 또는 "子" 형식
- `day_branch`: "子 (자)" 형식 또는 "子" 형식

### 3. 발견된 문제점

#### 문제 1: 일간 형식 불일치 처리
- `TIANYI_GUIREN`, `YANGREN`, `KONGWANG` 딕셔너리는 "甲 (갑)" 형식을 키로 사용
- 현재 코드는 `day_stem`이 이미 전체 형식으로 전달되므로 정상 작동해야 함
- 하지만 안전성을 위해 형식 확인 로직 추가 권장

#### 문제 2: 도화(桃花) 계산 로직 검증 필요
현재 로직:
```python
if branch_full == TAOHUA.get(year_branch_full) or branch_full == TAOHUA.get(day_branch_full):
```
- 이 로직은 각 기둥의 지지가 년지나 일지 기준 도화와 일치하는지 확인
- 명리학 이론상 도화는 "년지나 일지 기준으로 삼합의 끝에서 3위"를 찾는 것
- 현재 구현이 맞는지 검증 필요

#### 문제 3: 화개(華蓋) 계산 로직
현재 로직:
```python
if branch_full == HUAGAI.get(year_branch_full) or branch_full == HUAGAI.get(day_branch_full):
```
- 화개는 "년지나 일지를 기준으로 삼합의 중간"을 찾는 것
- 현재 구현 확인 필요

#### 문제 4: 역마(驛馬) 계산 로직
현재 로직:
```python
if branch_full == YIMA.get(year_branch_full) or branch_full == YIMA.get(day_branch_full):
```
- 역마는 "년지나 일지를 기준으로 대충(對沖)의 양쪽"을 찾는 것
- 현재 구현 확인 필요

#### 문제 5: 장성(將星) 계산 로직
현재 로직:
```python
if branch_full == JIANGXING.get(year_branch_full) or branch_full == JIANGXING.get(day_branch_full):
```
- 장성은 "년지나 일지를 기준으로 삼합의 첫 번째"를 찾는 것
- 현재 구현 확인 필요

### 4. 데이터 딕셔너리 검증

#### 천을귀인 (天乙貴人)
- 키: "甲 (갑)" 형식 ✓
- 값: ["丑 (축)", "未 (미)"] 형식 ✓
- 로직: 일간 기준으로 해당 지지 확인 ✓

#### 양인 (羊刃)
- 키: "甲 (갑)" 형식 ✓
- 값: "卯 (묘)" 형식 ✓
- 로직: 일간 기준으로 해당 지지 확인 ✓

#### 공망 (空亡)
- 키: "甲 (갑)" 형식 ✓
- 값: ["戌 (술)", "亥 (해)"] 형식 ✓
- 로직: 일간 기준으로 해당 지지 확인 ✓

### 5. 권장 수정사항

1. **형식 안전성 강화**: day_stem이 부분 형식("甲")으로 올 경우를 대비한 처리
2. **데이터 검증**: 신살 데이터 딕셔너리의 정확성 확인
3. **로직 명확화**: 주석을 통한 각 신살 계산 기준 명시

