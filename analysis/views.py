import json
from django.shortcuts import render, get_object_or_404
from reports.models import Report  # Report는 reports 앱에 있음

def analysis_view(request, report_id):
    report = get_object_or_404(Report, id=report_id)

    try:
        parsed_data = json.loads(report.parse_json or '{}')
    except json.JSONDecodeError:
        parsed_data = {}

    return render(request, "analysis.html", {
        "report": report,
        "parsed_data": parsed_data,
    })
