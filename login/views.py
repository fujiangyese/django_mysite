from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from . import models, forms
import hashlib


# Create your views here.
def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型，通过encode将字符串转为字节
    return h.hexdigest()


def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'login/index.html')


def login(request):
    # if request.is_ajax():
    #     result = dict()
    #     result['key'] = CaptchaStore.generate_key()
    #     result['image_url'] = captcha_image_url(result['key'])
    #     return JsonResponse(result)
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)  # 直接通过表单类获取登陆表单所有信息
        # 通过if去判断表单是否可以通过验证
        message = '请检查填写的内容'
        if login_form.is_valid():  # 使用表单类自带的is_valid方法一步完成数据验证工作
            username = login_form.cleaned_data.get('username')  # 从cleaned_data字典中获取表单具体的值
            password = login_form.cleaned_data.get('password')
            message = '请检查填写的内容'
            # 通过验证以后，尝试使用用户名去数据库模型中查找对应数据
            try:
                user = models.User.objects.get(name=username)
            except:
                message = '用户名不存在'
                return render(request, 'login/login.html', locals())
            if hash_code(password) == user.password:  # 验证密码成功就跳转到主页
                # 登陆成功之后将一些信息存放在session中
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = '密码不正确'
                return render(request, 'login/login.html', locals())
        else:  # 表单不能通过验证，返回登录页面
            return render(request, 'login/login.html', locals())
    login_form = forms.LoginForm()  # 发起的是GET请求，调用自定义的U直接返回登录页面
    return render(request, 'login/login.html', locals())  # 将login_form变量传给模板


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    request.session.flush()
    return redirect('/login/')  # 重定向到登陆页面


def register(request):
    # if request.is_ajax():
    #     result = dict()
    #     result['key'] = CaptchaStore.generate_key()
    #     result['image_url'] = captcha_image_url(result['key'])
    #     return JsonResponse(result)
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = '请检查填写的内容'
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            # email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'login/register.html', locals())
                # same_email_user = models.User.objects.filter(email=email)
                # if same_email_user:
                #     message = '该邮箱已经被注册了！'
                #     return render(request, 'login/register.html', locals())
                # 密码验证成功，对密码进行加密或者加盐，编写一个加密函数
                # 传入密码字符串，返回加盐后的密码
                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                # new_user.email = email
                new_user.sex = sex
                new_user.save()

                return redirect('/login/')
        else:
            return render(request, 'login/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


# 添加一个ajax点击刷新验证码功能，首先在视图函数写好功能函数

