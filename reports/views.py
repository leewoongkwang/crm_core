from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Report

@login_required
def analysis_view(request, report_id):
    report = get_object_or_404(Report, id=report_id, user=request.user)

    try:
        import json
        parsed_data = json.loads(report.parse_json) if report.parse_json else {}
    except Exception:
        parsed_data = {}

    return render(request, "analysis.html", {
        "report": report,
        "data": parsed_data
    })
