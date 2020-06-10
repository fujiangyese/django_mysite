from django.contrib import admin
from . import models
# Register your models here.

# 将定义的模型类注册到admin
admin.site.register(models.User)   # models里面的User类进行注册