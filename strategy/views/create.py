from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from strategy.models import Strategy
from strategy.forms import StrategyForm
from datetime import date

class StrategyCreateView(CreateView):
    model = Strategy
    form_class = StrategyForm
    template_name = "strategy/form.html"
    success_url = reverse_lazy("home")  # or strategy_detail

    def get_initial(self):
        today = date.today()
        return {"year": today.year, "month": today.month}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["initial"]["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
