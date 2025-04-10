from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 首页路由
]
