"""
로또 번호 생성 유틸리티
"""
import random
from datetime import datetime
from collections import Counter


def generate_lotto_numbers(method, birth_date=None, pillars_info=None, set_index=0):
    """
    로또 번호를 생성합니다.
    
    Args:
        method: 생성 방식
        birth_date: 생년월일 (datetime.date, 선택사항)
        pillars_info: 사주 정보 (선택사항)
        set_index: 세트 인덱스 (다중 세트 생성 시)
        
    Returns:
        dict: 로또 번호 정보
    """
    if method == "완전 랜덤":
        numbers = sorted(random.sample(range(1, 46), 6))
        explanation = "완전히 랜덤하게 생성된 번호입니다."
    
    elif method == "생년월일 기반":
        if birth_date:
            # 생년월일 숫자 추출
            year_digits = [int(d) for d in str(birth_date.year)[-2:]]  # 년도 마지막 2자리
            month = birth_date.month
            day = birth_date.day
            
            # 생년월일에서 추출한 숫자들
            date_numbers = [month, day] + year_digits
            date_numbers = [n for n in date_numbers if 1 <= n <= 45]
            
            # 부족한 번호는 랜덤으로 채움
            base_numbers = list(set(date_numbers))
            remaining = 6 - len(base_numbers)
            if remaining > 0:
                available = [n for n in range(1, 46) if n not in base_numbers]
                base_numbers.extend(random.sample(available, min(remaining, len(available))))
            
            numbers = sorted(base_numbers[:6])
            explanation = f"생년월일({birth_date.strftime('%Y년 %m월 %d일')})을 기반으로 생성된 번호입니다."
        else:
            numbers = sorted(random.sample(range(1, 46), 6))
            explanation = "생년월일 정보가 없어 랜덤으로 생성되었습니다."
    
    elif method == "사주 기반":
        # 사주 정보 활용
        if pillars_info:
            # 간지에서 숫자 추출 (간단한 변환)
            seed_numbers = []
            
            # 년, 월, 일, 시 간지 인덱스 활용
            for key in ['year_stem', 'year_branch', 'month_stem', 'month_branch', 
                       'day_stem', 'day_branch', 'hour_stem', 'hour_branch']:
                if key in pillars_info:
                    # 간지 문자열에서 숫자 추출 (간단한 해시 방식)
                    ganji = str(pillars_info[key])
                    for char in ganji:
                        if char.isdigit():
                            seed_numbers.append(int(char))
            
            # 추출한 숫자들을 1-45 범위로 변환
            base_numbers = []
            for num in seed_numbers:
                converted = ((num - 1) % 45) + 1
                if converted not in base_numbers:
                    base_numbers.append(converted)
            
            # 부족한 번호는 랜덤으로 채움
            remaining = 6 - len(base_numbers)
            if remaining > 0:
                available = [n for n in range(1, 46) if n not in base_numbers]
                base_numbers.extend(random.sample(available, min(remaining, len(available))))
            
            numbers = sorted(base_numbers[:6])
            explanation = "사주 정보를 기반으로 생성된 번호입니다."
        else:
            numbers = sorted(random.sample(range(1, 46), 6))
            explanation = "사주 정보가 없어 랜덤으로 생성되었습니다."
    
    elif method == "행운 숫자 조합":
        # 행운 숫자와 랜덤 조합
        if birth_date:
            # 행운 숫자: 생일 합산 등
            lucky_num = (birth_date.month + birth_date.day) % 45 + 1
            if lucky_num == 0:
                lucky_num = 45
            
            numbers = [lucky_num]
            available = [n for n in range(1, 46) if n != lucky_num]
            numbers.extend(random.sample(available, 5))
            numbers = sorted(numbers)
            explanation = f"행운의 숫자와 조합하여 생성된 번호입니다."
        else:
            numbers = sorted(random.sample(range(1, 46), 6))
            explanation = "행운 숫자 조합으로 생성된 번호입니다."
    
    elif method == "홀짝 균형형":
        # 홀수와 짝수를 3:3 또는 4:2로 균형있게 배분
        odd_numbers = [n for n in range(1, 46) if n % 2 == 1]
        even_numbers = [n for n in range(1, 46) if n % 2 == 0]
        
        # 3:3 또는 4:2 비율로 선택
        ratio = random.choice([(3, 3), (4, 2)])
        selected_odd = random.sample(odd_numbers, ratio[0])
        selected_even = random.sample(even_numbers, ratio[1])
        
        numbers = sorted(selected_odd + selected_even)
        explanation = f"홀수 {ratio[0]}개, 짝수 {ratio[1]}개로 균형있게 구성된 번호입니다."
    
    elif method == "고저 분포형":
        # 낮은 번호(1-15), 중간 번호(16-30), 높은 번호(31-45)를 골고루 배분
        low_range = list(range(1, 16))
        mid_range = list(range(16, 31))
        high_range = list(range(31, 46))
        
        # 2:2:2 또는 3:2:1 등 다양한 분포
        distribution = random.choice([(2, 2, 2), (3, 2, 1), (2, 3, 1), (1, 2, 3)])
        selected_low = random.sample(low_range, distribution[0])
        selected_mid = random.sample(mid_range, distribution[1])
        selected_high = random.sample(high_range, distribution[2])
        
        numbers = sorted(selected_low + selected_mid + selected_high)
        explanation = f"낮은 번호 {distribution[0]}개, 중간 번호 {distribution[1]}개, 높은 번호 {distribution[2]}개로 구성된 번호입니다."
    
    elif method == "연속 번호 포함형":
        # 연속된 번호를 2-3개 포함
        numbers = []
        available = list(range(1, 46))
        
        # 연속 번호 1쌍 추가
        start = random.randint(1, 43)
        consecutive = [start, start + 1]
        numbers.extend(consecutive)
        available = [n for n in available if n not in consecutive]
        
        # 나머지는 랜덤으로 채움
        numbers.extend(random.sample(available, 4))
        numbers = sorted(numbers)
        explanation = f"연속된 번호({start}, {start+1})를 포함한 번호입니다."
    
    elif method == "합계 조절형":
        # 번호 합계를 100-200 범위로 조절
        target_sum = random.randint(100, 200)
        
        # 그리디 방식으로 합계에 가까운 번호 선택
        numbers = []
        available = list(range(1, 46))
        current_sum = 0
        
        for _ in range(6):
            if not available:
                break
            
            # 남은 번호 수와 목표 합계를 고려하여 선택
            remaining = 6 - len(numbers)
            ideal_avg = (target_sum - current_sum) / remaining if remaining > 0 else 0
            
            # 이상적인 평균에 가까운 번호 우선 선택
            candidates = [n for n in available if abs(n - ideal_avg) <= 20]
            if not candidates:
                candidates = available
            
            selected = random.choice(candidates)
            numbers.append(selected)
            available.remove(selected)
            current_sum += selected
        
        numbers = sorted(numbers)
        actual_sum = sum(numbers)
        explanation = f"번호 합계 {actual_sum}으로 조절된 번호입니다."
    
    elif method == "시간 기반":
        # 현재 시간과 날짜를 기반으로 생성
        now = datetime.now()
        time_seed = (now.hour * 60 + now.minute + now.day) % 45 + 1
        
        numbers = [time_seed]
        
        # 시간 기반 시드로 추가 번호 생성
        seed_base = time_seed
        for _ in range(5):
            seed_base = (seed_base * 7 + 13) % 45 + 1
            while seed_base in numbers:
                seed_base = (seed_base + 1) % 45 + 1
                if seed_base == 0:
                    seed_base = 45
            numbers.append(seed_base)
        
        numbers = sorted(numbers)
        explanation = f"현재 시간({now.strftime('%H:%M')})을 기반으로 생성된 번호입니다."
    
    elif method == "생일 합산 기반":
        # 생년월일을 더 다양하게 활용
        if birth_date:
            # 년, 월, 일의 각 자리수 합산
            year_sum = sum(int(d) for d in str(birth_date.year))
            month = birth_date.month
            day = birth_date.day
            
            # 합산된 숫자들을 1-45 범위로 변환
            base_nums = []
            for num in [year_sum, month, day, month + day, year_sum % 45 + 1]:
                converted = ((num - 1) % 45) + 1
                if converted not in base_nums:
                    base_nums.append(converted)
            
            # 부족한 번호는 랜덤으로 채움
            remaining = 6 - len(base_nums)
            if remaining > 0:
                available = [n for n in range(1, 46) if n not in base_nums]
                base_nums.extend(random.sample(available, min(remaining, len(available))))
            
            numbers = sorted(base_nums[:6])
            explanation = f"생년월일의 각 자리수를 합산하여 생성된 번호입니다."
        else:
            numbers = sorted(random.sample(range(1, 46), 6))
            explanation = "생년월일 정보가 없어 랜덤으로 생성되었습니다."
    
    elif method == "사주 오행 기반":
        # 사주의 오행(五行)을 숫자로 변환
        if pillars_info:
            # 오행: 목(1-9), 화(10-18), 토(19-27), 금(28-36), 수(37-45)
            wuxing_ranges = {
                '목': list(range(1, 10)),
                '화': list(range(10, 19)),
                '토': list(range(19, 28)),
                '금': list(range(28, 37)),
                '수': list(range(37, 46))
            }
            
            # 간단한 오행 추출 (실제로는 더 복잡한 로직 필요)
            numbers = []
            used_ranges = set()
            
            # 각 오행에서 1-2개씩 선택
            for wuxing, num_range in wuxing_ranges.items():
                if len(numbers) >= 6:
                    break
                count = random.choice([1, 2]) if len(numbers) < 5 else 1
                selected = random.sample(num_range, min(count, len(num_range)))
                numbers.extend(selected)
                used_ranges.add(wuxing)
            
            # 부족하면 랜덤으로 채움
            if len(numbers) < 6:
                available = [n for n in range(1, 46) if n not in numbers]
                numbers.extend(random.sample(available, 6 - len(numbers)))
            
            numbers = sorted(numbers[:6])
            explanation = "사주 오행(목화토금수)을 기반으로 생성된 번호입니다."
        else:
            numbers = sorted(random.sample(range(1, 46), 6))
            explanation = "사주 정보가 없어 랜덤으로 생성되었습니다."
    
    else:
        # 기본: 랜덤
        numbers = sorted(random.sample(range(1, 46), 6))
        explanation = "랜덤으로 생성된 번호입니다."
    
    return {
        'numbers': numbers,
        'explanation': explanation,
        'set_index': set_index + 1
    }


