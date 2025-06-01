from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Customer

@login_required
def customer_list_view(request):
    customers = Customer.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "customer/list.html", {"customers": customers})

@login_required
def customer_detail_view(request, id):
    customer = get_object_or_404(Customer, id=id, user=request.user)
    return render(request, "customer/detail.html", {"customer": customer})

@login_required
def customer_add_view(request):
    if request.method == "POST":
        data = request.POST
        Customer.objects.create(
            user=request.user,
            name=data.get("name"),
            phone_encrypted=data.get("phone_encrypted"),
            birth_encrypted=data.get("birth_encrypted"),
            gender=data.get("gender"),
            attribute=data.get("attribute"),
            grade=data.get("grade"),
            propensity=data.get("propensity"),
            intimacy=data.get("intimacy"),
            priority=data.get("priority"),
            is_target_customer=bool(data.get("is_target_customer")),
            is_active_touching=bool(data.get("is_active_touching")),
            memo=data.get("memo"),
        )
        return redirect("customers:customer_list")
    return render(request, "customer/form.html")

@login_required
def customer_edit_view(request, id):
    customer = get_object_or_404(Customer, id=id, user=request.user)
    if request.method == "POST":
        data = request.POST
        for field in [
            "name", "phone_encrypted", "birth_encrypted", "gender", "attribute",
            "grade", "propensity", "intimacy", "priority", "memo"
        ]:
            setattr(customer, field, data.get(field))
        customer.is_target_customer = bool(data.get("is_target_customer"))
        customer.is_active_touching = bool(data.get("is_active_touching"))
        customer.save()
        return redirect("customers:customer_detail", id=id)
    return render(request, "customer/form.html", {"customer": customer})

@login_required
def customer_delete_view(request, id):
    customer = get_object_or_404(Customer, id=id, user=request.user)
    if request.method == "POST":
        customer.delete()
        return redirect("customers:customer_list")
    return render(request, "customer/delete.html", {"customer": customer})
