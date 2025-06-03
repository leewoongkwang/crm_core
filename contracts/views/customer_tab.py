from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from customers.models import Customer
from contracts.models import Contract

@login_required
def customer_contract_partial(request, pk):
    customer = get_object_or_404(Customer, pk=pk, user=request.user)
    contracts = Contract.objects.filter(customer=customer).order_by("-signed_at")

    return render(request, "contracts/partials/customer_tab.html", {
        "customer": customer,
        "contracts": contracts,
    })
