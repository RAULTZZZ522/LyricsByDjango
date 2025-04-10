from django.contrib import admin
from .models import Artist, Song, Lyric

# 注册模型到后台
admin.site.register(Artist)
admin.site.register(Song)
admin.site.register(Lyric)
