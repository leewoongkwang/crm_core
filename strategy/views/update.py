from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from strategy.models import Strategy
from strategy.forms import StrategyForm

class StrategyUpdateView(UpdateView):
    model = Strategy
    form_class = StrategyForm
    template_name = "strategy/form.html"
    success_url = reverse_lazy("home")  # or strategy_detail
