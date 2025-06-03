from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from customers.models import Customer
from customers.forms import CustomerForm
from django.shortcuts import redirect


@login_required
def customer_add_view(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            customer.save()
            request.session["success"] = "✅ 고객이 성공적으로 등록되었습니다."
            return redirect("customers:customer_list")
    else:
        form = CustomerForm()
    return render(request, "customers/form.html", {"form": form})