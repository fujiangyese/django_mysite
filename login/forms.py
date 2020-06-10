from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):  # 定义UserForm类继承自forms.Form  类比models.Model
    # 开始书写字段，每一个字段代表一个input
    username = forms.CharField(label='用户名', max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control dabiaoge', 'placeholder': 'Username', 'autofocus': ''}))
    password = forms.CharField(label='密码', max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    captcha = CaptchaField(label='验证码')
    # 使用widget参数设置为forms.PasswordInput，相当于在前端将type属性设置为password

    # 使用了Django的表单之后，也需要在视图中做相应修改


# 编写注册表单
class RegisterForm(forms.Form):
    gender = (
        ('male', '男'),
        ('female', '女'),
    )
    username = forms.CharField(label='用户名', max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='确认密码', max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    captcha = CaptchaField(label='验证码')
