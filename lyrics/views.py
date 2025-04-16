from django.shortcuts import render, get_object_or_404
from .models import Song
from django.db.models import Q

# 首页视图函数
def home(request):
    query = request.GET.get('query', '')
    songs = []
    if query:
        # 只搜索歌曲标题和歌手姓名，不搜索歌词内容或ID
        songs = Song.objects.filter(
            Q(title__icontains=query) | Q(artist__name__icontains=query)
        )
    context = {
        'songs': songs,
        'query': query
    }
    return render(request, 'lyrics/home.html', context)


# 歌曲详情视图
def song_detail(request, artist_name, song_id):
    # 根据主键获取歌曲，并确认歌手名字匹配
    song = get_object_or_404(Song, id=song_id, artist__name=artist_name)
    
    # 临时先返回纯文本内容以验证跳转
    return render(request, 'lyrics/song_detail.html', {'song': song})