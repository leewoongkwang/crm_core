from types import SimpleNamespace
from django.shortcuts import render, get_object_or_404
from reports.models import Report
from collections import defaultdict

def analysis_detail_view(request, report_id):
    report = get_object_or_404(Report, id=report_id)

    parse_data = report.parse_json or {}

    customer_info = parse_data.get("customer", {})

    coverage_list = parse_data.get("coverage", [])
    # ✅ coverage 키 변환 (템플릿에서 .coverage_name, .coverage_amount로 사용)
    coverage_list = [
        {
            "coverage_name": c.get("coverage_name") or c.get("담보명"),
            "coverage_amount": c.get("coverage_amount") or c.get("가입금액"),
        }
        for c in coverage_list
        if c
    ]

    overview = parse_data.get("insurance_overview", [])

    insurance_table = {}
    insurance_keys = []

    for idx, item in enumerate(overview):
        company = item.get("보험회사명", "")
        product = item.get("상품명", "")
        if not company or not product:
            continue

        # ✅ 중복 방지 키 생성
        key = f"{company} - {product} ({idx+1})"
        insurance_table[key] = item

        for k in item.keys():
            if k not in ("보험회사명", "상품명") and k not in insurance_keys:
                insurance_keys.append(k)

    context = {
        "customer": customer_info,
        "coverage": coverage_list,
        "overview": overview,
        "insurance_table": insurance_table,
        "insurance_keys": insurance_keys,       
    }
    return render(request, "analysis/detail.html", context)