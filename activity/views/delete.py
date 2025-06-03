
# activity/views/delete.py
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from activity.models import DailyStandardActivity

@method_decorator(login_required, name='dispatch')
class ActivityDeleteView(DeleteView):
    model = DailyStandardActivity
    template_name = 'activity/confirm_delete.html'
    success_url = reverse_lazy('activity:list')
