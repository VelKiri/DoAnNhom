from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from .models import Country
from django.conf import settings
from .models import CustomUser
# Create your views here.
def register_view(request):
    if request.method=='POST':
        form = UserRegisterForm(request.POST,request.FILES)
        print("POST:", request.POST)
        print("FORM VALID:", form.is_valid())
        print("FORM ERRORS:", form.errors)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.is_superuser = False
            user.is_staff = False
            user.save()
            messages.success(request, 'Dang ky thanh cong!')
            return redirect('login')
        else:
            messages.error(request, 'Dang ky that bai!')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html',{'form': form})

def login_view(request):

    if request.method == 'POST':

        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        try:
            user = CustomUser.objects.get(email=email)

            if user.check_password(password):

                login(request, user)

                return redirect('blog')

            else:

                messages.error(
                    request,
                    'Mật khẩu không đúng.'
                )

        except CustomUser.DoesNotExist:

            messages.error(
                request,
                'Email không tồn tại.'
            )

    return render(
        request,
        'user/login.html'
    )

def logout_view(request):
    logout(request)
    return  redirect('login')
