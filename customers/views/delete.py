from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from customers.models import Customer
from customers.forms import CustomerForm


@login_required
def customer_delete_view(request, id):
    customer = get_object_or_404(Customer, id=id, user=request.user)
    if request.method == "POST":
        customer.delete()
        return redirect("customers:customer_list")
    return render(request, "customers/delete.html", {"customer": customer})
