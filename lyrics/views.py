from django.shortcuts import render, get_object_or_404
from .models import Song

# 首页视图函数
def home(request):
    return render(request, 'lyrics/home.html')

# 歌曲详情视图
def song_detail(request, artist_name, song_id):
    # 根据主键获取歌曲，并确认歌手名字匹配
    song = get_object_or_404(Song, id=song_id, artist__name=artist_name)
    
    # 临时先返回纯文本内容以验证跳转
    return render(request, 'lyrics/song_detail.html', {'song': song})