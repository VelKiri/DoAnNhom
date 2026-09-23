from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages


User = get_user_model()


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        password2 = request.POST.get("password2", "")

        # Kiểm tra username
        if User.objects.filter(username=username).exists():
            messages.error(request, "Tên đăng nhập đã tồn tại!")
            return redirect("register")

        # Kiểm tra email
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email đã được sử dụng!")
            return redirect("register")

        # Kiểm tra mật khẩu
        if password != password2:
            messages.error(request, "Mật khẩu nhập lại không khớp!")
            return redirect("register")

        # Tạo tài khoản
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(
            request,
            "Đăng ký thành công! Vui lòng đăng nhập."
        )

        return redirect("login")

    return render(request, "user/register.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        messages.error(
            request,
            "Email hoặc mật khẩu không đúng!"
        )

    return render(request, "user/login.html")


def logout_view(request):
    logout(request)

    return redirect("login")


def home(request):
    return render(request, "user/home.html")