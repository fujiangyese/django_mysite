## 这是一个用户登录和注册练习项目
## 这是一个可重用的登录和注册APP


### 简单使用方法：
1. 创建虚拟环境
2. 使用pip安装第三方依赖
3. 运行migrate命令，创建数据库和数据表
4. 运行runserver启动服务器

### 路由设置
在根目录的urls文件中将验证码的路由添加进去
```python
from django.contrib import admin
from django.urls import path, include
from login import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('captcha/', include('captcha.urls'))   # 增加这一行
]