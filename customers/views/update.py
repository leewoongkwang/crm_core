from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from customers.models import Customer
from customers.forms import CustomerForm


@login_required
def customer_edit_view(request, id):
    customer = get_object_or_404(Customer, id=id, user=request.user)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            updated_customer = form.save(commit=False)
            updated_customer.user = request.user
            updated_customer.save()
            return redirect("customers:customer_list")
    else:
        form = CustomerForm(instance=customer)
    return render(request, "customers/form.html", {"form": form})