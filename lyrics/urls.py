from django.urls import path
from . import views

urlpatterns = [
    # 首页路由
    path('', views.home, name='home'),  
    # 歌词详情
    path('<str:artist_name>/<int:song_id>/', views.song_detail, name='song_detail'),
    # 历史记录
    path('history/', views.search_history, name='search_history'),
]

