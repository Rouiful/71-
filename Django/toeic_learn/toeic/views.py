from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib.auth import get_user_model

User = get_user_model() 
def home(request):
    return render(request, 'home.html', {'user': request.user})

def user(request):
    return render(request, 'user.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, '請輸入電子郵件和密碼')
            return render(request, 'login.html')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, '登入成功！')
                return redirect('home')
            else:
                messages.error(request, '帳號或密碼錯誤')
                return render(request, 'login.html')

        except User.DoesNotExist:
            messages.error(request, '該電子郵件未註冊')
            return render(request, 'login.html')

    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '註冊成功！')
            return redirect('home')
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})

def test_page(request):
    return render(request, 'test.html')

def ai_reading_test(request):
    return render(request, 'ai_reading_test.html')

def reading_test(request):
    return render(request, 'reading_test.html')

def listening_test(request):
    return render(request, 'listening_test.html')

def vocab_test(request):
    return render(request, 'vocab_test.html')

