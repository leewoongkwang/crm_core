# customers/views/detail.py

from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from customers.models import Customer

@method_decorator(login_required, name='dispatch')
class CustomerDetailView(DetailView):
    model = Customer
    template_name = "customers/detail.html"
    context_object_name = "customer"

    def get_object(self):
        obj = super().get_object()
        if obj.user_id != self.request.user.id:
            raise PermissionDenied("타인의 고객 정보에 접근할 수 없습니다.")
        return obj
