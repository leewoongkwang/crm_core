from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home:view")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home:view")
        else:
            messages.error(request, "로그인 정보가 올바르지 않습니다.")
    return render(request, "login.html")
