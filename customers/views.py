from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Customer
from .forms import CustomerForm
from django.core.paginator import Paginator

@login_required
def customer_list_view(request):
    customers = Customer.objects.filter(user=request.user)

    # 검색
    search = request.GET.get("search")
    if search:
        customers = customers.filter(
            name__icontains=search
        )

    # 필터
    grade = request.GET.get("grade")
    attribute = request.GET.get("attribute")
    propensity = request.GET.get("propensity")
    priority = request.GET.get("priority")
    target = request.GET.get("is_target_customer")

    if grade:
        customers = customers.filter(grade=grade)
    if attribute:
        customers = customers.filter(attribute=attribute)
    if propensity:
        customers = customers.filter(propensity=propensity)
    if priority:
        customers = customers.filter(priority=priority)
    if target == "1":
        customers = customers.filter(is_target_customer=True)
    elif target == "0":
        customers = customers.filter(is_target_customer=False)

    # 정렬
    sort = request.GET.get("sort", "-created_at")
    customers = customers.order_by(sort)

    # 페이징
    paginator = Paginator(customers, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "customers/list.html", {
        "page_obj": page_obj,
        "sort": sort,
        "request": request,  # 필터 폼에서 유지 필요
    })


@login_required
def customer_detail_view(request, id):
    customer = get_object_or_404(Customer, id=id, user=request.user)
    return render(request, "customers/detail.html", {"customer": customer})

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

@login_required
def customer_delete_view(request, id):
    customer = get_object_or_404(Customer, id=id, user=request.user)
    if request.method == "POST":
        customer.delete()
        return redirect("customers:customer_list")
    return render(request, "customers/delete.html", {"customer": customer})
