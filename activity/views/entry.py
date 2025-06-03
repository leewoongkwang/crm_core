# activity/views/entry.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.contrib import messages

from activity.models import DailyStandardActivity
from activity.forms import ActivityForm

@login_required
def activity_entry_view(request):
    today = now().date()
    instance, _ = DailyStandardActivity.objects.get_or_create(user=request.user, date=today)
    form = ActivityForm(request.POST or None, instance=instance)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "오늘의 KPI 실적이 저장되었습니다.")
        return redirect('activity:entry')

    history = DailyStandardActivity.objects.filter(user=request.user).exclude(date=today).order_by('-date')[:7]

    return render(request, 'activity/form.html', {
        'form': form,
        'history': history,
    })