def get_number_color(num):
    """로또 번호 대역별 색상을 반환합니다 (실제 로또와 동일)"""
    if 1 <= num <= 10:
        # 1-10: 노란색
        return {
            'bg': 'linear-gradient(135deg, #FBC02D 0%, #FDD835 100%)',
            'shadow': 'rgba(251, 192, 45, 0.4)',
            'color': '#1A202C'
        }
    elif 11 <= num <= 20:
        # 11-20: 파란색
        return {
            'bg': 'linear-gradient(135deg, #1976D2 0%, #2196F3 100%)',
            'shadow': 'rgba(25, 118, 210, 0.4)',
            'color': '#FFFFFF'
        }
    elif 21 <= num <= 30:
        # 21-30: 빨간색
        return {
            'bg': 'linear-gradient(135deg, #D32F2F 0%, #F44336 100%)',
            'shadow': 'rgba(211, 47, 47, 0.4)',
            'color': '#FFFFFF'
        }
    elif 31 <= num <= 40:
        # 31-40: 회색
        return {
            'bg': 'linear-gradient(135deg, #616161 0%, #757575 100%)',
            'shadow': 'rgba(97, 97, 97, 0.4)',
            'color': '#FFFFFF'
        }
    else:  # 41-45
        # 41-45: 초록색
        return {
            'bg': 'linear-gradient(135deg, #388E3C 0%, #4CAF50 100%)',
            'shadow': 'rgba(56, 142, 60, 0.4)',
            'color': '#FFFFFF'
        }


def calculate_statistics(sets):
    """로또 번호 세트들의 통계를 계산합니다."""
    # 모든 번호 합산
    all_numbers = []
    for lotto_set in sets:
        all_numbers.extend(lotto_set['numbers'])
    
    # 번호별 출현 횟수
    number_counts = Counter(all_numbers)
    
    # 가장 많이 나온 번호들
    most_common = number_counts.most_common(6)
    
    # 번호 구간별 분포
    ranges = {
        "1-15": len([n for n in all_numbers if 1 <= n <= 15]),
        "16-30": len([n for n in all_numbers if 16 <= n <= 30]),
        "31-45": len([n for n in all_numbers if 31 <= n <= 45])
    }
    
    return {
        'most_common': most_common,
        'ranges': ranges,
        'total_numbers': len(all_numbers)
    }

