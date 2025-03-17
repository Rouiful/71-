from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth import get_user_model

User = get_user_model() 
class RegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-container', 'placeholder': '使用者名稱'}),
        help_text=''  # 這行移除預設提示
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-container', 'placeholder': '電子郵件'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-container', 'placeholder': '密碼'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-container', 'placeholder': '確認密碼'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
