from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from strategy.models import Strategy
from strategy.forms import StrategyForm

@login_required
def strategy_entry_view(request):
    today = now()
    # ✅ 항상 현재월 전략 가져오기
    strategy, created = Strategy.objects.get_or_create(
        user=request.user,
        year=today.year,
        month=today.month,
        defaults={
            'monthly_cpc_goal': 0,
            'weekly_cpc_goal': 0,
            'daily_call_1min': 0,
            'daily_call_2min': 0,
            'weekly_call_2min': 0,
            'daily_proposals': 0,
            'daily_visit_proposals': 0,
            'daily_grade_potential': 0,
            'daily_band_verified': 0,
        }
    )
    print("🎯 전략 객체:", strategy.pk, "신규 생성 여부:", created)
    if request.method == 'POST':
        form = StrategyForm(request.POST, instance=strategy, user=request.user)
        if form.is_valid():
            form.save()
            print("✅ 전략 저장 완료:", strategy.pk)
            messages.success(request, "이번 달 전략이 저장되었습니다.")
            return redirect('strategy:entry')
        else:
            print("❌ 폼 유효성 실패:", form.errors)
    else:
        form = StrategyForm(instance=strategy, user=request.user)

    # ✅ 전략 히스토리 (이전 달)
    history = Strategy.objects.filter(user=request.user).exclude(pk=strategy.pk).order_by('-year', '-month')

    return render(request, 'strategy/form.html', {
        'form': form,
        'history': history
    })
