from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .forms import RegisterForm
# Create your views here.

def home(request):
    return render(request, 'home.html')
def user(request):
    return render(request, 'user.html')
def register(request):
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        # 這裡可以處理用戶登入邏輯
        email = request.POST['email']
        password = request.POST['password']
        # 進行登入邏輯處理，這裡可以檢查帳號密碼等
    return render(request, 'login.html')  # 渲染登入頁面

# def register_view(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             form.save()  # 儲存數據到資料庫
#             messages.success(request, '註冊成功！')
#     else:
#         form = UserForm()
    
#     return render(request, 'home.html', {'form': form})
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()  # 保存表單資料到資料庫
            messages.success(request, '註冊成功！')
            return redirect('home')  
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})
