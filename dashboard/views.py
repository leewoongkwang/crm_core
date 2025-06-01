from django.shortcuts import render, redirect, get_object_or_404
from customers.models import Customer
from django.utils import timezone

# ✅ 고정된 뷰
def home_view(request):
    return render(request, "home.html")
def tasks_view(request):
    return render(request, "tasks.html")
def strategy_view(request):
    return render(request, "strategy.html")
def touch_view(request):
    return render(request, "touch.html")
def analysis_view(request, report_id=None):
    return render(request, "analysis.html")

# ✅ 고객 관련
def customer_list_view(request):
    customers = Customer.objects.all().order_by("-created_at")
    return render(request, "customer/list.html", {"customers": customers})

def customer_detail_view(request, id):
    return render(request, "customer/detail.html")

def customer_add_view(request):
    if request.method == 'POST':
        data = request.POST
        name = data.get('name')
        phone = data.get('phone')
        birth = data.get('birth')
        gender = data.get('gender')
        attribute = data.get('attribute')
        grade = data.get('grade')
        priority = data.get('priority')
        created_at = timezone.now()

        Customer.objects.create(
            name=name,
            phone_encrypted=phone,  # 암호화 로직 이후 적용
            birth_encrypted=birth,
            gender=gender,
            attribute=attribute,
            grade=grade,
            priority=priority,
            created_at=created_at
        )
        return redirect('/customer/list/')
    return render(request, 'customer/form.html')
def customer_edit_view(request, id):
    customer = get_object_or_404(Customer, id=id)

    if request.method == 'POST':
        customer.name = request.POST.get('name')
        customer.phone_encrypted = request.POST.get('phone')
        customer.birth_encrypted = request.POST.get('birth')
        customer.gender = request.POST.get('gender')
        customer.attribute = request.POST.get('attribute')
        customer.grade = request.POST.get('grade')
        customer.priority = request.POST.get('priority')
        customer.save()
        return redirect('/customer/list/')

    return render(request, 'customer/form.html', {'customer': customer})

def customer_delete_view(request, id):
    customer = get_object_or_404(Customer, id=id)

    if request.method == 'POST':
        customer.delete()
        return redirect('/customer/list/')

    return render(request, 'customer/delete.html', {'customer': customer})

