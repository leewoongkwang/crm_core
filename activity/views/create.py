
# activity/views/create.py
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from activity.models import DailyStandardActivity
from activity.forms import ActivityForm

@method_decorator(login_required, name='dispatch')
class ActivityCreateView(CreateView):
    model = DailyStandardActivity
    form_class = ActivityForm
    template_name = 'activity/form.html'
    success_url = reverse_lazy('activity:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
