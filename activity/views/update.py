

# activity/views/update.py
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from activity.models import DailyStandardActivity
from activity.forms import ActivityForm

@method_decorator(login_required, name='dispatch')
class ActivityUpdateView(UpdateView):
    model = DailyStandardActivity
    form_class = ActivityForm
    template_name = 'activity/form.html'
    success_url = reverse_lazy('activity:list')