
# activity/views/list.py
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from activity.models import DailyStandardActivity

@method_decorator(login_required, name='dispatch')
class ActivityListView(ListView):
    model = DailyStandardActivity
    template_name = 'activity/list.html'
    context_object_name = 'activities'

    def get_queryset(self):
        return DailyStandardActivity.objects.filter(user=self.request.user).order_by('-date')
