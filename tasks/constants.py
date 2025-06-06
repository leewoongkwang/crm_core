# tasks/constants.py

# 14터치 단계 (순서 보장)
STEP_SEQUENCE = [
    ("report", "리포트"),
    ("pre_sms", "콜 전 문자"),
    ("call1", "1차 콜"),
    ("reject_sms", "거절 후 제안"),
    ("call2", "2차 콜"),
    ("visit", "방문 제안"),
    ("done", "완료"),
]

# key → label 매핑 (드롭다운/버튼용)
TOUCH_NEXT_MAP = dict(STEP_SEQUENCE)

# KPI 항목 정의: label → model field
DAILY_KPI_FIELDS = [
    ("1분콜", "daily_call_1min"),
    ("2분콜", "daily_call_2min"),
    ("고객 제안", "daily_proposals"),
    ("방문 제안", "daily_visit_proposals"),
    ("가망 확보", "daily_grade_potential"),
    ("밴드 인증", "daily_band_verified"),
]
