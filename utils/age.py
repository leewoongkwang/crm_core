# utils/age.py
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

def calculate_insurance_age(birth_date_str: str, reference_date_str: str) -> int:
    """
    한국 보험나이 계산: 기준일 기준 생일로부터 6개월 이상 지났으면 +1세

    Args:
        birth_date_str: 생년월일 (YYYY-MM-DD)
        reference_date_str: 기준일 (예: 가입일, 오늘 등) (YYYY-MM-DD)

    Returns:
        보험나이 (int)
    """
    birth_date = date.fromisoformat(birth_date_str)
    reference_date = date.fromisoformat(reference_date_str)

    # 기본 만 나이 계산
    age = reference_date.year - birth_date.year
    if (reference_date.month, reference_date.day) < (birth_date.month, birth_date.day):
        age -= 1

    # 생일 기준일 계산
    birthday_this_year = birth_date.replace(year=reference_date.year)
    six_months_after_birthday = birthday_this_year + relativedelta(months=6)

    # 기준일이 생일 + 6개월 이상이면 보험나이 +1
    if reference_date >= six_months_after_birthday:
        age += 1

    return age
    
def calculate_insurance_birthday(birth_date_str: str) -> str:
    """
    보험 상령일 계산: 현재년도 기준 생일에 6개월을 더한 날짜

    Args:
        birth_date_str: 생년월일 (YYYY-MM-DD)

    Returns:
        보험 상령일 (YYYY-MM-DD, ISO 형식)
    """
    try:
        birth_date = datetime.fromisoformat(birth_date_str).date()
    except ValueError:
        return None

    today = datetime.today().date()
    this_year = today.year

    # 올해 생일로 변환 (윤년 보정 포함)
    try:
        birthday_this_year = birth_date.replace(year=this_year)
    except ValueError:
        birthday_this_year = birth_date.replace(year=this_year, day=28)

    insurance_birthday = birthday_this_year + relativedelta(months=6)
    return insurance_birthday.isoformat()