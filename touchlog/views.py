from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from customers.models import Customer
from .models import TouchLog

@login_required
def touch_view(request):
    ids = request.GET.get("ids", "")
    customer_ids = [int(cid) for cid in ids.split(",") if cid.isdigit()]
    customers = Customer.objects.filter(user=request.user, id__in=customer_ids)

    if request.method == "POST":
        data = request.POST
        touched_at = now()
        for customer in customers:
            TouchLog.objects.create(
                user=request.user,
                customer=customer,
                type=data.get("type", "14touch"),
                content=data.get("content", ""),
                strategy_note=data.get("strategy_note", ""),
                medical_history=data.get("medical_history", ""),
                underwriting_status=data.get("underwriting_status", ""),
                underwriting_result=data.get("underwriting_result", ""),
                insurance_products=data.get("insurance_products", ""),
                touched_at=touched_at,
            )
        return redirect("customers:customer_list")

    return render(request, "touch.html", {"customers": customers})
