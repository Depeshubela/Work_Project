from django import forms
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from .models import User
'''
#widget與attrs可以更改顯示效果(類似前端工程)
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        #error_messages={'required': '尚未輸入帳號'}
    )
    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
        #error_messages={'required': '尚未輸入密碼'},
    )
'''
#UserCreationForm django內建的使用者表單新增功能 包含基礎功能與介面
#此處用來覆蓋原有功能
class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': '尚未輸入帳號'}
    )
    
    email = forms.EmailField(
        label=_('電子信箱'),
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
        error_messages={
            'invalid': '請輸入有效電子信箱',
            'required': '尚未輸入電子信箱',
        }
    )
    
    YEARS = [str(x) for x in range(1920, 2021)]
    MONTHS = {
        1: _('一月'), 2: _('二月'), 3: _('三月'), 4: _('四月'),
        5: _('五月'), 6: _('六月'), 7: _('七月'), 8: _('八月'),
        9: _('九月'), 10: _('十月'), 11: _('十一月'), 12: _('十二月')
    }
    
    date_of_birth = forms.DateField(
        label=_('生日'),
        widget=forms.SelectDateWidget(years=YEARS, months=MONTHS),
        error_messages={
            'invalid': '請輸入有效生日日期',
            'required': '請輸入生日',
        }
    )
    
    password1 = forms.CharField(
        label=_('密碼'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        error_messages={'required': '尚未輸入密碼'},
    )
    
    password2 = forms.CharField(
        label=_('確認密碼'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        error_messages={'required': '尚未輸入確認密碼'},
    )
    
    error_messages = {
        'password_mismatch': _('兩次密碼輸入不同'),
    }
    
    class Meta:
        model = User
        fields = ('username','email', 'date_of_birth', 'password1', 'password2')
    
    def clean_email(self):
    
        email = self.cleaned_data['email']
    
        try:
            account = User.objects.get(email=email)
        except Exception as e:
            return email
    
        raise forms.ValidationError(f'{email} 已被註冊')