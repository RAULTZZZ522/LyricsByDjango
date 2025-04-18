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
        
        # 保存搜索记录到 session
        history = request.session.get('search_history', [])
        if query not in history:
            history.insert(0, query)  # 新记录放前面
            if len(history) > 10:     # 最多保留 10 条
                history = history[:10]
            request.session['search_history'] = history
            
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

# 搜索记录视图
def search_history(request):
    history = request.session.get('search_history', [])
    matched_songs = []

    # 用集合去重歌曲ID，防止多次命中同一首歌
    seen_song_ids = set()

    for keyword in history:
        # 查找关键词匹配的歌曲
        songs = Song.objects.filter(
            Q(title__icontains=keyword) | Q(artist__name__icontains=keyword)
        )

        for song in songs:
            if song.id not in seen_song_ids:
                matched_songs.append(song)
                seen_song_ids.add(song.id)
            if len(matched_songs) >= 10:
                break
        if len(matched_songs) >= 10:
            break

    return render(request, 'lyrics/history.html', {'songs': matched_songs})