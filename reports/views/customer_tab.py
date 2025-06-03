from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from customers.models import Customer
from reports.models import Report

@login_required
def customer_report_partial(request, pk):
    customer = get_object_or_404(Customer, pk=pk, user=request.user)
    reports = Report.objects.filter(customer=customer).order_by("-uploaded_at")

    return render(request, "reports/partials/customer_tab.html", {
        "customer": customer,
        "reports": reports,
    })
