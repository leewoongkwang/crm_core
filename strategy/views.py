from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from .models import Strategy

@login_required
def strategy_view(request):
    today = now()
    strategy, _ = Strategy.objects.get_or_create(
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
            'daily_prospective_secure': 0,
            'daily_band_verified': 0,
        }
    )

    if request.method == 'POST':
        fields = [
            'monthly_cpc_goal', 'weekly_cpc_goal', 'daily_call_1min', 'daily_call_2min',
            'weekly_call_2min', 'daily_proposals', 'daily_visit_proposals',
            'daily_prospective_secure', 'daily_band_verified', 'memo'
        ]
        for field in fields:
            setattr(strategy, field, request.POST.get(field, getattr(strategy, field)))
        strategy.save()
        return redirect('strategy:view')

    return render(request, 'strategy.html', {'strategy': strategy})
