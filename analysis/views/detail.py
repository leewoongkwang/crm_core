# analysis/views/detail.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from reports.models import Report

@login_required
def analysis_detail_view(request, report_id):
    report = get_object_or_404(Report, id=report_id, user=request.user)
    data = report.parse_json or {}

    customer = data.get("customer", {})
    coverage = data.get("coverage", [])
    overview = data.get("insurance_overview", [])

    # 열 구성 기준
    contract_fields = [
        "계약자/피보험자", "보험가입일", "납입완료일", "보장만기일",
        "납입기간", "납입횟수", "납입률", "월납입보험료",
        "납입예정보험료", "총납입보험료"
    ]
    coverage_names = [item.get("coverage_name") or item.get("담보명") for item in coverage]

    # 열 이름: 보험회사명 - 상품명
    insurance_columns = list({f"{item['보험회사명']} - {item['상품명']}" for item in overview})

    # 열별 항목 매핑
    insurance_column_data = {
        col: {**{k: "-" for k in contract_fields + coverage_names}} for col in insurance_columns
    }
    for item in overview:
        col = f"{item['보험회사명']} - {item['상품명']}"
        for key, value in item.items():
            if key in contract_fields:
                insurance_column_data[col][key] = value
            elif key in coverage_names:
                insurance_column_data[col][key] = value

    # 테이블 구성
    combined_table = []
    for label in contract_fields + coverage_names:
        is_contract = label in contract_fields
        row = {
            "항목명": "" if is_contract else label,
            "전체보장현황": label if is_contract else next(
                (c["coverage_amount"] for c in coverage if (c.get("coverage_name") or c.get("담보명")) == label),
                "-"
            )
        }
        for col in insurance_columns:
            row[col] = insurance_column_data[col].get(label, "-")
        combined_table.append(row)

    return render(request, "analysis/detail.html", {
        "customer": customer,
        "coverage": coverage,
        "overview": overview,
        "insurance_table": combined_table,
        "insurance_keys": contract_fields + coverage_names
    })
