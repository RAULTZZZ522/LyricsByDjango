from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 首页路由
    # 歌词详情页：URL 格式为 /<artist_name>/<song_id>/
    path('<str:artist_name>/<int:song_id>/', views.song_detail, name='song_detail'),
]

