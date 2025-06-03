from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from customers.models import Customer
from touchlog.models import TouchLog

@login_required
def customer_touchlog_partial(request, pk):
    customer = get_object_or_404(Customer, pk=pk, user=request.user)
    logs = TouchLog.objects.filter(customer=customer).order_by("-touched_at")

    return render(request, "touchlog/partials/customer_tab.html", {
        "customer": customer,
        "touchlogs": logs,
    })
