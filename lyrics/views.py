from django.shortcuts import render

# 首页视图函数
def home(request):
    return render(request, 'lyrics/home.html')
