from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    # KPI, 계약, 차트 데이터는 실제 DB 연동에 따라 구현 필요
    # 지금은 정적 예시 구조 유지
    return render(request, "home.html")
